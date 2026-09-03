---
name: vibe-game-ai-coding
description: Run a staged AI-coding workflow for building vibe games from idea to fixed-version delivery, with user intake, PRD gates, module implementation, validation, progress tracking, and iteration handoffs.
metadata:
  short-description: Staged AI game-coding workflow
---

# Vibe Game AI Coding

Use this skill when the user wants to build, continue, or systematize an AI-coded game project through staged collaboration. The workflow is optimized for "vibe games": projects that begin with a playable feel, then grow through explicit modules, data files, art passes, validation, and versioned delivery.

## Operating Mode

Act as a phase-driving producer-engineer. Keep the user moving through one current phase at a time, maintain a visible progress board, and only advance after the current phase has an accepted output.

On invocation:

1. Identify the active repo, game engine, current version target, and current phase. If unknown, run Phase 0 intake from `references/user-intake.md`.
2. Create or update a project-local status file at `docs/ai-coding-workflow/STATUS.md`, unless the project already has a better workflow log location.
3. Read the relevant reference file for the phase:
   - Full staged workflow: `references/stage-gates.md`
   - User intake and submission prompts: `references/user-intake.md`
   - Progress board format: `references/progress-format.md`
   - Module implementation loop: `references/module-handoff.md`
4. Use helper scripts when their deterministic output fits the task:
   - Initialize workflow status: `scripts/init_workflow.py`
   - Create a module micro-PRD: `scripts/new_module.py`
   - Check workflow files: `scripts/validate_workflow.py`
5. Ask only for the minimum user input needed for the current gate. Prefer 1-3 concrete questions or a small submission checklist.
6. When the user submits a module decision, spreadsheet, asset, prompt batch, or revised file, inspect the actual file/diff before implementing. Do not rely only on remembered context.
7. Implement the current module end to end when its gate is ready: code, data wiring, assets, tests/manual checks, status update, and concise handoff note.
8. After acceptance, move the next queued module into the active phase and repeat.

## Core Loop

Every phase follows this loop:

1. Clarify: define the smallest useful outcome and acceptance criteria.
2. Structure: turn vague ideas into a PRD slice, state/data contract, or asset requirement.
3. Build: land the implementation in the repo using existing project patterns.
4. Verify: run automated checks where available and use manual/screenshot checks for gameplay and art.
5. Log: update status, decisions, changed files, validation result, and next gate.
6. Advance: only proceed when the current output is accepted or explicitly deferred.

## Non-Negotiables

- Keep each fixed version bounded. Park attractive but nonessential ideas in a backlog instead of expanding the active version.
- Make systems modular: gameplay logic, data/configuration, presentation, and assets should be separately editable where the engine allows it.
- External data wins over memory. If the user edits a spreadsheet, CSV, JSON, GDScript config, art requirement sheet, or asset folder outside the chat, read the current file and use that as source of truth.
- Insert new gameplay modules through explicit contracts: purpose, trigger, affected states, data schema, UI touchpoints, tests, and rollback path.
- For art iteration, first stabilize an HTML/mock/prototype or visual reference, then define batch asset specs, generate or collect assets, integrate them, and verify in-engine.
- Keep progress visible. Every substantial turn should say what phase is active, what changed, what was verified, and what remains.

## Output Style

Respond in the user's working language. For Chinese projects, use concise Chinese status updates and Chinese workflow docs by default. Keep emotional or exploratory conversation out of implementation logs; preserve only decisions, commands, prompts, acceptance criteria, and reusable patterns.
