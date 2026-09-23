"""Prompts for the knowledge-pr pipeline."""

# Review a batch of candidate claims against the full English article text.
# Three-way verdict: SUPPORTED (already in article), ABSENT (genuinely new),
# CONTRADICTED (conflicts with the article — flag for human adjudication).
# Placeholders: [article_title], [article_text], [claims]
REVIEW_PROMPT = """You are reviewing proposed additions to the English Wikipedia article "[article_title]". Each numbered claim below was extracted from a non-English edition of the same article. For each claim, determine its relationship to the ARTICLE TEXT:

- SUPPORTED — the article already states this information, either directly or through a more specific statement that entails it. The claim adds nothing new.
- ABSENT — the article does not state this information, and nothing in the article conflicts with it. The claim is a candidate addition.
- CONTRADICTED — the article states something incompatible with the claim (a different date, number, name, place, quantity, or relationship).

Rules:
- Judge ONLY against the article text below. Do not use outside knowledge about the topic.
- A claim that is partially in the article: if the new part conflicts with the article, use CONTRADICTED; if the new part is simply not mentioned, use ABSENT.
- For SUPPORTED and CONTRADICTED, copy the single most relevant sentence or span from the article verbatim into "evidence" (at most 40 words). For ABSENT, set "evidence" to null.

ARTICLE TEXT:
[article_text]

CLAIMS:
[claims]

Respond with ONLY a JSON array, one object per claim, in order:
[{"idx": 1, "verdict": "SUPPORTED", "evidence": "..."}, {"idx": 2, "verdict": "ABSENT", "evidence": null}, ...]"""


# Rewrite claims to be self-contained (ablation variant).
# Placeholders: [article_title], [claims]
DECONTEXT_PROMPT = """The following claims were extracted from the Wikipedia article "[article_title]". Some claims are not self-contained: they use pronouns ("he", "she", "it"), definite references ("the building", "the election"), or relative time ("that year", "later") that only make sense next to their source sentence.

Rewrite each claim so it is fully self-contained and understandable in isolation:
- Replace pronouns and definite references with the full entity name, using the article title and the source sentence to resolve them.
- Replace relative time expressions with absolute ones when the source sentence makes them resolvable; otherwise leave them.
- Do NOT add any information that is not in the claim or its source sentence. Do NOT change what the claim asserts.
- If a claim is already self-contained, return it unchanged.

Each item below gives the claim and the sentence it was extracted from.

CLAIMS:
[claims]

Respond with ONLY a JSON array, one object per claim, in order:
[{"idx": 1, "claim": "rewritten self-contained claim"}, ...]"""

# ── Claim decomposition + comparison prompts (stages 1-2) ─────────────────────
COVERAGE_PROMPT = """\
You are comparing claims extracted from two documents about the same topic.

Below are claims from document B, grouped under the source sentence they \
were extracted from (source text may be in any language; an English translation is provided \
where available):
[b_entries]

Does the following claim from document A express information that is semantically covered by \
any claim in document B?
A claim is "covered" only if at least one B claim expresses the same specific fact, even if \
worded differently. The specific information must actually be present in a B claim — a more \
general B claim about the same topic does not count. A claim containing a specific date, \
statistic, name, or event is only covered if that same specific detail appears in a B claim. \
Use the source sentences to inform your judgment.
A claim is "not covered" if no B claim contains the same specific information.

Claim from A: "[claim]"
Source sentence (document A): "[a_sentence]"

Respond with a JSON object only:
{"verdict": "COVERED" or "NOT_COVERED", "covered_by": "<exact text of the covering B claim, or null>"}"""


# ── LLM judge: evaluate English claims against a source-language sentence ─

