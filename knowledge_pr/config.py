"""config.py — run any `kpr-*` command from a JSON config file.

Every command takes `--config path.json`. The file holds the same options you
would type on the command line, so a run is a file you can read, diff and
commit instead of a shell line nobody can reconstruct later.

    kpr-report --config configs/report_kpr.json
    kpr-report --config configs/report_kpr.json --out-dir /tmp/try2

Keys are the long option names with or without the leading dashes, and `-` and
`_` are interchangeable, so `--out-dir`, `out-dir` and `out_dir` all work.
A key starting with `_` is ignored, which is how you leave notes in a config
that has to stay valid JSON.

Anything given on the command line beats the config, and the config beats the
command's built-in default. A required option is satisfied by the config, so
`--config` alone is usually enough.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


def load_config(path) -> Dict[str, Any]:
    """Read a config file into {dest: value}, dropping `_`-prefixed notes."""
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"config file not found: {p}")
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{p} is not valid JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise SystemExit(f"{p} must contain a JSON object, got {type(raw).__name__}")
    out = {}
    for k, v in raw.items():
        if k.startswith("_"):
            continue
        out[k.lstrip("-").replace("-", "_")] = v
    return out


def add_config_arg(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add `--config` to a parser. Pair with `parse_args_with_config`."""
    parser.add_argument("--config", metavar="FILE", default=None,
                        help="JSON file of options; command-line flags override it")
    return parser


def parse_args_with_config(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Parse arguments, letting `--config` supply defaults.

    Two passes: read `--config` first, fold it into the parser's defaults, then
    parse for real so explicit flags win. Required options are relaxed for the
    first pass, since the config is allowed to be the thing that satisfies
    them.
    """
    required = [a for a in parser._actions if a.required]
    for a in required:
        a.required = False
    preliminary, _ = parser.parse_known_args()
    for a in required:
        a.required = True

    path = getattr(preliminary, "config", None)
    if path:
        config = load_config(path)
        by_dest = {a.dest: a for a in parser._actions}
        known, unknown = {}, []
        for k, v in config.items():
            action = by_dest.get(k)
            if action is None:
                unknown.append(k)
                continue
            if action.choices is not None and v not in action.choices:
                parser.error(f"{path}: '{k}' is '{v}', expected one of "
                             f"{list(action.choices)}")
            if action.type is not None and isinstance(v, str):
                try:
                    v = action.type(v)
                except (TypeError, ValueError) as exc:
                    parser.error(f"{path}: '{k}' = {v!r} is not valid: {exc}")
            known[k] = v
            action.required = False
        if unknown:
            parser.error(f"{path}: unrecognized option(s) {', '.join(sorted(unknown))} "
                         f"— prefix a key with '_' if it is meant as a note")
        parser.set_defaults(**known)

    return parser.parse_args()
