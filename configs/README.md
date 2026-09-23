# Configs

Every `kpr-*` command takes `--config`, so a run can be a file you read, diff
and commit rather than a shell line nobody can reconstruct three months later.

```bash
kpr-report --config configs/report_kpr.json
```

Anything you also pass on the command line wins, which makes one-off variations
cheap:

```bash
kpr-report --config configs/report_kpr.json --out-dir /tmp/try2 --no-gate
```

## Writing one

Keys are the command's long options. Dashes are optional and `-` and `_` are
interchangeable, so `--out-dir`, `out-dir` and `out_dir` all mean the same
thing. A key starting with `_` is ignored, which is how you keep notes in a
file that still has to be valid JSON.

A typo is an error rather than a silent no-op — if a key is not an option of
the command you ran, it says so and stops. Values are checked against the
option's allowed choices too.

Run `kpr-<command> --help` for the full option list.

## What's here

| file | command | what it does |
|---|---|---|
| `decompose_corpus.json` | `kpr-decompose` | a flat document collection → claims |
| `decompose_wikipedia.json` | `kpr-decompose` | one MegaWika2 article, all editions → claims |
| `decompose_ragtime.json` | `kpr-decompose` | pull a RAGTIME task config's documents, then decompose |
| `build_pr.json` | `kpr-build-pr` | reviewed claims → a Wikipedia pull request |
| `report_kpr.json` | `kpr-report` | a report, with facts filtered before they reach the writer |
| `report_unfiltered.json` | `kpr-report` | the same, with nothing filtered |
| `report_topk.json` | `kpr-report` | keep only the N most relevant facts |
| `report_all_conditions.json` | `kpr-report` | all five conditions, one shared first round |
| `report_ragtime.json` | `kpr-report` | RAGTIME topics and per-round document batches |

The paths in them point at `work/`; change them to wherever your data is.

## Choosing what gets filtered

This is the main thing a config decides, and the reason to keep one per
experiment rather than retyping flags.

**Reports.** Three filters sit between extracting facts from a new batch of
documents and writing them into the report:

| option | what it drops |
|---|---|
| `gate` | facts that are off-topic for the request |
| `dedup` | facts already stated by another document |
| `max-claims` | everything past the N most relevant (implies `gate`) |

The relevance gate is usually the one that matters. Extracting claims from a
large document set produces a lot that has nothing to do with what was asked,
and the gate is what keeps a report about a bridge closure from absorbing
everything else those newspapers happened to print. It judges each fact against
the *request*, not against the report being written, so it does not quietly
decide the answer in advance.

Set `gate-votes` above 1 to sample the gate repeatedly and keep facts by
majority. That is worth doing when you use `max-claims`: with a single vote a
fact is simply in or out, so there is no ranking for the cap to cut along.

Turning all three off (`report_unfiltered.json`) is the comparison — same
documents, same prompts, nothing filtered — which is how you tell what the
filtering is buying.

**Wikipedia.** One filter, `min-importance`, scoring how much encyclopedic
content a fact carries: `0` keeps everything, `1` drops content-free facts like
translation fragments and category labels, `2` keeps only substantial ones.
This asks whether a fact belongs in an encyclopedia at all — a different
question from whether it is on topic for a request, which is why the two
pipelines filter differently.
