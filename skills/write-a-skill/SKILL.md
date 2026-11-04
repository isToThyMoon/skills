---
name: write-a-skill
description: 写、改、拆分或诊断 agent skill（SKILL.md），让 agent 拿到目标和信息后能自由发挥好。Use when the user wants to create a skill or turn a workflow into one, rewrite or split a skill that is too long or messy, review a skill, or find out why an agent isn't working well with one.
---

# Write a Skill

好的 skill 是 harness，不是流程单：写清目标、交付结果、可用的信息和验收，只对错了难挽回的地方设硬边界，中间怎么做留给模型发挥。这份 skill 也按此写，怎么组织工作由你判断。

本目录下的路径都相对于 skill 所在目录。`references/principles.md` 是规则和理由，定形状和起草时查阅；`references/review-checklist.md` 给审查子 agent。

## 交付结果

- **`<name>-workspace/brief.md`**：工作区放在目标仓库的 skills 目录之外（例如系统临时目录），免得被当成 skill 登记。brief 写明这个 skill 让 agent 做成什么；什么情况该触发它（每个真正不同的情况算一个分支）；产出是什么格式、放在哪里；怎样算它起作用了（"It's working if"）；调用方式和粒度（§1、§3）。
- **skill 本身**：从 `assets/skill-template.md` 起稿。包含 description（它是什么，加上每个触发分支，§2）、目标、交付结果、信息（每个分支都要用的写进正文，其余挪进 `references/` 并写明读取时机，§4）、验收（§5）。确定性、重复性的工作放进 `scripts/`，产出用的模板放进 `assets/`。
- **登记**：读目标仓库的 `AGENTS.md`、`README.md` 和清单文件（例如 `skills.sh.json`、`plugin.json`），按约定放置并登记。仓库里其他 skill 有 `agents/openai.yaml` 时，同步写一份。
- **给用户的报告**：调用方式和理由、拆分结构、审查结论、还没解决的问题、"It's working if"，以及建议的下一步：在新会话里用 skill-creator 跑带 skill 与不带 skill 的对比测试；模型自动调用的 skill，可以再跑它的 description 优化循环。仓库有给人看的 skill 文档时，把 "It's working if" 也写进去，因为工作区是临时的。

## 按请求调整

- **新建**：意图从当前对话里取：用户描述过的流程、用到的工具、纠正过的地方、输入输出的样子。缺的再问，附上推荐答案。
- **改写或拆分**：把原 skill `cp -r` 到 `<name>-workspace/baseline/`，意图从原 skill 和用户的抱怨里取。不改变行为的整理，交付时对照 `baseline/` 说明行为没变。
- **诊断或审查**：交付审查报告和最该先改的三处，意图从原 skill 和用户的抱怨里推出，不必等确认。用户同意修改后转为改写，来诊断时描述的那次问题就是失败记录。

## 硬边界

- **brief 要用户确认**（诊断除外），因为意图错了，后面都白做。
- **诊断时不改目标 skill。**
- **改变行为要有依据**：一次真实失败（跑了什么、skill 做了什么、本来期望什么），或用户明确要求的方向，记进 `brief.md`。"如果……会更好"不算。用户说不清时，建议先在新会话里用 skill-creator 跑一轮对比测试。修改时不要一个问题加一条规则，判断标准见 §11。

## 验收

运行 `python3 scripts/check_skill.py <草稿目录>`，修到输出 `OK`。`note:` 开头的行是启发式提示，改不改由你判断。`scripts/` 里的每个脚本都用最小输入跑通过一次。

多部分、带脚本或子 agent、要给别人用的 skill，以及所有诊断，再做一轮独立审查：在全新上下文里启动一个子 agent，可以用更便宜的模型（例如 Sonnet 或 Haiku），prompt 里给它草稿目录路径、`brief.md` 全文和 `references/review-checklist.md` 全文，要求它把结论写进 `<name>-workspace/review.md`。结论只从 `review.md` 里取。

完成条件：脚本输出 `OK`；审查过的，每条硬性问题都已修改，没改的判断类问题各有一句理由；跳过审查的，`brief.md` 里写了理由；正文里的每条禁令都配了替代做法；以上交付结果都已给出。诊断的完成条件换成：脚本输出和 `review.md` 都已交给用户，目标 skill 没有改动。
