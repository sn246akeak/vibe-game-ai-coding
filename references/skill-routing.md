# Specialist Routing

Read this only for the current specialist slice. `subskills.json` is the authoritative route/source manifest; `subskills.lock.json` records file-content digests fetched from its immutable commits. Do not maintain a second routing table.

## Resolve Before Use

```bash
python scripts/route_subskills.py --workflow "GAME/docs/ai-coding-workflow/workflow.json" --project "GAME"
python scripts/route_subskills.py --phase 4 --engine "Godot 4.4" --mechanics-verified
python scripts/route_subskills.py --phase 7 --engine threejs --plan-only
python scripts/check_subskills.py
```

Prefer workflow-driven resolution. The explicit `--mechanics-verified` flag is an operator assertion: use it only after observing functional checks. `--plan-only` lists candidates without checking availability and must not be treated as permission to invoke them.

The resolver returns `verified`, `missing`, `unverified` (no matching lock source), or `modified` (content differs). A selected unresolved route exits 2. Inventory checks all dependencies but only unresolved core entries affect its exit status; it does not prove that a particular phase is ready.

A content match proves only that the installed files match the pinned snapshot. It does not verify tool availability, credentials, engine/API compatibility, upstream trust or licensing. Inspect the relevant child and actual project version before use. Generated changes inside an installed skill can make its digest differ; inspect them rather than overwriting user files.

## Boundaries

- Design theory advises mechanics/PRD; the parent retains scope and user acceptance.
- Godot work uses the project's actual engine version. A Godot Web export is not an HTML/JavaScript source project.
- Web prototypes use `develop-web-game`; its own `progress.md` does not replace workflow state.
- Engine-neutral UI uses `game-ui-ux`; Three.js Phase 7 UI replaces it with `threejs-game-ui-designer`.
- `game-feel` requires current functional evidence. Recheck after polish and preserve game rules.
- Higgsfield is selected only when the user chooses that art/audio provider. It does not own game code or deployment.
- `multiplayer-game` applies only to an accepted RivetKit backend. Native Godot networking stays with the Godot adapter.

Use `subskill-contract.md` for bounded application. The same agent may apply the skill; do not invent a child process, task or tool. Returned artifacts do not accept a module.

## Installation and Maintenance

Dependencies are installed separately, not redistributed here. Use the built-in skill installer with the exact `repo`, `path` and `ref` from the manifest, then rerun resolution. Do not overwrite an existing customized skill. When installation is unavailable, explain the missing specialist and agree on a parent-only fallback recorded with `workflow.py note`; do not pretend delegation succeeded.

Some references are archival: the Web skill path was removed later, and the selected Higgsfield/Rivet skill revisions may differ from their current products. Pinned snapshots support reproducibility, not a promise of current API compatibility. Check official tool documentation when using those providers.

Maintainers can run `python scripts/pin_subskills.py` after intentionally reviewing a manifest update. It downloads ZIP snapshots, hashes them without extracting or executing code, and replaces the lock file. It does not install skills. Review the source/digest diff, rerun tests and assess applicable upstream licenses. A lock refresh alone is not a security audit.
