# External Data Workflow

Use for designer-edited cards, events, balance, characters, levels or asset requirements.

1. Agree on the editable source, stable ID column, allowed fields, types/ranges, references and runtime destination. Never match by row order or display name.
2. Preserve a baseline/export and source hash before asking the user to edit. Treat the latest actual source as authoritative when they return, not remembered conversation.
3. Reread the file. For XLSX, use an available spreadsheet parser and select explicit sheets/columns. Agree on formula handling; do not assume cached formulas are recalculated. Produce normalized CSV/JSON with consistent types when needed.
4. Run `scripts/diff_content.py BEFORE AFTER --id id --fields cost effect description`. It reports allowed changes, ignored-field changes, added rows and deleted rows. Reordering is not a semantic change. It rejects missing/duplicate IDs and missing editable fields, and never mutates source or runtime. Optional `--output report.json` refuses to overwrite an existing file.
5. Present effective changes. Added/deleted IDs and changes outside the allowlist are not automatically authorized; resolve them with the user. If the current module is frozen, use `workflow.py revise`, update its contract and obtain approval again. Accepted work gets a new revision module.
6. Validate project-specific types, bounds, cross-references and effect syntax. Implement/reuse a project-local importer with explicit paths, deterministic output and focused tests. The generic diff helper is not an XLSX importer, schema validator or balance engine.
7. Regenerate only affected runtime records. Preserve sources and unrelated handcrafted runtime logic. Check the generated diff and run engine tests plus a representative play case.
8. Log source path/hash, affected IDs, changed fields, export command, runtime files and evidence. Ask for acceptance against actual behavior.

Suggested user instruction: "I changed the cost and description columns in this table. Reread this file, compare stable IDs, update only those allowed fields, report additions/deletions separately, then import and verify in-game. Do not reconstruct changes from our conversation."
