"""report.py — generating a report, and keeping it current.

Round 1 writes the report from the first batch of sources; each later batch
updates it. The rewriting itself is `knowledge_pr.authoring` — this module is
the report profile over it: which filters run, what the writer is conditioned
on, and the context budgeting the iterative setting needs, since a report that
keeps growing eventually outgrows the window on its own.

    review              each claim vs the CURRENT report
    integrate           run the shared authoring pass over a Markdown report
    build_from_claims   round 1, from decomposed claims
    build_from_docs     round 1, from the documents themselves (the control)
    update_*            the five conditions

`report_run.py` is the driver (`kpr-report`).
"""

from __future__ import annotations

from collections import Counter
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from .article_model import parse_report, render_report, strip_think
from .authoring import Target, apply_edits, author
from .authoring.stages import extract_json_array
from .citations import CiteReg, tag_claims
from .corpus import DocStore, count_tokens
from .dedup import dedup_claims
from .gate import relevance_gate
from .prompts import (
    REPORT_FROM_CLAIMS_PROMPT, REPORT_FROM_DOCS_PROMPT, REPORT_REVIEW_PROMPT,
    REWRITE_COND_PROMPT,
)


# Context budget. The document/claim budget is whatever remains after the
# filled prompt scaffold, computed per call rather than guessed up front.
MODEL_CTX = 32768
OUTPUT_MAX = 4096
CHAT_SLACK = 400


def doc_budget(scaffold: str) -> int:
    """Tokens left for documents once the rest of the prompt is filled in."""
    return max(2000, MODEL_CTX - OUTPUT_MAX - CHAT_SLACK - count_tokens(scaffold))


def truncate_report(md: str, reserve: int) -> str:
    """Cap a prior report so it plus `reserve` fits the window.

    Truncation is marked rather than silent, so a clipped report is never
    mistaken for a complete one.
    """
    budget = MODEL_CTX - OUTPUT_MAX - CHAT_SLACK - reserve
    if budget <= 0 or count_tokens(md) <= budget:
        return md
    kept, tot = [], 0
    for ln in md.splitlines():
        t = count_tokens(ln) + 1
        if tot + t > budget:
            break
        kept.append(ln)
        tot += t
    return "\n".join(kept) + "\n[...report truncated for context...]"


def target_for(title: str = "") -> Target:
    """The authoring prompts' slots, addressed to a report."""
    return Target.report(title)


def review(report_md: str, request: str, claims: Sequence[dict], model,
           batch: int = 30) -> List[str]:
    """Each claim vs the current report: SUPPORTED | ABSENT | CONTRADICTED.

    Defaults to ABSENT on an unparseable verdict — a claim the reviewer failed
    to judge is offered to the writer rather than dropped, so a parse failure
    cannot silently delete new information.
    """
    verdicts = ["ABSENT"] * len(claims)
    if not claims:
        return verdicts
    claims_tok = max(count_tokens(c["claim"]) + 4 for c in claims) * batch
    report = truncate_report(report_md, reserve=count_tokens(request) + claims_tok + 300)

    prompts: List[str] = []
    spans: List[Tuple[int, int]] = []
    for s in range(0, len(claims), batch):
        chunk = claims[s:s + batch]
        block = "\n".join(f"{i + 1}. {c['claim']}" for i, c in enumerate(chunk))
        prompts.append(REPORT_REVIEW_PROMPT.replace("[request]", request)
                       .replace("[report]", report).replace("[claims]", block))
        spans.append((s, len(chunk)))
    for raw, (s, size) in zip(model.batch_infer(prompts), spans):
        for o in extract_json_array(raw) or []:
            if isinstance(o, dict) and "idx" in o:
                i = o["idx"] - 1
                v = str(o.get("verdict", "")).upper()
                if 0 <= i < size and v in ("SUPPORTED", "ABSENT", "CONTRADICTED"):
                    verdicts[s + i] = v
    return verdicts


