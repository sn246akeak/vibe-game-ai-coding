# Specialist Contract

Before a bounded specialist task, write a project-local JSON contract. Use actual module IDs and file paths. Required fields must be nonempty:

```json
{
  "module": "cards",
  "delegate": "game-feel",
  "objective": "Make card play and resolution readable.",
  "input_source": ["docs/modules/cards.md", "data/cards.csv", "docs/evidence/cards-functional.md"],
  "allowed_scope": ["card presentation and timing"],
  "forbidden": ["changing card rules", "changing balance", "starting another module"],
  "required_output": ["changed files", "validation evidence", "known limitations"],
  "return_gate": "cards: needs_user_review"
}
```

Call `workflow.py delegate cards --contract docs/contracts/cards.json` with the global project argument. The runtime checks required fields, current module/state, route eligibility and installed content. Contract fields describe boundaries; the script does not sandbox edits or validate every listed source path. The parent must inspect those actual inputs before work.

1. Read the selected skill and its necessary references.
2. Apply it in the same agent, or use a real available delegation facility within the user's authorization. Supply only the contract and relevant project context.
3. Inspect returned files/diff, validate behavior and record fresh evidence.
4. Submit the current module for user review; this clears Active Delegation. Only the user's decision permits acceptance.

Repository facts, the accepted PRD and module scope constrain specialist advice. Report conflicts and return a proposal instead of silently changing engine, provider, rules or version scope.
