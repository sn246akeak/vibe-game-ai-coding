#!/usr/bin/env python3
"""Fetch pinned source archives and record content hashes; never execute their code."""
import argparse
import io
import json
import re
import urllib.request
import zipfile
from pathlib import Path

from subskill_router import load_manifest, tree_digest

ROOT = Path(__file__).resolve().parents[1]


def build_lock(manifest):
    archives = {}
    result = {"schema_version": 1, "dependencies": {}}
    for dependency in manifest["dependencies"]:
        source = dependency["source"]
        repo, ref = source["repo"], source["ref"]
        if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo) or not re.fullmatch(r"[a-f0-9]{40}", ref):
            raise ValueError("expected a GitHub repository and immutable full commit SHA")
        key = (repo, ref)
        if key not in archives:
            request = urllib.request.Request(f"https://codeload.github.com/{repo}/zip/{ref}",
                                             headers={"User-Agent": "vibe-game-ai-coding"})
            with urllib.request.urlopen(request, timeout=60) as response:
                archives[key] = response.read()
        with zipfile.ZipFile(io.BytesIO(archives[key])) as archive:
            root = archive.namelist()[0].split("/")[0] + "/"
            prefix = root + source["path"].strip("/") + "/"
            files = {item.filename[len(prefix):]: archive.read(item) for item in archive.infolist()
                     if item.filename.startswith(prefix) and not item.is_dir()}
            if "SKILL.md" not in files:
                raise ValueError(f"missing SKILL.md in pinned source: {dependency['name']}")
            licenses = [name[len(root):] for name in archive.namelist()
                        if name.startswith(root) and "/" not in name[len(root):]
                        and name[len(root):].upper().startswith(("LICENSE", "COPYING"))]
            result["dependencies"][dependency["name"]] = {
                "source": source, "sha256": tree_digest(files), "files": len(files),
                "license_files": licenses,
                "license_review": "not assessed; upstream content is not redistributed"}
            print(f"pinned {dependency['name']}: {len(files)} files")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "references" / "subskills.lock.json")
    args = parser.parse_args()
    result = build_lock(load_manifest(ROOT / "references" / "subskills.json"))
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
