"""
reconstruct.py — assemble the full rewritten-article text from a PR JSON.

Shared by the Info eval and the rewrite-conditioned QA eval so both build the
rewrite the same way: modified sections use their rewritten base + drafted
subsections, unmodified sections keep the original text, new sections are
inserted after their anchor.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .article_model import load_article

_MARKER = re.compile(r"\s*\[\d+\](?:\[\d+\])*")


def reconstruct_rewrite(pr: dict, article, strip_citations: bool = False) -> str:
    edit_by_id = {e["section_id"]: e for e in pr.get("section_edits", [])}
    new_after = {}
    for ns in pr.get("new_sections", []):
        new_after.setdefault(ns.get("after_section_id"), []).append(ns)

    parts = []
    for sec in article.sections:
        e = edit_by_id.get(sec.id)
        if e and e.get("status") == "modified":
            parts.append("\n".join(e.get("rewritten", []) or sec.sentence_lines()))
            for sub in e.get("subsections", []):
                parts.append(f"== {sub['heading']} ==")
                parts.append("\n".join(sub.get("drafted", [])))
        else:
            parts.append(sec.text())
        for ns in new_after.get(sec.id, []):
            parts.append(f"== {ns['heading']} ==")
            parts.append("\n".join(ns.get("drafted", [])))
    for ns in new_after.get(None, []):
        parts.append(f"== {ns['heading']} ==")
        parts.append("\n".join(ns.get("drafted", [])))

    text = "\n\n".join(p for p in parts if p.strip())
    if strip_citations:
        text = _MARKER.sub("", text)
    return text


def load_rewrite_texts(prs_dir, documents_dir, strip_citations: bool = True) -> dict:
    """{article: reconstructed rewrite text} for every prs/*.json on disk."""
    out = {}
    for pj in sorted(Path(prs_dir).glob("*.json")):
        # the filename stem is the underscored dir/article name; pr["article"]
        # is the DISPLAY title (spaces), which won't resolve as a directory.
        art = pj.stem
        try:
            pr = json.loads(pj.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        article = load_article(documents_dir, art)
        if article is None:
            continue
        out[art] = reconstruct_rewrite(pr, article, strip_citations=strip_citations)
    return out
