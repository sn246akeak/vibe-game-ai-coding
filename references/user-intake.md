# User Intake

Use this reference to guide the user without overwhelming them. Ask only for the current phase's missing inputs.

## First Invocation

If there is no existing status file, ask for:

1. The fixed version target.
2. The current source of truth: repo path, prototype, spreadsheet, PRD, art folder, or conversation summary.
3. The next thing the user wants playable or visible.

If the repo exists, inspect it before asking follow-up questions. Prefer discovering engine version, folder structure, scripts, data files, and docs from the workspace.

## Useful User Submissions

Ask for one of these at a time:

- A rough gameplay idea.
- A rejected idea list.
- A reference game or screenshot.
- A spreadsheet with content, balance, cards, events, enemies, levels, or art specs.
- A folder of source assets.
- A paragraph describing what feels wrong in the current build.
- A short screen recording or screenshots.
- A desired module name and why it should exist.

## Prompt Pattern for the User

Use this structure when asking the user to submit material:

```text
当前阶段：{phase}
我需要你只提交这 1-3 项：
1. {input}
2. {input}
3. {input}

提交后我会做：
- 读取实际文件或内容
- 生成/更新当前模块 PRD
- 落地实现
- 验证并更新进度
```

## When the User Edits Files Outside AI

Use the current file as source of truth.

Required AI steps:

1. Read the changed file or run a diff.
2. Summarize the effective changes.
3. Validate schema and references.
4. Update generated/runtime files.
5. Run the smallest meaningful validation.
6. Log the update in the status file.

Never say "I remember you changed X" as the basis for implementation. Use the actual file state.

## When Requirements Are Vague

Convert vague input into a bounded gate:

- "更有压迫感" becomes triggers, numbers, feedback, and fail conditions.
- "更像卡牌系统" becomes deck, hand, draw, play, discard, cost, effect, and UI contract.
- "更有美术感" becomes style anchor, palette, character/background list, resolution, layers, and animation states.
- "更爽" becomes action frequency, feedback timing, reward visibility, and failure recovery.

Ask for examples only when the repo cannot answer the question.
