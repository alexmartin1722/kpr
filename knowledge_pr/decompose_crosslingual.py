#!/usr/bin/env python3
"""
decompose_crosslingual.py — native text in any language -> English atomic claims.

One uniform method for every language (English included), so a claim pool has a
single provenance and no machine translation enters the pipeline.

Two input modes, sharing the prompt, the parser and the endpoint:

  ARTICLE mode (--docs-dir/--article)
      A MegaWika2 article set, decomposed per SENTENCE with its paragraph as
      context. Output: {output-dir}/crosslingual/{article}_{lang}.jsonl, one row
      per sentence with para_idx/sent_idx provenance. This is the Wikipedia
      changelog pipeline's input and its schema is unchanged.

  CORPUS mode (--docs/--ragtime-doc-ids/--ragtime-config)
      A flat document collection, decomposed per UNIT (paragraph by default).
      Output: a single --out claims.jsonl, one row per unit:

          {"doc_id", "lang", "unit", "unit_index", "unit_text", "claims"}

      Paragraph is the default unit because sentence splitting is unreliable
      for Arabic and Chinese while a blank-line paragraph is safe in every
      script. Rows are kept per unit rather than pooled per document, so a
      later run can pool at whatever level it wants and a faithfulness check
      can point a claim back at the exact text it came from.

Usage:
    kpr-decompose --docs-dir DOCS --article Nabonidus --output-dir OUT --include-en
    kpr-decompose --docs docs.jsonl --out claims.jsonl
    kpr-decompose --ragtime-config v1_temporal.json --save-docs docs.jsonl --out claims.jsonl
    kpr-decompose --docs docs.jsonl --out claims.jsonl --shard 0 --nshards 20
    kpr-decompose --out claims.jsonl --merge
"""
import argparse, json, re, sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .config import add_config_arg, parse_args_with_config
from .prompts import DECOMP_CROSSLINGUAL_PROMPT
from .llm_api import ApiLLM, read_endpoint
from .corpus import RAGTIME_DOCS_DIR, DocStore


def load_doc(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def doc_id_from_path(path: Path) -> Tuple[str, str]:
    stem = path.stem
    parts = stem.rsplit("_", 1)
    return (stem, parts[1]) if len(parts) == 2 else (stem, "unknown")


def iter_sentences(doc: Dict[str, Any]):
    for para_idx, element in enumerate(doc.get("elements", [])):
        if element.get("type") != "paragraph":
            continue
        for sent_idx, sent in enumerate(element.get("sentences", [])):
            orig = sent.get("text", "").strip()
            trans = (sent.get("translated_text") or "").strip()
            if orig:
                yield para_idx, sent_idx, orig, trans


def get_paragraph_text(doc, para_idx, use_translated=False) -> str:
    element = doc["elements"][para_idx]
    key = "translated_text" if use_translated else "text"
    parts = []
    for s in element.get("sentences", []):
        t = (s.get(key) or s.get("text") or "").strip()
        if t:
            parts.append(t)
    return " ".join(parts)


def build_crosslingual_prompt(paragraph: str, sentence: str) -> str:
    return DECOMP_CROSSLINGUAL_PROMPT.replace("[paragraph]", paragraph).replace("[sentence]", sentence)


def parse_claims(raw: str) -> List[str]:
    raw = re.sub(r"<think>[\s\S]*?</think>", "", raw).strip()
    match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", raw, re.DOTALL)
    if not match:
        match = re.search(r"(\[[\s\S]*?\])", raw)
    if not match:
        return []
    try:
        items = json.loads(match.group(1))
        return [item["claim"] for item in items if isinstance(item, dict) and "claim" in item]
    except (json.JSONDecodeError, TypeError, KeyError):
        return []


UNITS = ("paragraph", "sentence", "document")
DEFAULT_MAX_UNIT_CHARS = 3000
# Latin + CJK sentence-final punctuation followed by a capital, digit or opener
_SENT_SPLIT = re.compile(r"(?<=[.!?\u3002\uFF01\uFF1F])\s+(?=[A-Z0-9\"'(\u00C0-\u024F])")


def split_units(text: str, unit: str = "paragraph",
                max_chars: int = DEFAULT_MAX_UNIT_CHARS) -> List[str]:
    """Split a flat document into decomposition units.

    paragraph (default) — blank-line separated blocks, safe in every script.
    sentence — paragraphs, then sentences.
    document — the whole document as one unit.
    """
    text = (text or "").strip()
    if not text:
        return []
    if unit == "document":
        paras = [text]
    elif unit in ("paragraph", "sentence"):
        paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()] or [text]
        if unit == "sentence":
            paras = [s.strip() for p in paras
                     for s in (_SENT_SPLIT.split(p) or [p]) if s.strip()]
    else:
        raise ValueError(f"unknown unit {unit!r}; expected one of {UNITS}")

    out: List[str] = []
    for p in paras:
        while len(p) > max_chars:          # guard a pathological mega-paragraph
            out.append(p[:max_chars])
            p = p[max_chars:]
        if p:
            out.append(p)
    return out


