# Workflow Runtime (v1)

The Python 3.10+ standard-library CLI owns state transitions, file snapshots and a generated progress board. The AI owns actual work and evidence interpretation; the user owns design approval and acceptance. No command launches a model, engine, paid service or background task.

## Project Files

- `docs/ai-coding-workflow/workflow.json`: state, ordered modules, snapshots, delegation and decision history. Mutate through CLI; do not hand-edit to bypass gates.
- `STATUS.md`: generated projection, not an independent source of truth.
- `modules/`, `evidence/`, `BACKLOG.md`: create as needed. Each check report records command/environment, observed result and artifact paths. Keep reports immutable after submission for review.
- `IMPLEMENTATION_LOG.md`: exclusive-create export; existing logs are preserved. Additional narrative SOPs can link to this evidence.

Run helpers from the installed skill directory, targeting the game with `--project`. In commands below `GAME` is the real absolute project path. Global arguments precede the subcommand. On resume inspect JSON and actual files; do not initialize again.

```bash
python scripts/workflow.py --project "GAME" init --version "v0.1" --engine "Godot 4.4"
python scripts/workflow.py --project "GAME" status
python scripts/workflow.py --project "GAME" validate
```

Use the actual engine version, not the example. Initial queue: charter, gameplay, PRD, playable MVP, art sample, art integration, audio/feedback, delivery. Additional gameplay/data modules are added through `add`; not every game needs the same modules.

If a legacy `STATUS.md` already exists, initialization refuses to overwrite it. Select `--directory docs/ai-coding-workflow/v1`, reconcile prior evidence with the user, and register remaining scope without manufacturing historical acceptance. Use this same directory argument on every subsequent call.

## Current Module Lifecycle

```text
intake_needed -> designing -> ready_to_build -> implementing
             -> verifying -> needs_user_review -> accepted
```

Only the first unfinished module can advance. Here is the charter gate as an example, with existing project-relative spec/check files. Substitute the user's real words for example decisions; do not execute the whole sequence before doing its work.

```bash
python scripts/workflow.py --project "GAME" transition phase-0 --to designing
python scripts/workflow.py --project "GAME" transition phase-0 --to ready_to_build --evidence docs/charter.md --decision "User approved the stated version scope"
python scripts/workflow.py --project "GAME" transition phase-0 --to implementing
python scripts/workflow.py --project "GAME" transition phase-0 --to verifying
python scripts/workflow.py --project "GAME" verify phase-0 --evidence docs/evidence/charter-review.md
python scripts/workflow.py --project "GAME" transition phase-0 --to needs_user_review
python scripts/workflow.py --project "GAME" transition phase-0 --to accepted --decision "User accepted the charter after review"
```

For early design phases, implementing means completing the agreed document, not prematurely writing game code. Approval evidence is snapshotted as an input. Source changes block subsequent progress until `revise` clears outdated snapshots and the AI obtains renewed design approval. Verification artifacts are hashed; a changed review artifact blocks acceptance.

`verify` can record functional-check evidence while still verifying so the feedback specialist becomes eligible. Record fresh checks after its changes. Hashes do not detect unlisted code changes; include a commit/diff identifier in the report and rerun checks after any implementation change.

```bash
python scripts/workflow.py --project "GAME" revise phase-0 --note "Source changed; reread and redesign"
python scripts/workflow.py --project "GAME" add cards --name "Card system" --phase 4 --source data/cards.csv --depends-on phase-3 --decision "User included cards in v0.1"
python scripts/workflow.py --project "GAME" context art_provider higgsfield --decision "User selected this provider"
```

`add` inserts before later-phase unfinished work without interrupting a started module. Dependencies must precede the new module and be accepted before implementation. To put data before cards, register the data module first, then register cards with that dependency. Keep delivery last. Scope cannot expand after delivery starts; finish that version and plan the next.

Context changes require intake/designing; revise first otherwise. Core gates (0/1/2/3/9) cannot be deferred. Optional current modules can use `defer MODULE --decision "actual user decision"`. New work on an accepted module needs a revision module with a new ID and dependency; do not erase past acceptance. A finished version requires a new directory.

## Delegation and Finish

```bash
python scripts/route_subskills.py --workflow "GAME/docs/ai-coding-workflow/workflow.json" --project "GAME"
python scripts/workflow.py --project "GAME" delegate cards --contract docs/contracts/cards.json
python scripts/workflow.py --project "GAME" export
```

The contract is project-relative JSON; see `subskill-contract.md`. Delegation requires an eligible, content-verified local skill. The parent checks returned artifacts, records new evidence, then clears delegation by submitting for review. Acceptance remains the same user gate.

Mutations use an exclusive lock to reject concurrent writes. After a crash, inspect state and ensure no writer is alive before removing a stale `.workflow.lock`. The generated board refreshes on the next successful mutation; JSON remains authoritative. Export never overwrites an earlier log.

Legacy `init_workflow.py` and `validate_workflow.py` manage the earlier Markdown format only; do not mix their writes with v1 state. `new_module.py` is a document scaffold, not a queue mutation.