def docs_block(claims: Sequence[dict], store: DocStore, reg: CiteReg,
               max_chars_per_doc: int = 8000) -> str:
    """The source documents behind a set of claims, as one prompt block.

    Used by the text-conditioned condition: the claims decide which documents
    are relevant to a section, and then the documents — not the claims — are
    what the rewrite sees.
    """
    doc_ids = list(dict.fromkeys(c["doc_id"] for c in claims))
    for d in doc_ids:
        reg.num(d)
    block, _used, _dropped = store.concat(
        doc_ids, max_chars_per_doc=max_chars_per_doc,
        max_input_tokens=doc_budget(""), numbering=reg.numbering())
    return block


def integrate(report_md: str, claims: Sequence[dict], model, reg: CiteReg,
              title: str = "", store: Optional[DocStore] = None) -> str:
    """Run the shared authoring pass over a Markdown report; return the new one.

    With `store`, each section is rewritten from the FULL SOURCE DOCUMENTS of
    the claims routed to it instead of from the claims — the text-conditioned
    baseline. The routing is identical either way, so the two differ in exactly
    one variable.
    """
    if not claims:
        return report_md
    article = parse_report(report_md, title)
    content_for = (lambda cs: docs_block(cs, store, reg)) if store is not None else None
    edits, new_sections, _routing = author(
        article, claims, model, target_for(title),
        refs_of=lambda c: [reg.num(c["doc_id"])],
        content_for=content_for)
    return render_report(apply_edits(article, edits, new_sections))


# claim tokens per report-writing prompt; above this the report is built
# iteratively instead of in one shot
CLAIM_WRITE_BUDGET = 14000

EMPTY_REPORT = "## Overview\nNo relevant information was found in the sources.\n"


def chunk_claims(claims: Sequence[dict], budget: Optional[int] = None) -> List[List[dict]]:
    """Split a pool into per-prompt chunks within the claim write budget."""
    budget = CLAIM_WRITE_BUDGET if budget is None else budget
    chunks: List[List[dict]] = []
    cur: List[dict] = []
    curtok = 0
    for c in claims:
        t = count_tokens(c["claim"]) + 6          # + "- " and the [N] tag
        if cur and curtok + t > budget:
            chunks.append(cur)
            cur, curtok = [], 0
        cur.append(c)
        curtok += t
    if cur:
        chunks.append(cur)
    return chunks


def build_from_claims(request: str, claims: Sequence[dict], model,
                      reg: Optional[CiteReg] = None, title: str = ""
                      ) -> Tuple[str, CiteReg, dict]:
    """Write a report from claims. One-shot if the pool fits, else iterative."""
    reg = reg or CiteReg()
    if not claims:
        return EMPTY_REPORT, reg, {"chunks": 0, "claims": 0}
    chunks = chunk_claims(claims)
    p = (REPORT_FROM_CLAIMS_PROMPT.replace("[request]", request)
         .replace("[claims]", tag_claims(chunks[0], reg)))
    md = strip_think(model.batch_infer([p])[0])
    for ch in chunks[1:]:
        md = integrate(md, ch, model, reg, title)
    return md, reg, {"chunks": len(chunks), "claims": len(claims)}


def build_from_docs(request: str, doc_ids: Sequence[str], store: DocStore, model,
                    reg: Optional[CiteReg] = None,
                    max_chars_per_doc: int = 8000) -> Tuple[str, CiteReg, dict]:
    """Write a report from concatenated documents — the no-decomposition control.

    Documents that do not fit the context are dropped and named in the stats,
    never silently swallowed: that ceiling is the thing this condition exists
    to expose.
    """
    reg = reg or CiteReg()
    for did in doc_ids:                      # number before budgeting
        if store.text(did):
            reg.num(did)
    scaffold = (REPORT_FROM_DOCS_PROMPT.replace("[request]", request)
                .replace("[documents]", ""))
    block, used, dropped = store.concat(doc_ids, max_chars_per_doc=max_chars_per_doc,
                                        max_input_tokens=doc_budget(scaffold),
                                        numbering=reg.numbering())
    p = (REPORT_FROM_DOCS_PROMPT.replace("[request]", request)
         .replace("[documents]", block))
    md = strip_think(model.batch_infer([p])[0])
    return md, reg, {"docs_used": len(used), "docs_dropped": len(dropped),
                     "dropped_doc_ids": dropped}


