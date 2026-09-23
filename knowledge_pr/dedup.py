"""dedup.py — cross-document claim dedup, and recovering provenance after it.

Decomposing many documents about one topic restates the same fact many ways.
`dedup_claims` collapses that with the same LLM (no embedding model): an exact
normalized pass first, then sorted batches so near-duplicates land together
without embeddings, then an optional second pass for cross-batch duplicates.

Merging rewords, so a surviving claim's source document has to be RECOVERED
rather than carried — `attach_doc_ids` does that. Guessing it inside the merge
loop (e.g. attributing a reworded claim to its batch's first entry) silently
collapses every citation onto whichever document happened to sort first.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Sequence, Tuple

from .prompts import DEDUP_PROMPT
from .authoring.stages import extract_json_array


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


def _toks(s: str) -> set:
    return set(normalize(s).split())


def _parse_claim_strings(raw: str) -> Optional[List[str]]:
    arr = extract_json_array(raw)
    if arr is None:
        return None
    out = []
    for x in arr:
        if isinstance(x, str) and x.strip():
            out.append(x.strip())
        elif isinstance(x, dict) and x.get("claim"):
            out.append(str(x["claim"]).strip())
    return out or None


def attach_doc_ids(claims: Sequence[dict], pool: Sequence[dict]) -> List[dict]:
    """Re-attach each claim's source document by matching it against `pool`.

    An exact normalized match is the fast path; otherwise the pool claim with
    the most shared tokens wins, which is the document that (near-)stated it
    and therefore entails it.

    Scoring goes through an inverted index so only pool claims sharing at least
    one token are compared — the pool runs to tens of thousands of claims and
    an all-pairs scan would be quadratic.
    """
    exact: Dict[str, dict] = {}
    token_index: Dict[str, List[int]] = {}
    pool_toks: List[set] = []
    for i, c in enumerate(pool):
        exact.setdefault(normalize(c["claim"]), c)
        t = _toks(c["claim"])
        pool_toks.append(t)
        for tok in t:
            token_index.setdefault(tok, []).append(i)

    out: List[dict] = []
    for c in claims:
        hit = exact.get(normalize(c["claim"]))
        if hit is None:
            counts: Dict[int, int] = {}
            for tok in _toks(c["claim"]):
                for i in token_index.get(tok, ()):
                    counts[i] = counts.get(i, 0) + 1
            if counts:
                # most shared tokens; tie-break on the tighter match, so a
                # specific pool claim beats a long rambling one
                best = max(counts.items(), key=lambda kv: (kv[1], -len(pool_toks[kv[0]])))
                hit = pool[best[0]]
        if hit is None:
            out.append(dict(c))
            continue
        out.append({**c, "doc_id": hit.get("doc_id") or c.get("doc_id"),
                    "lang": hit.get("lang") or c.get("lang")})
    return out


def dedup_claims(claims: Sequence[dict], model, passes: int = 2,
                 batch: int = 60) -> Tuple[List[dict], dict]:
    """Collapse restatements. Returns (claims, stats), provenance re-attached."""
    by_text: Dict[str, dict] = {}
    for c in claims:                                   # exact dedup, order kept
        k = normalize(c["claim"])
        if k and k not in by_text:
            by_text[k] = c
    cur = list(by_text.values())
    stats = {"input": len(claims), "after_exact": len(cur)}

    for p in range(passes):
        if len(cur) <= 1:
            break
        ordered = sorted(cur, key=lambda c: normalize(c["claim"]))
        chunks = [ordered[i:i + batch] for i in range(0, len(ordered), batch)]
        prompts = [DEDUP_PROMPT.replace(
            "[claims]", "\n".join(f"- {c['claim']}" for c in ch)) for ch in chunks]
        survivors: List[dict] = []
        for ch, raw in zip(chunks, model.batch_infer(prompts)):
            got = _parse_claim_strings(raw)
            if not got:
                survivors.extend(ch)                   # unparseable: keep the batch
                continue
            survivors.extend({"claim": t} for t in got)
        nxt: Dict[str, dict] = {}
        for c in survivors:
            k = normalize(c["claim"])
            if k and k not in nxt:
                nxt[k] = c
        nxt_list = list(nxt.values())
        stats[f"after_pass{p + 1}"] = len(nxt_list)
        if len(nxt_list) >= len(cur):                  # converged
            cur = nxt_list
            break
        cur = nxt_list

    return attach_doc_ids(cur, claims), stats
