# Knowledge Pull Requests for Continual Document Authoring

<div align="center">
<a href="" target="_blank"><img src=https://img.shields.io/badge/arXiv-2510.24870-b5212f.svg?logo=arxiv></a>
</div>

A **knowledge pull request** (KPR) rewrites existing documents with information from external sources producing:
- a **claim proposal** — every new fact, in plain language, with the source sentence it came from; and
- a **document diff** — a sentence-level changelog showing exactly how the text changes.



The repo covers two settings:

- **Editing an existing document.** The main one in the paper: English Wikipedia articles enriched with facts that exist only in other language editions. 591 rewritten articles are in [`wikipedia/`](#the-rewritten-wikipedia-articles).
- **Writing and maintaining a report.** No starting document — write one from a collection of sources, then keep it current as new batches arrive.

## Install

```bash
pip install -e .
```

That gives you the `kpr-*` commands and one dependency, `openai`, used to talk to any OpenAI-compatible endpoint. Extras: `.[vllm]` to load a model in-process instead of calling a server, `.[tokenizer]` for exact multilingual token counting.

You will need an LLM endpoint. The paper uses Qwen3.5-27B served with vLLM, but anything speaking the OpenAI chat-completions API works.

## Quick start

`example/` ships the English and German editions of **Nabonidus**, the last king of Babylon. German Wikipedia has a deep Assyriology tradition and carries hundreds of facts the English article lacks; the demo merges them in.

```bash
./run_demo.sh http://localhost:8000/v1 Qwen/Qwen3.5-27B
```

It writes to `example/work/`:

| file | what it is |
|---|---|
| `candidates/additions.jsonl` | the claim proposal — facts to add |
| `candidates/conflicts.jsonl` | facts that contradict the English article |
| `prs/Nabonidus.json` | the pull request: proposal plus per-section diff |

## The rewritten Wikipedia articles

If you just want to read the output, `wikipedia/` has 591 English articles rewritten with the knowledge found in their other-language editions. One directory per article, three files each:

| file | what it is |
|---|---|
| `claim_proposal.md` | every proposed fact, grouped by the section it was routed to, each with its source language and the original sentence |
| `document_diff.md` | the sentence-level changelog, original → merged |
| `final_article.md` | the full English article after merging |

A proposal entry looks like this (from `wikipedia/Nabonidus/`):

```
### Family, children and descendants
- Nitoris was the daughter of Nebuchadnezzar II
  _[ar]_ ← "من المحتمل أنه كان على صلة بالملوك الكلدان عن طريق الزواج، وربما تزوج من نكتوريس..."
```

so you can trace any sentence in the merged article back to the edition it came from. That one article pulled 2,529 facts from 24 languages and surfaced 154 conflicts with the English text.

## QA data

`QA/` holds the question-answering sets from the paper's QA tables, if you want to benchmark against the same questions. Each question is built from a fact that exists in a non-English Wikipedia edition but is absent from (or contradicts) the English article — so answering it means the model had information English Wikipedia does not carry.

| file | questions | what it covers |
|---|---:|---|
| `multilingual_qa.jsonl` | 28,116 | facts from other-language editions, 557 articles |
| `english_qa.jsonl` | 25,483 | facts the English article already had — tests whether a rewrite *preserved* them |
| `hardest_100.jsonl` | 100 | the questions the open models we tested cannot answer closed-book |
| `hardest_100_translated.jsonl` | 100 | the same 100, asked in each fact's source language |
| `articles.txt` | — | the 591 articles the questions come from |

Each question file is exactly the set that gets scored — nothing to filter, no
article list to apply. Score on unique questions (rows run ~3% higher, since
one question can come from two editions) and count an unanswered question as
wrong; those counts are the paper's denominators. The articles are the same
591 as in `wikipedia/`, so every question has a merged article to read
alongside it. `QA/README.md` has the fields and a snippet.

## Configs

Every command takes `--config`, so a run is a file rather than a shell line:

```bash
kpr-report --config configs/report_kpr.json
kpr-report --config configs/report_kpr.json --out-dir /tmp/try2   # flags override
```

`configs/` has a worked example per command, including which facts get filtered
before they reach the writer — the relevance gate, dedup and top-N for reports,
the content gate for Wikipedia. See `configs/README.md`.

## Running the Wikipedia pipeline

Every stage is a console script, and also `python -m knowledge_pr.<module>`. Point each at an endpoint with `--api-base/--api-model`, or set `KPR_SERVER_READY` to a file whose first two lines are the base URL and the
model name.

| Stage | Command |
|---|---|
| 1. Decompose each edition into atomic English claims | `kpr-decompose --docs-dir D --article A --output-dir O --include-en` |
| 2. Find claims present in another language but not English | `kpr-compare --article A --strategy-a crosslingual --lang-a en --strategy-b crosslingual --lang-b de --decomp-dir O --output-dir C --mode api` |
| 3a. Clean and dedupe the candidates | `kpr-build-candidates --diff-dir C --strategy crosslingual --lang de --keep-verdicts SUPPORTED UNJUDGED --out cand.jsonl` |
| 3b. Check each candidate against the full English article | `kpr-review --candidates cand.jsonl --documents-dir D --output-dir R` |
| 3c. Split into additions and conflicts | `kpr-aggregate --reviews-dir R --out-dir cands` |
| 4. Build the pull request | `kpr-build-pr --reviewed pr_reviewed.jsonl --method crosslingual --documents-dir D --out-dir P` |

Step 3b is what separates a genuinely new fact (`ABSENT`) from one the article
already states (`SUPPORTED`) or contradicts (`CONTRADICTED`). Only the new ones
are proposed; conflicts go to the queue for a human.

The rewrite is **faithful-fluent**: it writes natural encyclopedic prose and
merges related facts into single sentences, but every clause has to be
traceable to a provided fact. No added significance, no evaluative language, no
rounded numbers.

Input documents are MegaWika2 article JSON, laid out as
`documents/{article}/{article}_{lang}.json`. See `example/documents/` for the
shape.

## Running the report pipeline

Here there is no document to start from. The first batch of sources produces a
report; each later batch updates it.

```bash
kpr-decompose --docs docs.jsonl --out claims.jsonl
kpr-report --claims claims.jsonl --docs docs.jsonl --requests requests.jsonl \
    --condition kpr --out-dir reports
```

**Documents** are a JSONL of `{"doc_id", "text", "lang"}`. Adapters pull that
shape out of corpora you already have — `--ragtime-doc-ids` / `--ragtime-config`
for RAGTIME, `--docs-dir/--article` for MegaWika2 — and `--save-docs` freezes
the result so a rerun does not rescan a multi-gigabyte corpus.

**Requests** are a JSONL of `{"report_id", "request", "rounds": [[...], [...]]}`.
Each entry in `rounds` is one batch of document ids. Use `doc_ids` instead for a
single batch, or leave both out to use everything. RAGTIME-style
`title`/`background`/`problem_statement` fields are assembled into a request if
`request` is missing.

`--condition` picks how a new batch gets folded in:

| condition | what the writer sees for a new batch |
|---|---|
| `kpr` | only the facts that are new or that correct something |
| `conclaim` | every extracted fact, unfiltered |
| `context` | the full source documents behind those facts |
| `scratch` | every document so far, regenerated from nothing |
| `rewrite_cond` | the previous report plus the new documents, in one pass |

`kpr` never re-reads the sources. It extracts the batch's facts, keeps the ones
on topic for the request, collapses restatements, checks each against the
current report, and integrates only what is new — correcting facts are marked
so the stale value is replaced rather than left sitting next to its
replacement. Because facts are folded in a chunk at a time, there is no limit
on how much new material a round can carry. The other conditions concatenate
documents into the prompt and will drop what does not fit; dropped ids are
listed in `stats.dropped_doc_ids`.

Running several conditions at once gives them all the same first-round report,
so a strong starting point does not flatter one of them.

Output is one JSON per report and condition, plus the Markdown. Every round is
kept under `rounds`, and the last one is copied to the top level so you can
ignore rounds if you do not need them. Sentences carry `[N]` markers and
`citations` maps each `N` to the document id it came from.

## Environment variables

| variable | default | what it does |
|---|---|---|
| `KPR_SERVER_READY` | `server_ready.txt` | file holding the endpoint URL and model name |
| `KPR_TOKENIZER` | `Qwen/Qwen3.5-27B` | tokenizer for context budgeting; `none` falls back to a character estimate |
| `KPR_TOKENIZER_CACHE` | — | where to look for a cached tokenizer |
| `KPR_TOKENIZER_DOWNLOAD` | unset | set to `1` to allow fetching an uncached tokenizer |
| `KPR_RAGTIME_DOCS` | `/exp/scale25/ragtime/docs` | RAGTIME corpus location |

Context budgeting counts tokens rather than characters, because the same
paragraph of Chinese and English tokenizes very differently and a character
budget overflows the window. A cached tokenizer loads instantly; an uncached
one is only downloaded if you ask, so a run on a machine without HuggingFace
access does not stall.

## Repository layout

```
knowledge_pr/
  authoring/          routing claims into sections and rewriting them
  build_pr.py         the Wikipedia pipeline
  report.py           the report pipeline
  report_run.py       its driver (kpr-report)
  decompose_crosslingual.py, compare_claims.py, build_candidates.py,
  review_claims.py, aggregate_reviews.py    the claim stages
  article_model.py, citations.py, claims.py, corpus.py, requests.py,
  gate.py, dedup.py, render_pr.py, prompts.py, config.py, llm_api.py
configs/              a worked config per command
QA/                   evaluation sets
wikipedia/            591 rewritten articles
example/              demo inputs
```

Both pipelines share `authoring/`, so a fix to how claims are routed or
integrated applies to both.

## Citation