DECOMP_CROSSLINGUAL_PROMPT = """\
Instructions:
- You are given a paragraph and one sentence from the paragraph to decompose
- The text may be in any language
- Decompose the sentence into atomic claims and output them in ENGLISH regardless of the input language
- You must output a JSON array: [{"claim": "..."}, {"claim": "..."}, ...]

##PARAGRAPH##: Le 15 avril 2019, peu avant 18h20 CEST, un incendie s'est déclaré dans la charpente de la cathédrale Notre-Dame de Paris, une cathédrale catholique médiévale située à Paris, en France. Au moment où l'incendie a été éteint, la flèche en bois de la cathédrale s'était effondrée, la majeure partie de la toiture en bois avait été détruite et les murs supérieurs de la cathédrale avaient été gravement endommagés.
##SENTENCE##: Le 15 avril 2019, peu avant 18h20 CEST, un incendie s'est déclaré dans la charpente de la cathédrale Notre-Dame de Paris, une cathédrale catholique médiévale située à Paris, en France.
##DECOMPOSITION##:
```json
[
    {"claim": "A structural fire broke out"},
    {"claim": "The fire broke out on 15 April 2019"},
    {"claim": "The fire broke out just before 18:20 CEST"},
    {"claim": "The fire broke out in the roof space"},
    {"claim": "Notre-Dame de Paris is a medieval Catholic cathedral"},
    {"claim": "Notre-Dame de Paris is located in Paris, France"}
]
```

##PARAGRAPH##: El huracán Irma fue un extremadamente poderoso huracán de Cabo Verde que causó una destrucción generalizada en su camino a principios de septiembre de 2017. Irma fue el primer huracán de categoría 5 en golpear las Islas de Barlovento, seguido por María dos semanas después.
##SENTENCE##: El huracán Irma fue un extremadamente poderoso huracán de Cabo Verde que causó una destrucción generalizada en su camino a principios de septiembre de 2017.
##DECOMPOSITION##:
```json
[
    {"claim": "Hurricane Irma was a Cape Verde hurricane"},
    {"claim": "Hurricane Irma was extremely powerful"},
    {"claim": "Hurricane Irma caused widespread destruction"},
    {"claim": "Hurricane Irma occurred in early September 2017"}
]
```

##PARAGRAPH## [paragraph]
##SENTENCE## [sentence]
##DECOMPOSITION##:"""


# ═══════════════════════════════════════════════════════════════════════════
# Report pipeline — the generation side.
#
# Where the Wikipedia pipeline edits an existing article, these build and then
# iteratively update a report from a document collection. Placeholders are
# bracketed tokens replaced with str.replace.
#
#   GATE_RELEVANCE     is this claim on-topic for the report request?
#   DEDUP              collapse restatements across documents
#   REPORT_FROM_*      write a report from claims / from documents
#   REPORT_REVIEW      is this claim already in the report, absent, or contradicted?
#   REPORT_ROUTE       which section does this claim belong in?
#   REPORT_SECTION_*   fold new information into one section
#   REWRITE_COND       full conditioned rewrite (the whole-report baseline)
# ═══════════════════════════════════════════════════════════════════════════

# The relevance gate. Depends on the report REQUEST, not on the report being
# written, so it does not presuppose the output it is filtering for — unlike
# the Wikipedia CHECKWORTHY_PROMPT gate, which scores encyclopedic importance.
# Placeholders: [request], [claims]
GATE_RELEVANCE_PROMPT = """\
A user requested the following report:

REPORT REQUEST:
[request]

Below are candidate facts extracted from source documents. For EACH fact, decide whether it is ON-TOPIC and relevant to include in THIS report — i.e. it directly addresses the report request or provides context a reader of this report would need. Mark a fact NOT relevant if it is off-topic, about an unrelated event/entity, generic boilerplate, or would not belong in this specific report even if true.

Judge relevance to the request only; do not judge whether the fact is interesting or novel.

CANDIDATE FACTS:
[claims]

Respond with ONLY a JSON array, one object per fact, in order:
[{"idx": 1, "relevant": true}, {"idx": 2, "relevant": false}, ...]"""


# Cross-document dedup. Fine-grained decomposition over many documents restates
# the same fact many ways; collapse that before writing.
# Placeholders: [claims]
DEDUP_PROMPT = """\
You are cleaning a list of factual claims extracted from many documents about the same topic. Many are exact duplicates, paraphrases (the same fact stated differently), or one claim is fully entailed by another.

Merge redundant claims: for each DISTINCT fact, keep exactly ONE clear, complete, self-contained claim and drop the restatements. Prefer the most specific, complete phrasing. Do NOT merge claims that state different facts (different entities, numbers, dates, events). Do NOT add any new information.

CLAIMS:
[claims]

Output ONLY a JSON array of the deduplicated canonical claims (strings):
["...", "...", ...]"""


