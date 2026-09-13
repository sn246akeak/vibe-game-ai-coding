# Vibe Game AI Coding

[English](README.en.md) | 中文

一套从玩法想法推进到固定版本交付的 Codex skill。AI 分阶段引导你提交材料或共同完成设计，每次只落地一个模块，验证并由你验收后再进入下一轮。

**v1.0.0：引导规范 + 可执行状态机 + 内容变更检查 + 专项 skill 路由。** 它不是无人值守的造游戏程序，也不自带游戏引擎或付费美术服务。

## 安装

需要 Codex 和 Python 3.10+。核心脚本只使用 Python 标准库。在 Codex 中可以这样提出：

> 使用 skill-installer，从 sn246akeak/vibe-game-ai-coding 仓库根目录安装 vibe-game-ai-coding。

也可手动克隆到 Codex 的 skills 目录。PowerShell 示例：

```powershell
$skills = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills" } else { Join-Path $HOME ".codex" "skills" }
git clone https://github.com/sn246akeak/vibe-game-ai-coding.git (Join-Path $skills "vibe-game-ai-coding")
```

已有目录时先检查本地修改，不要覆盖。安装后重新开启 Codex 会话以发现 skill。Godot、浏览器测试工具、素材生成工具按项目需要单独准备。

## 怎么用

在游戏项目中对 AI 说：

```text
运行 $vibe-game-ai-coding。
目标版本是 v0.1，我想做一个……游戏。
请先检查当前工程，每次只引导我完成当前模块需要的材料；
材料和设计经我确认后再实施，展示可检查的结果；
我验收当前模块后，再进入下一模块。
```

恢复工作：

```text
继续运行 $vibe-game-ai-coding，读取已有 workflow.json 和实际文件，
告诉我当前模块、已验收进度、阻塞项以及这次需要我提交什么。
不要重建已有进度，不要从聊天记忆猜测文件变化。
```

你不必亲自运行所有脚本。AI 负责执行、更新进度和整理证据，你负责方向、设计确认、体验反馈和验收。不会要求你一开始填写整套材料。

## 实现流程

| 阶段 | 你与 AI 共同确定 | 落地与验收产物 |
|---|---|---|
| 0 版本目标 | 平台、引擎、目标体验、范围 | 项目约定与初始队列 |
| 1 核心玩法 | 玩家动作、压力、取舍、胜负与重开 | 玩法闭环及可验证场景 |
| 2 第一版 PRD | 系统边界、数据、场景、非目标 | 确认后的 PRD 与模块顺序 |
| 3 白盒 MVP | 最小可玩承诺 | 一次完整游戏流程 |
| 4 玩法模块 | 触发、状态、规则、UI、测试 | 逐模块的可玩增量 |
| 5 外部数据 | 稳定 ID、可改字段、导入规则 | 表格修改到引擎行为的闭环 |
| 6 美术样张 | 风格、构图、规格、统一提示词 | 引擎内样张确认与素材清单 |
| 7 美术落地 | 批量生产、分层、动画、修改范围 | 集成截图、交互与视觉验收 |
| 8 音效与反馈 | 事件、时序、音量、动效 | 完整一局的视听检查 |
| 9 固定版本交付 | 回归、已知问题、下一版范围 | 可运行版本、日志和复用命令 |

阶段是工作类型，不是强制一次性的流水线。玩法/数据阶段可按模块重复，依赖的数据管线可以先于玩法接入。可选工作可由你明确延期，核心玩法、PRD、可玩闭环和交付不能跳过。

每个模块遵循：

```text
收集材料 → 共建设计 → 确认规格 → 实施 → 验证 → 等你验收 → 下一模块
                         ↑                      |
                         └──── 需要修改 ────────┘
```

大模块可以拆成多个独立验收的小模块，例如：卡牌数据合同、抽牌出牌最小闭环、完整效果与 UI、数值与反馈。子 skill 完成任务不等于你的验收。

## 文件与脚本

工程内的默认状态目录为 `docs/ai-coding-workflow/`：