def decompose_documents(doc_ids, store, model, unit: str = "paragraph",
                        max_unit_chars: int = DEFAULT_MAX_UNIT_CHARS) -> Dict[str, List[dict]]:
    """Decompose several documents in one batch -> {doc_id: [unit rows]}.

    Every (document, unit) is one prompt and they all go out together, so the
    endpoint stays saturated instead of being driven document by document.
    """
    prompts, rows = [], []
    for did in doc_ids:
        text = store.text(did)
        if not text:
            continue
        for i, u in enumerate(split_units(text, unit, max_unit_chars)):
            # the unit is both its own context and the span to decompose
            prompts.append(build_crosslingual_prompt(u, u))
            rows.append({"doc_id": did, "lang": store.lang(did), "unit": unit,
                         "unit_index": i, "unit_text": u})
    out: Dict[str, List[dict]] = {d: [] for d in doc_ids}
    if not prompts:
        return out
    for row, raw in zip(rows, model.batch_infer(prompts)):
        out[row["doc_id"]].append({**row, "claims": parse_claims(raw)})
    return out


def _shard_path(out: Path, shard: int) -> Path:
    return out.with_suffix(out.suffix + f".shard{shard:03d}")


def _done_doc_ids(path: Path) -> set:
    """doc_ids already written (a document's units are always written together)."""
    done = set()
    if path.exists():
        with path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    done.add(json.loads(line)["doc_id"])
                except (json.JSONDecodeError, KeyError):
                    continue
    return done


def _corpus_store(args) -> DocStore:
    if args.docs:
        return DocStore.from_jsonl(args.docs)
    ragtime_dir = Path(args.ragtime_docs_dir) if args.ragtime_docs_dir else RAGTIME_DOCS_DIR
    if args.ragtime_config:
        from .requests import config_doc_ids
        return DocStore.from_ragtime(config_doc_ids(args.ragtime_config), docs_dir=ragtime_dir)
    ids = [x for x in Path(args.ragtime_doc_ids).read_text().split() if x]
    return DocStore.from_ragtime(ids, docs_dir=ragtime_dir)


def run_corpus(args):
    """CORPUS mode: a flat document collection -> one claims.jsonl, per unit."""
    args.out.parent.mkdir(parents=True, exist_ok=True)

    if args.merge:
        shards = sorted(args.out.parent.glob(args.out.name + ".shard*"))
        if not shards:
            sys.exit(f"no shard files matching {args.out}.shard*")
        n = 0
        with args.out.open("w", encoding="utf-8") as w:
            for sf in shards:
                for line in sf.open(encoding="utf-8"):
                    w.write(line)
                    n += 1
        print(f"merged {len(shards)} shards, {n} unit rows -> {args.out}")
        return

    store = _corpus_store(args)
    if not len(store):
        sys.exit("document source resolved to 0 documents")
    if args.save_docs:
        print(f"froze {store.to_jsonl(args.save_docs)} documents -> {args.save_docs}")

    all_ids = sorted(store.doc_ids())
    mine = ([d for i, d in enumerate(all_ids) if i % args.nshards == args.shard]
            if args.nshards > 1 else all_ids)
    out_file = _shard_path(args.out, args.shard) if args.nshards > 1 else args.out
    if args.overwrite and out_file.exists():
        out_file.unlink()

    done = _done_doc_ids(out_file)
    todo = [d for d in mine if d not in done]
    tag = f"[shard {args.shard}/{args.nshards}] " if args.nshards > 1 else ""
    print(f"{tag}{len(mine)} documents; {len(done)} already done, {len(todo)} to go "
          f"(unit={args.unit})", flush=True)
    if not todo:
        print(f"{tag}nothing to do -> {out_file}")
        return

    api_base, api_model = args.api_base, args.api_model
    if not api_base or not api_model:
        fb, fm = read_endpoint()
        api_base, api_model = api_base or fb, api_model or fm
    if not api_base:
        sys.exit("no endpoint: pass --api-base/--api-model or set KPR_SERVER_READY")
    print(f"{tag}endpoint {api_base} ({api_model})", flush=True)
    model = ApiLLM(api_base=api_base, api_model=api_model,
                   max_tokens=args.max_tokens, concurrency=args.concurrency)

    n_units = n_claims = 0
    with out_file.open("a", encoding="utf-8") as w:
        for i in range(0, len(todo), args.batch_docs):
            chunk = todo[i:i + args.batch_docs]
            pooled = decompose_documents(chunk, store, model, args.unit, args.max_unit_chars)
            for did in chunk:
                for row in pooled.get(did, []):
                    w.write(json.dumps(row, ensure_ascii=False) + "\n")
                    n_units += 1
                    n_claims += len(row["claims"])
            w.flush()
            print(f"{tag}{min(i + args.batch_docs, len(todo))}/{len(todo)} documents, "
                  f"{n_units} units, {n_claims} claims", flush=True)
    print(f"{tag}done -> {out_file}  ({n_units} units, {n_claims} claims)", flush=True)


