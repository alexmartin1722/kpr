#!/usr/bin/env python3
"""
compare_claims.py — Set-difference comparison of claims between two documents.

For a given article and pair of decomposition outputs, computes:
  A − B  claims in A not covered by any claim in B
  B − A  claims in B not covered by any claim in A
  A ∩ B  claims present in both

Coverage is determined semantically by an LLM: a claim is "covered" if any
claim in the other set expresses the same information, even if worded differently.

Typical usage: compare the English baseline against a non-English document
processed through a decomposition strategy, to find what information each
language version has that the other lacks.

Output per article:
  output_dir/{strategy_b}/{article}_{lang_b}_vs_{lang_a}.json

Usage (local vLLM):
    python compare_claims.py \\
        --strategy-b  native_then_translate --lang-b fr \\
        --decomp-dir  outputs --output-dir  claim_diffs \\
        [--model Qwen/Qwen3.5-9B] [--tp 1] [--max-tokens 256]

Usage (API):
    python compare_claims.py \\
        --strategy-b  native_then_translate --lang-b fr \\
        --decomp-dir  outputs --output-dir  claim_diffs \\
        --mode api [--api-base http://localhost:8000/v1] [--api-model qwen-27b] \\
        [--concurrency 8] [--skip-existing]
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, DefaultDict, Dict, List, Optional, Tuple

from .config import add_config_arg, parse_args_with_config
from .prompts import COVERAGE_PROMPT

STRATEGIES = [
    "native_then_translate",
    "translate_then_decomp",
    "crosslingual",
    "llm_translate_then_decomp",
    "en_baseline",
]

# ---------------------------------------------------------------------------
# LLM wrapper — local vLLM or remote OpenAI-compatible API
# ---------------------------------------------------------------------------

class QwenLLM:
    """Local vLLM backend — loads model weights onto this machine's GPUs."""

    def __init__(
        self,
        model: str = "Qwen/Qwen3.5-9B",
        download_dir: str = "models",  # local vLLM cache (--mode local only)
        enable_thinking: bool = False,
        temperature: float = 0.0,
        top_p: float = 0.8,
        top_k: int = 20,
        max_tokens: int = 256,
        seed: int = 42,
        repetition_penalty: float = 1.0,
        presence_penalty: float = 1.5,
        tp: int = 1,
    ):
        from vllm import LLM, SamplingParams

        self.enable_thinking = enable_thinking
        self.llm = LLM(
            model=model,
            download_dir=download_dir,
            seed=seed,
            tensor_parallel_size=tp,
        )
        self.sampling_params = SamplingParams(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_tokens=max_tokens * 5 if enable_thinking else max_tokens,
            seed=seed,
            repetition_penalty=repetition_penalty,
            presence_penalty=presence_penalty,
        )

    def batch_infer(self, prompts: List[str]) -> List[str]:
        conversations = [[{"role": "user", "content": p}] for p in prompts]
        outputs = self.llm.chat(
            conversations,
            sampling_params=self.sampling_params,
            chat_template_kwargs={"enable_thinking": self.enable_thinking},
        )
        return [o.outputs[0].text for o in outputs]


