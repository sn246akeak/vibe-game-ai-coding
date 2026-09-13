#!/usr/bin/env python3
"""Check installed subskills against the pinned workflow manifest."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from subskill_router import inspect_dependencies, load_manifest, resolve_routes


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "references" / "subskills.json"


def default_skills_root() -> Path:
    codex_root = os.environ.get("CODEX_HOME")
    if codex_root:
        return Path(codex_root).expanduser().resolve() / "skills"
    return Path.home() / ".codex" / "skills"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", default=str(default_skills_root()))
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = load_manifest(MANIFEST_PATH)
    root = Path(args.skills_root).expanduser().resolve()
    result = inspect_dependencies(manifest, root)
    inventory = dict(manifest, routes=[{"phase": 0, "skill": d["name"]} for d in manifest["dependencies"]])
    lock_path = MANIFEST_PATH.with_name("subskills.lock.json")
    lock = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.exists() else {}
    resolved = {r["skill"]: r["status"] for r in resolve_routes(inventory, 0, {}, root, lock)}
    for item in result:
        item["status"] = resolved[item["name"]]
    missing_core = [item for item in result if item["tier"] == "core" and item["status"] != "verified"]
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result:
            state = item["status"]
            print(f"{state:9} {item['tier']:8} {item['name']}")
        if missing_core:
            print("core inventory incomplete; resolve the actual phase before specialist use")
    return 1 if missing_core else 0


if __name__ == "__main__":
    raise SystemExit(main())
