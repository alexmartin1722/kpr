"""requests.py — the report request, and where document batches come from.

A ReportRequest is what the writer is asked for plus the ordered batches of
documents it gets. One batch is an ordinary single-pass report; several batches
is the iterative setting — batch 1 builds the report, each later batch updates
it, which is the whole point of the claim-based pipeline.

Three sources:

    load_requests(path)             a generic requests.jsonl
    from_ragtime_topics(...)        RAGTIME topics -> title/background/problem
    from_ragtime_config(...)        a frozen task config -> per-topic set1/set2

Generic requests.jsonl, one row per report:

    {"report_id": "r1", "request": "Report on ...", "doc_ids": ["d1", "d2"]}
    {"report_id": "r2", "title": "...", "background": "...",
     "problem_statement": "...", "rounds": [["d1"], ["d2", "d3"]]}

`request` is used verbatim when present; otherwise the RAGTIME-style
title/background/problem_statement fields are assembled into a request block.
`doc_ids` is shorthand for a single round, and omitting both means every
document in the store.

(This module is `knowledge_pr.requests`; it does not shadow the HTTP library,
which other modules still reach with a plain `import requests`.)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

import os

RAGTIME_TOPICS_FILE = Path(os.environ.get(
    "KPR_RAGTIME_TOPICS", "/exp/scale25/ragtime/topics/ragtime25_main_all.jsonl"))


@dataclass
class ReportRequest:
    report_id: str
    request: str
    title: str = ""
    # ordered document batches; one entry = single-pass, several = iterative.
    # An empty list means "every document in the store", resolved by the driver.
    rounds: List[List[str]] = field(default_factory=list)

    @property
    def doc_ids(self) -> List[str]:
        """Every document this report draws on, across all rounds, in order."""
        seen, out = set(), []
        for batch in self.rounds:
            for d in batch:
                if d not in seen:
                    seen.add(d)
                    out.append(d)
        return out

    def resolved_rounds(self, store) -> List[List[str]]:
        """Rounds with an unspecified batch filled in from the store."""
        if not self.rounds:
            return [list(store.doc_ids())]
        return [list(b) if b else list(store.doc_ids()) for b in self.rounds]


def request_block(title: str = "", background: str = "",
                  problem_statement: str = "") -> str:
    """Assemble the RAGTIME-style fields into one request block."""
    parts = []
    if title:
        parts.append(f"TITLE: {title}")
    if background:
        parts.append(f"BACKGROUND: {background}")
    if problem_statement:
        parts.append(f"REPORT REQUEST: {problem_statement}")
    return "\n".join(parts).strip()


def _from_row(row: dict, fallback_id: str) -> ReportRequest:
    rid = str(row.get("report_id") or row.get("request_id") or row.get("topic_id")
              or fallback_id)
    title = row.get("title", "") or ""
    request = row.get("request") or request_block(
        title, row.get("background", ""), row.get("problem_statement", ""))
    rounds = row.get("rounds")
    if rounds is None:
        doc_ids = row.get("doc_ids")
        rounds = [list(doc_ids)] if doc_ids is not None else []
    else:
        rounds = [list(b) for b in rounds]
    return ReportRequest(report_id=rid, request=request, title=title, rounds=rounds)


def load_requests(path) -> List[ReportRequest]:
    """Read a generic requests.jsonl."""
    out = []
    with Path(path).open(encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            out.append(_from_row(json.loads(line), str(i)))
    return out


@lru_cache(maxsize=4)
def _ragtime_topics(topics_file: str) -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    with Path(topics_file).open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            rid = str(d.get("request_id") or d.get("topic_id") or "")
            if rid:
                out[rid] = {"title": d.get("title", ""),
                            "background": d.get("background", ""),
                            "problem_statement": d.get("problem_statement", "")}
    return out


def from_ragtime_topics(request_ids: Optional[Iterable[str]] = None,
                        topics_file=RAGTIME_TOPICS_FILE,
                        rounds_by_id: Optional[Dict[str, List[List[str]]]] = None
                        ) -> List[ReportRequest]:
    """RAGTIME topics -> ReportRequests (document batches supplied separately)."""
    topics = _ragtime_topics(str(topics_file))
    ids = [str(r) for r in request_ids] if request_ids is not None else sorted(topics)
    out = []
    for rid in ids:
        t = topics.get(rid)
        if t is None:
            continue
        out.append(ReportRequest(
            report_id=rid, title=t["title"],
            request=request_block(t["title"], t["background"], t["problem_statement"]),
            rounds=(rounds_by_id or {}).get(rid, [])))
    return out


def from_ragtime_config(config_file, topics_file=RAGTIME_TOPICS_FILE,
                        round_keys: Sequence[str] = ("set1_docs", "set2_docs"),
                        cap_per_round: Optional[Dict[str, int]] = None
                        ) -> List[ReportRequest]:
    """A frozen RAGTIME task config -> one ReportRequest per topic.

    The config is {request_id: {set1_docs: [...], set2_docs: [...], ...}}; each
    key in `round_keys` becomes one round, in order. `cap_per_round` truncates a
    batch (the document-budget sweep), e.g. {"set2_docs": 20}.
    """
    cfg = json.loads(Path(config_file).read_text(encoding="utf-8"))
    rounds_by_id: Dict[str, List[List[str]]] = {}
    for rid, entry in cfg.items():
        batches = []
        for key in round_keys:
            docs = list(entry.get(key, []) or [])
            cap = (cap_per_round or {}).get(key)
            if cap:
                docs = docs[:cap]
            batches.append(docs)
        rounds_by_id[str(rid)] = batches
    return from_ragtime_topics(sorted(rounds_by_id), topics_file, rounds_by_id)


def config_doc_ids(config_file, round_keys: Sequence[str] = ("set1_docs", "set2_docs"),
                   include_noise: bool = False) -> List[str]:
    """Every document id a config references — what to pull from the corpus."""
    cfg = json.loads(Path(config_file).read_text(encoding="utf-8"))
    keys = list(round_keys) + (["noise_docs"] if include_noise else [])
    seen, out = set(), []
    for entry in cfg.values():
        for key in keys:
            for d in entry.get(key, []) or []:
                if d not in seen:
                    seen.add(d)
                    out.append(d)
    return out
