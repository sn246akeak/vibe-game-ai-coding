#!/usr/bin/env python3
"""Select delegated game-development skills for one workflow phase."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from subskill_router import load_manifest, select_routes


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "references" / "subskills.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", type=int, choices=range(10), required=True)
    parser.add_argument("--engine", default="")
    parser.add_argument("--runtime", default="")
    parser.add_argument("--prototype", default="")
    parser.add_argument("--multiplayer-backend", default="")
    parser.add_argument("--art-provider", default="")
    parser.add_argument("--mechanics-verified", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    context = {
        "engine": args.engine,
        "runtime": args.runtime,
        "prototype": args.prototype,
        "multiplayer_backend": args.multiplayer_backend,
        "art_provider": args.art_provider,
        "mechanics_verified": args.mechanics_verified,
    }
    routes = select_routes(load_manifest(MANIFEST_PATH), args.phase, context)
    if args.as_json:
        print(json.dumps(routes, ensure_ascii=False, indent=2))
        return 0

    print(f"Phase {args.phase} subskill route")
    if not routes:
        print("- orchestrator only")
        return 0
    for route in routes:
        print(f"- {route['skill']} [{route['mode']}]: {route['purpose']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
