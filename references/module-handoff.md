# Module Handoff

Use this reference whenever the user submits or approves a module, such as a card system, event deck, character system, art batch, animation set, or balancing table.

## Handoff Loop

1. Intake the module.
2. Freeze the module contract.
3. Implement the smallest complete slice.
4. Verify the slice.
5. Ask for review or mark accepted.
6. Expand or move to the next module.

## Step 1: Intake

Collect only what is necessary:

- Module name.
- Why it exists.
- Where it appears in the core loop.
- User-editable source of truth.
- Required feel.
- Must-have cases.
- Explicit non-goals.

If the user provides a spreadsheet or file, inspect the file and summarize its current contents before coding.

## Step 2: Freeze the Contract

Create a micro-PRD before editing implementation files.

Required fields:

- Objective.
- Player-facing behavior.
- System states touched.
- Data schema.
- UI or scene touchpoints.
- Error handling.
- Acceptance criteria.
- Validation commands or manual checks.

The contract can be short, but it must be explicit enough for another AI turn to resume.

## Step 3: Implement the Slice

Implementation order:

1. Data/schema validation.
2. Domain logic.
3. Engine integration.
4. UI/visual feedback.
5. Debug or designer affordances.
6. Tests/checks.
7. Status log update.

Preserve existing project conventions. Avoid broad refactors while landing a module unless they are necessary to isolate the module.

## Step 4: Verify

Pick the smallest checks that prove the module is alive:

- Unit tests for deterministic logic.
- Import/parse checks for spreadsheets or JSON.
- Engine scene load checks.
- Manual playthrough checklist.
- Screenshots for UI or art work.
- Asset existence and size checks.

Report failures plainly and fix them before asking for acceptance when feasible.

## Step 5: Review Gate

When handing back to the user, include:

- What changed.
- How to inspect it.
- What was verified.
- Known limitations.
- The exact question for acceptance, such as "这个卡牌模块是否进入 accepted，还是继续调整数值/表现？"

Do not start the next module until the user accepts, defers, or explicitly asks to continue.

## Step 6: Repeat

After acceptance:

1. Mark the module `accepted`.
2. Move the next queued module to `intake_needed` or `designing`.
3. Ask for only that module's missing inputs.
4. Keep the fixed-version scope unchanged unless the user intentionally reopens it.

## Common Module Patterns

### Card System

Ask for or define:

- Deck source.
- Draw timing.
- Hand size.
- Cost or restriction.
- Effect categories.
- Targeting rules.
- Discard/exhaust behavior.
- UI feedback.
- Balance knobs.

### Art Batch

Ask for or define:

- Style anchor.
- Asset categories.
- Resolution and aspect ratio.
- Background transparency.
- Layer separation.
- Animation states.
- Naming convention.
- Output folder.
- Sample-first validation before full batch.

### External Spreadsheet

Ask for or define:

- Required columns.
- Stable IDs.
- Type/range constraints.
- Relationship fields.
- Export path.
- Runtime format.
- Validation script.
- What AI should regenerate after the user edits it.
