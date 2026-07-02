---
name: interview-impact-stories
description: "Interview stories from codebases. Use when the user wants to turn a repository, portfolio project, resume draft, or job target into evidence-backed interview material: project stories, resume bullets, STAR/CAR answers, technical deep dives, role-specific capability framing, or interviewer follow-up prep."
---

# Interview Impact Stories

## Overview

Turn a repository and the user's prompt into evidence-backed interview stories. Optimize for what a strong interviewer can verify and score highly: clear problem framing, credible ownership, technical depth, business or user impact, tradeoffs, results, and crisp answers under follow-up.

## Inputs

Expected inputs may include:

- A repository path, current working directory, uploaded files, or pasted code.
- A pre-prompt from the user describing goals, background, target companies, target role, seniority, language, or desired tone.
- Optional resume, job description, PRD, README, demo link, commit history, issues, screenshots, metrics, or deployment notes.

If the target role or seniority is missing, infer it from the prompt and repository. Ask a concise clarification only when the missing detail would materially change the output.

## Workflow

### 1. Build the Evidence Base

Inspect the repository before writing polished claims. Build an evidence ledger before drafting answers. Prefer fast, broad discovery first, then focused reading:

- Identify product purpose from README, docs, package manifests, route names, screenshots, seed data, tests, deployment config, and domain terms.
- Identify architecture from entrypoints, module boundaries, data models, API routes, background jobs, state management, infra files, and integrations.
- Identify real functionality by reading user-facing flows, tests, examples, CLI commands, controllers, components, services, schemas, and configuration.
- Identify quality signals from tests, validation, error handling, observability, CI, security boundaries, migrations, performance work, accessibility, and operational scripts.
- Check git history, issues, or changelog when available to infer evolution, ownership, and before/after changes.

Keep an evidence ledger while reading:

```markdown
| Claim candidate | Evidence | Confidence | Gaps |
|---|---|---:|---|
| [What seems true] | [file paths, commit, tests, docs, observed behavior] | High/Medium/Low | [what to ask or verify] |
```

Use file paths, commit references, or concrete code concepts as evidence. Do not invent metrics, scale, users, revenue, latency, ownership, or production usage.

Completion criterion: do not draft final interview material until the ledger covers product purpose, at least one user-facing or operator-facing flow, architecture boundaries, quality signals, and gaps. If the repository does not contain enough evidence for one of these, record the missing evidence explicitly.

### 2. Derive the Project Story

For each strong project or feature, fill this story spine:

- Problem: what user, business, operational, or developer pain the work addressed.
- Context: who used it, why it mattered, and what constraints existed.
- Contribution: what the candidate personally built or would credibly claim, separated from team or framework behavior.
- Technical core: architecture, algorithms, data model, protocols, integrations, UX flows, infra, tests, or automation that made the work non-trivial.
- Decisions: key tradeoffs, rejected alternatives, and why the chosen approach fit the constraints.
- Result: measured outcome if present; otherwise observable outcome such as enabled workflow, reduced manual steps, improved reliability posture, added capability, or made future change easier.
- Proof: files, tests, screenshots, docs, or demo behavior supporting the story.

Completion criterion: every selected story has a concrete contribution, a technical core, a result or defensible effect, and proof. Drop or mark as "needs confirmation" any story missing two or more of those parts.

### 3. Score Like an Interviewer

Prioritize stories that score well on at least three dimensions:

- Business or user relevance: the answer explains why the work mattered beyond "I used technology X."
- Ownership clarity: the answer says what the candidate did, not just what the app contains.
- Technical depth: the interviewer can ask follow-ups about design, data flow, edge cases, failure modes, and tradeoffs.
- Complexity under constraints: the work involved ambiguity, scale, integration, reliability, performance, security, UX, migration, or maintainability pressure.
- Outcome credibility: the result is specific and defensible, even if not numeric.
- Reflection: the answer includes what changed, what was learned, and what would be improved next.

