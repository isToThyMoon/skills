---
name: init-harness
description: 给项目铺设或优化最小 harness：AGENTS.md 入口、业务词表、统一检查入口和 UI token。
disable-model-invocation: true
---

# Init Harness

目标是让之后每个 coding agent 在新会话里都能快速定位需求点，并沿用项目的技术栈、架构和视觉风格。harness 只提供引导和反馈，大部分决定留给之后干活的 agent。`assets/`、`references/`、`scripts/` 都相对于本 skill 所在目录，不是目标仓库。

每句要写进 harness 的话都过一道筛子：**删掉它，agent 会犯错吗？它能从代码、配置或 `ls` 查到吗？** 只留"会犯错且查不到"的。研究显示 agent 会照做文件里的指令，多余内容会让任务变难、成本变高，而目录概览并没有帮它更快找到文件（[arXiv 2602.11988](https://arxiv.org/html/2602.11988v1)）。所以目录靠 `ls`，定位靠词表和 grep。

产出留在工作区供用户审查，用户要求时才提交。

## 1. 盘点现状

运行 `git status --porcelain`。有输出时停下，请用户先提交或 stash，这样本次产出才是一份能单独审查的 diff；不是 git 仓库时，征得用户同意后 `git init`。

然后按实际情况选分支（可以同时命中"已有代码"和"已有 harness"）：

- **空仓库**：还没有业务代码。
- **已有代码**：一切从代码、配置、测试、README 和 git 历史提取，架构保持原样。
- **已有 harness**：存在 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`.cursor/rules/`、`.cursorrules`、`.github/copilot-instructions.md`、词表、检查脚本或 token 中的任何一个。全部按本 skill 的标准优化。

再判断项目有没有界面（Web、App、桌面端都算）。把分支、是否有界面、已有 harness 文件清单和待问用户的问题写进 `$TMPDIR/init-harness/plan.md`（放在仓库外，免得混进 diff）。

完成条件：工作区干净，`plan.md` 写明分支和是否有界面，已有 harness 的每个文件都列在清单里。

## 2. 定下项目事实

只问代码里读不到的，每个问题附上推荐答案，一次问完：产品一句话、核心业务词、架构上不能破的约束。

**空仓库**还要定技术栈，再用该技术栈的官方脚手架起骨架（例如 `npm create vite`、`flutter create`），这样目录和配置都符合生态习惯。skill 本身不内置技术栈模板。业务代码留给之后的任务。

**已有 harness** 逐条审计旧内容，在 `plan.md` 里为每条事实记一个去向：

| 这条事实 | 去向 |
| --- | --- |
| 通用、关键、处处要用 | 留在根 `AGENTS.md` |
| 只对某个子项目或目录成立 | 该目录的 `AGENTS.md`，旁边配一个只写 `@AGENTS.md` 的 `CLAUDE.md`（根目录有 `CLAUDE.md` 时，Claude Code 默认不读 `AGENTS.md`，靠这个 import 才加载） |
| 决定和原因 | `<repo>/docs/adr/` |
| 业务词 | `GLOSSARY.md` |
| 只对 Claude Code 成立 | `.claude/rules/` |
| 与代码不符 | 核对代码后修正 |
| 能查到、模型默认会做、或泛泛而谈 | 删除，并在报告里写明理由 |

现有的 hook、pre-commit、CI 是用户有意的强制手段，保持原样；觉得多余的写进报告，由用户决定。`CLAUDE.local.md` 是个人文件，也保持原样。

完成条件：`plan.md` 的问题清单逐条有答复；空仓库的骨架能启动；`plan.md` 里已有 harness 的每条事实都有去向。

## 3. 写入口文档

从 `assets/AGENTS.template.md` 和 `assets/GLOSSARY.template.md` 起稿，写出根目录的 `AGENTS.md` 和 `GLOSSARY.md`；用项目已有文档的语言，没有文档时用与用户对话的语言。`CLAUDE.md` 全文只有一行 `@AGENTS.md`。

- **语义地图**只写 `ls` 看不出的：哪块业务在哪、哪里不再加新功能、哪里容易改错。
- **词表**是中文需求和英文代码之间的桥，所以每个词都给出代码里的真实标识，agent 查到标识就能 grep。标识比路径稳定，词条不写路径。已有代码时从代码提取核心业务词；中文叫法拿不准的，列进报告请用户确认。
- **面向 grep 的写法**管今后写的代码。铺设时旧代码保持原样，批量改名和加注释会让 diff 无法审查，也可能带来业务风险。
- **其他工具**：仓库有 `.gemini/` 或 `.aider.conf.yml` 时，按 <https://agents.md> 的说明把它们指向 `AGENTS.md`。其他工具的规则文件把通用内容迁入 `AGENTS.md` 后，只留工具专属配置。

完成条件：`AGENTS.md` 里每条命令都实际跑过；模板占位符都已替换或删除；词表包含产品一句话里的每个业务词（空仓库的标识待首次实现时补，先写成 `待定`）。

## 4. 建检查入口

提供一条命令，跑完这个项目所有的 lint、类型检查和测试。技术栈有惯用入口时（`make check`、`npm run check`、`just check`）用它，没有就写 `<repo>/scripts/check`。agent 会自己运行文档里列出的检查并修复失败，所以这条命令就是它的反馈回路。

至少要跑到一个真实测试：没有测试时，为一条核心行为补一个最小的测试，空仓库就测骨架能启动。自写检查的失败信息要写明怎么修，agent 下一步会照着做。

这一步到此为止：hook、pre-commit 和 CI 都留给同样的错反复出现之后，再由用户决定是否加上。

已有代码的历史失败不属于本次范围，修它们可能牵动业务。在 `plan.md` 里逐条记下失败项，第 6 步带上 `--allow-check-failure`。

完成条件：检查命令退出 0，或每个失败项都确认在铺设前就存在并已记录；输出里有测试运行的结果。

## 5. 建 UI token（有界面时）

读 `references/ui-tokens.md`，按其中的步骤完成。没有界面时跳过；之后加了前端，重跑本 skill 即可补上。

完成条件：`references/ui-tokens.md` 末尾的完成条件都满足。

## 6. 验证

运行 `python3 <skill 目录>/scripts/check_harness.py <repo> --check-cmd "<检查命令>" --expect-output "<测试运行时一定会打印的正则>"`，修到输出 `OK`。有界面时加 `--tokens <代码 token 文件>`，第 4 步记录了历史失败时加 `--allow-check-failure`。`note:` 开头的行逐条判断。

已有代码时再做一次定位测试。先从词表挑两个词，各写一条只用业务词描述、不提文件名和标识符的需求，把需求和正确的文件记进 `plan.md`。然后在全新上下文里启动一个子 agent（不支持子 agent 的工具，请用户在新会话里跑），prompt 只给仓库路径和这两条需求，要求它找出要改的文件、只读不改、最后说明搜了几次。结果写进 `plan.md`。它找错或搜索超过 5 次时，修正词表或语义地图后再测一次。

完成条件：脚本输出 `OK`；已有代码时，两条需求都在 5 次搜索内找到了正确的文件，或未通过的情况已写进报告。

## 7. 报告

告诉用户：

- 分支，以及新建和改动的文件；
- 已有 harness 的优化结果：删减或迁移的每条事实和去向，来自 `plan.md`；
- 检查命令和它的历史失败；定位测试结果；
- 请用户确认的词条和设计决定；词表要深入打磨时，可以用 domain-modeling skill，文件格式与它兼容；
- 改动还没提交，请用户审查 diff。

最后提醒一句：之后 agent 反复犯同一个错时，能写成检查就写成检查，不能的再往 `AGENTS.md` 补一句。

完成条件：报告覆盖以上各项，每条被删减的事实都有交代。
