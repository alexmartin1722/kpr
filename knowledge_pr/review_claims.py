#!/usr/bin/env python3
"""
review_claims.py — Stage-1 knowledge-PR review: verify candidate claims
against the FULL English article text.

For each candidate claim (from build_candidates.py), an LLM judge reads the
English article and assigns:

  SUPPORTED    — already in the article (drop from the PR; also a signal that
                 the en_baseline decomposition missed it)
  ABSENT       — genuinely new information (candidate addition)
  CONTRADICTED — conflicts with the article (flag for human adjudication),
                 with the conflicting article span quoted as evidence
  ERROR        — model output missing/unparseable (never silently mapped to a
                 real verdict)

Claims are batched per article (default 25/call); long articles are split
into windows and per-window verdicts merged (SUPPORTED > CONTRADICTED >
ABSENT > ERROR).

Output: one JSONL per article in --output-dir, each line a candidate record
plus review_verdict / review_evidence / en_revision.

Usage (API mode; endpoint defaults from fact-compare/sbatch/server_ready.txt):
    python review_claims.py \\
        --candidates candidates/pr_candidates.jsonl \\
        [--api-base http://HOST:PORT/v1 --api-model qwen-27b] \\
        [--concurrency 16] [--skip-existing] [--limit-articles 5]
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

from .config import add_config_arg, parse_args_with_config
from .llm_api import ApiLLM, read_endpoint
from .prompts import REVIEW_PROMPT

_REPO = Path(__file__).resolve().parents[1]          # repo root (kpr/)
_KPR_DIR = _REPO / "knowledge-pr"
_DOCUMENTS_DIR = (
    _REPO / "data" / "documents"
)

REVIEW_VERDICTS = ("SUPPORTED", "ABSENT", "CONTRADICTED")
# Merge precedence across article windows: definite signals beat ABSENT,
# ABSENT beats ERROR (an ERROR window can't veto a clean ABSENT elsewhere,
# but an all-ERROR claim stays ERROR).
_PRECEDENCE = {"SUPPORTED": 3, "CONTRADICTED": 2, "ABSENT": 1, "ERROR": 0}


def load_article(documents_dir: Path, article: str) -> Optional[Dict]:
    path = documents_dir / article / f"{article}_en.json"
    if not path.exists():
        return None
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not doc.get("text"):
        return None
    return doc


def split_windows(text: str, window_chars: int) -> List[str]:
    """Split article text into windows on paragraph boundaries."""
    if len(text) <= window_chars:
        return [text]
    paragraphs = text.split("\n")
    windows, current, size = [], [], 0
    for para in paragraphs:
        if current and size + len(para) > window_chars:
            windows.append("\n".join(current))
            current, size = [], 0
        current.append(para)
        size += len(para) + 1
    if current:
        windows.append("\n".join(current))
    return windows


def build_prompt(article_title: str, window_text: str, claims: List[Dict]) -> str:
    claim_lines = "\n".join(f"{i + 1}. {c['claim']}" for i, c in enumerate(claims))
    return (
        REVIEW_PROMPT
        .replace("[article_title]", article_title.replace("_", " "))
        .replace("[article_text]", window_text)
        .replace("[claims]", claim_lines)
    )


def parse_review(raw: str, n_claims: int) -> List[Dict]:
    """Parse the judge's JSON array. Anything unparseable -> ERROR (explicit)."""
    results = [{"verdict": "ERROR", "evidence": None} for _ in range(n_claims)]
    raw = re.sub(r"<think>[\s\S]*?</think>", "", raw).strip()
    match = re.search(r"```(?:json)?\s*(\[[\s\S]*?\])\s*```", raw)
    if not match:
        match = re.search(r"(\[[\s\S]*\])", raw)
    if not match:
        return results
    try:
        items = json.loads(match.group(1))
    except json.JSONDecodeError:
        return results
    if not isinstance(items, list):
        return results
    for item in items:
        if not isinstance(item, dict):
            continue
        idx = item.get("idx")
        if not isinstance(idx, int) or not (1 <= idx <= n_claims):
            continue
        verdict = str(item.get("verdict", "")).strip().upper()
        if verdict not in REVIEW_VERDICTS:
            continue
        evidence = item.get("evidence")
        if not isinstance(evidence, str) or verdict == "ABSENT":
            evidence = None
        results[idx - 1] = {"verdict": verdict, "evidence": evidence}
    return results


def merge_window_results(per_window: List[Dict]) -> Dict:
    best = max(per_window, key=lambda r: _PRECEDENCE[r["verdict"]])
    return dict(best)