Downgrade stories that are mostly CRUD, library setup, cosmetic UI, copied boilerplate, or claims with no evidence unless they can be reframed around real constraints or outcomes.

Completion criterion: select the strongest stories by score, not by file size or implementation volume. For each selected story, name the interview dimension it demonstrates best.

### 4. Tailor to the Target Role

Map the same evidence differently by role:

- Backend: data modeling, API design, consistency, throughput, reliability, security, observability, operational simplicity.
- Frontend: product thinking, interaction quality, state management, accessibility, performance, design-system consistency, user feedback loops.
- Full-stack: end-to-end ownership, integration boundaries, product delivery, data flow, deployment, cross-layer debugging.
- AI/ML or agent roles: evaluation, prompt/tool architecture, retrieval, data pipelines, model constraints, failure analysis, safety, measurement.
- Platform/infra: deployment, automation, CI/CD, scalability, cost, security, developer experience, incident prevention.
- Early-career roles: learning velocity, decomposition, testing discipline, debugging, collaboration, and ability to explain fundamentals.
- Senior roles: ambiguous problem framing, architecture tradeoffs, mentoring, cross-team impact, risk management, and long-term maintainability.

Use the user's preferred interview language. If not specified, answer in the user's language.

Completion criterion: each final story must make the role-relevant capability explicit. Avoid generic "full-stack project" phrasing when the target role implies a sharper capability.

## Output Structure

Adapt the format to the request, but default to this structure:

```markdown
## Interview Positioning
[2-4 sentences: what this project proves about the candidate for the target role.]

## Best Stories
### 1. [Story title]
- Interview use: [behavioral / technical deep dive / resume / system design / leadership]
- What I built: [candidate-centered claim]
- Business/user context: [why it mattered]
- Technical substance: [architecture and implementation depth]
- Result/effect: [measured or defensible observed outcome]
- Evidence: [files, tests, docs, commits, or observed behavior]
- Strong answer: [60-90 second answer in STAR/CAR form]
- Likely follow-ups: [3-5 interviewer questions]
- How to answer follow-ups: [specific talking points]

## Resume Bullets
- [Action verb + technical contribution + business/result evidence]

## Technical Deep Dive Bank
- Architecture:
- Data flow:
- Tradeoffs:
- Failure modes:
- Testing/quality:
- Performance/security/reliability:

## Gaps To Confirm
- [Questions or missing metrics that would make the story stronger]
```

For a quick request, produce only the strongest 3-5 stories and the best resume bullets. For a thorough request, include all sections.

Completion criterion: the output must contain enough evidence for the user to defend the answer under follow-up. If evidence is weak, surface gaps instead of polishing the claim.

## Answer Quality Rules

- Lead with the problem and outcome before naming tools.
- Replace vague claims with concrete mechanisms: not "improved performance," but "reduced redundant client fetches by centralizing cache invalidation" if the code supports it.
- Separate facts, inferences, and suggested wording. Mark uncertain claims as "needs confirmation."
- Prefer "I designed/implemented/debugged/validated" only when ownership is supported by the user's prompt, commit history, or explicit instruction.
- If no real metrics exist, offer metric-ready phrasing such as "reduced manual review steps" or "made X workflow possible," and list what data would quantify it.
- Keep answers defensible under follow-up. Every polished answer should have at least one concrete file, component, test, decision, or behavior behind it.
- Include at least one tradeoff or limitation for each major story; perfect-sounding answers are less credible.
- Do not overfit to buzzwords. Use role keywords only when the repository evidence supports them.

## Common Gotchas

- Do not summarize the repository like documentation. Convert facts into interview value.
- Do not output only "亮点." Also produce the reasoning, evidence, answer scripts, follow-up preparation, resume wording, and missing proof.
- Do not assume production scale, users, revenue, latency, or business impact from code alone.
- Do not bury weak evidence. Say what is observed and what the candidate should confirm.
- Do not treat framework defaults as candidate achievement unless the candidate customized, integrated, operated, or made a meaningful decision around them.