# ── shared rule blocks ─────────────────────────────────────────────────────
# Every report sentence carries the [N] tag(s) of what it used; a per-report
# registry maps N -> doc_id, which is what CiteF1 needs.
# Same citation convention as the shared authoring prompts: a claim carries a
# trailing "[cite: 3]" tag and the model emits "[3]" on the sentence using it.
_CITE_CLAIMS_RULE = (
    "- CITATIONS: some facts end with a tag like [cite: 3]. Append the marker(s) at the END "
    "of the sentence that uses the fact (\"...Army.[3]\"); combine when merging (\"...[3][5]\"). "
    "Use only numbers given; never invent; never write the \"[cite: ...]\" text. PRESERVE any "
    "[N] markers already in the text.")

_CITE_DOCS_RULE = (
    "- After EVERY sentence, cite the source document number(s) it is based on, "
    "in square brackets — e.g. [1] or [2][5]. The numbers are the \"[Document N]\" "
    "markers in the SOURCE DOCUMENTS. Every factual sentence must carry at least one citation.")

# The faithful-fluent contract: fluent merging is allowed, but no clause may go
# beyond what a fact states. The banners repeat at both ends because a
# mid-prompt rule alone gets dropped in long contexts.
_FAITHFUL_TOP = (
    "CRITICAL RULES (override fluency; apply to every sentence):\n"
    "1. FAITHFUL: write ONLY what the facts state. No added significance, evaluation, cause, "
    "effect, or characterization (e.g. \"pioneering\", \"renowned\", \"major\", "
    "\"successfully\"); no generalizing beyond the facts; keep every number, date, name, and "
    "qualifier exact.\n"
    "2. CONCISE & DENSE: aggressively MERGE related facts into as few sentences as possible. Do "
    "NOT restate a fact, pad, or spread one fact across multiple sentences. Fewer, denser, "
    "fully-supported sentences — never a long list of near-duplicate sentences.\n")

_FAITHFUL_BOTTOM = (
    "\nBEFORE YOU WRITE, RE-READ: (1) every clause directly stated by a fact — no evaluation, "
    "significance, cause, characterization, or invented nickname; numbers/qualifiers exact. "
    "(2) Be concise — merge aggressively, no restating or padding.")


# Write a report from claims. Placeholders: [request], [claims]
REPORT_FROM_CLAIMS_PROMPT = _FAITHFUL_TOP + """
You are an analyst writing an English-language report that answers the request below, using ONLY the facts provided.

[request]

Guidelines:
- Use ONLY the given facts; do not add outside knowledge.
- Organize the report into sections with Markdown headings ("## Section Title").
- Combine closely related facts into coherent sentences rather than one fact per line.
- Write one sentence per line under each heading; blank line between paragraphs.
""" + _CITE_CLAIMS_RULE + """
- Objective, factual tone. No preamble or meta-commentary.

FACTS:
[claims]
""" + _FAITHFUL_BOTTOM + """

Write the report now (Markdown, "## " headings, one sentence per line, every sentence cited [N]):"""


# Write a report from the documents themselves — the no-decomposition control.
# Placeholders: [request], [documents]
REPORT_FROM_DOCS_PROMPT = """\
You are an analyst writing an English-language report that answers the request below, using ONLY the information in the provided source documents. The documents may be in several languages; read them all and write the report in English.

[request]

Guidelines:
- Report ONLY facts supported by the source documents; do not add outside knowledge.
- Organize the report into sections with Markdown headings ("## Section Title").
- Write one sentence per line under each heading; blank line between paragraphs.
- Be comprehensive: cover every distinct, relevant fact the documents provide that bears on the request.
""" + _CITE_DOCS_RULE + """
- Objective, factual tone. No preamble or meta-commentary.

SOURCE DOCUMENTS:
[documents]

Write the report now (Markdown, "## " headings, one sentence per line, every sentence cited [N]):"""


