# Subskill Delegation Contract

Use this contract before handing a bounded task to a specialist skill. Record the active delegation in the project `STATUS.md`.

```yaml
phase: Phase 4
module: card-system
delegate: game-feel
mode: module-polish
objective: Make card play and resolution readable and satisfying.
input_source:
  - docs/ai-coding-workflow/modules/card-system.md
  - data/cards.xlsx
  - current engine implementation
allowed_scope:
  - card play feedback
  - resource-change feedback
  - timing values owned by presentation
forbidden:
  - changing card rules or balance data
  - changing fixed-version scope
  - starting another module
required_output:
  - changed files or generated assets
  - validation evidence
  - known limitations
return_gate: Phase 4 module acceptance
```

## Handoff

1. The orchestrator reads the selected child skill's `SKILL.md` in full and any references required by that task.
2. Give the child only the contract, actual source files, and minimum project context needed for the bounded work.
3. The child implements or reviews the specialist slice and returns artifacts plus evidence. It does not mark the module accepted.
4. The orchestrator inspects the actual diff/files, runs the phase validation, updates `STATUS.md`, and asks the user for the current gate decision.

If a child skill conflicts with the fixed PRD, module contract, engine version, or current repository state, the repository and accepted project documents win. Record the conflict instead of silently changing the design.