def review_article(
    article: str,
    claims: List[Dict],
    doc: Dict,
    model: ApiLLM,
    claims_per_call: int,
    window_chars: int,
) -> List[Dict]:
    windows = split_windows(doc["text"], window_chars)
    batches = [claims[i:i + claims_per_call] for i in range(0, len(claims), claims_per_call)]

    prompts, owners = [], []  # owners[k] = (batch_idx, window_idx)
    for bi, batch in enumerate(batches):
        for wi, window in enumerate(windows):
            prompts.append(build_prompt(article, window, batch))
            owners.append((bi, wi))

    raw_outputs = model.batch_infer(prompts)

    # per_claim[batch_idx][claim_idx_in_batch] = list of window results
    per_claim: Dict[int, Dict[int, List[Dict]]] = {}
    for (bi, _wi), raw in zip(owners, raw_outputs):
        parsed = parse_review(raw, len(batches[bi]))
        for ci, res in enumerate(parsed):
            per_claim.setdefault(bi, {}).setdefault(ci, []).append(res)

    reviewed = []
    for bi, batch in enumerate(batches):
        for ci, rec in enumerate(batch):
            merged = merge_window_results(per_claim[bi][ci])
            reviewed.append({
                **rec,
                "review_verdict": merged["verdict"],
                "review_evidence": merged["evidence"],
                "en_revision": doc.get("last_revision"),
                "n_windows": len(windows),
            })
    return reviewed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Review PR-candidate claims against full English article text."
    )
    parser.add_argument("--candidates", type=Path,
                        default=_KPR_DIR / "candidates" / "pr_candidates.jsonl")
    parser.add_argument("--documents-dir", type=Path, default=_DOCUMENTS_DIR)
    parser.add_argument("--output-dir", type=Path, default=_KPR_DIR / "reviews")
    parser.add_argument("--claim-field", default="claim",
                        help="Which field holds the claim text to review "
                             "(use with decontextualized candidate files)")
    parser.add_argument("--article", default=None, help="Review only this article")
    parser.add_argument("--lang", default=None, help="Restrict to one source language")
    parser.add_argument("--limit-articles", type=int, default=None,
                        help="Review only the first N articles (smoke tests)")
    parser.add_argument("--claims-per-call", type=int, default=25)
    parser.add_argument("--window-chars", type=int, default=60_000,
                        help="Max article chars per prompt window")
    parser.add_argument("--api-base", default=None,
                        help="Defaults to fact-compare/sbatch/server_ready.txt")
    parser.add_argument("--api-model", default=None)
    parser.add_argument("--concurrency", type=int, default=16)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--enable-thinking", action="store_true")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the first prompt and exit (no API calls)")
    add_config_arg(parser)
    args = parse_args_with_config(parser)
    api_base, api_model = args.api_base, args.api_model
    if api_base is None or api_model is None:
        file_base, file_model = read_endpoint()
        api_base = api_base or file_base
        api_model = api_model or file_model or "qwen-27b"
    if not args.dry_run and not api_base:
        sys.exit("No --api-base given and no server_ready.txt found — is the vLLM server up?")

    # Load and group candidates by article
    by_article: Dict[str, List[Dict]] = {}
    with args.candidates.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if args.article and rec["article"] != args.article:
                continue
            if args.lang and rec["lang"] != args.lang:
                continue
            if args.claim_field != "claim":
                rec = {**rec, "claim": rec[args.claim_field]}
            by_article.setdefault(rec["article"], []).append(rec)

    articles = sorted(by_article)
    if args.limit_articles:
        articles = articles[: args.limit_articles]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.skip_existing:
        before = len(articles)
        articles = [a for a in articles if not (args.output_dir / f"{a}.jsonl").exists()]
        print(f"Skipped {before - len(articles)} already-reviewed articles.")

    total_claims = sum(len(by_article[a]) for a in articles)
    print(f"Reviewing {total_claims} claims across {len(articles)} articles "
          f"(claim field: {args.claim_field})")

    if args.dry_run:
        for a in articles:
            doc = load_article(args.documents_dir, a)
            if doc is None:
                continue
            windows = split_windows(doc["text"], args.window_chars)
            batch = by_article[a][: args.claims_per_call]
            print(build_prompt(a, windows[0], batch))
            return
        sys.exit("dry-run: no article with a loadable English document found")

    model = ApiLLM(
        api_base=api_base,
        api_model=api_model,
        enable_thinking=args.enable_thinking,
        max_tokens=args.max_tokens,
        concurrency=args.concurrency,
    )
    print(f"Backend: {api_base}  model={api_model}  concurrency={args.concurrency}")

    verdict_counts = Counter()
    missing_docs: List[str] = []
    for n, article in enumerate(articles, 1):
        claims = by_article[article]
        doc = load_article(args.documents_dir, article)
        if doc is None:
            missing_docs.append(article)
            # Explicit NO_ARTICLE records so nothing vanishes silently
            reviewed = [{**rec, "review_verdict": "NO_ARTICLE",
                         "review_evidence": None, "en_revision": None,
                         "n_windows": 0} for rec in claims]
        else:
            try:
                reviewed = review_article(article, claims, doc, model,
                                          args.claims_per_call, args.window_chars)
            except Exception as exc:
                print(f"  [ERROR] {article}: {exc}", file=sys.stderr)
                continue

        out_path = args.output_dir / f"{article}.jsonl"
        with out_path.open("w", encoding="utf-8") as f:
            for rec in reviewed:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        counts = Counter(r["review_verdict"] for r in reviewed)
        verdict_counts.update(counts)
        print(f"[{n}/{len(articles)}] {article}: {len(claims)} claims — "
              + "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))

    print("\n=== Totals ===")
    for verdict, count in verdict_counts.most_common():
        print(f"  {verdict:14s} {count}")
    if missing_docs:
        print(f"[warn] {len(missing_docs)} articles had no English document: "
              f"{missing_docs[:10]}{' ...' if len(missing_docs) > 10 else ''}", file=sys.stderr)
    print(f"\nDone. Reviews in {args.output_dir}")


if __name__ == "__main__":
    main()
