# Rewritten Wikipedia articles

591 English Wikipedia articles, each merged with the knowledge found in its
other-language editions. Together they add **132,047 facts** drawn from 48
languages, and surface **11,122 places where an edition contradicts the English
text**.

Most articles are modest — the median picks up 48 facts — but the tail is long:
`Russia/` alone proposes 36,081.

## What's in each directory

One directory per article, three files:

| file | what it is |
|---|---|
| `claim_proposal.md` | every proposed fact, grouped by the section it was routed to, each with its source language and the original sentence |
| `document_diff.md` | a sentence-level diff, original English → merged |
| `final_article.md` | the full article after merging |

The proposal is the reviewable part. Each fact carries the language it came
from and the sentence it was extracted from, so nothing in the merged article
is unattributable:

```
### Family, children and descendants
- Nitoris was the daughter of Nebuchadnezzar II
  _[ar]_ ← "من المحتمل أنه كان على صلة بالملوك الكلدان عن طريق الزواج، وربما تزوج من نكتوريس..."
```

Facts that *contradict* the English article are listed separately from the
additions. They are never merged in — a disagreement between two editions is
not something to resolve automatically, so it is surfaced for a human instead.

The diff is sentence-per-line, so a changed fact shows up as one `-`/`+` pair
rather than a reflowed paragraph:

```diff
@@ -25,2 +25,54 @@
 He may have been alive in exile as late as the reign of Darius the Great (522–486 BC).
+
+== Names and titles ==
+
+Nabonid is also known as Nabonaid and Nabunaid.
```

## Which languages contributed

French, German and Spanish appear most often (274, 243 and 212 articles), then
Italian, Russian and Arabic. The full spread is 48 languages, and the smaller
editions matter more than their volume suggests — they tend to carry local
detail no larger edition has.

## Reading these

`Nabonidus/` is a good place to start: the last king of Babylon, where German
and Arabic scholarship both carry a great deal that English does not. It pulls
2,529 facts from 24 editions and flags 154 conflicts.

The rewrites are faithful-fluent — the text reads as normal encyclopedic prose,
but every clause traces back to a proposed fact. No added significance, no
evaluative language, no numbers rounded on the way in.

To regenerate any of these from scratch, or run the pipeline on an article of
your own, see the main README; `../run_demo.sh` walks through one article end
to end.
