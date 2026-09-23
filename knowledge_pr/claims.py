"""claims.py — the claim pool a report is written from.

`cg`-style decomposition writes one row per decomposed unit
({doc_id, lang, unit_index, unit_text, claims}); `pool_claims` flattens those
rows for a set of documents into [{claim, doc_id, lang}], deduplicated on
normalized text so the same sentence appearing in two documents does not enter
the pool twice.

Pooling is done at read time rather than baked into the cache, so one
decomposition run can serve any document subset and any round split.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

from .dedup import normalize


def load_claim_rows(path, doc_ids: Optional[Iterable[str]] = None) -> List[dict]:
    """Read a claims.jsonl, optionally filtered to doc_ids."""
    want = set(map(str, doc_ids)) if doc_ids is not None else None
    rows = []
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if want is not None and str(r.get("doc_id")) not in want:
                continue
            rows.append(r)
    return rows


def pool_claims(claim_rows: Sequence[dict],
                doc_ids: Optional[Sequence[str]] = None) -> List[dict]:
    """Flatten decomposed unit rows into a deduplicated [{claim, doc_id, lang}]."""
    want = set(map(str, doc_ids)) if doc_ids is not None else None
    out: List[dict] = []
    seen = set()
    for r in claim_rows:
        did = str(r.get("doc_id", ""))
        if want is not None and did not in want:
            continue
        for c in r.get("claims") or []:
            c = str(c).strip()
            k = normalize(c)
            if not k or k in seen:
                continue
            seen.add(k)
            out.append({"claim": c, "doc_id": did, "lang": r.get("lang")})
    return out
