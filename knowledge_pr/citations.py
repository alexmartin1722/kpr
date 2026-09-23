"""
citations.py — Re-attach source citations to claims (Approach A).

Citations live in the SOURCE-language MW2 doc under `excerpts_with_citations`
(each excerpt = a cited passage with `text`, `translated_text`, and a list of
`citations` carrying the <ref> wikitext, url, name). There is no para/sent
index on excerpts, so a claim inherits a citation by TEXT-MATCHING its
`source_sentence` to the excerpt that contains it (≈93% match rate observed).

`attach_citations` enriches each claim with `cite_refs` (article-wide reference
numbers) and returns the reference registry {ref_num -> {url, name, content}}.
Downstream, the draft/rewrite prompts tag claims with `[cite: N]` and the model
emits the `[N]` markers (Approach A — the model does the attribution; CiteP is
meant to later catch mis-cites).

`CiteReg` is the other half: where `attach_citations` numbers Wikipedia <ref>s,
CiteReg numbers whole source documents, which is what a report cites. Both feed
the same `[cite: N]` tag, so the authoring prompts never need to know which.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def _norm(s: str) -> str:
    return "".join((s or "").split())


def load_excerpts(docs_dir: Path, article: str, lang: str):
    """Return [(normalized_text, [citation dicts]), ...] for a source-lang doc."""
    p = Path(docs_dir) / article / f"{article}_{lang}.json"
    if not p.exists():
        return []
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    out = []
    for e in doc.get("excerpts_with_citations", []):
        out.append((_norm(e.get("text", "")), e.get("citations", []) or []))
    return out


def _match_citations(source_sentence: str, excerpts) -> List[dict]:
    """Citations of the excerpt containing the source sentence (or vice-versa)."""
    ss = _norm(source_sentence)
    if not ss:
        return []
    for et, cits in excerpts:
        if not et:
            continue
        if ss in et or et in ss or (len(ss) > 20 and ss[:24] in et):
            return cits
    return []


def _ref_key(c: dict) -> str:
    return c.get("name") or c.get("url") or (c.get("content", "") or "")[:80]


def attach_citations(claims: List[dict], docs_dir: Path, article: str
                     ) -> Tuple[List[dict], Dict[int, dict]]:
    """Enrich each claim with `cite_refs` (list[int]); return (claims, registry).

    registry maps ref_num -> {url, name, content}. Numbering is per-article and
    shared across source languages (deduped by name/url)."""
    excerpt_cache: Dict[str, list] = {}
    key_to_num: Dict[str, int] = {}
    registry: Dict[int, dict] = {}

    for claim in claims:
        lang = claim.get("lang")
        if lang not in excerpt_cache:
            excerpt_cache[lang] = load_excerpts(docs_dir, article, lang)
        cits = _match_citations(claim.get("source_sentence", ""), excerpt_cache[lang])
        refs = []
        for c in cits:
            k = _ref_key(c)
            if not k:
                continue
            if k not in key_to_num:
                num = len(key_to_num) + 1
                key_to_num[k] = num
                registry[num] = {"url": c.get("url"), "name": c.get("name"),
                                 "content": c.get("content"), "lang": lang}
            refs.append(key_to_num[k])
        claim["cite_refs"] = sorted(set(refs))
    return claims, registry


def coverage(claims: List[dict]) -> Tuple[int, int]:
    """(#claims with >=1 citation, total)."""
    tot = len(claims)
    cited = sum(1 for c in claims if c.get("cite_refs"))
    return cited, tot


# ── document-level citations (generated reports) ──────────────────────────
class CiteReg:
    """Assigns a stable 1-based [N] to each doc_id, in first-use order.

    One registry per report, carried across rounds, so [N] means the same
    document in round 3 as it did in round 1 and the mapping resolves to real
    corpus ids rather than prompt-local numbers.
    """

    def __init__(self, mapping: Optional[Dict[str, int]] = None):
        self._m: Dict[str, int] = dict(mapping or {})

    def num(self, doc_id: str) -> int:
        if doc_id not in self._m:
            self._m[doc_id] = len(self._m) + 1
        return self._m[doc_id]

    def numbering(self) -> Dict[str, int]:
        """{doc_id: N}, for DocStore.concat."""
        return dict(self._m)

    def mapping(self) -> Dict[str, str]:
        """{"1": doc_id, ...} — JSON-safe, for the output record."""
        return {str(n): d for d, n in self._m.items()}

    def copy(self) -> "CiteReg":
        return CiteReg(self._m)


def tag_claims(claims, reg: CiteReg) -> str:
    """'1. <claim>  [cite: N]' — the same convention the authoring prompts use.

    N is the registry number of the claim's source document; the prompt tells
    the model to turn the tag into a "[N]" marker on the sentence that uses it.
    """
    return "\n".join(f"{i + 1}. {c['claim']}  [cite: {reg.num(c['doc_id'])}]"
                     for i, c in enumerate(claims))
