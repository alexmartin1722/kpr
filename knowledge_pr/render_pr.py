"""
render_pr.py — render an article PR as a git-changelog-style unified diff.

Modified sections are shown as unified diffs (sentence-per-line, so each changed
fact is one -/+ line). New sections are shown as all-addition blocks. A header
summarizes the article, revision, and change counts.
"""

from __future__ import annotations

import difflib
import re
from typing import List

from .authoring import NewSection, SectionEdit


def _section_diff(edit: SectionEdit) -> List[str]:
    a = edit.original_lines
    b = edit.rewritten_lines
    label = "Introduction" if edit.section_id == "sec_lead" else edit.heading
    diff = list(difflib.unified_diff(
        a, b, fromfile=f"a/{label}", tofile=f"b/{label}", lineterm="", n=3))
    return diff


def render_pr(article_title: str, revision, method: str,
              edits: List[SectionEdit], new_sections: List[NewSection],
              total_claims: int, registry: dict = None) -> str:
    modified = [e for e in edits if e.status == "modified"]
    out: List[str] = []
    out.append(f"# Knowledge PR: {article_title.replace('_', ' ')}")
    out.append(f"# revision reviewed against: {revision}")
    out.append(f"# decomposition method: {method}")
    n_added_existing = sum(len(e.added_claims) for e in modified)
    n_added_new = sum(len(ns.claims) for ns in new_sections)
    out.append(f"# {total_claims} ABSENT claims → "
               f"{len(modified)} sections modified (+{n_added_existing} facts), "
               f"{len(new_sections)} new sections (+{n_added_new} facts)")
    out.append("")

    for e in modified:
        label = "Introduction" if e.section_id == "sec_lead" else e.heading
        sub_note = f", {len(e.subsections)} subsections" if e.subsections else ""
        out.append(f"@@ section: {label}  (+{len(e.added_claims)} facts{sub_note}) @@")
        diff = _section_diff(e)
        if diff:
            out.extend(diff)
        elif e.subsections:
            # base text unchanged; show it as context so the additions have an anchor
            out.append(f"--- a/{label}")
            out.append(f"+++ b/{label}")
            for ln in e.original_lines:
                out.append(f" {ln}" if ln else " ")
        for sub in e.subsections:
            out.append(f"+")
            out.append(f"+ === {sub.heading} ===")
            for ln in sub.drafted_lines:
                out.append(f"+ {ln}" if ln else "+")
        out.append("")

    for ns in new_sections:
        after = "(lead)" if ns.after_section_id in (None, "sec_lead") else ns.after_section_id
        out.append(f"@@ NEW section: {ns.heading}  (after {after}, +{len(ns.claims)} facts) @@")
        out.append(f"+ == {ns.heading} ==")
        for ln in ns.drafted_lines:
            out.append(f"+ {ln}" if ln else "+")
        out.append("")

    # Reference list — cite markers [N] in the text resolve here. Only list refs
    # the model actually used in the rendered output.
    if registry:
        used = set(int(n) for n in re.findall(r"\[(\d+)\]", "\n".join(out)))
        cited = [n for n in sorted(registry) if n in used]
        if cited:
            out.append("@@ References @@")
            for n in cited:
                r = registry[n]
                label = r.get("url") or r.get("name") or (r.get("content", "") or "")[:80]
                out.append(f"+ [{n}] {label}")
            unused = [n for n in sorted(registry) if n not in used]
            if unused:
                out.append(f"# ({len(unused)} attached refs went uncited by the model)")
            out.append("")

    return "\n".join(out)


def render_claim_proposal(article_title: str, method: str,
                          edits: List[SectionEdit], new_sections: List[NewSection]) -> str:
    """A structured 'claim proposal' doc: exactly which claims are proposed into
    which section (existing vs NEW), independent of the prose diff. Pairs with the
    diff — the proposal says WHAT is being added, the diff shows HOW the text changes.
    """
    def _cite(c):
        refs = c.get("cite_refs") or []
        return f"  [cite: {','.join(str(r) for r in refs)}]" if refs else ""

    modified = [e for e in edits if e.status == "modified"]
    n_existing = sum(len(e.added_claims) for e in modified)
    n_new = sum(len(ns.claims) for ns in new_sections)
    out: List[str] = []
    out.append(f"# Claim Proposal: {article_title.replace('_', ' ')}")
    out.append(f"# method: {method}")
    out.append(f"# {n_existing + n_new} claims proposed → "
               f"{len(modified)} existing sections (+{n_existing}), "
               f"{len(new_sections)} new sections (+{n_new})")
    out.append("")

    for e in modified:
        label = "Introduction" if e.section_id == "sec_lead" else e.heading
        if e.subsections:
            out.append(f"## → {label}  (+{len(e.added_claims)} claims, "
                       f"{len(e.subsections)} proposed subsections)")
            for s in e.subsections:
                out.append(f"### {s.heading}  (+{len(s.claims)})")
                for c in s.claims:
                    out.append(f"- {c['claim']}{_cite(c)}")
        else:
            out.append(f"## → {label}  (into existing section, +{len(e.added_claims)} claims)")
            for c in e.added_claims:
                out.append(f"- {c['claim']}{_cite(c)}")
        out.append("")

    for ns in new_sections:
        after = "(lead)" if ns.after_section_id in (None, "sec_lead") else ns.after_section_id
        out.append(f"## + NEW SECTION: {ns.heading}  (after {after}, +{len(ns.claims)} claims)")
        for c in ns.claims:
            out.append(f"- {c['claim']}{_cite(c)}")
        out.append("")

    return "\n".join(out)


def pr_to_dict(article_title: str, revision, method: str,
               edits: List[SectionEdit], new_sections: List[NewSection],
               routed_summary: dict) -> dict:
    return {
        "article": article_title,
        "revision": revision,
        "method": method,
        "routing": routed_summary,
        "section_edits": [
            {
                "section_id": e.section_id,
                "heading": e.heading,
                "status": e.status,
                "added_claim_ids": [c.get("claim_id") for c in e.added_claims],
                "original": e.original_lines,
                "rewritten": e.rewritten_lines,
                "subsections": [
                    {
                        "heading": s.heading,
                        "claim_ids": [c.get("claim_id") for c in s.claims],
                        "drafted": s.drafted_lines,
                    }
                    for s in e.subsections
                ],
            }
            for e in edits
        ],
        "new_sections": [
            {
                "heading": ns.heading,
                "after_section_id": ns.after_section_id,
                "claim_ids": [c.get("claim_id") for c in ns.claims],
                "drafted": ns.drafted_lines,
            }
            for ns in new_sections
        ],
    }
