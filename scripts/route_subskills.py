#!/usr/bin/env python3
"""Select delegated game-development skills for one workflow phase."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from subskill_router import load_manifest, select_routes, resolve_routes


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "references" / "subskills.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", type=int, choices=range(10))
    parser.add_argument("--workflow", type=Path, help="Read phase and context from workflow.json")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project root for workflow evidence paths")
    parser.add_argument("--plan-only", action="store_true", help="Show candidates without resolving installed dependencies")
    parser.add_argument("--skills-root", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills")
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
    if args.workflow:
        from workflow import current, check_state, check_sources, check_evidence
        state = json.loads(args.workflow.read_text(encoding="utf-8"))
        check_state(state)
        active = current(state)
        if active is None:
            print("Version delivered; no active route")
            return 0
        args.phase = active["phase"]
        if not args.plan_only:
            try:
                check_sources(args.project.resolve(), active)
                check_evidence(args.project.resolve(), active)
            except (OSError, ValueError) as error:
                print(f"routing error: {error}")
                return 2
        context = dict(state["context"], mechanics_verified=bool(active["evidence"]))
    if args.phase is None:
        print("Provide --phase or --workflow")
        return 2
    manifest = load_manifest(MANIFEST_PATH)
    if args.plan_only:
        routes = select_routes(manifest, args.phase, context)
    else:
        lock_path = MANIFEST_PATH.with_name("subskills.lock.json")
        lock = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.exists() else {}
        routes = resolve_routes(manifest, args.phase, context, args.skills_root, lock)
    failed = any(r.get("status", "verified") != "verified" for r in routes)
    if args.as_json:
        print(json.dumps(routes, ensure_ascii=False, indent=2))
        return 2 if failed else 0

    print(f"Phase {args.phase} subskill route")
    if not routes:
        print("- orchestrator only")
        return 0
    for route in routes:
        print(f"- {route['skill']} [{route.get('status', 'candidate')}; {route['mode']}]: {route['purpose']}")
    return 2 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