class ApiLLM:
    """Remote API backend — calls an OpenAI-compatible vLLM server."""

    def __init__(
        self,
        api_base: str = "http://localhost:8000/v1",
        api_model: str = "qwen-27b",
        enable_thinking: bool = False,
        temperature: float = 0.0,
        max_tokens: int = 256,
        concurrency: int = 8,
    ):
        import getpass
        import openai

        self._client = openai.OpenAI(base_url=api_base, api_key="dummy")
        self._api_model = api_model
        self._enable_thinking = enable_thinking
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._concurrency = concurrency
        self._user = __import__("os").environ.get("USER") or getpass.getuser()

    def _call_one(self, prompt: str) -> str:
        import time
        for attempt in range(5):
            try:
                response = self._client.chat.completions.create(
                    model=self._api_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self._temperature,
                    max_tokens=self._max_tokens,
                    user=self._user,
                    extra_body={"chat_template_kwargs": {"enable_thinking": self._enable_thinking}},
                )
                msg = response.choices[0].message
                return msg.content or getattr(msg, "reasoning_content", None) or ""
            except Exception as e:
                if attempt == 4:
                    raise
                time.sleep(2 ** attempt)
        return ""

    def batch_infer(self, prompts: List[str]) -> List[str]:
        results: List[str] = [""] * len(prompts)
        with ThreadPoolExecutor(max_workers=self._concurrency) as pool:
            futures = {pool.submit(self._call_one, p): i for i, p in enumerate(prompts)}
            for future in as_completed(futures):
                results[futures[future]] = future.result()
        return results


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_claims(decomp_dir: Path, strategy: str, article: str, lang: str) -> List[Dict]:
    """
    Load all claim records for a given article + language from a strategy's output dir.
    Returns a flat list of dicts with the claim, its source sentence, the reconstructed
    paragraph it came from, and (for non-English docs) the translated source sentence.
    """
    path = decomp_dir / strategy / f"{article}_{lang}.jsonl"
    if not path.exists():
        return []

    # First pass: collect all sentence records so we can reconstruct paragraphs
    all_recs = []
    para_buckets: Dict[Any, List[Dict]] = defaultdict(list)
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            all_recs.append(rec)
            para_buckets[rec.get("para_idx")].append(rec)

    # Reconstruct each paragraph from its sorted sentences (original language)
    para_text: Dict[Any, str] = {}
    for para_idx, recs in para_buckets.items():
        sents = sorted(recs, key=lambda r: r.get("sent_idx", 0))
        para_text[para_idx] = " ".join(
            r["original_text"] for r in sents if r.get("original_text")
        )

    # Second pass: emit one record per claim with full context
    records = []
    for rec in all_recs:
        para_idx = rec.get("para_idx")
        # translated_text present on non-EN docs; llm_translated_text on strategy D
        translation = (
            rec.get("translated_text")
            or rec.get("llm_translated_text")
            or ""
        )
        for claim in rec.get("claims", []):
            records.append({
                "claim": claim,
                "source_sentence": rec.get("original_text", ""),
                "source_sentence_translation": translation,
                "source_paragraph": para_text.get(para_idx, ""),
                "para_idx": para_idx,
                "sent_idx": rec.get("sent_idx"),
            })
    return records


def find_articles(decomp_dir: Path, strategy: str, lang: Optional[str] = None) -> List[Tuple[str, str]]:
    """
    Return [(article, lang), ...] for all JSONL files in a strategy dir,
    optionally filtered to a specific language.
    """
    subdir = decomp_dir / strategy
    if not subdir.is_dir():
        return []
    results = []
    for p in sorted(subdir.glob("*.jsonl")):
        stem = p.stem  # e.g. Brussels_Basketball_fr
        parts = stem.rsplit("_", 1)
        if len(parts) != 2:
            continue
        article_name, file_lang = parts
        if lang is None or file_lang == lang:
            results.append((article_name, file_lang))
    return results


# ---------------------------------------------------------------------------
# Prompt building + response parsing
# ---------------------------------------------------------------------------

# Max claims from the other document per coverage prompt. Large articles get
# multiple chunks; a claim is COVERED if any chunk covers it (coverage is an OR
# over the other document's claims, so chunking preserves semantics).
B_CHUNK_SIZE = 200


def format_b_entries(b_claims: List[Dict]) -> str:
    """Format B claims grouped by source sentence for the coverage prompt."""
    # Group claims under their source sentence so each sentence (and its
    # translation) is printed once instead of once per claim.
    groups: Dict[Tuple[str, str], List[str]] = {}
    for r in b_claims:
        key = (r.get("source_sentence", ""), r.get("source_sentence_translation", ""))
        groups.setdefault(key, []).append(r["claim"])

    lines = []
    for (src, translation), claims in groups.items():
        if src:
            lines.append(f"- Source sentence: {src}")
            if translation and translation != src:
                lines.append(f"  Source sentence (EN): {translation}")
            lines.extend(f"  - Claim: {c}" for c in claims)
        else:
            lines.extend(f"- Claim: {c}" for c in claims)
    return "\n".join(lines)


def build_coverage_prompt(claim: str, a_sentence: str, b_claims: List[Dict]) -> str:
    b_entries = format_b_entries(b_claims)
    return (
        COVERAGE_PROMPT
        .replace("[b_entries]", b_entries)
        .replace("[claim]", claim)
        .replace("[a_sentence]", a_sentence)
    )


def parse_coverage(raw: str) -> Dict[str, Any]:
    raw = re.sub(r"<think>[\s\S]*?</think>", "", raw).strip()
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if not match:
        match = re.search(r"(\{[^{}]*\})", raw, re.DOTALL)
    if match:
        try:
            obj = json.loads(match.group(1))
            verdict = obj.get("verdict", "").strip().upper()
            if verdict not in ("COVERED", "NOT_COVERED"):
                verdict = "NOT_COVERED"
            return {"verdict": verdict, "covered_by": obj.get("covered_by")}
        except (json.JSONDecodeError, AttributeError):
            pass
    # keyword fallback
    upper = raw.upper()
    verdict = "COVERED" if "NOT_COVERED" not in upper and "COVERED" in upper else "NOT_COVERED"
    return {"verdict": verdict, "covered_by": None}