CONDITIONS = ("kpr", "conclaim", "context", "scratch", "rewrite_cond")

# claims marked this way tell the section prompt to REPLACE the value it
# contradicts rather than keep both
REVISES_SUFFIX = "  (REVISES)"


def update_kpr(report_md: str, request: str, claims: Sequence[dict], model,
               reg: CiteReg, title: str = "", gate: bool = True, dedup: bool = True,
               max_claims: Optional[int] = None, gate_votes: int = 1
               ) -> Tuple[str, dict]:
    """Gate -> dedup -> review -> integrate only what is new or correcting."""
    stats = {"pooled": len(claims)}
    working = list(claims)

    if gate or max_claims:
        working, _dropped = relevance_gate(working, request, model,
                                        votes=gate_votes, keep_top=max_claims)
        stats["gated_kept"] = len(working)
    if dedup:
        working, dstats = dedup_claims(working, model)
        stats["deduped"] = len(working)
        stats["dedup"] = dstats
    if not working:
        stats.update(absent=0, contradicted=0, supported=0)
        return report_md, stats

    verdicts = review(report_md, request, working, model)
    counts = Counter(verdicts)
    stats.update(absent=counts.get("ABSENT", 0),
                 contradicted=counts.get("CONTRADICTED", 0),
                 supported=counts.get("SUPPORTED", 0))

    to_add = [c for c, v in zip(working, verdicts) if v == "ABSENT"]
    to_revise = [{**c, "claim": c["claim"] + REVISES_SUFFIX}
                 for c, v in zip(working, verdicts) if v == "CONTRADICTED"]
    to_integrate = to_add + to_revise
    stats["integrated"] = len(to_integrate)
    if not to_integrate:
        return report_md, stats
    return integrate(report_md, to_integrate, model, reg, title), stats


def update_conclaim(report_md: str, request: str, claims: Sequence[dict], model,
                    reg: CiteReg, title: str = "") -> Tuple[str, dict]:
    """Route the unfiltered pool and integrate it, conditioned on the claims."""
    stats = {"pooled": len(claims), "integrated": len(claims)}
    if not claims:
        return report_md, stats
    return integrate(report_md, claims, model, reg, title), stats


def update_context(report_md: str, request: str, claims: Sequence[dict],
                   store: DocStore, model, reg: CiteReg, title: str = ""
                   ) -> Tuple[str, dict]:
    """Route the unfiltered pool, then rewrite sections from the full documents."""
    stats = {"pooled": len(claims),
             "docs": len({c["doc_id"] for c in claims})}
    if not claims:
        return report_md, stats
    return integrate(report_md, claims, model, reg, title, store=store), stats


def update_scratch(request: str, all_doc_ids: Sequence[str], store: DocStore,
                   model, reg: Optional[CiteReg] = None) -> Tuple[str, dict]:
    """Discard the prior report; regenerate from every document seen so far."""
    md, reg, stats = build_from_docs(request, all_doc_ids, store, model, reg)
    return md, stats


def update_rewrite_cond(report_md: str, request: str, new_doc_ids: Sequence[str],
                        store: DocStore, model, reg: CiteReg,
                        max_chars_per_doc: int = 8000) -> Tuple[str, dict]:
    """Whole-report conditioned rewrite: prior report + new documents, one pass."""
    for did in new_doc_ids:
        if store.text(did):
            reg.num(did)
    # the prior report shares the window with the documents, so cap it first
    prev = truncate_report(report_md, reserve=len(request) // 3 + 2400)
    scaffold = (REWRITE_COND_PROMPT.replace("[request]", request)
                .replace("[previous]", prev).replace("[documents]", ""))
    block, used, dropped = store.concat(new_doc_ids, max_chars_per_doc=max_chars_per_doc,
                                        max_input_tokens=doc_budget(scaffold),
                                        numbering=reg.numbering())
    p = (REWRITE_COND_PROMPT.replace("[request]", request)
         .replace("[previous]", prev).replace("[documents]", block))
    md = strip_think(model.batch_infer([p])[0])
    return md, {"docs_used": len(used), "docs_dropped": len(dropped),
                "dropped_doc_ids": dropped}
