from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported subskill manifest schema")
    return manifest


def _matches(expected: dict[str, list[Any]], context: dict[str, Any]) -> bool:
    for key, allowed_values in expected.items():
        actual = context.get(key)
        if isinstance(actual, str):
            actual = actual.lower()
        normalized = [value.lower() if isinstance(value, str) else value for value in allowed_values]
        if actual not in normalized:
            return False
    return True


def select_routes(
    manifest: dict[str, Any], phase: int, context: dict[str, Any]
) -> list[dict[str, Any]]:
    selected = [
        route
        for route in manifest.get("routes", [])
        if route.get("phase") == phase and _matches(route.get("when", {}), context)
    ]
    replaced = {
        name
        for route in selected
        for name in route.get("replaces", [])
    }
    return [route for route in selected if route.get("skill") not in replaced]


def inspect_dependencies(
    manifest: dict[str, Any], skills_root: Path
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for dependency in manifest.get("dependencies", []):
        skill_path = skills_root / dependency["name"] / "SKILL.md"
        result.append(
            {
                "name": dependency["name"],
                "tier": dependency.get("tier", "optional"),
                "installed": skill_path.is_file(),
                "path": str(skill_path),
                "source": dependency.get("source", {}),
                "note": dependency.get("note"),
            }
        )
    return result