# ---------------------------------------------------------------------------
# Core comparison
# ---------------------------------------------------------------------------

def compare(
    a_claims: List[Dict],
    b_claims: List[Dict],
    model: QwenLLM,
) -> Tuple[List[Dict], List[Dict]]:
    """
    Returns (a_results, b_results).
    Each result list mirrors the input claims list with an added 'verdict' and 'covered_by'.
    The other document's claims are split into chunks of B_CHUNK_SIZE so prompts stay
    bounded regardless of article size; a claim is COVERED if any chunk covers it.
    """
    a_chunks = [a_claims[i:i + B_CHUNK_SIZE] for i in range(0, len(a_claims), B_CHUNK_SIZE)]
    b_chunks = [b_claims[i:i + B_CHUNK_SIZE] for i in range(0, len(b_claims), B_CHUNK_SIZE)]

    # Build all prompts: first all A→B checks, then all B→A checks.
    # owners[k] records which (side, claim index) prompt k belongs to.
    prompts: List[str] = []
    owners: List[Tuple[str, int]] = []
    for i, r in enumerate(a_claims):
        for chunk in b_chunks:
            prompts.append(build_coverage_prompt(r["claim"], r.get("source_sentence", ""), chunk))
            owners.append(("a", i))
    for i, r in enumerate(b_claims):
        for chunk in a_chunks:
            prompts.append(build_coverage_prompt(r["claim"], r.get("source_sentence", ""), chunk))
            owners.append(("b", i))

    if not prompts:
        return [], []

    raw_outputs = model.batch_infer(prompts)

    a_results = [{**r, "verdict": "NOT_COVERED", "covered_by": None} for r in a_claims]
    b_results = [{**r, "verdict": "NOT_COVERED", "covered_by": None} for r in b_claims]
    for (side, i), raw in zip(owners, raw_outputs):
        coverage = parse_coverage(raw)
        results = a_results if side == "a" else b_results
        if coverage["verdict"] == "COVERED" and results[i]["verdict"] != "COVERED":
            results[i].update(coverage)

    return a_results, b_results


