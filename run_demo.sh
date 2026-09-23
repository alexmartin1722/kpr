#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# KPR end-to-end demo.
#
# Merges facts from the GERMAN edition of "Nabonidus" into the
# ENGLISH Wikipedia article, producing a claim proposal + a document diff (the
# "changelog"). Runs all four stages on the example article in example/.
#
# Requirements:
#   pip install -e .                       # installs the kpr-* console scripts
#   an OpenAI-compatible LLM endpoint      # e.g. a vLLM server; Qwen3.5-27B used in the paper
#
# Usage:
#   ./run_demo.sh [API_BASE] [API_MODEL]
#   ./run_demo.sh http://localhost:8000/v1 Qwen/Qwen3.5-27B
#   KPR_API_BASE=... KPR_API_MODEL=... ./run_demo.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

API_BASE="${1:-${KPR_API_BASE:-http://localhost:8000/v1}}"
API_MODEL="${2:-${KPR_API_MODEL:-Qwen/Qwen3.5-27B}}"
API="--api-base $API_BASE --api-model $API_MODEL"

HERE="$(cd "$(dirname "$0")" && pwd)"
DOCS="$HERE/example/documents"          # input: {article}/{article}_{lang}.json
WORK="$HERE/example/work"               # all intermediates + the final PR
ART="Nabonidus"
rm -rf "$WORK"; mkdir -p "$WORK"

echo "using LLM endpoint: $API_BASE  ($API_MODEL)"

echo; echo "### 1/4  DECOMPOSE — atomic English claims from the EN + DE articles"
kpr-decompose --docs-dir "$DOCS" --article "$ART" \
    --output-dir "$WORK/decomp" --include-en $API

echo; echo "### 2/4  COMPARE — claims present in DE but absent from EN (set-difference)"
kpr-compare --article "$ART" \
    --strategy-a crosslingual --lang-a en \
    --strategy-b crosslingual --lang-b de \
    --decomp-dir "$WORK/decomp" --output-dir "$WORK/claim_diffs" --mode api $API

echo; echo "### 3/4  PROPOSE + REVIEW"
echo "  (a) cleaned candidate pool (dedup; no LLM)"
kpr-build-candidates --diff-dir "$WORK/claim_diffs" --strategy crosslingual --lang de \
    --keep-verdicts SUPPORTED UNJUDGED --out "$WORK/candidates/pr_candidates.jsonl"
echo "  (b) review each candidate vs the FULL English article -> SUPPORTED/ABSENT/CONTRADICTED"
kpr-review --candidates "$WORK/candidates/pr_candidates.jsonl" \
    --documents-dir "$DOCS" --output-dir "$WORK/reviews" $API
echo "  (c) aggregate -> pr_reviewed.jsonl + additions.jsonl (PR) + conflicts.jsonl (adjudication)"
kpr-aggregate --reviews-dir "$WORK/reviews" --out-dir "$WORK/candidates"

echo; echo "### 4/4  CHANGELOG — route ABSENT claims + rewrite sections (KPR rewrite)"
kpr-build-pr --reviewed "$WORK/candidates/pr_reviewed.jsonl" --method crosslingual \
    --documents-dir "$DOCS" --out-dir "$WORK/prs" --article "$ART" $API

echo; echo "### DONE."
echo "  Claim proposal + conflicts : $WORK/candidates/{additions,conflicts}.jsonl"
echo "  PR (claim proposal + diff) : $WORK/prs/${ART}.json"
