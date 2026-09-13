# Vibe Game AI Coding

English | [中文](README.md)

A Codex skill for taking a game from a gameplay idea to a bounded, accepted version. AI guides intake and co-design, implements one module, presents validation evidence, and waits for your acceptance before starting the next cycle.

**v1.0.0 combines workflow instructions, an executable state machine, content diffs, and specialist routing.** It is not an unattended game factory and does not bundle a game engine or paid asset service.

## Install

Requires Codex and Python 3.10+. Core helpers use only the Python standard library. Ask Codex:

> Use skill-installer to install vibe-game-ai-coding from the root of sn246akeak/vibe-game-ai-coding.

Or clone it into your Codex skills directory. PowerShell example:

```powershell
$skills = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills" } else { Join-Path $HOME ".codex" "skills" }
git clone https://github.com/sn246akeak/vibe-game-ai-coding.git (Join-Path $skills "vibe-game-ai-coding")
```

Inspect local changes before updating an existing directory. Start a new Codex session after installation so the skill can be discovered. Prepare engine, browser-test and asset-generation tools separately as needed.

## Use

Open your game project and say:

```text
Run $vibe-game-ai-coding. My target is v0.1, a game about ...
Inspect the existing project first. Guide me through only the current module's
missing materials. Help me design them, obtain my design approval, implement
the module and show verifiable results. Move on only after my acceptance.
```

To resume:

```text
Continue $vibe-game-ai-coding. Read the existing workflow.json and actual files.
Show the current module, accepted progress, blockers and the next input you need.
Do not rebuild progress or infer file changes from conversational memory.
```

You do not need to run every helper yourself. AI executes commands and maintains evidence; you decide direction, approve design, playtest and accept outcomes. Intake is incremental, not one large up-front questionnaire.

## Process

| Phase | Joint decisions | Accepted output |
|---|---|---|
| 0 Charter | Platform, engine, experience, scope | Bounded version and initial queue |
| 1 Gameplay | Actions, pressure, choices, outcomes, restart | Core loop and testable moments |
| 2 First PRD | Systems, data, scenes, non-goals | Approved specification and module order |
| 3 White-box MVP | Smallest playable promise | One complete playable session |
| 4 Gameplay modules | Triggers, states, rules, UI, checks | Individually accepted playable slices |
| 5 External data | Stable IDs, editable fields, import rules | Designer edit to runtime behavior |
| 6 Art sample | Style, composition, shared prompt/spec | Approved in-engine sample and manifest |
| 7 Art integration | Batches, layers, animation, revision scope | Visual and interaction evidence |
| 8 Audio/feedback | Events, timing, gain, motion | Full-session audiovisual checks |
| 9 Delivery | Regression, issues, next-version scope | Runnable version and implementation log |

Phases classify work, not a single inflexible pass. Gameplay/data modules may repeat, and a prerequisite pipeline can precede gameplay integration. Optional work may be explicitly deferred. Core gameplay, PRD, playable-session and delivery gates cannot be skipped.

Every module follows intake → co-design → design approval → implementation → verification → user review → acceptance or revision. Large systems can become separately accepted data-contract, minimum-loop, effects/UI and balancing modules. Specialist completion never substitutes for user acceptance.

## Files and Executable Helpers

Project state defaults to `docs/ai-coding-workflow/`. `workflow.json` is authoritative; `STATUS.md` is generated. Create module specifications, evidence and backlog as needed. `IMPLEMENTATION_LOG.md` is an exclusive-create export, not an automatic reconstruction of historical conversations.

| Script | Purpose |
|---|---|
| `workflow.py` | Initialize, queue, check dependencies, transition, revise, defer, note, delegate, accept and export |
| `diff_content.py` | Stable-ID CSV/JSON diff with editable-field allowlist and separate additions/deletions |
| `route_subskills.py` | Select phase/context specialists and verify installed content |
| `check_subskills.py` | Inventory installed specialists and content status |
| `pin_subskills.py` | Maintainer utility to lock immutable upstream content without installing/executing it |
| `new_module.py` | Scaffold a micro-PRD, without changing workflow state |
| `init_workflow.py`, `validate_workflow.py` | Legacy Markdown compatibility; do not mix with v1 state |

Run from the installed skill directory; replace `GAME` with the absolute project path:

```bash
python scripts/workflow.py --project "GAME" init --version v0.1 --engine godot
python scripts/workflow.py --project "GAME" status
python scripts/workflow.py --project "GAME" validate
python scripts/route_subskills.py --workflow "GAME/docs/ai-coding-workflow/workflow.json" --project "GAME"
```

See [runtime commands](references/workflow-runtime.md). Existing legacy logs are preserved: choose a new `--directory` for v1. Delivered versions start their successors in a new directory.

## External Data and Art

Example request: "I changed cost and description in this table. Reread the actual file, compare by ID, synchronize only those columns, report additions/deletions separately, then verify in-game."

Frozen input hashes invalidate stale approval after a source change. The AI must reread, revise and obtain renewed approval. The diff helper does not modify runtime files or parse XLSX. Project adapters own XLSX/formula handling, business validation and deterministic runtime import. See [data workflow](references/data-workflow.md).

Art begins with a playable HTML/white-box reference. Approve an in-engine sample before producing characters, backgrounds, UI, animation and audio under shared specifications and a manifest. Keep originals and derivatives separately; revise selected IDs. See [art workflow](references/art-workflow.md). This repository does not misrepresent project-specific atlas, background-removal or engine-import scripts as universal tools.

## Specialist Integration

Design, UI and feedback use `game-design-theory`, `game-ui-ux` and `game-feel`. Engine/prototype adapters include `godot` and `develop-web-game`. Higgsfield, Three.js UI and RivetKit are conditional, not universal dependencies.

Sources and exact revisions live in [subskills.json](references/subskills.json); content digests live in [subskills.lock.json](references/subskills.lock.json). Upstream skills are installed separately, not redistributed. Ask the built-in skill installer to use the exact repo/path/ref for currently needed dependencies, then resolve the actual phase. Do not overwrite customized installations.

`verified` means installed content matches a snapshot, not that tooling, credentials, APIs, security or licensing are validated. Some paths use archival revisions; check applicable official documentation before runtime use. Missing/modified dependencies need remediation or an explicit parent-only fallback, never fabricated delegation. See [routing boundaries](references/skill-routing.md) and [contracts](references/subskill-contract.md).

## Validation and Limits

```bash
python -m unittest discover -s tests -v
python scripts/check_subskills.py
```

Tests cover the full state cycle, cross-process resume, gates, changed inputs/evidence, dependency insertion, delegation, legacy preservation and data diffs. They use simulated approvals and temporary files, not a real end-to-end game-production acceptance test.

The state machine cannot prove a written test claim is true or authenticate user approval text. AI must use observed results and actual user decisions, and rerun checks after implementation changes. This skill does not automatically publish repositories, deploy games, purchase services, sign into accounts or launch background agents.
