"""Claim-driven authoring — the single rewriting implementation in KPR.

Every pipeline routes claims into a sectioned document and rewrites the
sections they land in. That pass lives here, once, and is retargeted by two
arguments: `document` (what the prompts call the thing being edited) and
`refs_of` (a claim's citation numbers).

    from knowledge_pr.authoring import author, apply_edits

The prompts ARE the Wikipedia prompts, with three words turned into slots so a
report can use them; the Wikipedia rendering is byte-identical to the original.

`build_pr.py` is the Wikipedia profile over it (MegaWika2 documents, `<ref>`
citations, a unified-diff ChangeLog) and `report.py` the report profile
(Markdown, source-document citations, iterative rounds). Neither implements
rewriting itself.
"""

from .engine import apply_edits, author
from .prompts import (
    CLUSTER_SECTION_PROMPT, NEW_SECTION_PROMPT, PLAN_STRUCTURE_PROMPT,
    ROUTE_PROMPT, SECTION_REWRITE_PROMPT, WIKI_SLOTS,
)
from .stages import (
    CLUSTER_THRESHOLD, DRAFT_CHUNK, NewSection, SectionEdit, Subsection, Target,
    cited_block, clean_lines, cluster_section_claims, draft_new_section,
    draft_prose, extract_json_array, no_refs, numbered_block, outline,
    plan_new_sections, rewrite_section, route_claims, to_sentence_lines,
)

__all__ = [
    "apply_edits", "author",
    "CLUSTER_SECTION_PROMPT", "NEW_SECTION_PROMPT", "PLAN_STRUCTURE_PROMPT",
    "ROUTE_PROMPT", "SECTION_REWRITE_PROMPT", "WIKI_SLOTS",
    "CLUSTER_THRESHOLD", "DRAFT_CHUNK", "NewSection", "SectionEdit", "Subsection", "Target",
    "cited_block", "clean_lines", "cluster_section_claims", "draft_new_section",
    "draft_prose", "extract_json_array", "no_refs", "numbered_block", "outline",
    "plan_new_sections", "rewrite_section", "route_claims", "to_sentence_lines",
]
