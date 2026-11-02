---
tags: [write-a-skill]
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

帮我写一个 skill：每周五我都要把当前仓库最近 7 天的 commit 按主题整理成一份中文周报（markdown），分"新功能 / 修复 / 重构 / 其他"四块，每条一句话加 commit 短 hash，最后列出这周改动最多的三个目录。之前都是我手动让你做的，经常漏掉 merge commit 的处理规则（merge commit 不单独列）和作者过滤（只要我自己的，邮箱 me@example.com）。放在 ./skills/weekly-digest 下。直接做，不用问我。
