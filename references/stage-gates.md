# Stage Gates

This reference defines the standard staged workflow for an AI-coded vibe game. Use it as the source of truth when deciding which phase should run next.

## Phase 0: Project Charter

Goal: create a bounded fixed-version target before implementation starts.

Required user inputs:

- Game engine or target runtime.
- One-sentence game fantasy.
- Target version name, such as `v0.1 playable prototype`.
- Platform and control assumptions.
- Existing repo, prototype, spreadsheet, or art reference locations.

AI outputs:

- Project status file.
- Fixed-version goal.
- Initial backlog with `must`, `should`, and `later`.
- First risk list.

Gate to advance:

- The user accepts the version target and the first playable outcome.

## Phase 1: Core Gameplay

Goal: define the game's smallest repeatable loop before expanding systems.

Required decisions:

- Player role and verb.
- Opposing force, pressure, timer, economy, or conflict.
- Round/session structure.
- Win, loss, partial success, and restart conditions.
- What makes one decision interesting.

AI outputs:

- Core loop statement.
- State list.
- Input/output map.
- First 3-5 testable gameplay moments.

Gate to advance:

- The user can describe what a player does every 10-30 seconds and why it is fun.

## Phase 2: First PRD

Goal: turn the vibe into a buildable first version.

Required sections:

- Vision and target feel.
- Core loop.
- System modules.
- Data model.
- Scene/UI map.
- Art/audio direction at placeholder level.
- Acceptance criteria.
- Out-of-scope list.

AI outputs:

- First PRD or PRD slice in the repo.
- Module queue ordered by dependency.
- Data files that should be user-editable.
- Validation plan.

Gate to advance:

- The user accepts the PRD and module order.

## Phase 3: White-Box MVP

Goal: make the game mechanically playable with plain or placeholder presentation.

Implementation focus:

- Scene flow.
- Core state machine.
- Minimal UI.
- Data loading.
- One complete gameplay session.
- Reset/retry loop.

AI outputs:

- Running build in the target engine.
- Basic validation notes.
- Known bug list.
- Updated status board.

Gate to advance:

- The user can play one complete session and verify the intended decision loop exists.

## Phase 4: Gameplay Module Insertion

Goal: add one meaningful module without destabilizing the core loop.

Use this phase for modules like card systems, pressure systems, character abilities, event decks, reward shops, negotiation moves, enemy patterns, or stage modifiers.

Required module contract:

- Module purpose.
- Trigger and lifecycle.
- Affected game states.
- Data schema and editable source files.
- UI and feedback requirements.
- Balance knobs.
- Test cases.
- Rollback or disable switch.

AI outputs:

- Micro-PRD for the module.
- Implementation plan.
- Code/data integration.
- Validation result.
- Before/after gameplay notes.

Gate to advance:

- The module works in-engine, its data can be edited safely, and the user accepts its feel.

## Phase 5: External Data Pipeline

Goal: let the user change balance, content, and module definitions outside the AI chat.

Preferred sources:

- `.xlsx` for design editing.
- `.csv`, `.json`, `.tres`, or engine-native resources for runtime import.
- A generation or validation script when manual copying is error-prone.

AI behavior:

- Ask the user to edit the source file.
- Read the changed file/diff after the user returns.
- Validate schema, IDs, required fields, ranges, and references.
- Generate runtime files or update engine resources.
- Report exactly what changed.

Gate to advance:

- The project has a repeatable path from external design edits to in-engine behavior.

## Phase 6: Art Direction and Batch Asset Specs

Goal: convert a mechanical prototype into a visually coherent first art pass.

Required decisions:

- Visual anchor image or HTML/mock prototype.
- Camera, composition, resolution, and safe areas.
- Character list.
- Background list.
- UI asset list.
- Animation states.
- Naming conventions and output folders.

AI outputs:

- Art requirements file or spreadsheet.
- Batch prompt framework.
- Asset manifest.
- One sample asset or sample integration before batch expansion.

Gate to advance:

- One representative asset style is accepted and the batch spec is stable.

## Phase 7: Art Integration and Iteration

Goal: make the game feel visually intentional in-engine.

Implementation focus:

- Import settings.
- Layer separation.
- Scene placement.
- Animation setup.
- UI skinning.
- Visual state feedback.
- Screenshot validation.

AI outputs:

- Integrated assets.
- Any helper scripts used for derivatives, slicing, atlases, or composites.
- Screenshot or manual QA notes.
- Updated asset manifest.

Gate to advance:

- The user accepts the in-engine look for the fixed version.

## Phase 8: Audio and Juice

Goal: make core actions legible and satisfying.

Implementation focus:

- SFX map for player actions, UI actions, rewards, failures, and transitions.
- Music loop or ambience.
- Volume groups.
- Animation/audio timing.
- Settings or mute behavior when appropriate.

Gate to advance:

- The user can play a full session with clear audiovisual feedback.

## Phase 9: Version Completion

Goal: freeze the fixed version and produce reusable evidence.

Required outputs:

- Build/package or runnable instructions.
- Regression checklist.
- Known issues.
- Final status board.
- Implementation log.
- Scripts copied or documented.
- Backlog for next version.

Gate to complete:

- The user accepts the fixed version as delivered, deferred items are recorded, and the next version has a clean starting point.
