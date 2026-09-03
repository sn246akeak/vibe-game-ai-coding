#!/usr/bin/env python3
"""Create a micro-PRD handoff document for one game module."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    return value.strip("-") or "module"


MODULE_TEMPLATE = """# Module Handoff: {name}

## Metadata

- Created: {today}
- State: intake_needed
- Owner: user + AI
- Source of Truth: {source}

## Objective

{purpose}

## Player-Facing Behavior

TBD

## Core Loop Touchpoint

TBD

## States Touched

- TBD

## Data Schema

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | string | yes | Stable module/content ID |

## UI / Scene Touchpoints

- TBD

## Feedback Requirements

- Visual: TBD
- Audio: TBD
- Animation: TBD

## Acceptance Criteria

- {gate}

## Validation

- Automated: TBD
- Manual: TBD

## Implementation Notes

- Keep this module independently disableable or deferrable where practical.
- Read external files or diffs before implementation if the user updates data outside AI.

## Review Question

Should this module move to `accepted`, or should it stay in iteration?
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create docs/ai-coding-workflow/modules/<module>.md as a module micro-PRD."
    )
    parser.add_argument("name", help="Module name, such as 'card system'.")
    parser.add_argument("--project", default=".", help="Project root. Defaults to current directory.")
    parser.add_argument("--purpose", default="TBD", help="Why this module exists.")
    parser.add_argument("--source", default="TBD", help="Source of truth, such as cards.xlsx or assets/art_manifest.csv.")
    parser.add_argument("--gate", default="Module works in-engine and is accepted by the user.", help="Acceptance gate.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing module file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = Path(args.project).expanduser().resolve()
    modules_dir = project / "docs" / "ai-coding-workflow" / "modules"
    module_path = modules_dir / f"{slugify(args.name)}.md"

    if module_path.exists() and not args.force:
        print(f"exists: {module_path}")
        print("Use --force to overwrite.")
        return 2

    modules_dir.mkdir(parents=True, exist_ok=True)
    module_path.write_text(
        MODULE_TEMPLATE.format(
            name=args.name,
            today=date.today().isoformat(),
            source=args.source,
            purpose=args.purpose,
            gate=args.gate,
        ),
        encoding="utf-8",
        newline="\n",
    )
    print(f"created: {module_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
