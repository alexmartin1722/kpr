"""gate.py — the two claim filters that run before authoring.

    relevance_gate  is this claim on-topic for THIS request?     (reports)
    content_gate    does this claim carry encyclopedic content?  (Wikipedia)

They answer different questions and neither is authoring, which is why they sit
here rather than in `knowledge_pr.authoring`. The relevance gate depends on the
query rather than on the document being written, so it is not circular; the
content gate scores a claim against the article title and drops content-free
ones (MT fragments, citation metadata, category labels).

Both judge in batches, and both KEEP a batch whose response will not parse:
losing a real fact is worse than carrying a weak one the writer can decline.
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from .authoring.stages import extract_json_array, numbered_block
from .prompts import CHECKWORTHY_PROMPT, GATE_RELEVANCE_PROMPT


def relevance_gate(claims: Sequence[dict], request: str, model, batch: int = 40,
                votes: int = 1, keep_top: Optional[int] = None
                ) -> Tuple[List[dict], List[dict]]:
    """Keep the claims relevant to `request`. Returns (kept, dropped).

    `votes` > 1 samples the gate repeatedly and takes a majority (ties keep),
    which is also what makes `keep_top` discriminative: with a single vote the
    keep-fraction is 0 or 1 and cannot rank the survivors.
    """
    if not claims:
        return [], []
    texts = [c["claim"] if isinstance(c, dict) else str(c) for c in claims]

    prompts: List[str] = []
    spans: List[Tuple[int, int]] = []
    for s in range(0, len(texts), batch):
        chunk = texts[s:s + batch]
        block = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(chunk))
        p = GATE_RELEVANCE_PROMPT.replace("[request]", request).replace("[claims]", block)
        for _ in range(votes):
            prompts.append(p)
            spans.append((s, len(chunk)))

    keep_votes = [0] * len(texts)
    seen = [0] * len(texts)
    for raw, (s, size) in zip(model.batch_infer(prompts), spans):
        arr = extract_json_array(raw)
        verdicts = [True] * size                      # parse failure keeps
        if arr:
            for o in arr:
                if isinstance(o, dict) and "idx" in o:
                    i = o["idx"] - 1
                    if 0 <= i < size:
                        verdicts[i] = bool(o.get("relevant", True))
        for j in range(size):
            seen[s + j] += 1
            if verdicts[j]:
                keep_votes[s + j] += 1

    dropped: List[dict] = []
    scored: List[Tuple[float, int, dict]] = []
    for i, c in enumerate(claims):
        if keep_votes[i] * 2 >= max(1, seen[i]):       # majority; ties keep
            scored.append((keep_votes[i] / max(1, seen[i]), i, c))
        else:
            dropped.append(c)
    if keep_top is not None and len(scored) > keep_top:
        scored.sort(key=lambda t: (-t[0], t[1]))       # most on-topic first
        dropped.extend(c for _, _, c in scored[keep_top:])
        scored = scored[:keep_top]
    scored.sort(key=lambda t: t[1])                    # restore pool order
    return [c for _, _, c in scored], dropped


def content_gate(title: str, claims: List[dict], model, min_importance: int = 1,
                batch_size: int = 40):
    """Score each claim 0-2 for factual content; return (kept, dropped).

    Every claim gets an `importance` field, dropped ones included, so the
    decision is auditable. An unparsed score defaults to 1 (keep): a gate that
    silently deletes facts when the model burps is worse than one that lets a
    weak claim through.
    """
    batches = [claims[i:i + batch_size] for i in range(0, len(claims), batch_size)]
    prompts = [
        CHECKWORTHY_PROMPT.replace("[title]", title.replace("_", " "))
                          .replace("[claims]", numbered_block(b))
        for b in batches
    ]
    outputs = model.batch_infer(prompts) if prompts else []
    kept, dropped = [], []
    for b, raw in zip(batches, outputs):
        score = {}
        for item in extract_json_array(raw) or []:
            if isinstance(item, dict) and isinstance(item.get("idx"), int):
                s = item.get("score")
                if isinstance(s, (int, float)):
                    score[item["idx"]] = int(s)
        for i, claim in enumerate(b, start=1):
            s = score.get(i, 1)
            c = {**claim, "importance": s}
            (kept if s >= min_importance else dropped).append(c)
    return kept, dropped


# the report pipeline's historical name for the relevance gate
gate_claims = relevance_gate
