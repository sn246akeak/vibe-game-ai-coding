#!/usr/bin/env python3
"""Validate the presence and rough shape of staged AI game-coding workflow files."""

from __future__ import annotations

import argparse
from pathlib import Path


STATUS_SECTIONS = [
    "# AI Coding Game Workflow Status",
    "## Version Target",
    "## Current Phase",
    "## Module Queue",
    "## Phase Log",
    "## Risks",
    "## Backlog",
]

MODULE_SECTIONS = [
    "# Module Handoff:",
    "## Metadata",
    "## Objective",
    "## Player-Facing Behavior",
    "## Core Loop Touchpoint",
    "## Data Schema",
    "## Acceptance Criteria",
    "## Validation",
    "## Review Question",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check docs/ai-coding-workflow/STATUS.md and module handoff files."
    )
    parser.add_argument("--project", default=".", help="Project root. Defaults to current directory.")
    return parser.parse_args()


def missing_sections(text: str, sections: list[str]) -> list[str]:
    return [section for section in sections if section not in text]


def main() -> int:
    args = parse_args()
    project = Path(args.project).expanduser().resolve()
    workflow_dir = project / "docs" / "ai-coding-workflow"
    status_path = workflow_dir / "STATUS.md"
    failures: list[str] = []

    if not status_path.exists():
        failures.append(f"missing status file: {status_path}")
    else:
        text = status_path.read_text(encoding="utf-8")
        for section in missing_sections(text, STATUS_SECTIONS):
            failures.append(f"STATUS.md missing section: {section}")

    modules_dir = workflow_dir / "modules"
    module_paths = sorted(modules_dir.glob("*.md")) if modules_dir.exists() else []
    for module_path in module_paths:
        text = module_path.read_text(encoding="utf-8")
        for section in missing_sections(text, MODULE_SECTIONS):
            failures.append(f"{module_path.name} missing section: {section}")

    if failures:
        print("workflow validation failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("workflow validation passed")
    print(f"status: {status_path}")
    print(f"modules: {len(module_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