# Review each new claim against the CURRENT report.
# Placeholders: [request], [report], [claims]
REPORT_REVIEW_PROMPT = """\
You are updating an English report (shown below) that answers the request. Each numbered claim was extracted from a newly retrieved source document. For each claim, determine its relationship to the CURRENT REPORT:

- SUPPORTED — the report already states this information (directly or via a more specific statement). Adds nothing new.
- ABSENT — the report does not state this, and nothing in the report conflicts with it. A candidate addition.
- CONTRADICTED — the report states something incompatible with the claim (a different date, number, name, place, outcome, or relationship).

[request]

CURRENT REPORT:
[report]

CLAIMS:
[claims]

Respond with ONLY a JSON array, one object per claim, in order:
[{"idx": 1, "verdict": "ABSENT"}, {"idx": 2, "verdict": "SUPPORTED"}, ...]"""


# Conditioned full rewrite: revise the whole prior report given new documents.
# Placeholders: [request], [previous], [documents]
REWRITE_COND_PROMPT = """\
You previously wrote the report below. A new batch of source documents has arrived (possibly in several languages). Produce an UPDATED English report that answers the request, incorporating any new relevant information from the new documents while preserving the information already in the report.

[request]

Guidelines:
- Keep all still-relevant information from the previous report; add new relevant facts from the new documents.
- If a new document contradicts the previous report (a changed number, date, name, outcome), prefer the new information and revise the report accordingly.
- Report ONLY facts supported by the previous report or the new documents; no outside knowledge.
- Markdown "## " headings, one sentence per line, blank line between paragraphs.
""" + _CITE_DOCS_RULE + """
- Objective, factual tone. No preamble or meta-commentary.

PREVIOUS REPORT:
[previous]

NEW SOURCE DOCUMENTS:
[documents]

Write the updated report now:"""

# The authoring prompts that used to live here — ROUTE, SECTION_UPDATE (and its
# relevance and documents variants), NEW_SECTIONS — are gone. There is one set
# of them now, shared with the Wikipedia pipeline, in
# `knowledge_pr.authoring.prompts`. What stays here is what only the report
# pipeline has: the relevance gate, cross-document dedup, writing a report from
# nothing, and the review and whole-report-rewrite steps.


# ═══════════════════════════════════════════════════════════════════════════
# Wikipedia profile — the content gate and the two rewrite-eval judges.
# ═══════════════════════════════════════════════════════════════════════════

CHECKWORTHY_PROMPT = """You are curating facts to add to the English Wikipedia article "[title]". Rate how much important, checkable factual content each candidate fact adds to an encyclopedia article, on a 0-2 scale:

- 0 = no real content: a translation or linguistic note (e.g. "the phrase X means Y"), a tautology, a sentence fragment, a category/navigation label, boilerplate, or nonsense.
- 1 = a minor but real factual detail.
- 2 = substantial factual content.

Be conservative about 0 — use it only when the item clearly carries no encyclopedic fact about the topic. When unsure between 0 and 1, choose 1.

CLAIMS:
[claims]

Respond with ONLY a JSON array, one object per claim, in order:
[{"idx": 1, "score": 2}, {"idx": 2, "score": 0}, ...]"""


# --- Rewrite-eval: is an added/changed sentence supported by the claims? -----
# Placeholders: [claims], [sentence]
ADDITION_SUPPORT_PROMPT = """We added or changed a sentence in a Wikipedia article using a set of source facts. Decide whether the sentence's information is fully supported by those facts (do not use outside knowledge).

SOURCE FACTS:
[claims]

SENTENCE:
[sentence]

Is every piece of information in the sentence supported by the source facts? Reply with exactly one word: YES, NO, or PARTIAL."""


# --- Rewrite-eval: is an original sentence's info preserved in the rewrite? --
# Placeholders: [original], [rewritten]
PRESERVATION_PROMPT = """A Wikipedia section was rewritten. Check whether the information in an ORIGINAL sentence is still present in the REWRITTEN section (possibly reworded or merged into another sentence).

ORIGINAL SENTENCE:
[original]

REWRITTEN SECTION:
[rewritten]

Is the original sentence's information still present in the rewritten section? Reply with exactly one word: YES (fully preserved), NO (dropped), or PARTIAL (some detail lost)."""

# --- Step A: route each ABSENT claim to an existing section or "new section" ---
# Placeholders: [title], [outline], [claims]
