from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path
from typing import Any


def normalize_engine(value: str) -> str:
    value = value.strip().lower()
    if re.match(r"^godot(?:\b|\d)", value):
        return "godot"
    if value in {"three.js", "threejs", "three"}:
        return "threejs"
    if value in {"phaser", "pixi", "pixijs", "html5", "js", "typescript"}:
        return "web"
    return value


def tree_digest(files: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    for name, content in sorted(files.items()):
        digest.update(name.encode("utf-8") + b"\0")
        digest.update(hashlib.sha256(content).digest())
    return digest.hexdigest()


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported subskill manifest schema")
    names = [item["name"] for item in manifest["dependencies"]]
    if len(names) != len(set(names)):
        raise ValueError("duplicate dependency names")
    for route in manifest.get("routes", []):
        if route["skill"] not in names:
            raise ValueError("route references unknown dependency")
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
    context = dict(context, engine=normalize_engine(str(context.get("engine", ""))))
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


def resolve_routes(manifest: dict[str, Any], phase: int, context: dict[str, Any],
                   skills_root: Path, lock: dict[str, Any]) -> list[dict[str, Any]]:
    dependencies = {item["name"]: item for item in manifest["dependencies"]}
    result = []
    for route in select_routes(manifest, phase, context):
        name = route["skill"]
        folder = skills_root / name
        entry = lock.get("dependencies", {}).get(name, {})
        status = "missing"
        if (folder / "SKILL.md").is_file():
            status = "unverified"
            if entry.get("source") == dependencies[name]["source"]:
                files = {p.relative_to(folder).as_posix(): p.read_bytes()
                         for p in folder.rglob("*") if p.is_file()
                         and not any(part in {".git", "__pycache__"} for part in p.relative_to(folder).parts)
                         and p.suffix != ".pyc"}
                status = "verified" if tree_digest(files) == entry.get("sha256") else "modified"
        result.append(dict(route, status=status, path=str(folder / "SKILL.md")))
    return result
