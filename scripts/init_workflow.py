#!/usr/bin/env python3
"""Initialize a staged AI game-coding workflow status file."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


STATUS_TEMPLATE = """# AI Coding Game Workflow Status

## Version Target

- Version: {version}
- Engine/runtime: {engine}
- Current playable promise: {promise}
- Frozen scope: {scope}
- Deferred ideas: {deferred}

## Current Phase

- Phase: Phase 0 - Project Charter
- Gate: accept version target and first playable outcome
- Owner: user + AI
- Status: intake_needed
- Needed from user: confirm fixed version target, current source of truth, and next playable/visible result
- Next AI action: inspect the project and prepare Phase 1 core gameplay intake

## Active Delegation

- Child skill:
- Mode:
- Objective:
- Allowed scope:
- Required output:
- Return gate:

## Module Queue

| Order | Module | Purpose | State | Source of Truth | Gate |
|---:|---|---|---|---|---|
| 1 | Core loop | Establish one complete playable session | intake_needed | user brief + repo | Player can complete one session |

## Phase Log

| Date | Phase | Decision / Change | Validation | Next |
|---|---|---|---|---|
| {today} | Phase 0 | Workflow initialized | Status file created | Confirm version target |

## Risks

| Risk | Signal | Mitigation |
|---|---|---|
| Scope creep | New ideas enter active version without a gate | Keep fixed-version scope and defer extras |

## Backlog

| Idea | Reason Deferred | Revisit In |
|---|---|---|
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create docs/ai-coding-workflow/STATUS.md for a staged AI-coded game project."
    )
    parser.add_argument("--project", default=".", help="Project root. Defaults to current directory.")
    parser.add_argument("--version", default="v0.1", help="Fixed version target.")
    parser.add_argument("--engine", default="TBD", help="Game engine or runtime.")
    parser.add_argument("--promise", default="TBD", help="Current playable promise.")
    parser.add_argument("--scope", default="TBD", help="Frozen scope summary.")
    parser.add_argument("--deferred", default="TBD", help="Deferred ideas summary.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing STATUS.md.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = Path(args.project).expanduser().resolve()
    workflow_dir = project / "docs" / "ai-coding-workflow"
    status_path = workflow_dir / "STATUS.md"

    if status_path.exists() and not args.force:
        print(f"exists: {status_path}")
        print("Use --force to overwrite.")
        return 2

    workflow_dir.mkdir(parents=True, exist_ok=True)
    status_path.write_text(
        STATUS_TEMPLATE.format(
            version=args.version,
            engine=args.engine,
            promise=args.promise,
            scope=args.scope,
            deferred=args.deferred,
            today=date.today().isoformat(),
        ),
        encoding="utf-8",
        newline="\n",
    )
    print(f"created: {status_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
