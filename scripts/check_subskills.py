#!/usr/bin/env python3
"""Check installed subskills against the pinned workflow manifest."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from subskill_router import inspect_dependencies, load_manifest


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
    result = inspect_dependencies(
        load_manifest(MANIFEST_PATH), Path(args.skills_root).expanduser().resolve()
    )
    missing_core = [item for item in result if item["tier"] == "core" and not item["installed"]]
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result:
            state = "installed" if item["installed"] else "missing"
            print(f"{state:9} {item['tier']:8} {item['name']}")
        if missing_core:
            print("core subskills missing; the orchestrator can continue, but specialist routing is degraded")
    return 1 if missing_core else 0


if __name__ == "__main__":
    raise SystemExit(main())
