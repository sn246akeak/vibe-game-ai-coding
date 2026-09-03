# Progress Format

Maintain a project-local progress board. Prefer `docs/ai-coding-workflow/STATUS.md`; if the project already has a diary or implementation-log folder, place it there and keep the filename obvious.

## Status Template

```markdown
# AI Coding Game Workflow Status

## Version Target

- Version:
- Engine/runtime:
- Current playable promise:
- Frozen scope:
- Deferred ideas:

## Current Phase

- Phase:
- Gate:
- Owner:
- Status:
- Needed from user:
- Next AI action:

## Module Queue

| Order | Module | Purpose | State | Source of Truth | Gate |
|---:|---|---|---|---|---|
| 1 | Core loop | Playable round | accepted | PRD | One full session works |
| 2 | Card system | Add tactical pressure choices | implementing | spreadsheet + module PRD | Cards editable and playable |

## Phase Log

| Date | Phase | Decision / Change | Validation | Next |
|---|---|---|---|---|

## Risks

| Risk | Signal | Mitigation |
|---|---|---|

## Backlog

| Idea | Reason Deferred | Revisit In |
|---|---|---|
```

## Module States

Use these states consistently:

- `not_started`: named but not shaped.
- `intake_needed`: waiting for user material.
- `designing`: AI is turning the idea into a contract.
- `ready_to_build`: scope and acceptance criteria are clear.
- `implementing`: code/data/assets are being changed.
- `verifying`: checks or playtest are running.
- `needs_user_review`: playable or visible result is ready for user judgment.
- `accepted`: gate passed.
- `deferred`: intentionally moved out of the fixed version.
- `blocked`: cannot progress without a concrete missing input or external issue.

## Turn Update Pattern

For substantial work, use this concise shape:

```text
当前阶段：{phase}
进度：{one-line status}
我刚完成：{completed work}
正在验证：{test/build/manual check}
下一步：{next gate or user review}
```

## Completion Rule

A module is not complete until all are true:

- The implementation exists in the repo.
- The data/source files are documented or discoverable.
- The smallest meaningful validation has run.
- The user-facing behavior or asset result can be inspected.
- The status file records the outcome and next step.
