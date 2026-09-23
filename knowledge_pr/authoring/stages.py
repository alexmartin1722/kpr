"""The authoring stages, implemented once for every target document.

    route_claims          each claim -> an existing section, or NEW
    plan_new_sections     group the NEW bucket into proposed sections
    rewrite_section       integrate claims into an existing section
    draft_section         write a new section from its claims
    cluster_section_claims  split an overloaded section into subsections

Every stage takes a `document` label (what the prompts call `[document]`) and a
`refs_of` callable mapping a claim to its citation numbers. Those two are the
only things a caller has to supply to retarget the whole engine — a Wikipedia
article and a report differ in nothing else at this level.

Parsing is defensive throughout: unparseable output routes claims to NEW or
leaves a section unchanged rather than raising, because one bad LLM response
should cost one section, not the run.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence

from ..article_model import Article, Section
from .prompts import (
    CLUSTER_SECTION_PROMPT, NEW_SECTION_PROMPT, PLAN_STRUCTURE_PROMPT,
    ROUTE_PROMPT, SECTION_REWRITE_PROMPT, WIKI_SLOTS,
)

# claims per section-rewrite call before the section is split into subsections
CLUSTER_THRESHOLD = 25
# claims per draft call — a single call cannot faithfully render dozens of facts
DRAFT_CHUNK = 20


# ── the document being authored ────────────────────────────────────────────
@dataclass(frozen=True)
class Target:
    """What the prompts' [document] / [doctype] / [style] slots are filled with.

    `Target.wikipedia(title)` reproduces the original Wikipedia prompts exactly;
    `Target.report(title)` is the same prompts addressed to a report.
    """
    document: str
    doctype: str = "article"
    style: str = "encyclopedic"

    @classmethod
    def wikipedia(cls, title: str) -> "Target":
        return cls(document=WIKI_SLOTS["[document]"].replace(
            "[title]", title.replace("_", " ")))

    @classmethod
    def report(cls, title: str = "") -> "Target":
        return cls(document=f'the report "{title}"' if title else "the report",
                   doctype="report", style="analytical")

    def fill(self, prompt: str) -> str:
        return (prompt.replace("[document]", self.document)
                      .replace("[doctype]", self.doctype)
                      .replace("[style]", self.style))


# ── data ───────────────────────────────────────────────────────────────────
@dataclass
class Subsection:
    heading: str
    claims: List[dict] = field(default_factory=list)
    drafted_lines: List[str] = field(default_factory=list)


@dataclass
class SectionEdit:
    section_id: str
    heading: str
    original_lines: List[str]
    rewritten_lines: List[str]
    added_claims: List[dict] = field(default_factory=list)
    status: str = "modified"          # modified | unchanged | error
    subsections: List[Subsection] = field(default_factory=list)


@dataclass
class NewSection:
    heading: str
    after_section_id: Optional[str]
    claims: List[dict] = field(default_factory=list)
    drafted_lines: List[str] = field(default_factory=list)


# ── parsing helpers ────────────────────────────────────────────────────────
def extract_json_array(raw: str):
    raw = re.sub(r"<think>[\s\S]*?</think>", "", raw or "").strip()
    m = re.search(r"```(?:json)?\s*(\[[\s\S]*?\])\s*```", raw) or re.search(r"(\[[\s\S]*\])", raw)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def clean_lines(raw: str) -> List[str]:
    raw = re.sub(r"<think>[\s\S]*?</think>", "", raw or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```[a-z]*\s*|\s*```$", "", raw).strip()
    lines = [ln.rstrip() for ln in raw.split("\n")] if raw else []
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return lines


# sentence boundary = terminal .!? (plus any trailing citation markers) before a
# capital, quote or digit. Keeps markers on the sentence they cite, so a merged
# multi-fact sentence stays one line.
_SENT_CITE_BOUNDARY = re.compile(r'([.!?](?:\[\d+\])*)\s+(?=[A-Z0-9"\'(])')


def to_sentence_lines(lines: Sequence[str]) -> List[str]:
    """Force one sentence per line, preserving blank-line paragraph breaks."""
    out: List[str] = []
    for ln in lines:
        if not ln:
            out.append("")
            continue
        parts = [s.strip() for s in _SENT_CITE_BOUNDARY.sub(r"\1\n", ln.strip()).split("\n")
                 if s.strip()]
        out.extend(parts if parts else [ln])
    return out


def no_refs(_claim: dict) -> List[int]:
    """Default `refs_of`: the document carries no citations."""
    return []


def numbered_block(claims: Sequence[dict]) -> str:
    """'1. <claim>' — for the stages whose answer indexes back into the list."""
    return "\n".join(f"{i + 1}. {c['claim']}" for i, c in enumerate(claims))


def cited_block(claims: Sequence[dict], refs_of: Callable[[dict], Sequence[int]]) -> str:
    """'1. <claim>  [cite: 1,3]' — the Wikipedia convention the prompts expect.

    The prompts tell the model to turn a `[cite: 1,3]` tag into `[1][3]` on the
    sentence that uses the fact.
    """
    lines = []
    for i, c in enumerate(claims):
        refs = refs_of(c) or []
        tag = f"  [cite: {','.join(str(r) for r in refs)}]" if refs else ""
        lines.append(f"{i + 1}. {c['claim']}{tag}")
    return "\n".join(lines)


def outline(article: Article) -> str:
    """1-based numbered outline.

    Deliberately 1-based: the routing prompt reserves 0 for "no section fits",
    so numbering from 0 would make the first section unaddressable.
    """
    lines = []
    for i, s in enumerate(article.sections, 1):
        name = "Introduction" if s.is_lead else s.heading
        lines.append(f"[{i}] {name} — {s.gist()}")
    return "\n".join(lines)


# ── Stage A ────────────────────────────────────────────────────────────────
def route_claims(article: Article, claims: Sequence[dict], model, target: Target,
                 batch_size: int = 40) -> Dict[str, List[dict]]:
    """{section_id | "NEW": [claims]}. Unroutable claims go to NEW."""
    ol = outline(article)
    batches = [claims[i:i + batch_size] for i in range(0, len(claims), batch_size)]
    prompts = [target.fill(ROUTE_PROMPT)
               .replace("[outline]", ol).replace("[claims]", numbered_block(b))
               for b in batches]
    outputs = model.batch_infer(prompts) if prompts else []

    routed: Dict[str, List[dict]] = {}
    sections = article.sections
    for b, raw in zip(batches, outputs):
        pick = {}
        for item in extract_json_array(raw) or []:
            if isinstance(item, dict) and isinstance(item.get("idx"), int):
                pick[item["idx"]] = item.get("section")
        for i, claim in enumerate(b, start=1):
            sec = pick.get(i, 0)
            sid = (sections[sec - 1].id
                   if isinstance(sec, int) and 1 <= sec <= len(sections) else "NEW")
            routed.setdefault(sid, []).append(claim)
    return routed


# ── Stage B ────────────────────────────────────────────────────────────────
def plan_new_sections(article: Article, orphan_claims: Sequence[dict], model,
                      target: Target, plan_cap: int = 150) -> List[NewSection]:
    """Group the NEW bucket into proposed sections."""
    if not orphan_claims:
        return []
    id_by_index = {i: s.id for i, s in enumerate(article.sections)}
    # bound the planner prompt; anything past plan_cap falls to the catch-all
    shown = orphan_claims[:plan_cap]
    prompt = (target.fill(PLAN_STRUCTURE_PROMPT)
              .replace("[outline]", outline(article))
              .replace("[claims]", numbered_block(shown)))
    arr = extract_json_array(model.batch_infer([prompt])[0]) or []

    planned: List[NewSection] = []
    assigned = set()
    for item in arr:
        if not isinstance(item, dict):
            continue
        heading = str(item.get("heading", "")).strip()
        if not heading:
            continue
        after = item.get("after_section")
        after_id = id_by_index.get(after) if isinstance(after, int) else None
        sec_claims = []
        for j in item.get("claim_idxs", []):
            if isinstance(j, int) and 1 <= j <= len(orphan_claims) and j not in assigned:
                sec_claims.append(orphan_claims[j - 1])
                assigned.add(j)
        if sec_claims:
            planned.append(NewSection(heading, after_id, sec_claims))

    leftover = [orphan_claims[j - 1] for j in range(1, len(orphan_claims) + 1)
                if j not in assigned]
    if leftover:
        planned.append(NewSection(
            "Additional information",
            article.sections[-1].id if article.sections else None, leftover))
    return planned


# ── Stage D (used by C as well) ────────────────────────────────────────────
def draft_prose(heading: str, claims: Sequence[dict], model, target: Target,
                refs_of: Callable[[dict], Sequence[int]] = no_refs,
                chunk: int = DRAFT_CHUNK, content_block: Optional[str] = None) -> List[str]:
    """Draft prose for a (sub)section from its claims, in bounded chunks.

    A single call cannot faithfully render dozens of facts — it collapses to a
    lossy blob — so the claims are chunked and the chunks concatenated.

    `content_block` replaces the rendered claim list with text the caller built
    itself. That is how a text-conditioned baseline feeds whole source
    documents through this same prompt instead of claims; it is one block, so
    no chunking applies.
    """
    if content_block is not None:
        raw = model.batch_infer([target.fill(NEW_SECTION_PROMPT)
                                 .replace("[heading]", heading)
                                 .replace("[claims]", content_block)])[0]
        return to_sentence_lines(clean_lines(raw))
    batches = [claims[i:i + chunk] for i in range(0, len(claims), chunk)]
    prompts = [target.fill(NEW_SECTION_PROMPT)
               .replace("[heading]", heading)
               .replace("[claims]", cited_block(b, refs_of))
               for b in batches]
    outputs = model.batch_infer(prompts) if prompts else []
    lines: List[str] = []
    for out in outputs:
        chunk_lines = to_sentence_lines(clean_lines(out))
        if lines and chunk_lines:
            lines.append("")                      # paragraph break between chunks
        lines.extend(chunk_lines)
    return lines


def draft_new_section(new_section: NewSection, model, target: Target,
                      refs_of: Callable[[dict], Sequence[int]] = no_refs) -> NewSection:
    new_section.drafted_lines = draft_prose(new_section.heading, new_section.claims,
                                            model, target, refs_of)
    return new_section


# ── within-section clustering ──────────────────────────────────────────────
def cluster_section_claims(section: Section, claims: Sequence[dict], model,
                           target: Target, batch: int = 120) -> List[Subsection]:
    """Group one section's claims into subsections, in bounded batches.

    Batched because a section can receive hundreds of claims and a single
    clustering prompt would blow the context window; subsections with the same
    heading are merged across batches.
    """
    heading = "Introduction" if section.is_lead else section.heading
    current = "\n".join(section.sentence_lines()[:8])
    batches = [claims[i:i + batch] for i in range(0, len(claims), batch)]
    prompts = [target.fill(CLUSTER_SECTION_PROMPT)
               .replace("[heading]", heading).replace("[current]", current)
               .replace("[claims]", numbered_block(b))
               for b in batches]
    outputs = model.batch_infer(prompts) if prompts else []

    merged: Dict[str, List[dict]] = {}
    order: List[str] = []

    def bucket(h, items):
        if h not in merged:
            merged[h] = []
            order.append(h)
        merged[h].extend(items)

    for b, raw in zip(batches, outputs):
        assigned = set()
        for item in extract_json_array(raw) or []:
            if not isinstance(item, dict):
                continue
            h = str(item.get("heading", "")).strip()
            idxs = [j for j in item.get("claim_idxs", []) if isinstance(j, int)]
            sc = [b[j - 1] for j in idxs if 1 <= j <= len(b) and j not in assigned]
            assigned.update(idxs)
            if h and sc:
                bucket(h, sc)
        leftover = [b[j - 1] for j in range(1, len(b) + 1) if j not in assigned]
        if leftover:
            bucket(order[-1] if order else "Details", leftover)
    return [Subsection(heading=h, claims=merged[h]) for h in order]


# ── Stage C ────────────────────────────────────────────────────────────────
def rewrite_section(section: Section, claims: Sequence[dict], model, target: Target,
                    refs_of: Callable[[dict], Sequence[int]] = no_refs,
                    cluster_threshold: int = CLUSTER_THRESHOLD,
                    content_block: Optional[str] = None) -> SectionEdit:
    """Integrate claims into one existing section.

    Past `cluster_threshold` claims the section keeps its original text as the
    base — the minimal edit — and the new facts are organized into drafted
    subsections instead of forced through one rewrite call.

    `content_block` replaces the rendered claim list with text the caller built
    (whole source documents, for a text-conditioned baseline). Clustering is
    skipped in that case: there is one block to integrate, not N claims to
    group.
    """
    original = section.sentence_lines()

    if content_block is None and cluster_threshold and len(claims) > cluster_threshold:
        subs = cluster_section_claims(section, claims, model, target)
        for sub in subs:
            sub.drafted_lines = draft_prose(sub.heading, sub.claims, model, target, refs_of)
        return SectionEdit(section.id, section.heading, original, original,
                           list(claims), "modified", subs)

    heading = "Introduction" if section.is_lead else section.heading
    prompt = (target.fill(SECTION_REWRITE_PROMPT)
              .replace("[heading]", heading)
              .replace("[current]", "\n".join(original))
              .replace("[claims]", content_block if content_block is not None
                       else cited_block(claims, refs_of)))
    rewritten = to_sentence_lines(clean_lines(model.batch_infer([prompt])[0]))
    if not rewritten:
        status = "error"
    elif rewritten == original:
        status = "unchanged"
    else:
        status = "modified"
    return SectionEdit(section.id, section.heading, original, rewritten or original,
                       list(claims), status)
