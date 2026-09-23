# QA evaluation sets

These are the question–answer sets used to measure whether a model actually
gained knowledge from a rewrite.

Each question is built from a single fact that appears in a non-English
Wikipedia edition but **not** in the English article on the same topic — or
that contradicts what the English article says. Answering one correctly means
the model had information English Wikipedia does not carry. Ask a model
closed-book and accuracy is low; give it the KPR-merged article and it goes up,
and the size of that gap is what the questions measure.

```json
{"question": "How many times did Van der Linde play for the Springboks in 2005?",
 "answer": "11",
 "claim": "Van der Linde played for the Springboks 11 times in 2005",
 "source_sentence": "Van der Linde het in 2005 11 keer vir die Springbokke gespeel...",
 "lang": "af", "article": "CJ_van_der_Linde",
 "review_verdict": "CONTRADICTED", "qa_grade": "A"}
```

## The files

| file | rows | unique questions | what it is |
|---|---:|---:|---|
| `multilingual_qa.jsonl` | 28,982 | 28,116 | facts from other-language editions, over 557 articles |
| `english_qa.jsonl` | 26,750 | 25,483 | facts already in the English article, over 588 articles |
| `hardest_100.jsonl` | 100 | 100 | the 100 hardest multilingual questions |
| `hardest_100_translated.jsonl` | 100 | 100 | those 100, asked in each fact's own language |
| `articles.txt` | 591 | — | the articles the questions come from |

Each question file is exactly the set that gets scored — there is no subset to select
and nothing to filter out. Run a model on the whole file.

Rows slightly outnumber unique questions because the same question can be
generated from more than one edition carrying the same fact; the extra rows
differ only in `lang` and `source_sentence`. Deduplicate on `question` before
scoring, or you will ask 3% of them twice.

**`multilingual_qa.jsonl`** is the main set — the knowledge a rewrite is
supposed to add. German, French and Russian dominate, with a long tail down to
single-digit counts. 92% of the facts are absent from English, 8% contradict it.

**`english_qa.jsonl`** is the other half of the story: questions about what the
English article *already* said. A rewrite that scores well on the multilingual
set but poorly here has added knowledge by damaging what was there, so the two
are meant to be read together.

**`hardest_100.jsonl`** is the subset no dense open model above 20B gets right
closed-book — facts genuinely outside parametric knowledge rather than merely
missing from one article. 26 languages, led by German (15), Russian (12) and
Japanese (9).

**`hardest_100_translated.jsonl`** asks the same 100 questions in the language
the fact came from, with the English wording kept in `question_en`. It answers
the obvious objection — maybe the model knows the fact but only in the source
language. It mostly does not: asking natively moves open models by 1–5 points.

## Scoring comparably

**Fix the denominator.** Score every system against every unique question in
the file, and count a question a system did not answer as wrong. Letting the
denominator shrink to whatever a system attempted flatters a system that skips
the hard ones.

```python
import json

rows = [json.loads(l) for l in open("multilingual_qa.jsonl")]
questions = {r["question"]: r["answer"] for r in rows}
len(questions)   # 28116  — the denominator, no filtering needed
```

That gives 28,116 for the multilingual set and 25,483 for English, which are
the numbers in the paper.

These two files were already restricted to the articles that every rewrite
method in the paper produced output for. Methods that rewrite different sets of
articles cannot be compared on their own sets, so the two articles some method
failed on — `Russia`, far larger than anything else, and `Fafner_in_the_Azure`
— were dropped for everyone. Their questions are not shipped, because nothing
scores them.

## Fields

`multilingual_qa.jsonl`:

| field | meaning |
|---|---|
| `question`, `answer` | the question and its gold answer |
| `claim` | the fact the question was generated from |
| `claim_id` | stable id for that fact |
| `lang` | the edition the fact came from |
| `article` | the English article it was proposed for |
| `review_verdict` | `ABSENT` (missing from English) or `CONTRADICTED` (conflicts) |
| `qa_grade` | generation quality, A or B; lower grades were dropped |
| `qa_grade_reason` | why the grader gave that grade |
| `source_sentence` | the original sentence, in its own language |
| `source_sentence_translation` | machine translation of it, where available |
| `para_idx`, `sent_idx` | where in the source article it appeared |

`english_qa.jsonl` has the same fields minus `claim_id` and `review_verdict`,
plus `strategy` (how the English claim was extracted).

`hardest_100.jsonl` is slimmer: `question`, `answer`, `gold_answer`, `lang`,
`article`, `review_verdict`. `hardest_100_translated.jsonl` adds `question_en`
and replaces `question` with the translated wording.

## How the sets relate

`hardest_100_translated` lines up with `hardest_100` one-to-one on
`question_en`.

`hardest_100` is **not** a subset of `multilingual_qa`. It was drawn before the
article restriction above, so 25 of its 100 questions come from the two
articles dropped there (23 from `Russia`, 2 from `Fafner_in_the_Azure`). It is
self-contained — question, answer and gold answer are all in the file — so
evaluate on it directly; just do not expect to find those 25 in the
multilingual set.

`articles.txt` lists all 591 articles the questions come from. It is the same
set as the rewritten articles in `../wikipedia/`, so every question here has a
merged article you can read alongside it.

## How the data was built

Each non-English edition of an article was decomposed into atomic English
claims, compared against the claims from the English article to find what was
missing, and each surviving candidate was checked against the full English text
to label it `SUPPORTED`, `ABSENT` or `CONTRADICTED`. The `ABSENT` and
`CONTRADICTED` facts became questions, which were then graded for quality;
only grade A and B questions are kept here. The pipeline that does all of this
is in the repo root — see the main README.
