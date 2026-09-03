# Vibe Game AI Coding Skill

中文 | [English](#english)

一个用于 AI coding 游戏项目的 Codex skill。它把“从模糊玩法灵感到固定版本交付”的过程拆成可推进、可验收、可复用的阶段工作流：玩法澄清、第一版 PRD、白盒 MVP、玩法模块插入、外部表格/配置管线、美术批量生产与接入、测试打包和复盘。

这个 skill 的核心不是替你一次性写完整游戏，而是让 AI 像制作人加工程师一样分阶段引导你提交材料、冻结当前模块、落地实现、验证结果，并在验收后进入下一轮。

## 适用场景

- 你想用 AI coding 做一个游戏，但还没有稳定玩法。
- 你已经有 HTML 原型、Godot/Unity/网页项目或其他可运行原型，想继续工程化。
- 你希望把卡牌、事件、角色、关卡、美术、动画、音频等模块逐个插入，而不是一次性把需求堆给 AI。
- 你希望自己在 AI 外修改表格、JSON、CSV、素材文件，然后让 AI 读取真实文件并更新工程。
- 你希望每个固定版本都有进度、验收门、交付记录和下个版本 backlog。

## 安装

把本仓库放入本机 Codex skills 目录：

```bash
cd ~/.codex/skills
git clone https://github.com/sn246akeak/vibe-game-ai-coding.git vibe-game-ai-coding
```

Windows 常见路径：

```powershell
cd $env:USERPROFILE\.codex\skills
git clone https://github.com/sn246akeak/vibe-game-ai-coding.git vibe-game-ai-coding
```

安装后，Codex 的 skill 列表中应出现 `vibe-game-ai-coding`。

## 快速开始

在一个游戏项目中对 Codex 说：

```text
运行 $vibe-game-ai-coding。当前目标是 v0.1，请从项目现状开始，引导我按阶段提交材料、实现模块、验收后再推进下一模块。
```

也可以从某个模块开始：

```text
运行 $vibe-game-ai-coding。这个版本我要先插入卡牌系统，请先让我提交当前模块需要的表格和玩法规则，然后你根据真实文件落地实现。
```

## 工作方式

skill 会维护一个项目本地进度文件，默认位置是：

```text
docs/ai-coding-workflow/STATUS.md
```

如果项目已有更合适的日志目录，AI 会沿用项目习惯。

每一阶段都遵循同一个循环：

1. 澄清当前阶段目标和验收标准。
2. 让用户只提交当前阶段必要材料。
3. 把材料转成 PRD 切片、模块契约、数据结构或美术规格。
4. AI 在工程中落地实现。
5. 运行自动检查或手动验收步骤。
6. 更新进度文件。
7. 当前模块验收后，再推进下一模块。

## 标准阶段

| 阶段 | 目标 | 典型产出 |
|---|---|---|
| Phase 0 | 项目建档与版本目标 | 固定版本目标、范围、风险、初始 backlog |
| Phase 1 | 核心玩法澄清 | 核心循环、状态、胜负条件、关键体验 |
| Phase 2 | 第一版 PRD | 可实现 PRD、模块队列、数据源、验收标准 |
| Phase 3 | 白盒 MVP | 可完整游玩的一局、基础状态机、占位 UI |
| Phase 4 | 玩法模块插入 | 模块微型 PRD、实现、验证、用户验收 |
| Phase 5 | 外部数据管线 | 表格/CSV/JSON/资源导入、校验脚本、运行时数据 |
| Phase 6 | 美术规格与批量生产 | 风格锚点、资产清单、命名规则、批量 prompt |
| Phase 7 | 美术接入与迭代 | 导入设置、图层、动画、场景摆放、截图验证 |
| Phase 8 | 音频与反馈 | SFX、音乐、动效时序、设置项 |
| Phase 9 | 版本完成 | 打包、回归检查、实现日志、脚本沉淀、下版 backlog |

## 模块插入流程

当你想加入一个新模块，比如卡牌系统、事件系统、角色技能、敌人行为、关卡机制或美术批量资产时，AI 会先冻结模块契约：

- 模块目的是什么。
- 它在哪个核心循环节点触发。
- 会影响哪些状态。
- 数据从哪里来，哪些字段允许用户编辑。
- 需要哪些 UI、动画、音效或反馈。
- 有哪些验收标准。
- 如何关闭、回滚或延后。

然后 AI 才会修改工程。实现完成后，模块会进入 `needs_user_review`，等待你确认是否 `accepted`，再继续下一个模块。

## 外部文件协作

如果你在 AI 外修改了表格、CSV、JSON、素材文件或脚本，正确用法是：

```text
我已经修改了 cards.xlsx。运行 $vibe-game-ai-coding，请读取真实文件，先总结变化，再更新运行时数据和工程实现。
```

skill 要求 AI 必须读取当前真实文件或 diff，不能只凭记忆改代码。

## 仓库结构

```text
vibe-game-ai-coding/
|-- SKILL.md
|-- README.md
|-- agents/
|   `-- openai.yaml
`-- references/
    |-- stage-gates.md
    |-- user-intake.md
    |-- progress-format.md
    `-- module-handoff.md
```

## English

A Codex skill for AI-coding game projects. It turns the path from a vague game idea to a fixed-version delivery into a staged, inspectable workflow: gameplay clarification, first PRD, white-box MVP, gameplay module insertion, external data/config pipelines, batch art production, art integration, validation, packaging, and retrospective logging.

The skill is not designed to ask the AI to build an entire game in one pass. Instead, it makes the AI act like a producer-engineer: guide the user through one phase at a time, request only the current materials, freeze the active module, implement it, validate it, update progress, and advance only after acceptance.

## Use Cases

- You want to build a game with AI coding but do not yet have a stable gameplay loop.
- You already have an HTML prototype, Godot/Unity/web project, or runnable prototype and want to turn it into a structured project.
- You want to insert systems such as cards, events, characters, levels, art, animation, and audio one module at a time.
- You want to edit spreadsheets, JSON, CSV, or assets outside the AI chat, then have the AI read the actual files and update the project.
- You want every fixed version to have visible progress, gates, validation notes, implementation logs, and a backlog for the next version.

## Installation

Place this repository inside your local Codex skills directory:

```bash
cd ~/.codex/skills
git clone https://github.com/sn246akeak/vibe-game-ai-coding.git vibe-game-ai-coding
```

Common Windows path:

```powershell
cd $env:USERPROFILE\.codex\skills
git clone https://github.com/sn246akeak/vibe-game-ai-coding.git vibe-game-ai-coding
```

After installation, Codex should list `vibe-game-ai-coding` as an available skill.

## Quick Start

Inside a game project, ask Codex:

```text
Use $vibe-game-ai-coding. The target is v0.1. Start from the current project state, guide me through staged submissions, implement each module, and only move forward after acceptance.
```

Or start from a specific module:

```text
Use $vibe-game-ai-coding. For this version I want to insert a card system first. Ask me for the table and gameplay rules needed for this module, then implement it from the actual files.
```

## Workflow

The skill maintains a project-local progress file, usually:

```text
docs/ai-coding-workflow/STATUS.md
```

If the project already has a better workflow log location, the AI should follow the existing convention.

Every phase uses the same loop:

1. Clarify the phase goal and acceptance criteria.
2. Ask the user for only the necessary current materials.
3. Convert those materials into a PRD slice, module contract, data schema, or art specification.
4. Implement the result in the project.
5. Run automated checks or manual validation.
6. Update the progress file.
7. Move to the next module only after acceptance.

## Standard Phases

| Phase | Goal | Typical Output |
|---|---|---|
| Phase 0 | Project charter and version target | Version scope, risks, initial backlog |
| Phase 1 | Core gameplay clarification | Core loop, states, win/loss conditions, target feel |
| Phase 2 | First PRD | Buildable PRD, module queue, data sources, acceptance criteria |
| Phase 3 | White-box MVP | One complete playable session, basic state machine, placeholder UI |
| Phase 4 | Gameplay module insertion | Module micro-PRD, implementation, validation, user acceptance |
| Phase 5 | External data pipeline | Spreadsheet/CSV/JSON/resource import, validation scripts, runtime data |
| Phase 6 | Art specs and batch production | Style anchor, asset manifest, naming rules, batch prompts |
| Phase 7 | Art integration and iteration | Import settings, layers, animation, scene placement, screenshot checks |
| Phase 8 | Audio and feedback | SFX, music, animation timing, settings |
| Phase 9 | Version completion | Build, regression checklist, implementation log, scripts, next backlog |

## Module Insertion

For a module such as a card system, event system, character ability set, enemy behavior, level mechanic, or batch art package, the AI first freezes a module contract:

- Module purpose.
- Where it appears in the core loop.
- Game states it touches.
- Source of truth and editable fields.
- UI, animation, audio, or feedback requirements.
- Acceptance criteria.
- Disable, rollback, or defer path.

Only then should the AI modify project files. Once implemented, the module enters `needs_user_review`; after the user accepts it, the module becomes `accepted` and the next module can begin.

## External File Collaboration

If you edit a spreadsheet, CSV, JSON, asset file, or script outside the AI chat, use a prompt like:

```text
I updated cards.xlsx. Use $vibe-game-ai-coding, read the actual file, summarize the changes first, then update the runtime data and project implementation.
```

The skill requires the AI to inspect the actual current file or diff before changing the project. Memory is not the source of truth.

## Repository Structure

```text
vibe-game-ai-coding/
|-- SKILL.md
|-- README.md
|-- agents/
|   `-- openai.yaml
`-- references/
    |-- stage-gates.md
    |-- user-intake.md
    |-- progress-format.md
    `-- module-handoff.md
```
