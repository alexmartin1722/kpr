"""corpus.py — the document store the report pipeline reads, plus adapters.

The native format is a generic JSONL, one row per document:

    {"doc_id": "d1", "text": "...", "lang": "eng", "date": "2024-05-01", "url": "..."}

`doc_id` and `text` are required; `lang`, `date`, `url` are optional (`id` is
accepted as an alias for `doc_id`). Three adapters materialize that shape:

    DocStore.from_jsonl(...)    the generic format
    DocStore.from_ragtime(...)  {eng,arb,rus,zho}.jsonl native RAGTIME corpora
    DocStore.from_mw2(...)      documents/{article}/{article}_{lang}.json

No machine translation is ever read — the RAGTIME adapter deliberately ignores
the `.mt` files, because the whole point of claim decomposition here is to reach
non-English content without translating the documents first. `to_jsonl()`
freezes an adapter's output so a run is reproducible without re-scanning a
multi-gigabyte corpus.

Token counting drives context budgeting. It prefers a real tokenizer
(`pip install -e ".[tokenizer]"`, model from $KPR_TOKENIZER) because
multilingual text tokenizes to very different counts per character — budgeting
Chinese by character overflows the window. Without one it falls back to a
deliberately conservative character heuristic.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

RAGTIME_DOCS_DIR = Path(os.environ.get("KPR_RAGTIME_DOCS", "/exp/scale25/ragtime/docs"))
RAGTIME_LANGS = ("eng", "arb", "rus", "zho")

TOKENIZER_MODEL = os.environ.get("KPR_TOKENIZER", "Qwen/Qwen3.5-27B")
TOKENIZER_CACHE = os.environ.get("KPR_TOKENIZER_CACHE") or None

# conservative chars-per-token when no tokenizer is available; CJK and Arabic run
# near 1 char/token, so under-estimating would overflow the context window
_CHARS_PER_TOKEN_FALLBACK = 2.0

_TOK: object | None = None
_TOK_TRIED = False


def _tokenizer():
    """The tokenizer, or None to use the character fallback.

    Resolution is deliberately fast: a cached tokenizer loads instantly, and an
    uncached one is only fetched over the network when KPR_TOKENIZER_DOWNLOAD=1
    — otherwise a run on a compute node without HuggingFace access would stall
    on every fresh process. KPR_TOKENIZER=none skips it outright.
    """
    global _TOK, _TOK_TRIED
    if _TOK_TRIED:
        return _TOK
    _TOK_TRIED = True
    if TOKENIZER_MODEL.lower() in ("none", "off", ""):
        return None
    try:
        from transformers import AutoTokenizer
    except ImportError:
        return None
    allow_download = os.environ.get("KPR_TOKENIZER_DOWNLOAD", "") not in ("", "0", "false")
    for local_only in ((True, False) if allow_download else (True,)):
        try:
            _TOK = AutoTokenizer.from_pretrained(
                TOKENIZER_MODEL, cache_dir=TOKENIZER_CACHE, local_files_only=local_only)
            return _TOK
        except Exception:  # noqa: BLE001 - not cached, or no network
            continue
    return None


def count_tokens(text: str) -> int:
    if not text:
        return 0
    tok = _tokenizer()
    if tok is None:
        return int(len(text) / _CHARS_PER_TOKEN_FALLBACK) + 1
    return len(tok.encode(text))


def _normalize_row(row: dict) -> Optional[Tuple[str, dict]]:
    did = row.get("doc_id") or row.get("id")
    text = row.get("text")
    if not did or not text:
        return None
    return str(did), {"text": text, "lang": row.get("lang"),
                      "date": row.get("date"), "url": row.get("url")}


class DocStore:
    """{doc_id: {text, lang, date, url}} with context-budgeted concatenation."""

    def __init__(self, index: Optional[Dict[str, dict]] = None):
        self.idx: Dict[str, dict] = dict(index or {})

    # ── construction ────────────────────────────────────────────────────────
    @classmethod
    def from_jsonl(cls, paths, doc_ids: Optional[Iterable[str]] = None) -> "DocStore":
        """Load one or more generic docs.jsonl files, optionally filtered to doc_ids."""
        if isinstance(paths, (str, Path)):
            paths = [paths]
        want = set(map(str, doc_ids)) if doc_ids is not None else None
        idx: Dict[str, dict] = {}
        for p in paths:
            with Path(p).open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    norm = _normalize_row(row)
                    if norm is None:
                        continue
                    did, rec = norm
                    if want is not None and did not in want:
                        continue
                    idx[did] = rec
        return cls(idx)

    @classmethod
    def from_ragtime(cls, doc_ids: Iterable[str], docs_dir: Path = RAGTIME_DOCS_DIR,
                     langs: Sequence[str] = RAGTIME_LANGS) -> "DocStore":
        """Pull specific documents out of the native RAGTIME corpora.

        The corpora are multi-gigabyte, so each language file is streamed once
        with a cheap id prefilter ahead of json.loads, and the scan stops as
        soon as every wanted id has been found.
        """
        want = set(map(str, doc_ids))
        idx: Dict[str, dict] = {}
        for lang in langs:
            p = Path(docs_dir) / f"{lang}.jsonl"
            if not p.exists() or not want:
                continue
            with p.open(encoding="utf-8") as f:
                for line in f:
                    if not want:
                        break
                    j = line.find('"id":')
                    if j < 0:
                        continue
                    try:
                        did = line[j + 5:].split('"', 2)[1]
                    except IndexError:
                        continue
                    if did not in want:
                        continue
                    d = json.loads(line)
                    idx[did] = {"text": d.get("text", ""), "lang": lang,
                                "date": d.get("date"), "url": d.get("url")}
                    want.discard(did)
        return cls(idx)

    @classmethod
    def from_mw2(cls, documents_dir, article: str,
                 langs: Optional[Sequence[str]] = None) -> "DocStore":
        """Load a MegaWika2 article set: documents/{article}/{article}_{lang}.json.

        doc_id is "{article}_{lang}", so claim provenance keeps the language.
        """
        art_dir = Path(documents_dir) / article
        idx: Dict[str, dict] = {}
        for p in sorted(art_dir.glob(f"{article}_*.json")):
            lang = p.stem.rsplit("_", 1)[-1]
            if langs is not None and lang not in langs:
                continue
            try:
                doc = json.loads(p.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            text = doc.get("text") or ""
            if not text:
                continue
            idx[p.stem] = {"text": text, "lang": lang,
                           "date": doc.get("last_revision"), "url": doc.get("url")}
        return cls(idx)

    # ── access ──────────────────────────────────────────────────────────────
    def __len__(self) -> int:
        return len(self.idx)

    def __contains__(self, doc_id: str) -> bool:
        return doc_id in self.idx

    def doc_ids(self) -> List[str]:
        return list(self.idx)

    def text(self, doc_id: str) -> str:
        return self.idx.get(doc_id, {}).get("text", "") or ""

    def lang(self, doc_id: str) -> Optional[str]:
        return self.idx.get(doc_id, {}).get("lang")

    def date(self, doc_id: str) -> Optional[str]:
        return self.idx.get(doc_id, {}).get("date")

    def to_jsonl(self, path) -> int:
        """Freeze this store as a generic docs.jsonl. Returns rows written."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as w:
            for did, rec in self.idx.items():
                w.write(json.dumps({"doc_id": did, **rec}, ensure_ascii=False) + "\n")
        return len(self.idx)

    # ── context budgeting ───────────────────────────────────────────────────
    def concat(self, doc_ids: Sequence[str], max_chars_per_doc: Optional[int] = 8000,
               max_input_tokens: Optional[int] = None,
               numbering: Optional[Dict[str, int]] = None) -> Tuple[str, List[str], List[str]]:
        """Concatenate document texts into one prompt block.

        Returns (text, used_ids, dropped_ids). Documents that do not fit
        `max_input_tokens` are DROPPED and returned so callers can log them —
        the concatenation ceiling the text-conditioned baselines hit and the
        claim-based pipeline does not. `numbering` supplies the [Document N]
        index per document (a CiteReg); without it they are numbered in order.
        """
        blocks: List[str] = []
        used: List[str] = []
        dropped: List[str] = []
        total = 0
        for did in doc_ids:
            t = self.text(did)
            if not t:
                continue
            if max_chars_per_doc:
                t = t[:max_chars_per_doc]
            n = numbering[did] if numbering else len(used) + 1
            block = (f"[Document {n}] (id={did}, lang={self.lang(did)}, "
                     f"date={self.date(did)})\n{t}")
            if max_input_tokens is not None:
                tl = count_tokens(block) + 2  # +2 for the "\n\n" join
                if used and total + tl > max_input_tokens:
                    dropped.append(did)
                    continue
                total += tl
            blocks.append(block)
            used.append(did)
        return "\n\n".join(blocks), used, dropped
