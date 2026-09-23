#!/usr/bin/env python3
"""
build_candidates.py — Build the cleaned PR-candidate pool from claim diffs,
FOR A SINGLE DECOMPOSITION METHOD.

The decomposition method (native_then_translate, crosslingual, ...) is an
orthogonal experimental condition, NOT something to pool: the pipeline is
    decomp method -> compare claims -> knowledge PR -> article rewrite
and each method runs as its own independent track. This script therefore
builds one candidate pool per method; run it once per method into separate
output files and keep the downstream review/analysis separate too.

Takes b_minus_a claims (non-English claims not covered by the English claim
set) from fact-compare/claim_diffs for the chosen method, then:

  1. Joins per-claim faithfulness verdicts from fact-compare/eval and keeps
     only SUPPORTED claims (decomposition artifacts / hallucinations out).
  2. Deduplicates exact (normalized) duplicates within (article, lang) — i.e.
     the same claim text extracted from more than one sentence of the same
     article. This is intra-method only; different methods are never merged.
     Optional fuzzy dedup (token Jaccard).
  3. Mints a stable content-hash claim_id for every surviving claim.

Reads article/lang from the diff JSON fields (never the filename), and logs
every skipped file and unjoined claim instead of dropping silently.

Usage:
    python build_candidates.py --strategy native_then_translate
    python build_candidates.py --strategy crosslingual
        [--fuzzy-dedup] [--fuzzy-threshold 0.9]
        [--keep-verdicts SUPPORTED]
        [--out candidates/pr_candidates_<strategy>.jsonl]
"""

from .config import add_config_arg, parse_args_with_config

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

_REPO = Path(__file__).resolve().parents[1]          # repo root (kpr/)
_KPR_DIR = _REPO / "knowledge-pr"
_DATA = _REPO / "data"

FAITHFULNESS_VERDICTS = {"SUPPORTED", "HALLUCINATED", "CONTRADICTED", "CANNOT_DETERMINE"}

# Wiki category/classification markup that leaked into decomposition as
# "sentences" (e.g. "Classification:People from Prague Classification:Poets
# ..."). Claims decomposed from these are navigational cruft, not article
# facts. Patterns are checked against the source sentence and its translation.
_CRUFT_PATTERN = re.compile(
    r"(?:Category|Classification|Kategorie|Catégorie|Categoría|Categoria|"
    r"Categorie|Kategoria|Kategori|Категория|Категорія|分類|分类|カテゴリ):"
)


def is_cruft(entry: Dict) -> bool:
    text = f"{entry.get('source_sentence') or ''} {entry.get('source_sentence_translation') or ''}"
    return bool(_CRUFT_PATTERN.search(text))


def normalize_claim(text: str) -> str:
    """Normalization used for dedup keys and claim IDs (not for display)."""
    text = text.strip().casefold()
    text = re.sub(r"\s+", " ", text)
    text = text.rstrip(".")
    return text


def claim_id_for(article: str, lang: str, claim: str) -> str:
    key = f"{article}|{lang}|{normalize_claim(claim)}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]


def load_eval_verdicts(eval_dir: Path, strategy: str, article: str, lang: str) -> Dict[Tuple, str]:
    """Map (para_idx, sent_idx, claim) -> faithfulness verdict for one doc."""
    path = eval_dir / strategy / f"{article}_{lang}.jsonl"
    vmap: Dict[Tuple, str] = {}
    if not path.exists():
        return vmap
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            for v in rec.get("verdicts", []):
                vmap[(rec.get("para_idx"), rec.get("sent_idx"), v.get("claim"))] = v.get("verdict")
    return vmap


