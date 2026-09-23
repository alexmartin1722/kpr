"""
article_model.py — Parse a MegaWika2 English document into a section model,
and reconstruct section text for diffing. Also parses and renders the Markdown
form a generated report uses, so both kinds of document become the same
Article/Section model and the authoring engine does not care which it got.

MW2 `elements` is an ordered list of {type: heading|paragraph|infobox}:
  heading   -> {text, level, ...}          starts a new section
  paragraph -> {sentences: [{text, ...}]}  belongs to the current section
  infobox   -> {content: <wikitext>}       kept aside (not prose-edited)

The lead (paragraphs before the first heading) is section "lead".

Sections get stable ids by order (sec_0 = lead, sec_1, ...). Section text is
rendered ONE SENTENCE PER LINE — this is the unit the rewriter emits and the
unit the diff is computed over, so a changed fact shows as a single -/+ line.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Section:
    id: str
    heading: str            # "lead" for the intro
    level: int              # 1 for lead, else heading level (2, 3, ...)
    paragraphs: List[List[str]] = field(default_factory=list)  # [para][sentence]

    @property
    def is_lead(self) -> bool:
        return self.id == "sec_lead"

    def sentences(self) -> List[str]:
        return [s for para in self.paragraphs for s in para]

    def text(self) -> str:
        """Human-readable section text: blank line between paragraphs."""
        return "\n\n".join(" ".join(para) for para in self.paragraphs)

    def sentence_lines(self) -> List[str]:
        """One sentence per line, with a blank line marking paragraph breaks.
        This is the canonical form fed to the rewriter and to difflib."""
        lines: List[str] = []
        for i, para in enumerate(self.paragraphs):
            if i > 0:
                lines.append("")      # paragraph boundary
            lines.extend(para)
        return lines

    def gist(self, max_chars: int = 160) -> str:
        """Short summary of the section for routing prompts (first sentence)."""
        sents = self.sentences()
        return (sents[0][:max_chars] if sents else "").strip()


@dataclass
class Article:
    title: str
    revision: Optional[str]
    sections: List[Section]
    infobox: Optional[str] = None

    def section(self, sid: str) -> Optional[Section]:
        return next((s for s in self.sections if s.id == sid), None)

    def outline(self) -> str:
        """Numbered outline for routing/structure prompts."""
        lines = []
        for i, s in enumerate(self.sections):
            name = "Introduction (lead)" if s.is_lead else s.heading
            indent = "  " * max(0, s.level - 2) if not s.is_lead else ""
            lines.append(f"[{i}] {indent}{name} — {s.gist()}")
        return "\n".join(lines)


_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")


def _split_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    return [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]


def parse_article(doc: dict) -> Article:
    """Build an Article from a loaded MW2 *_en.json document."""
    title = doc.get("title", "")
    revision = doc.get("last_revision")
    infobox = None

    lead = Section(id="sec_lead", heading="lead", level=1)
    sections: List[Section] = [lead]
    current = lead
    idx = 1

    for el in doc.get("elements", []):
        t = el.get("type")
        if t == "infobox":
            infobox = el.get("content")
        elif t == "heading":
            heading = (el.get("text") or "").strip()
            level = el.get("level", 2)
            current = Section(id=f"sec_{idx}", heading=heading, level=level)
            sections.append(current)
            idx += 1
        elif t == "paragraph":
            sents = [s.get("text", "").strip()
                     for s in el.get("sentences", []) if s.get("text", "").strip()]
            if sents:
                current.paragraphs.append(sents)

    # Drop the lead if it has no prose (some articles start with a heading)
    if not lead.paragraphs:
        sections = [s for s in sections if s.id != "sec_lead"]

    return Article(title=title, revision=revision, sections=sections, infobox=infobox)


def load_article(documents_dir, article: str) -> Optional[Article]:
    """Load and parse {documents_dir}/{article}/{article}_en.json."""
    import json
    from pathlib import Path
    p = Path(documents_dir) / article / f"{article}_en.json"
    if not p.exists():
        return None
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not doc.get("elements"):
        return None
    return parse_article(doc)


# ── Markdown form (generated reports) ─────────────────────────────────────
_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")
# Latin + CJK sentence-final punctuation followed by a capital, digit or opener
_SENT_SPLIT = re.compile(r"(?<=[.!?。！？])\s+(?=[A-Z0-9\"'(À-ɏ])")
_THINK = re.compile(r"<think>[\s\S]*?</think>")
CITATION_MARKER = re.compile(r"\s*\[\d+\](?:\[\d+\])*")


def split_sentences(text: str) -> List[str]:
    text = (text or "").strip()
    if not text:
        return []
    return [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]


def strip_think(raw: str) -> str:
    """Drop the reasoning block a thinking model may emit before its answer."""
    return _THINK.sub("", raw or "").strip()


def strip_citations(text: str) -> str:
    """Remove inline [N] markers — InfoF1 scores the prose, not the citations."""
    return CITATION_MARKER.sub("", text or "").strip()


def set_section_text(sec: Section, block: str) -> None:
    """Replace a section body from a one-sentence-per-line block."""
    paras: List[List[str]] = []
    buf: List[str] = []
    for ln in (block or "").splitlines():
        ln = ln.strip()
        if _HEADING.match(ln):            # a stray heading echo is not body text
            continue
        if ln:
            buf.append(ln)
        elif buf:
            paras.append(buf)
            buf = []
    if buf:
        paras.append(buf)
    if paras:
        sec.paragraphs = paras


def parse_report(md: str, title: str = "") -> Article:
    """Markdown report -> Article. Text before the first heading is the lead."""
    md = strip_think(md)
    lead = Section(id="sec_lead", heading="lead", level=1)
    sections = [lead]
    current = lead
    idx = 1
    buf: List[str] = []

    def flush():
        if buf:
            current.paragraphs.append([s for s in buf if s.strip()])
            buf.clear()

    for raw in md.splitlines():
        line = raw.rstrip()
        m = _HEADING.match(line)
        if m:
            flush()
            heading = m.group(1).strip() or f"Section {idx}"
            current = Section(id=f"sec_{idx}", heading=heading, level=2)
            sections.append(current)
            idx += 1
        elif not line.strip():
            flush()
        else:
            # already one sentence per line; split anything that packs several
            for s in split_sentences(line) or [line.strip()]:
                buf.append(s)
    flush()

    if not lead.paragraphs:
        sections = [s for s in sections if s.id != "sec_lead"]
    if not sections:                      # empty output: give routing a target
        sections = [Section(id="sec_1", heading="Overview", level=2)]
    return Article(title=title, revision=None, sections=sections, infobox=None)


def render_report(article: Article) -> str:
    """Article -> Markdown ("## Heading", one sentence per line)."""
    out: List[str] = []
    for s in article.sections:
        if not s.is_lead:
            out.append(f"## {s.heading}")
        for i, para in enumerate(s.paragraphs):
            if i > 0:
                out.append("")
            out.extend(para)
        out.append("")
    return "\n".join(out).strip() + "\n"


def report_sentences(md: str, drop_citations: bool = True) -> List[str]:
    """Flat sentence list — the unit a MiRAGE prediction is keyed on."""
    sents = [s for sec in parse_report(md).sections for s in sec.sentences()]
    if drop_citations:
        sents = [strip_citations(s) for s in sents]
    return [s for s in sents if s]
