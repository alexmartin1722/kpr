#!/usr/bin/env python3
"""run.py — the report driver (`kpr-report`).

Builds a report from the first batch of documents and updates it with each
later batch, under one condition. With a single batch it is just report
generation; with several it is the iterative setting the conditions exist to
compare.

    kpr-report --claims claims.jsonl --requests requests.jsonl \\
        --condition kpr --out-dir reports

    # every condition over a frozen RAGTIME config, two rounds (set1 -> set2)
    kpr-report --claims claims.jsonl --docs docs.jsonl \\
        --ragtime-config configs/v1_temporal.json \\
        --condition kpr,conclaim,context,scratch --out-dir reports

Round 1 is written from claims (kpr, conclaim) or from documents (context,
scratch, rewrite_cond), matching what each condition conditions on later.
The `--shared-seed` flag instead gives every condition the SAME round-1 report,
so a strong claim-built seed never flatters a text-conditioned update — that is
the comparison you usually want, and it is on by default for a multi-condition
run.

One JSON per report, plus the final Markdown. The record keeps every round, and
the top-level `report`/`citations`/`claims_used` mirror the final round so the
MiRAGE export reads it unchanged.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

from .config import add_config_arg, parse_args_with_config
from .citations import CiteReg
from .claims import load_claim_rows, pool_claims
from .corpus import DocStore
from .llm_api import ApiLLM, read_endpoint
from .report import (
    CONDITIONS, build_from_claims, build_from_docs, update_conclaim, update_context,
    update_kpr, update_rewrite_cond, update_scratch,
)
from .requests import ReportRequest, from_ragtime_config, load_requests

# conditions whose round-1 report is written from claims rather than documents
CLAIM_SEEDED = {"kpr", "conclaim"}


def _seed(condition: str, req: ReportRequest, batch: List[str], claim_rows,
          store: DocStore, model, reg: CiteReg, gate: bool, dedup: bool,
          max_claims, gate_votes):
    """Round 1 for one condition."""
    if condition in CLAIM_SEEDED:
        pool = pool_claims(claim_rows, batch)
        stats = {"pooled": len(pool)}
        claims = pool
        if condition == "kpr":
            if gate or max_claims:
                from .gate import relevance_gate
                claims, _d = relevance_gate(claims, req.request, model,
                                         votes=gate_votes, keep_top=max_claims)
                stats["gated_kept"] = len(claims)
            if dedup:
                from .dedup import dedup_claims
                claims, dstats = dedup_claims(claims, model)
                stats["deduped"] = len(claims)
                stats["dedup"] = dstats
        md, reg, wstats = build_from_claims(req.request, claims, model, reg, req.title)
        stats.update(wstats)
        return md, stats, claims
    md, reg, stats = build_from_docs(req.request, batch, store, model, reg)
    return md, stats, []


def _update(condition: str, report_md: str, req: ReportRequest, batch: List[str],
            seen: List[str], claim_rows, store: DocStore, model, reg: CiteReg,
            gate: bool, dedup: bool, max_claims, gate_votes):
    """One later round for one condition."""
    if condition == "scratch":
        md, stats = update_scratch(req.request, seen, store, model, reg)
        return md, stats, []
    if condition == "rewrite_cond":
        md, stats = update_rewrite_cond(report_md, req.request, batch, store, model, reg)
        return md, stats, []

    pool = pool_claims(claim_rows, batch)
    if condition == "kpr":
        md, stats = update_kpr(report_md, req.request, pool, model, reg, req.title,
                               gate=gate, dedup=dedup, max_claims=max_claims,
                               gate_votes=gate_votes)
        return md, stats, pool
    if condition == "conclaim":
        md, stats = update_conclaim(report_md, req.request, pool, model, reg, req.title)
        return md, stats, pool
    if condition == "context":
        md, stats = update_context(report_md, req.request, pool, store, model, reg, req.title)
        return md, stats, pool
    raise ValueError(f"unknown condition {condition!r}")


def run_one(req: ReportRequest, condition: str, claim_rows, store: DocStore, model,
            gate: bool, dedup: bool, max_claims, gate_votes,
            seed: Optional[tuple] = None) -> dict:
    """Every round for one (report, condition). Returns the output record."""
    t0 = time.time()
    rounds_docs = req.resolved_rounds(store)
    reg = CiteReg()
    rounds: List[dict] = []
    seen: List[str] = []
    md = ""
    used_claims: List[dict] = []

    for n, batch in enumerate(rounds_docs, 1):
        seen.extend(d for d in batch if d not in seen)
        if n == 1:
            if seed is not None:
                md, stats, used_claims = seed[0], dict(seed[1]), list(seed[2])
                reg = seed[3].copy()
                stats["shared_seed"] = True
            else:
                md, stats, used_claims = _seed(condition, req, batch, claim_rows, store,
                                               model, reg, gate, dedup, max_claims,
                                               gate_votes)
        else:
            md, stats, used_claims = _update(condition, md, req, batch, seen, claim_rows,
                                             store, model, reg, gate, dedup, max_claims,
                                             gate_votes)
        rounds.append({"round": n, "n_docs": len(batch), "doc_ids": list(batch),
                       "report": md, "citations": reg.mapping(), "stats": stats,
                       "claims_used": [{"claim": c["claim"], "doc_id": c["doc_id"]}
                                       for c in used_claims]})

    last = rounds[-1]
    return {
        "report_id": req.report_id,
        "title": req.title,
        "request": req.request,
        "condition": condition,
        "n_rounds": len(rounds),
        "doc_ids": seen,
        "rounds": rounds,
        # the final round, hoisted so downstream readers need no round logic
        "report": last["report"],
        "citations": last["citations"],
        "claims_used": last["claims_used"],
        "stats": last["stats"],
        "elapsed_s": round(time.time() - t0, 1),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--claims", type=Path, default=None,
                    help="claims.jsonl from kpr-decompose (corpus mode)")
    ap.add_argument("--docs", type=Path, default=None,
                    help="docs.jsonl; required for context/scratch/rewrite_cond")
    ap.add_argument("--requests", type=Path, default=None,
                    help="generic requests.jsonl")
    ap.add_argument("--ragtime-config", default=None,
                    help="frozen RAGTIME task config -> per-topic set1/set2 rounds")
    ap.add_argument("--ragtime-topics", default=None,
                    help="override the RAGTIME topics file")
    ap.add_argument("--request", default=None, help="a single report request, as text")
    ap.add_argument("--report-id", default="report", help="id for a single --request run")

    ap.add_argument("--condition", default="kpr",
                    help=f"comma list of {','.join(CONDITIONS)} (default kpr)")
    ap.add_argument("--shared-seed", action=argparse.BooleanOptionalAction, default=None,
                    help="give every condition the same round-1 report "
                         "(default: on for multi-condition runs)")
    ap.add_argument("--seed-from", choices=["docs", "claims"], default="docs",
                    help="how the shared round-1 seed is written (default docs)")

    ap.add_argument("--gate", action=argparse.BooleanOptionalAction, default=True,
                    help="query-relevance gate, kpr only (default on)")
    ap.add_argument("--dedup", action=argparse.BooleanOptionalAction, default=True,
                    help="cross-document dedup, kpr only (default on)")
    ap.add_argument("--gate-votes", type=int, default=1)
    ap.add_argument("--max-claims", type=int, default=None,
                    help="cap the pool to the N most on-topic claims (implies --gate)")

    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--skip-existing", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--api-base", default=None)
    ap.add_argument("--api-model", default=None)
    ap.add_argument("--concurrency", type=int, default=16)
    ap.add_argument("--max-tokens", type=int, default=4096)
    add_config_arg(ap)
    args = parse_args_with_config(ap)
    conditions = [c.strip() for c in args.condition.split(",") if c.strip()]
    bad = [c for c in conditions if c not in CONDITIONS]
    if bad:
        sys.exit(f"unknown condition(s) {bad}; expected from {list(CONDITIONS)}")
    if args.shared_seed is None:
        args.shared_seed = len(conditions) > 1
    needs_docs = {"context", "scratch", "rewrite_cond"} & set(conditions)
    if needs_docs and not args.docs:
        sys.exit(f"--docs docs.jsonl is required for {sorted(needs_docs)}")
    if (set(conditions) - {"scratch", "rewrite_cond"}) and not args.claims:
        sys.exit("--claims claims.jsonl is required for kpr/conclaim/context")

    # ── requests ────────────────────────────────────────────────────────────
    if args.ragtime_config:
        kw = {"topics_file": args.ragtime_topics} if args.ragtime_topics else {}
        requests = from_ragtime_config(args.ragtime_config, **kw)
    elif args.requests:
        requests = load_requests(args.requests)
    elif args.request:
        requests = [ReportRequest(report_id=args.report_id, request=args.request)]
    else:
        sys.exit("give --requests, --ragtime-config, or --request")

    if args.nshards > 1:
        requests = [r for i, r in enumerate(requests) if i % args.nshards == args.shard]
    if args.limit:
        requests = requests[:args.limit]
    args.out_dir.mkdir(parents=True, exist_ok=True)

    def out_path(rid, cond):
        d = args.out_dir / cond if len(conditions) > 1 else args.out_dir
        d.mkdir(parents=True, exist_ok=True)
        return d / f"{rid}.json"

    tag = f"[shard {args.shard}/{args.nshards}] " if args.nshards > 1 else ""
    print(f"{tag}{len(requests)} reports x {len(conditions)} condition(s) "
          f"-> {args.out_dir}"
          f"{' (shared round-1 seed)' if args.shared_seed and len(conditions) > 1 else ''}",
          flush=True)
    if not requests:
        return

    claim_rows = load_claim_rows(args.claims) if args.claims else []
    store = DocStore.from_jsonl(args.docs) if args.docs else DocStore()

    api_base, api_model = args.api_base, args.api_model
    if not api_base or not api_model:
        fb, fm = read_endpoint()
        api_base, api_model = api_base or fb, api_model or fm
    if not api_base:
        sys.exit("no endpoint: pass --api-base/--api-model or set KPR_SERVER_READY")
    print(f"{tag}endpoint {api_base} ({api_model})", flush=True)
    model = ApiLLM(api_base, api_model, enable_thinking=False, temperature=0.0,
                   max_tokens=args.max_tokens, concurrency=args.concurrency)

    for n, req in enumerate(requests, 1):
        todo = [c for c in conditions
                if not (args.skip_existing and out_path(req.report_id, c).exists())]
        if not todo:
            print(f"{tag}[{n}/{len(requests)}] {req.report_id}: all conditions exist, skip",
                  flush=True)
            continue

        seed = None
        if args.shared_seed and len(conditions) > 1:
            batch = req.resolved_rounds(store)[0]
            reg = CiteReg()
            try:
                if args.seed_from == "claims":
                    pool = pool_claims(claim_rows, batch)
                    md, reg, st = build_from_claims(req.request, pool, model, reg, req.title)
                    seed = (md, st, pool, reg)
                else:
                    md, reg, st = build_from_docs(req.request, batch, store, model, reg)
                    seed = (md, st, [], reg)
            except Exception as exc:  # noqa: BLE001
                print(f"{tag}[{n}/{len(requests)}] {req.report_id}: SEED ERROR "
                      f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
                continue

        for cond in todo:
            try:
                rec = run_one(req, cond, claim_rows, store, model, args.gate, args.dedup,
                              args.max_claims, args.gate_votes, seed=seed)
            except Exception as exc:  # noqa: BLE001 - one bad report must not stop the run
                print(f"{tag}[{n}/{len(requests)}] {req.report_id}/{cond}: ERROR "
                      f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
                continue
            op = out_path(req.report_id, cond)
            op.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
            md = rec["report"]
            op.with_suffix(".md").write_text(md if md.endswith("\n") else md + "\n",
                                             encoding="utf-8")
            print(f"{tag}[{n}/{len(requests)}] {req.report_id}/{cond} "
                  f"{rec['n_rounds']}r {rec['elapsed_s']}s {rec['stats']}", flush=True)
    print(f"{tag}done -> {args.out_dir}", flush=True)


if __name__ == "__main__":
    main()
