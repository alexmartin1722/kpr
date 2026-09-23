#!/usr/bin/env python3
"""
aggregate_reviews.py — Merge per-article review files into pool-level exports.

Reads reviews/{article}.jsonl (from review_claims.py) and writes:

  pr_reviewed.jsonl  — all reviewed claims (one line per claim)
  additions.jsonl    — review_verdict == ABSENT   (the actual PR content)
  conflicts.jsonl    — review_verdict == CONTRADICTED (human adjudication
                       queue; includes the conflicting article span). Also the
                       input for the QA-conflict analysis: for each conflict,
                       which answer did a model give — the English article's
                       or the non-English claim's?
  review_summary.json — verdict counts overall, per language, per article

Usage:
    python aggregate_reviews.py [--reviews-dir reviews] [--out-dir candidates]
"""

from .config import add_config_arg, parse_args_with_config

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

_KPR_DIR = Path("/home/hltcoe/amartin/report_gen/changelog/knowledge-pr")


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate per-article reviews.")
    parser.add_argument("--reviews-dir", type=Path, default=_KPR_DIR / "reviews")
    parser.add_argument("--out-dir", type=Path, default=_KPR_DIR / "candidates")
    add_config_arg(parser)
    args = parse_args_with_config(parser)
    files = sorted(args.reviews_dir.glob("*.jsonl"))
    if not files:
        raise SystemExit(f"No review files in {args.reviews_dir}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    overall = Counter()
    by_lang = defaultdict(Counter)
    by_article = defaultdict(Counter)

    with (args.out_dir / "pr_reviewed.jsonl").open("w", encoding="utf-8") as all_f, \
         (args.out_dir / "additions.jsonl").open("w", encoding="utf-8") as add_f, \
         (args.out_dir / "conflicts.jsonl").open("w", encoding="utf-8") as con_f:
        for fp in files:
            with fp.open(encoding="utf-8") as f:
                for line in f:
                    rec = json.loads(line)
                    verdict = rec.get("review_verdict", "MISSING")
                    overall[verdict] += 1
                    by_lang[rec.get("lang", "?")][verdict] += 1
                    by_article[rec.get("article", "?")][verdict] += 1
                    all_f.write(line if line.endswith("\n") else line + "\n")
                    if verdict == "ABSENT":
                        add_f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    elif verdict == "CONTRADICTED":
                        con_f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    summary = {
        "n_articles": len(files),
        "overall": dict(overall.most_common()),
        "by_lang": {lang: dict(c.most_common()) for lang, c in sorted(by_lang.items())},
        "by_article": {a: dict(c.most_common()) for a, c in sorted(by_article.items())},
    }
    (args.out_dir / "review_summary.json").write_text(json.dumps(summary, indent=2))

    total = sum(overall.values())
    print(f"{total} reviewed claims across {len(files)} articles")
    for verdict, count in overall.most_common():
        print(f"  {verdict:14s} {count:8d}  ({100 * count / total:.1f}%)")
    print(f"\nWrote pr_reviewed.jsonl, additions.jsonl, conflicts.jsonl, "
          f"review_summary.json to {args.out_dir}")


if __name__ == "__main__":
    main()
