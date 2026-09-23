"""The single authoring prompt set — the Wikipedia prompts, generalized.

These ARE the Wikipedia prompts. They are reproduced verbatim from the
changelog pipeline; the only edit is that three document-specific words became
slots, so a report can use the same prompts:

    [document]  'the English Wikipedia article "Nabonidus"' | 'the report "X"'
    [doctype]   'article' | 'report'
    [style]     'encyclopedic' | 'analytical'

Substituting the Wikipedia values reproduces the original strings character for
character, so the Wikipedia pipeline's behaviour is unchanged and its published
results still stand. The report pipeline is the side that changed: it dropped
its own routing, section-update and new-section prompts and adopted these.

    ROUTE_PROMPT            each claim -> an existing section, or a new one
    PLAN_STRUCTURE_PROMPT   group the claims that fit nowhere into new sections
    SECTION_REWRITE_PROMPT  integrate claims into an existing section
    NEW_SECTION_PROMPT      write one new section from its claims
    CLUSTER_SECTION_PROMPT  split an overloaded section into subsections

Citations follow the Wikipedia convention: a claim carries a trailing
`[cite: 3]` tag and the model emits `[3]` on the sentence that uses it. What
`3` refers to is the caller's business — a `<ref>` in an article, a source
document in a report — which is why the prompts never say.

Prompts with no Wikipedia counterpart (writing a report from nothing, the
relevance gate, cross-document dedup, review-against-the-report, the
whole-report rewrite) stay in `knowledge_pr.prompts`.
"""

# The Wikipedia profile's slot values. Substituting these into any prompt below
# reproduces the original Wikipedia prompt exactly; there is a check for that
# in the module's __main__.
WIKI_SLOTS = {"[document]": 'the English Wikipedia article "[title]"',
              "[doctype]": "article",
              "[style]": "encyclopedic"}

# --- Stage A: route each claim to a section, or 0 for a new one.
# Placeholders: [document], [doctype], [outline], [claims]
ROUTE_PROMPT = """\
You are editing [document]. Below is the [doctype]'s current section outline, then a list of new facts (claims) to add to the [doctype]. For EACH claim, choose the single existing section it best belongs in. If no existing section is a good fit, assign it 0 (a new section will be created for it).

Prefer an existing section — only use 0 when the claim's topic is genuinely not covered by any section.

SECTION OUTLINE:
[outline]

CLAIMS:
[claims]

Respond with ONLY a JSON array, one object per claim, in order:
[{"idx": 1, "section": 3}, {"idx": 2, "section": 0}, ...]
where "section" is the [n] index of the chosen section, or 0 for "needs a new section"."""

# --- Stage B: group the orphan claims into proposed new sections.
# Placeholders: [document], [outline], [claims]
PLAN_STRUCTURE_PROMPT = """\
You are editing [document]. The claims below did not fit any existing section (outline shown for context). Propose one or more NEW sections to hold them, grouping related claims together. Keep the number of new sections small; only propose a section when several claims share a topic, or a single claim is clearly its own topic.

EXISTING OUTLINE:
[outline]

ORPHAN CLAIMS:
[claims]

Respond with ONLY a JSON array of proposed sections:
[{"heading": "Reception", "after_section": 4, "claim_idxs": [1, 3, 5]}, ...]
- "heading": the new section title (Wikipedia style, plain).
- "after_section": the [n] index of the existing section this new section should follow (use the highest sensible index; 0 to place right after the lead).
- "claim_idxs": the claim numbers (from the list above) that belong in this section.
Every claim must appear in exactly one proposed section."""

