# Subskill Routing

Use this reference after the current phase and project context are known. The machine-readable source of truth is `subskills.json`; use `scripts/route_subskills.py` instead of reconstructing the route from memory.

## Authority

`vibe-game-ai-coding` remains the orchestrator. It owns the fixed-version scope, current phase, user intake, progress board, acceptance gate, and decision to advance. A delegated skill owns only the bounded specialist task named in its delegation contract.

A child skill must not:

- Expand the fixed-version scope.
- Replace the accepted PRD or module contract without returning a proposal.
- Start the next phase or module.
- Treat its own completion checklist as user acceptance.
- Modify files outside the allowed scope unless the orchestrator explicitly widens it.

## Standard Routes

| Phase | Default specialists | Conditional specialists |
|---:|---|---|
| 0 | Orchestrator only | None |
| 1 | `game-design-theory` | `develop-web-game` for a Web prototype |
| 2 | `game-design-theory`, `game-ui-ux` | `godot` for Godot; `multiplayer-game` only for RivetKit |
| 3 | `game-ui-ux` | `godot` for Godot; `develop-web-game` for HTML/JavaScript/Three.js source |
| 4 | `game-design-theory` | Engine adapter; `game-feel` only after mechanics pass; RivetKit when selected |
| 5 | Orchestrator data pipeline | `godot` for Godot resource integration |
| 6 | Orchestrator art specification | `higgsfield-game-generation` when selected as asset provider |
| 7 | `game-ui-ux` | `godot`; Higgsfield revisions; Three.js UI replaces generic UI |
| 8 | `game-feel` | Higgsfield audio assets |
| 9 | Orchestrator release gate | Engine validation; browser source validation; RivetKit validation when selected |

## Boundaries

- `game-design-theory` reviews design intent and trade-offs. It does not implement code or decide acceptance.
- `godot` is the default engine adapter for Godot projects. Read the project's `project.godot` before using version-specific advice.
- `develop-web-game` owns the deterministic HTML/JavaScript operation loop. Its `progress.md` supplements, but does not replace, the workflow `STATUS.md`.
- `game-ui-ux` owns engine-neutral layout, focus, scaling, screen flow, and state wiring.
- `game-feel` runs only after the underlying mechanic works. It cannot change game rules to make feedback easier.
- `higgsfield-game-generation` is assets-only. It may create manifests, style formulas, visual assets, animation, and audio; it does not own game code or deployment.
- `threejs-game-ui-designer` replaces `game-ui-ux` during the Three.js-specific Phase 7 UI pass.
- `multiplayer-game` is RivetKit-specific. Native Godot multiplayer stays with the Godot adapter unless the user explicitly selects RivetKit.

## Routing Command

```bash
python scripts/route_subskills.py --phase 4 --engine godot --mechanics-verified
```

Provide only context already accepted in the current version. A route is a recommendation for the current phase, not permission to install tools, authenticate services, deploy, publish, or spend credits.