def token_jaccard(a: str, b: str) -> float:
    ta, tb = set(normalize_claim(a).split()), set(normalize_claim(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build cleaned PR-candidate claim pool.")
    parser.add_argument("--diff-dir", type=Path, default=_DATA / "claim_diffs")
    parser.add_argument("--eval-dir", type=Path, default=_DATA / "eval")
    parser.add_argument("--strategy", default="native_then_translate",
                        help="Decomposition method to build a pool for. Methods are "
                             "independent tracks and are never pooled — run once per method.")
    parser.add_argument("--keep-verdicts", nargs="+", default=["SUPPORTED"],
                        help="Faithfulness verdicts to keep (default: SUPPORTED only)")
    parser.add_argument("--keep-cruft", action="store_true",
                        help="Keep claims whose source sentence is category/"
                             "classification markup (dropped by default)")
    parser.add_argument("--fuzzy-dedup", action="store_true",
                        help="Also merge near-duplicate claims within (article, lang) "
                             "by token Jaccard similarity")
    parser.add_argument("--fuzzy-threshold", type=float, default=0.9)
    parser.add_argument("--lang", default=None, help="Restrict to one language code")
    parser.add_argument("--out", type=Path, default=None,
                        help="Output path (default: candidates/pr_candidates_<strategy>.jsonl)")
    add_config_arg(parser)
    args = parse_args_with_config(parser)
    if args.out is None:
        args.out = _DATA / "candidates" / f"pr_candidates_{args.strategy}.jsonl"

    keep_verdicts = {v.upper() for v in args.keep_verdicts}
    bad = keep_verdicts - FAITHFULNESS_VERDICTS
    if bad:
        sys.exit(f"Unknown faithfulness verdicts: {bad}")

    stats = Counter()
    verdict_drops = Counter()
    skipped_files: List[str] = []

    # kept[(article, lang, norm_claim)] = record (intra-method dedup)
    kept: Dict[Tuple[str, str, str], Dict] = {}

    strategy = args.strategy
    strat_dir = args.diff_dir / strategy
    if not strat_dir.is_dir():
        sys.exit(f"No diff dir for strategy '{strategy}': {strat_dir}")
    files = sorted(strat_dir.glob("*_vs_en.json"))
    print(f"[{strategy}] {len(files)} diff files")

    for fp in files:
        try:
            diff = json.loads(fp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            skipped_files.append(f"{fp} ({exc})")
            continue

        article = diff.get("article")
        lang = diff.get("lang_b")
        if not article or not lang:
            skipped_files.append(f"{fp} (missing article/lang_b fields)")
            continue
        if args.lang and lang != args.lang:
            continue

        vmap = load_eval_verdicts(args.eval_dir, strategy, article, lang)

        for entry in diff.get("b_minus_a", []):
            claim = entry.get("claim", "").strip()
            if not claim:
                continue
            stats["total_b_minus_a"] += 1

            if not args.keep_cruft and is_cruft(entry):
                stats["dropped_cruft"] += 1
                continue

            verdict = vmap.get((entry.get("para_idx"), entry.get("sent_idx"), claim))
            if verdict is None:
                verdict = "UNJUDGED"
                stats["unjoined"] += 1
            if verdict not in keep_verdicts:
                verdict_drops[verdict] += 1
                continue
            stats["faithful"] += 1

            key = (article, lang, normalize_claim(claim))
            if key in kept:
                # same claim text from another sentence of the same article
                stats["exact_dups_merged"] += 1
                continue

            kept[key] = {
                "claim_id": claim_id_for(article, lang, claim),
                "article": article,
                "lang": lang,
                "claim": claim,
                "strategy": strategy,
                "faithfulness": verdict,
                "source_sentence": entry.get("source_sentence", ""),
                "source_sentence_translation": entry.get("source_sentence_translation", ""),
                "source_paragraph": entry.get("source_paragraph", ""),
                "para_idx": entry.get("para_idx"),
                "sent_idx": entry.get("sent_idx"),
            }

    # Optional fuzzy dedup within (article, lang)
    records = list(kept.values())
    if args.fuzzy_dedup:
        by_doc: Dict[Tuple[str, str], List[Dict]] = {}
        for rec in records:
            by_doc.setdefault((rec["article"], rec["lang"]), []).append(rec)
        survivors: List[Dict] = []
        for _, group in sorted(by_doc.items()):
            group_kept: List[Dict] = []
            for rec in group:
                dup_of = next(
                    (g for g in group_kept
                     if token_jaccard(rec["claim"], g["claim"]) >= args.fuzzy_threshold),
                    None,
                )
                if dup_of is not None:
                    stats["fuzzy_dups_merged"] += 1
                else:
                    group_kept.append(rec)
            survivors.extend(group_kept)
        records = survivors

    records.sort(key=lambda r: (r["article"], r["lang"], r["para_idx"] or 0, r["sent_idx"] or 0))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    summary = {
        "strategy": args.strategy,
        "total_b_minus_a": stats["total_b_minus_a"],
        "dropped_cruft": stats["dropped_cruft"],
        "dropped_by_faithfulness": dict(verdict_drops),
        "faithful": stats["faithful"],
        "unjoined_eval": stats["unjoined"],
        "exact_dups_merged": stats["exact_dups_merged"],
        "fuzzy_dups_merged": stats["fuzzy_dups_merged"],
        "final_candidates": len(records),
        "skipped_files": skipped_files,
        "keep_verdicts": sorted(keep_verdicts),
        "fuzzy_dedup": args.fuzzy_dedup,
    }
    stats_path = args.out.with_suffix(".stats.json")
    stats_path.write_text(json.dumps(summary, indent=2))

    print(json.dumps({k: v for k, v in summary.items() if k != "skipped_files"}, indent=2))
    if skipped_files:
        print(f"[warn] {len(skipped_files)} diff files skipped — see {stats_path}", file=sys.stderr)
    print(f"\nWrote {len(records)} candidates to {args.out}")


if __name__ == "__main__":
    main()