# --- Stage C: integrate claims into an existing section.
# Placeholders: [document], [style], [heading], [current], [claims]
SECTION_REWRITE_PROMPT = """\
You are editing the "[heading]" section of [document]. Integrate the NEW FACTS into the section as fluent, natural [style] prose.

FAITHFULNESS — THE PRIMARY REQUIREMENT (a reader must be able to trace every word to a fact):
- Every clause you write must be directly and fully stated by one of the NEW FACTS, or already present in the CURRENT SECTION. Add NOTHING else.
- Do NOT add: causes, effects, significance, context, motivation, comparison, or transitions a fact does not state; evaluative words ("notable", "major", "successful", "renowned"); or generalizations/summaries of the facts.
- Preserve each fact's exact quantities, dates, names, titles, and qualifiers ("some", "reportedly", "circa", "approximately"). Never round, broaden, narrow, or infer a value the facts do not give.
- You MAY merge several facts about the same subject into one flowing sentence using coordination and lists — but ONLY join what the facts say; introduce no new relationship between them.
  Example — these facts:
    - The 1876 Constitution maintained Spain as a constitutional monarchy.
    - The 1876 Constitution granted the king the power to appoint members of the Senate.
    - The 1876 Constitution granted the king the power to repeal laws.
  become ONE sentence:
    "The 1876 Constitution maintained Spain as a constitutional monarchy and granted the king the power to appoint members of the Senate and to repeal laws."
  (Nothing about importance, cause, or consequence is added.)
- Keep existing sentences as-is unless a new fact must be woven in; place new prose next to the related existing content. Do not drop still-valid information.
- CITATIONS: some facts end with a tag like [cite: 3]. Append the marker(s) at the END of the sentence that uses the fact ("...Army.[3]"); combine when merging ("...[3][5]"). Use only numbers given; never invent; never write the "[cite: ...]" text.
- Objective, [style] tone. Output ONE SENTENCE PER LINE (a merged multi-fact sentence is ONE line). Blank line between paragraphs. No heading, no commentary.

CURRENT SECTION (one sentence per line):
[current]

NEW FACTS TO ADD:
[claims]

Respond with ONLY the rewritten section text, one sentence per line."""

# --- Stage D: write a new section from its claims.
# Placeholders: [document], [style], [heading], [claims]
NEW_SECTION_PROMPT = """\
You are writing the "[heading]" section of [document] using ONLY the facts below. Write fluent, natural [style] prose — not a list of one-fact sentences.

FAITHFULNESS — THE PRIMARY REQUIREMENT (a reader must be able to trace every word to a fact):
- Every clause you write must be directly and fully stated by one of the facts below. Add NOTHING else.
- Do NOT add: causes, effects, significance, context, motivation, comparison, or transitions a fact does not state; evaluative words ("notable", "major", "successful", "renowned"); or generalizations/summaries of the facts.
- Preserve each fact's exact quantities, dates, names, titles, and qualifiers ("some", "reportedly", "circa", "approximately"). Never round, broaden, narrow, or infer a value the facts do not give.
- You MAY merge several facts about the same subject into one flowing sentence using coordination and lists — but ONLY join what the facts say; introduce no new relationship between them.
  Example — these facts:
    - The 1876 Constitution maintained Spain as a constitutional monarchy.
    - The 1876 Constitution granted the king the power to appoint members of the Senate.
    - The 1876 Constitution granted the king the power to repeal laws.
  become ONE sentence:
    "The 1876 Constitution maintained Spain as a constitutional monarchy and granted the king the power to appoint members of the Senate and to repeal laws."
  (Nothing about importance, cause, or consequence is added.)
- CITATIONS: some facts end with a tag like [cite: 3]. Append the marker(s) at the END of the sentence ("...Army.[3]"); combine when merging ("...[3][5]"). Use only numbers given; never invent; never write the "[cite: ...]" text.
- Objective, [style] tone. Output ONE SENTENCE PER LINE (a merged multi-fact sentence is ONE line). Blank line between paragraphs. No heading, no commentary.

FACTS:
[claims]

Respond with ONLY the section text."""

# --- Split a section that received too many claims into subsections.
# Placeholders: [document], [style], [heading], [current], [claims]
CLUSTER_SECTION_PROMPT = """\
The "[heading]" section of [document] is receiving many new facts. Organize the new facts into a small number of coherent SUBSECTIONS (level-3 headings) so the section reads well instead of as one long list.

Guidelines:
- Group facts by sub-topic. Aim for roughly 10-20 facts per subsection, and create AS MANY subsections as needed to keep each one focused — do not force a large set of facts into a few oversized subsections.
- Give each subsection a short, plain, [style] heading that fits under "[heading]".
- Every fact must go in exactly one subsection.

CURRENT SECTION (for context):
[current]

NEW FACTS:
[claims]

Respond with ONLY a JSON array:
[{"heading": "Government response", "claim_idxs": [1, 4, 7]}, ...]"""


if __name__ == "__main__":  # verify the Wikipedia rendering is still verbatim
    import sys
    for _n in ("ROUTE_PROMPT", "PLAN_STRUCTURE_PROMPT", "SECTION_REWRITE_PROMPT",
               "NEW_SECTION_PROMPT", "CLUSTER_SECTION_PROMPT"):
        _t = globals()[_n]
        for _slot, _val in WIKI_SLOTS.items():
            _t = _t.replace(_slot, _val)
        print(f"{_n}: {len(_t)} chars rendered for Wikipedia")
        if "[document]" in _t or "[doctype]" in _t or "[style]" in _t:
            sys.exit(f"{_n} still has an unfilled slot")
