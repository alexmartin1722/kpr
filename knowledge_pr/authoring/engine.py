"""engine.py — the one authoring pass, shared by every pipeline.

    author(article, claims, model, document, refs_of)
        -> (section_edits, new_sections, routing_summary)

That is the whole of "rewriting" in KPR: route the claims, integrate them into
the sections they landed in, plan and draft sections for the ones that fit
nowhere. What differs between a Wikipedia article and a report is upstream (how
the document was parsed, which claims survived filtering) and downstream (a
unified diff or a Markdown report) — not here.

`apply_edits` folds the result back into an Article, for callers that want the
updated document rather than a diff.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Sequence, Tuple

from ..article_model import Article, Section
from .stages import (
    CLUSTER_THRESHOLD, NewSection, SectionEdit, Target, draft_prose, no_refs,
    plan_new_sections, rewrite_section, route_claims,
)


def author(article: Article, claims: Sequence[dict], model, target: Target,
           refs_of: Callable[[dict], Sequence[int]] = no_refs,
           cluster_threshold: int = CLUSTER_THRESHOLD,
           plan_new: bool = True,
           content_for: Optional[Callable[[Sequence[dict]], str]] = None,
           ) -> Tuple[List[SectionEdit], List[NewSection], Dict[str, int]]:
    """Route `claims` into `article` and produce the resulting edits.

    Returns (section_edits, new_sections, routing_summary). Sections that
    received no claims are absent from the edits — an untouched section is not
    an edit.

    `content_for` maps a section's routed claims to the text the rewrite should
    be conditioned on. Supply it to condition on something other than the
    claims themselves — a text-conditioned baseline passes back the full source
    documents those claims came from, and the claims then serve only to route.
    """
    if not claims:
        return [], [], {}

    routed = route_claims(article, claims, model, target)
    routing_summary = {sid: len(cs) for sid, cs in routed.items()}

    edits: List[SectionEdit] = []
    for sid, sec_claims in routed.items():
        if sid == "NEW":
            continue
        section = article.section(sid)
        if section is None:
            continue
        edits.append(rewrite_section(
            section, sec_claims, model, target, refs_of, cluster_threshold,
            content_block=content_for(sec_claims) if content_for else None))

    new_sections: List[NewSection] = []
    if plan_new:
        new_sections = plan_new_sections(article, routed.get("NEW", []), model, target)
        for ns in new_sections:
            ns.drafted_lines = draft_prose(
                ns.heading, ns.claims, model, target, refs_of,
                content_block=content_for(ns.claims) if content_for else None)

    return edits, new_sections, routing_summary


def apply_edits(article: Article, edits: Sequence[SectionEdit],
                new_sections: Sequence[NewSection]) -> Article:
    """Fold the edits back into an Article — the updated document.

    A clustered section keeps its original body and gains its subsections as
    level-3 sections placed directly after it; a new section is inserted after
    the section it was planned to follow.
    """
    by_id = {e.section_id: e for e in edits}
    after: Dict[object, List[NewSection]] = {}
    for ns in new_sections:
        after.setdefault(ns.after_section_id, []).append(ns)

    def as_section(sid: str, heading: str, level: int, lines: Sequence[str]) -> Section:
        paras: List[List[str]] = []
        buf: List[str] = []
        for ln in lines:
            if ln.strip():
                buf.append(ln.strip())
            elif buf:
                paras.append(buf)
                buf = []
        if buf:
            paras.append(buf)
        return Section(id=sid, heading=heading, level=level, paragraphs=paras)

    out: List[Section] = []
    n_new = 0
    for sec in article.sections:
        e = by_id.get(sec.id)
        if e is not None and e.status == "modified":
            out.append(as_section(sec.id, sec.heading, sec.level, e.rewritten_lines))
            for i, sub in enumerate(e.subsections, 1):
                n_new += 1
                out.append(as_section(f"{sec.id}_sub{i}", sub.heading, 3, sub.drafted_lines))
        else:
            out.append(sec)
        for ns in after.get(sec.id, []):
            n_new += 1
            out.append(as_section(f"sec_new{n_new}", ns.heading, 2, ns.drafted_lines))

    for ns in after.get(None, []):                 # planner gave no anchor
        n_new += 1
        out.append(as_section(f"sec_new{n_new}", ns.heading, 2, ns.drafted_lines))

    return Article(title=article.title, revision=article.revision, sections=out,
                   infobox=article.infobox)
