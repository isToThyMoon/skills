# 维护说明

本文件面向维护本技能的人；运行技能的 agent 只读 `SKILL.md` 及其引用的 `references/`。

## 行为测试

`evals/evals.json` 提供带语料的测试案例。验证蒸馏流程时，在临时目录和独立上下文中运行案例的请求，检查实际生成的文件与试写；预期结果留给评估环节。带 `usage_test` 的案例在生成后另开上下文，按给定话轮逐个发送，检验生成物的使用效果。案例文件本身只是定义，执行记录另存。

## 评分校准

复核评审规则时，把 `evals/calibration-inputs.json` 单独交给评审，再由检查者对照 `evals/calibration-expected.json`；预期文件留在评审之外。控制项只验证规则应用，写作效果另评。

## 历史运行

- [2026-09-11 Luna 运行报告](evals/reports/2026-09-11-luna/report.md)：首次两阶段试跑，记录生成、装载、匿名比较、用户拒绝两个候选及重跑中断的边界。
- [补完报告](evals/reports/2026-09-11-luna/completion-report.md)：剩余测试的执行结果。

`evals/reports/` 目前随仓库分发，约 330KB，主要是 artifacts JSON。