def build_diff(
    a_results: List[Dict],
    b_results: List[Dict],
    article: str,
    lang_a: str,
    strategy_a: str,
    lang_b: str,
    strategy_b: str,
) -> Dict:
    a_minus_b = [r for r in a_results if r["verdict"] == "NOT_COVERED"]
    b_minus_a = [r for r in b_results if r["verdict"] == "NOT_COVERED"]
    a_and_b   = [r for r in a_results if r["verdict"] == "COVERED"]

    return {
        "article": article,
        "lang_a": lang_a,
        "strategy_a": strategy_a,
        "lang_b": lang_b,
        "strategy_b": strategy_b,
        "stats": {
            "total_a": len(a_results),
            "total_b": len(b_results),
            "a_minus_b": len(a_minus_b),
            "b_minus_a": len(b_minus_a),
            "intersection": len(a_and_b),
            "a_coverage_pct": round(100 * len(a_and_b) / len(a_results), 1) if a_results else 0.0,
            "b_coverage_pct": round(100 * (len(b_results) - len(b_minus_a)) / len(b_results), 1) if b_results else 0.0,
        },
        "a_minus_b": a_minus_b,
        "b_minus_a": b_minus_a,
        "intersection": a_and_b,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

_DATA = Path(__file__).resolve().parents[1] / "data"   # repo-root/data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Set-difference comparison of claims between two decomposed documents."
    )
    parser.add_argument(
        "--strategy-b", required=True, choices=STRATEGIES,
        help="Decomposition strategy used for document B (the non-English document)",
    )
    parser.add_argument(
        "--lang-b", required=True,
        help="Language code for document B (e.g. fr, es, ru)",
    )
    parser.add_argument(
        "--strategy-a", default="en_baseline", choices=STRATEGIES,
        help="Decomposition strategy for document A (default: en_baseline)",
    )
    parser.add_argument(
        "--lang-a", default="en",
        help="Language code for document A (default: en)",
    )
    parser.add_argument(
        "--article", default=None,
        help="Process only this article (e.g. Brussels_Basketball). "
             "Omit to process all articles found for strategy-b / lang-b.",
    )
    parser.add_argument(
        "--decomp-dir", type=Path, default=_DATA / "claims",
        help="Root decomposition output directory",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=_DATA / "claim_diffs",
        help="Root output directory; results written to {output-dir}/{strategy_b}/",
    )
    # Backend selection
    parser.add_argument(
        "--mode", default="local", choices=["local", "api"],
        help="'local' uses vLLM on this machine; 'api' calls the remote server",
    )
    # Local mode args
    parser.add_argument("--model", default="Qwen/Qwen3.5-9B")
    parser.add_argument("--download-dir", default="models",
                        help="HF model cache for --mode local (ignored in api mode)")
    parser.add_argument("--tp", type=int, default=1)
    # API mode args
    parser.add_argument("--api-base", default="http://localhost:8000/v1")
    parser.add_argument("--api-model", default="qwen-27b")
    parser.add_argument("--concurrency", type=int, default=8,
                        help="Max parallel API requests (api mode only)")
    # Shared args
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--enable-thinking", action="store_true")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip articles whose output file already exists (useful for resume)")
    add_config_arg(parser)
    args = parse_args_with_config(parser)
    # Collect articles to process
    if args.article:
        articles = [(args.article, args.lang_b)]
    else:
        articles = find_articles(args.decomp_dir, args.strategy_b, args.lang_b)
        if not articles:
            print(f"No files found for strategy '{args.strategy_b}' lang '{args.lang_b}' "
                  f"in {args.decomp_dir}", file=sys.stderr)
            sys.exit(1)

    out_subdir = args.output_dir / args.strategy_b
    out_subdir.mkdir(parents=True, exist_ok=True)

    if args.skip_existing:
        before = len(articles)
        articles = [
            (article, lang_b) for article, lang_b in articles
            if not (out_subdir / f"{article}_{lang_b}_vs_{args.lang_a}.json").exists()
        ]
        print(f"Skipped {before - len(articles)} already-complete articles.")

    print(f"Processing {len(articles)} article(s): "
          f"{args.lang_a}/{args.strategy_a}  vs  {args.lang_b}/{args.strategy_b}")

    if args.mode == "api":
        print(f"Backend: API  ({args.api_base}  model={args.api_model}  concurrency={args.concurrency})")
        model = ApiLLM(
            api_base=args.api_base,
            api_model=args.api_model,
            enable_thinking=args.enable_thinking,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            concurrency=args.concurrency,
        )
    else:
        print(f"Backend: local vLLM  model={args.model}  tp={args.tp}")
        model = QwenLLM(
            model=args.model,
            download_dir=args.download_dir,
            enable_thinking=args.enable_thinking,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            tp=args.tp,
        )

    failed: List[str] = []
    for article, lang_b in articles:
        a_claims = load_claims(args.decomp_dir, args.strategy_a, article, args.lang_a)
        b_claims = load_claims(args.decomp_dir, args.strategy_b, article, lang_b)

        if not a_claims and not b_claims:
            print(f"[skip] {article}: no claims found for either document")
            continue
        if not a_claims:
            print(f"[warn] {article}: no A claims ({args.strategy_a}/{args.lang_a}), skipping")
            continue
        if not b_claims:
            print(f"[warn] {article}: no B claims ({args.strategy_b}/{lang_b}), skipping")
            continue

        print(f"[{article}] A={len(a_claims)} claims, B={len(b_claims)} claims — "
              f"{len(a_claims) + len(b_claims)} coverage checks ...")

        try:
            a_results, b_results = compare(a_claims, b_claims, model)
        except Exception as exc:
            print(f"  [ERROR] {article}: {exc}", file=sys.stderr)
            failed.append(article)
            continue

        diff = build_diff(a_results, b_results, article,
                          args.lang_a, args.strategy_a, lang_b, args.strategy_b)

        s = diff["stats"]
        print(f"  A−B={s['a_minus_b']}  B−A={s['b_minus_a']}  A∩B={s['intersection']}  "
              f"A coverage={s['a_coverage_pct']}%  B coverage={s['b_coverage_pct']}%")

        out_path = out_subdir / f"{article}_{lang_b}_vs_{args.lang_a}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(diff, f, ensure_ascii=False, indent=2)

    if failed:
        print(f"\n{len(failed)} article(s) failed (likely context overflow):", file=sys.stderr)
        for a in failed:
            print(f"  {a}", file=sys.stderr)
    print(f"\nDone. Results in {out_subdir}")


if __name__ == "__main__":
    main()
