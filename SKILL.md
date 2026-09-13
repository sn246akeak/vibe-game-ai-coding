---
name: vibe-game-ai-coding
description: Guide a game project from gameplay discovery through an approved PRD, one-module-at-a-time implementation, user acceptance, and fixed-version delivery. Use for an end-to-end staged game workflow or resuming its progress, not for an isolated game bug or asset request.
metadata:
  short-description: Staged AI game-coding workflow
  version: "1.0.0"
---

# Vibe Game AI Coding

Act as the producer-engineer for a bounded game version. Guide the user, co-design missing materials, implement the current module, present evidence, and advance after the user's actual acceptance. This skill is an AI-guided workflow, not a background agent launcher or a game engine.

## Start or Resume

1. Inspect the project and its actual engine version, documents, data and working tree. Discover existing progress before initializing anything.
2. Read [workflow-runtime.md](references/workflow-runtime.md). Use `scripts/workflow.py` for persistent state in the project. `workflow.json` is authoritative; `STATUS.md` is generated. Preserve legacy logs and use a new directory for migration.
3. Identify the fixed version, accepted scope, current module and next gate. Read [user-intake.md](references/user-intake.md) for missing inputs and [stage-gates.md](references/stage-gates.md) for phase outputs. Ask only 1-3 current questions, not the whole project's questionnaire.
4. Give a short progress update in the user's language: current module/state, accepted versus deferred counts, latest evidence, next needed decision. A blocker stays in the current state with a concrete note; it is not acceptance.

## Module Loop

Follow [module-handoff.md](references/module-handoff.md): intake, co-design a micro-PRD, get design approval, implement, verify, user review, then accept or revise. Documentation phases produce reviewed documents; implementation phases must produce runnable behavior and real checks.

- Freeze objective, triggers, states, data schema, UI touchpoints, allowed changes, non-goals and acceptance checks before implementation. Use `scripts/new_module.py` for a document scaffold if useful, then fill it from actual project evidence.
- Register version modules with `workflow.py add`; use stable IDs and dependencies. This command registers scope, not implementation. New ideas go to backlog unless the user agrees to include them.
- For a large inserted system, split independently acceptable slices such as data contract, minimum playable loop, full effects/UI and balance. Do not silently equate one big checklist with phased delivery.
- Record actual user decisions with `--decision`, never invent approval. `ready_to_build` needs an approved spec file; `needs_user_review` needs validation artifacts; `accepted` needs the user's decision on those artifacts.
- If the user changes inputs, reread the actual files and revise the current module. For previously accepted work, add an explicit revision module instead of rewriting its history. A delivered version gets a new workflow directory.
- Automation validates state, file existence and hashes, not whether a written claim is true. Run the relevant engine/build/playtest checks and inspect their results before recording success.

## Specialists

Read [skill-routing.md](references/skill-routing.md) only when specialist work is needed. Resolve the current module with `scripts/route_subskills.py`; use the manifest and content lock instead of remembered mappings. A candidate is not a verified dependency or permission to use a paid service.

Before applying a selected skill, read its `SKILL.md` and necessary references. Record a bounded [subskill contract](references/subskill-contract.md) with `workflow.py delegate`. Use the same agent unless actual delegation tools are available and appropriate. The CLI records the contract; it does not launch another agent.

The parent retains version scope, state and acceptance. Missing or modified dependencies require explicit remediation or a documented parent-only fallback, not a fictitious successful invocation. Preserve user customizations. Never auto-run upstream bootstraps, change providers, publish or incur charges merely because a child suggests it.

## Conditional Workflows

- External tables/config: [data-workflow.md](references/data-workflow.md). Stable IDs, editable-field allowlist, actual before/after diff, validation, deterministic runtime export, in-engine check. Source files outrank conversational memory.
- Art/animation/audio: [art-workflow.md](references/art-workflow.md). Preserve playable layout, approve an in-engine sample, freeze shared specs, batch by manifest, retain originals, revise selected IDs, verify integration.
- Progress and resumption: [progress-format.md](references/progress-format.md). Record decisions and evidence without emotional conversation or invented historical quotes.

## Delivery

Close only when all fixed-version modules are accepted or explicitly deferred and the delivery gate is accepted. Record runnable instructions, regression evidence, limitations, reusable script commands and next-version backlog. Export the implementation log with `workflow.py export`; keep source Markdown when another format is requested. Do not claim an exported status log automatically contains a complete historical SOP: enrich the diary with the productive prompts, design decisions and verified scripts actually used.
