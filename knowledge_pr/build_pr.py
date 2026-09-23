#!/usr/bin/env python3
"""
build_pr.py — Stage 2 driver: turn ABSENT claims into an article-edit PR.

For an article:
  1. parse the English article into sections           (article_model)
  2. route each ABSENT claim to a section or NEW        (stage A)
  3. plan new sections from the NEW-bucket claims        (stage B)
  4. rewrite each touched existing section, min edit     (stage C)
  5. draft each new section                              (stage D)
  6. render a git-changelog-style diff + structured JSON (render_pr)

CONTRADICTED claims are intentionally excluded (additions only, for now).

Input claims: the union review (`knowledge-pr/reviews/`) or `pr_reviewed.jsonl`,
filtered to review_verdict == ABSENT and the chosen decomposition method.

Usage:
    python build_pr.py --article 140_West_57th_Street          # one article
    python build_pr.py --article 140_West_57th_Street --dry-run # parse+route only
    python build_pr.py --limit-articles 5                       # first N articles
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# make sibling knowledge-pr/llm_api.py importable WITHOUT shadowing this dir's
# own modules (prompts.py etc.) — append so the script dir keeps precedence.
from .config import add_config_arg, parse_args_with_config
from .article_model import load_article
from .authoring import Target, author
from .authoring.stages import outline as authoring_outline, route_claims
from .citations import attach_citations, coverage
from .gate import content_gate
from .llm_api import ApiLLM, read_endpoint
from .render_pr import pr_to_dict, render_claim_proposal, render_pr

_REPO = Path(__file__).resolve().parents[1]          # repo root (kpr/)
_KPR = _REPO / "knowledge-pr"
_DOCS = _REPO / "data" / "documents"                 # place the MW2 document corpus here


def load_absent_claims(reviewed_file: Path, method: str, article: str = None) -> dict:
    """Return {article: [ {claim_id, claim, lang}, ... ]} for ABSENT claims of `method`."""
    by_article = {}
    with reviewed_file.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("review_verdict") != "ABSENT":
                continue
            strat = r.get("strategies") or [r.get("strategy")]
            if method not in strat:
                continue
            art = r["article"]
            if article and art != article:
                continue
            by_article.setdefault(art, []).append(
                {"claim_id": r.get("claim_id"), "claim": r["claim"], "lang": r.get("lang"),
                 "source_sentence": r.get("source_sentence", "")})
    return by_article


def build_article_pr(article_name: str, claims: list, model, docs_dir: Path,
                     method: str, dry_run: bool = False, min_importance: int = 1,
                     cluster_threshold: int = 25, cite: bool = True):
    article = load_article(docs_dir, article_name)
    if article is None:
        print(f"[skip] {article_name}: no English document", file=sys.stderr)
        return None

    # Content-quality gate: drop content-free claims before routing
    n_in = len(claims)
    claims, dropped = content_gate(article.title, claims, model, min_importance)
    if dropped:
        print(f"  [gate] {article_name}: dropped {len(dropped)}/{n_in} low-content claims "
              f"(e.g. {dropped[0]['claim'][:60]!r})")
    if not claims:
        print(f"[skip] {article_name}: all claims dropped by content gate", file=sys.stderr)
        return None

    # Re-attach source citations to the surviving claims (Approach A)
    registry = {}
    if cite:
        claims, registry = attach_citations(claims, docs_dir, article_name)
        cited, tot = coverage(claims)
        print(f"  [cite] {article_name}: {cited}/{tot} claims got a source citation "
              f"({len(registry)} unique refs)")

    target = Target.wikipedia(article.title)

    if dry_run:
        routed = route_claims(article, claims, model, target)
        routed_summary = {sid: len(cs) for sid, cs in routed.items()}
        print(f"\n=== {article_name} — {len(claims)} ABSENT claims, "
              f"{len(article.sections)} sections ===")
        print(authoring_outline(article))
        print("\nrouting:")
        for sid, cs in sorted(routed.items()):
            sec = article.section(sid)
            name = "NEW SECTION(S)" if sid == "NEW" else (
                "Introduction" if sec and sec.is_lead else (sec.heading if sec else sid))
            print(f"  {name}: {len(cs)} claims")
            for c in cs[:3]:
                print(f"      - {c['claim'][:80]}")
            if len(cs) > 3:
                print(f"      ... (+{len(cs) - 3} more)")
        return None

    # The shared authoring pass: route -> rewrite touched sections -> plan and
    # draft new ones. Wikipedia citations are the <ref> numbers citations.py
    # attached to each claim.
    edits, new_sections, routed_summary = author(
        article, claims, model, target,
        refs_of=lambda c: c.get("cite_refs") or [],
        cluster_threshold=cluster_threshold)

    diff = render_pr(article.title, article.revision, method, edits, new_sections,
                     len(claims), registry=registry)
    doc = pr_to_dict(article.title, article.revision, method, edits, new_sections, routed_summary)
    doc["gate_dropped"] = [{"claim_id": c.get("claim_id"), "claim": c["claim"],
                            "importance": c.get("importance")} for c in dropped]
    doc["references"] = {str(n): registry[n] for n in sorted(registry)}
    proposal = render_claim_proposal(article.title, method, edits, new_sections)
    return diff, doc, proposal


def main():
    ap = argparse.ArgumentParser(description="Build stage-2 article-edit PRs from ABSENT claims.")
    ap.add_argument("--reviewed", type=Path, default=_KPR / "candidates" / "pr_reviewed.jsonl")
    ap.add_argument("--method", default="crosslingual")
    ap.add_argument("--documents-dir", type=Path, default=_DOCS)
    ap.add_argument("--out-dir", type=Path, default=_KPR / "rewrite" / "prs")
    ap.add_argument("--article", default=None, help="Build PR for one article")
    ap.add_argument("--limit-articles", type=int, default=None)
    ap.add_argument("--shard", type=int, default=0, help="this shard's index (0-based)")
    ap.add_argument("--nshards", type=int, default=1, help="total shards; article i handled by shard i%%nshards")
    ap.add_argument("--max-claims", type=int, default=None,
                    help="Cap claims per article (safety for huge articles)")
    ap.add_argument("--min-importance", type=int, default=1, choices=[0, 1, 2],
                    help="Content gate: keep claims with importance >= this "
                         "(0=keep all, 1=drop content-free [default], 2=only substantial)")
    ap.add_argument("--cluster-threshold", type=int, default=25,
                    help="Sections receiving more than this many claims are "
                         "organized into drafted subsections instead of a flat rewrite")
    ap.add_argument("--no-citations", action="store_true",
                    help="Disable source-citation attachment (Approach A)")
    ap.add_argument("--skip-existing", action="store_true",
                    help="Skip articles whose PR .diff already exists (resume)")
    ap.add_argument("--api-base", default=None)
    ap.add_argument("--api-model", default=None)
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--dry-run", action="store_true", help="Parse + route only; no rewrite")
    add_config_arg(ap)
    args = parse_args_with_config(ap)
    print(f"Loading ABSENT/{args.method} claims from {args.reviewed} ...")
    by_article = load_absent_claims(args.reviewed, args.method, args.article)
    articles = sorted(by_article)
    if args.nshards > 1:
        articles = [a for i, a in enumerate(articles) if i % args.nshards == args.shard]
        print(f"shard {args.shard}/{args.nshards}: {len(articles)} articles")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    if args.skip_existing:
        before = len(articles)
        articles = [a for a in articles if not (args.out_dir / f"{a}.diff").exists()]
        print(f"skip-existing: {before - len(articles)} already built, {len(articles)} to go")
    if args.limit_articles:
        articles = articles[: args.limit_articles]
    if not articles:
        sys.exit("No matching ABSENT claims found (or all already built).")
    total = sum(len(by_article[a]) for a in articles)
    print(f"{len(articles)} articles, {total} ABSENT claims")

    # Routing (stage A) needs the model even in --dry-run; only C/D are skipped.
    api_base, api_model = args.api_base, args.api_model
    if not api_base or not api_model:
        fb, fm = read_endpoint()
        api_base = api_base or fb
        api_model = api_model or fm or "qwen-27b"
    if not api_base:
        sys.exit("No --api-base and no server_ready.txt found.")
    model = ApiLLM(api_base=api_base, api_model=api_model,
                   max_tokens=args.max_tokens, concurrency=args.concurrency)
    print(f"Backend: {api_base} ({api_model})")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    failed = []
    for n, art in enumerate(articles, 1):
        claims = by_article[art]
        if args.max_claims:
            claims = claims[: args.max_claims]
        try:
            result = build_article_pr(art, claims, model, args.documents_dir,
                                      args.method, dry_run=args.dry_run,
                                      min_importance=args.min_importance,
                                      cluster_threshold=args.cluster_threshold,
                                      cite=not args.no_citations)
        except Exception as exc:
            # one bad article (e.g. context overflow) must not kill the whole run
            print(f"[{n}/{len(articles)}] [ERROR] {art}: {type(exc).__name__}: {exc}",
                  file=sys.stderr)
            failed.append(art)
            continue
        if args.dry_run or result is None:
            continue
        diff, doc, proposal = result
        (args.out_dir / f"{art}.diff").write_text(diff, encoding="utf-8")
        (args.out_dir / f"{art}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2))
        (args.out_dir / f"{art}.proposal.md").write_text(proposal, encoding="utf-8")
        ne = sum(1 for e in doc["section_edits"] if e["status"] == "modified")
        print(f"[{n}/{len(articles)}] {art}: {len(claims)} claims → "
              f"{ne} sections modified, {len(doc['new_sections'])} new → {art}.diff")

    if failed:
        print(f"\n{len(failed)} article(s) failed: {failed[:20]}", file=sys.stderr)

    if not args.dry_run:
        print(f"\nDone. PRs in {args.out_dir}")


if __name__ == "__main__":
    main()