- `workflow.json`：唯一权威状态，包含模块队列、输入快照、证据、委派与决策历史。
- `STATUS.md`：自动生成的进度看板，不能独立手改推进状态。
- 模块 PRD、验收证据、BACKLOG：按实际需要创建，由状态记录关联。
- `IMPLEMENTATION_LOG.md`：状态与证据日志导出，不覆盖已有文件。

| 脚本 | 用途 |
|---|---|
| `workflow.py` | 初始化、排队、依赖检查、状态推进、修订、延期、备注、委派、验收、日志导出 |
| `diff_content.py` | CSV/JSON 按稳定 ID 比较，只报告指定可改字段；新增、删除和其他字段变化单列 |
| `route_subskills.py` | 按当前阶段与引擎选择专项 skill，并核验锁定内容 |
| `check_subskills.py` | 检查全部专项 skill 的安装与内容状态 |
| `pin_subskills.py` | 维护者从固定上游提交生成内容锁，不安装或执行上游代码 |
| `new_module.py` | 生成模块 PRD 文档骨架，不自动推进队列 |
| `init_workflow.py`、`validate_workflow.py` | 旧版 Markdown 工作流兼容工具，不与 v1 状态混用 |

命令在安装后的 skill 目录执行；`GAME` 替换为实际游戏工程绝对路径：

```bash
python scripts/workflow.py --project "GAME" init --version v0.1 --engine godot
python scripts/workflow.py --project "GAME" status
python scripts/workflow.py --project "GAME" validate
python scripts/route_subskills.py --workflow "GAME/docs/ai-coding-workflow/workflow.json" --project "GAME"
```

完整操作见 [状态运行说明](references/workflow-runtime.md)。已有旧日志不会被覆盖，可指定新的 `--directory` 保存 v1；已交付的版本用新目录开启下一版。

## 外部表格与美术

你可以说：“我修改了表格里的 cost 和 description。读取实际文件，按 ID 比较，只同步这两列，新增删除先单列，再验证游戏表现。”

脚本会对冻结输入做哈希检查：文件变化后必须重新读取、修订并确认，不能拿旧快照继续推进。`diff_content.py` 不直接改游戏，也不解析 XLSX；XLSX 读取、公式处理、业务校验和运行时导入由项目适配器承担。详见 [数据流程](references/data-workflow.md)。

美术从已跑通的 HTML/白盒出发，先确认引擎内样张，再用统一规格和素材清单生产人物、背景、UI、动画与音频。保留原始素材与运行时派生物，迭代只针对指定素材 ID。详见 [美术流程](references/art-workflow.md)。本仓库没有伪装成通用能力的项目专用图集、抠图或 Godot 导入脚本。

## 专项 Skill 接入

核心设计、UI、反馈分别使用 `game-design-theory`、`game-ui-ux`、`game-feel`。引擎与原型按需使用 `godot`、`develop-web-game`；Higgsfield、Three.js UI、RivetKit 联机为条件接入。

来源与固定提交见 [subskills.json](references/subskills.json)，内容摘要见 [subskills.lock.json](references/subskills.lock.json)。专项 skill 单独安装，不随本仓库分发。让 AI 使用内置 skill-installer 按清单的 repo/path/ref 安装当前需要的项，再检查实际路由。不要无条件安装全部依赖或覆盖已定制的目录。

`verified` 仅表示安装内容与锁定快照一致，不保证引擎/API 兼容、凭据、服务可用性、安全或许可证。一些上游路径使用历史快照；调用时仍需核对官方文档。缺失或修改过的依赖须明确处理，或记录由主 skill 直接完成的降级方案。详见 [路由边界](references/skill-routing.md) 和 [委派合同](references/subskill-contract.md)。

## 验证与边界

```bash
python -m unittest discover -s tests -v
python scripts/check_subskills.py
```

测试覆盖完整状态循环、跨进程恢复、门禁、输入/证据变化、依赖插入、委派、旧日志保护与内容差异。测试使用模拟确认和临时文件，不能代替真实游戏制作验收。

状态机不能证明 AI 写入的“测试通过”是真的，也不能证明决策文本一定来自用户。AI 必须使用真实检查结果与用户原话，不得自动自验收；代码变更后需重新测试。该 skill 不自动发布仓库、部署游戏、购买服务、登录账户或启动后台代理。