def run_article(args):

    art_dir = args.docs_dir / args.article
    doc_paths = [p for p in sorted(art_dir.glob("*.json"))
                 if args.include_en or doc_id_from_path(p)[1] != "en"]
    print(f"docs to decompose: {[p.name for p in doc_paths]}")

    prompts, meta = [], []
    for path in doc_paths:
        doc = load_doc(path)
        doc_id, lang = doc_id_from_path(path)
        for para_idx, sent_idx, orig, trans in iter_sentences(doc):
            para = get_paragraph_text(doc, para_idx, use_translated=False)
            prompts.append(build_crosslingual_prompt(para, orig))
            meta.append({"doc_id": doc_id, "lang": lang, "para_idx": para_idx,
                         "sent_idx": sent_idx, "original_text": orig,
                         "translated_text": trans})

    print(f"[crosslingual] {len(prompts)} sentences across {len(doc_paths)} docs")
    model = ApiLLM(api_base=args.api_base, api_model=args.api_model,
                   max_tokens=args.max_tokens, concurrency=args.concurrency)
    raw_outputs = model.batch_infer(prompts)

    grouped: Dict[str, List[Dict]] = defaultdict(list)
    for m, raw in zip(meta, raw_outputs):
        grouped[m["doc_id"]].append({**m, "claims": parse_claims(raw), "raw_decomp": raw})

    strategy_dir = args.output_dir / "crosslingual"
    strategy_dir.mkdir(parents=True, exist_ok=True)
    for doc_id, records in grouped.items():
        out = strategy_dir / f"{doc_id}.jsonl"
        with out.open("w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        n_claims = sum(len(r["claims"]) for r in records)
        print(f"  wrote {out.name}: {len(records)} sentences, {n_claims} claims")




def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    art = ap.add_argument_group("ARTICLE mode (MegaWika2 article set)")
    art.add_argument("--docs-dir", type=Path, help="MegaWika2 documents/ dir")
    art.add_argument("--article", help="article name")
    art.add_argument("--output-dir", type=Path,
                     help="writes {output-dir}/crosslingual/{article}_{lang}.jsonl")
    art.add_argument("--include-en", action="store_true",
                     help="also decompose the English edition (the comparison baseline)")

    cor = ap.add_argument_group("CORPUS mode (flat document collection)")
    cor.add_argument("--docs", help="generic docs.jsonl: {doc_id, text, lang}")
    cor.add_argument("--ragtime-doc-ids", help="file of RAGTIME doc ids (whitespace separated)")
    cor.add_argument("--ragtime-config", help="a frozen task config; uses every doc it names")
    cor.add_argument("--ragtime-docs-dir", default=None,
                     help="override the RAGTIME corpus dir (default $KPR_RAGTIME_DOCS)")
    cor.add_argument("--save-docs", type=Path, default=None,
                     help="freeze the resolved documents as a generic docs.jsonl")
    cor.add_argument("--out", type=Path, help="output claims.jsonl")
    cor.add_argument("--unit", choices=UNITS, default="paragraph",
                     help="decomposition unit (default: paragraph)")
    cor.add_argument("--max-unit-chars", type=int, default=DEFAULT_MAX_UNIT_CHARS)
    cor.add_argument("--batch-docs", type=int, default=200,
                     help="documents per flush to the output file")
    cor.add_argument("--shard", type=int, default=0)
    cor.add_argument("--nshards", type=int, default=1)
    cor.add_argument("--merge", action="store_true",
                     help="concatenate <out>.shardNNN files into <out> and exit")
    cor.add_argument("--overwrite", action="store_true",
                     help="ignore existing output and start over (default: resume)")

    ap.add_argument("--api-base", default=None)
    ap.add_argument("--api-model", default=None)
    ap.add_argument("--concurrency", type=int, default=16)
    ap.add_argument("--max-tokens", type=int, default=512)
    add_config_arg(ap)
    args = parse_args_with_config(ap)
    corpus_mode = bool(args.docs or args.ragtime_doc_ids or args.ragtime_config or args.merge)
    if corpus_mode:
        if not args.out:
            ap.error("corpus mode needs --out claims.jsonl")
        return run_corpus(args)
    if not (args.docs_dir and args.article and args.output_dir):
        ap.error("give a corpus source (--docs/--ragtime-doc-ids/--ragtime-config) "
                 "or an article set (--docs-dir --article --output-dir)")
    if not args.api_base or not args.api_model:
        fb, fm = read_endpoint()
        args.api_base = args.api_base or fb
        args.api_model = args.api_model or fm
    if not args.api_base:
        ap.error("no endpoint: pass --api-base/--api-model or set KPR_SERVER_READY")
    return run_article(args)


if __name__ == "__main__":
    main()
