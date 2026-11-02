---
type: regex
target: { source: file, path: release-notes/SKILL.md }
pattern: '(?=[\s\S]*Release notes skill\.)(?=[\s\S]*Understand them well)(?=[\s\S]*Make sure the quality is good)(?=[\s\S]*NEVER use emoji \(this is important\))'
match: contains
weight: 1
---

release-notes/SKILL.md still has the lines a fix would change first
