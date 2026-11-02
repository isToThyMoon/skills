---
name: write-a-skill
description: 写、改、拆分或诊断 agent skill（SKILL.md），让 agent 每次都按说明走。Use when the user wants to create a skill or turn a workflow into one, rewrite or split a skill that is too long or messy, review a skill, or find out why an agent isn't following one.
---

# Write a Skill

本目录下的路径都相对于 skill 所在目录。`references/principles.md` 是规则和理由，第 1 步读其中 §1、§3，第 2 步读全文；`references/review-checklist.md` 只在第 3 步交给审查子 agent。

先建一个工作区 `<name>-workspace/`，放在目标仓库的 skills 目录之外（例如系统临时目录），免得被当成 skill 登记。意图和快照都放在这里。

按请求选分支：

- **新建**：第 1 步走到第 4 步。
- **改写或拆分**：先把原 skill `cp -r` 到 `<name>-workspace/baseline/`，再从第 1 步开始；意图从原 skill 和用户的抱怨里取。改写要以一次真实失败为依据（见第 1 步）；拆分是结构问题，不受这一限制。
- **诊断或审查**：做第 1 步（意图从原 skill 和用户的抱怨里推出，不必等用户确认）和第 3 步的审查，把审查报告和最该先改的三处交给用户，不改文件。用户同意修改后，转入改写分支：用户来诊断时描述的那次没照着做，就是失败记录；审查报告里的其他问题只作参考，不单独作为修改依据。

## 1. 抓意图，定形状

先从当前对话里取：用户描述过的流程、用到的工具、纠正过的地方、输入输出的样子。缺的再问，问时附上你的推荐答案。写进 `<name>-workspace/brief.md`：

- 这个 skill 让 agent 做成什么；
- 什么情况该触发它（每个真正不同的情况算一个分支）；
- 产出是什么格式，放在哪里；
- 怎样算它起作用了（"It's working if"）；
- **调用方式**：模型干活中途主动调用它有用，就做成模型自动调用；只在人想用时才跑（大流程、有副作用、个人习惯），就加 `disable-model-invocation: true`，description 写成给人看的一行；
- **粒度**：一个 skill 只做一件事，已有 skill 能覆盖的部分用 `Call the Skill tool with "<name>"` 组合进来；一次运行放不进一个短会话，就按阶段拆，阶段之间用文件交接。

改写分支再记一次真实失败：跑了什么、skill 做了什么、本来期望什么。用户给不出实例时，建议用户先在新会话里用 skill-creator 跑一轮对比测试，拿到失败再回来；"如果……会更好"不算失败。没有结构性问题时，修改只针对记下的失败，通常补一句就够（§11）。

完成条件：`brief.md` 里每一项都有一句结论，改写分支含一条失败记录，用户确认过（诊断分支除外）。

## 2. 起草

读 `references/principles.md` 全文，从 `assets/skill-template.md` 起稿。依次写：

1. **description**：它是什么，加上每个触发分支（§2）。
2. **步骤**：每步用祈使句，结尾写完成条件（§5）；跨步骤要用的结论落成文件（§6）。
3. **参考**：每个分支都要用的写进正文，只有部分分支用的挪进 `references/`，附一句写明读取时机的指引（§4）。
4. **脚本和资源**：确定性、重复性的工作放进 `scripts/`，产出用的模板放进 `assets/`（§4）。
5. **压制规则**：每条"不要"先改写成"要怎样"；确实要压制的，按 §8 分层，交给脚本或审查清单。
6. **措辞**：按 §7 过一遍。

完成条件：每一步都有完成条件；每个 `references/` 文件都有一句写明读取时机的指引；正文里的每条禁令都配了替代做法；`scripts/` 里的每个脚本用一个最小输入跑通过一次，边界情况留给交付后的对比测试。

## 3. 检查

运行 `python3 scripts/check_skill.py <草稿目录>`，修到输出 `OK`。

多步流程、带脚本或子 agent、要给别人用的 skill，再做一轮独立审查；一两步的小 skill 只跑脚本。诊断分支始终审查。审查时在全新上下文里启动一个子 agent，可以用更便宜的模型（例如 Sonnet 或 Haiku），prompt 里给它草稿目录路径、`brief.md` 全文和 `references/review-checklist.md` 全文，要求它逐条对照清单，引用原文，分"硬性问题"和"需要判断的问题"，每条附改法，500 字以内，写进 `<name>-workspace/review.md`。审查结论只从 `review.md` 里取。只审一轮，除非修改动了结构。

完成条件：脚本输出 `OK`；审查过的，`review.md` 已存在，其中每条硬性问题都已修改，没改的判断类问题各有一句理由；跳过审查的，在 `brief.md` 里写一句理由。

## 4. 交付

读目标仓库的 `AGENTS.md`、`README.md` 和清单文件（例如 `skills.sh.json`、`plugin.json`），按约定放置并登记新 skill。仓库里其他 skill 有 `agents/openai.yaml` 时，同步写一份。

告诉用户：调用方式和理由、拆分结构、审查结论、还没解决的问题。再建议下一步在新会话里做（`brief.md` 和 `baseline/` 留在工作区作交接）：用 skill-creator 跑带 skill 与不带 skill 的对比测试；模型自动调用的 skill，可以再跑它的 description 优化循环。上线后的修改方式见 §11。

完成条件：skill 已放到位，该登记的都已登记，报告里列出了未解决的问题和建议的测试。
