---
name: <skill-name>
description: <它是什么，一句话>. Use when <分支 1>, <分支 2>, or <分支 3>.
# 只在人想用时才跑的 skill，加上下面这行，并把 description 改成给人看的一行摘要：
# disable-model-invocation: true
---

# <Skill 标题>

<一两句：这个 skill 做什么，为什么这样做。核心概念词在这里第一次出现。>

<有多个分支时，写清按什么选分支：>

- **<分支 A>**：<走哪些步骤>
- **<分支 B>**：<走哪些步骤>

## 1. <步骤名>

<祈使句写要做什么。需要理由的地方写理由。>

完成条件：<agent 怎么判断这一步做完了。能用命令判断的，写成"某命令输出 X"。>

## 2. <步骤名>

<需要另一个 skill 时：Call the Skill tool with "<name>".>
<需要子 agent 时：在全新上下文里启动子 agent，把它需要的材料完整写进 prompt。>

完成条件：<……>

## <参考：规则或定义>

<每个分支都要用的平铺规则写在这里。只有部分分支用的，挪到 references/，在这里写一句：>
<在<什么情况>时，读 `references/<file>.md`。>
