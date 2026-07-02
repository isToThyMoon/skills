---
name: interview-impact-stories
description: "Interview project stories from evidence. Use when the user wants to turn repositories, project notes, resumes, job descriptions, PRDs, docs, screenshots, metrics, demos, or other materials into impressive but defensible interview material: project story packaging, experience deepening, resume bullets, STAR/CAR answers, technical deep dives, reviewer challenges, candidate-ready answer boundaries, and follow-up prep."
---

# Interview Project Stories

## Overview

Turn project evidence and the user's prompt into impressive, evidence-backed interview stories. Optimize for what a strong interviewer can verify and score highly: clear problem framing, credible ownership, technical depth, business or user impact, tradeoffs, results, and crisp answers under follow-up.

## Inputs

Expected inputs may include:

- A repository path, current working directory, uploaded files, or pasted code.
- Project notes, resume drafts, job descriptions, PRDs, README/docs, demo links, commit history, issues, screenshots, metrics, deployment notes, or user-provided work context.
- A pre-prompt describing goals, background, target companies, target role, seniority, language, or desired tone.

If the target role or seniority is missing, infer it from the prompt and materials. Ask a concise clarification only when the missing detail would materially change the output.

## Workflow

### 1. Triage the Inputs

Identify the target role, seniority, interview language, available repository/materials, and whether the user wants a quick pass or a thorough pass. Default to a thorough pass when the user asks for resume-ready, interview-ready, or high-confidence material.

Completion criterion: before material analysis starts, know the target role or record the inferred role, know the output language, and know which materials are available.

### 2. Run Parallel Material Reconnaissance

For a thorough pass, use independent subagents when the client supports them. If subagents are unavailable, run the same lanes sequentially and keep their notes separate until synthesis. Do not let one lane see another lane's conclusions before it has produced its own evidence.

Default lanes:

- Product/domain lane: identify users, workflows, business context, core features, demos, docs, domain terms, and externally visible value.
- Implementation/evidence lane: identify code architecture when available; otherwise extract concrete work from project notes, PRDs, docs, screenshots, metrics, demos, and user context.
- Quality/evolution lane: identify tests, validation, errors, security, observability, performance, CI/CD, migrations, git history, issues, changelog, before/after evolution, or non-code evidence of delivery and quality.

Each lane returns:

```markdown
## Lane: [name]
- What the system does:
- Strong claim candidates:
- Evidence:
- Gaps or weak claims:
- Files/commits/docs inspected:
```

Completion criterion: each lane has inspected different evidence and produced claim candidates with citations to files, commits, tests, docs, screenshots, metrics, demos, or user-confirmed context. If only one agent is available, the final notes still separate the three lanes.

### 3. Build the Evidence Base

Inspect the available materials before writing polished claims. Build an evidence ledger before drafting answers. Prefer fast, broad discovery first, then focused reading:

- Build a project map naming product purpose, target users, workflows, stack or tools when available, main deliverables, integrations, data or content handled, quality signals, deployment/runtime or delivery shape, and obvious gaps.
- If code is available, trace at least one real vertical flow end to end: UI/CLI/API entrypoint -> validation or state change -> domain/service logic -> persistence or external call -> response/error handling -> test or observable behavior.
- If code is not available, trace at least one real work flow end to end: requirement or problem -> user/business constraint -> candidate action -> artifact/deliverable -> feedback/outcome -> follow-up work.
- Run a default/boilerplate audit: separate custom candidate decisions from scaffolded code, generated files, templates, library defaults, conventional setup, or team-owned context.
- Check git history, issues, changelog, PR notes, docs, metrics, screenshots, user notes, or blame for ownership and evolution. If unavailable, too noisy, or outside scope, record that limitation in the ledger.

Keep an evidence ledger while reading:

```markdown
| Claim candidate | Evidence | Source type | Confidence | Gaps |
|---|---|---|---:|---|
| [What seems true] | [files, commits, tests, docs, screenshots, metrics, demos, runtime behavior, user confirmation] | code/docs/test/git/runtime/product/user | High/Medium/Low | [what to ask or verify] |
```

Use concrete artifacts as evidence: file paths, commit references, code concepts, docs, PRDs, screenshots, metrics, demos, tickets, or user-confirmed work context. High-confidence final claims need at least one concrete artifact plus one corroborator when available. Do not invent metrics, scale, users, revenue, latency, ownership, or production usage.

Completion criterion: do not draft final interview material until the ledger contains a cited project map, one traced code or work flow, technical or delivery boundaries, quality signals, ownership/evolution evidence or a recorded reason it is unavailable, and explicit gaps. If any category is missing, carry it forward as a gap rather than compensating with polished wording.

### 4. Derive the Project Story

For each strong project or feature, fill this story spine:

- Problem: what user, business, operational, or developer pain the work addressed.
- Context: who used it, why it mattered, and what constraints existed.
- Contribution: what the candidate personally did, using explicit user input, commit history, or other evidence. If ownership is not proven, label it as team/app behavior and avoid "I designed" or "I built."
- Technical core: architecture, algorithms, data model, protocols, integrations, UX flows, infra, tests, or automation that made the work non-trivial.
- Decisions: key tradeoffs, rejected alternatives, and why the chosen approach fit the constraints.
- Result: measured outcome if present; otherwise an observable before/after effect tied to a concrete mechanism, such as removed manual steps, enabled a user flow, prevented a known failure mode, simplified a change path, or added validation/tests around a risky path.
- Proof: files, tests, screenshots, docs, or demo behavior supporting the story.

Completion criterion: every selected story has a concrete contribution, a technical core, a result or defensible effect, and proof. Drop or mark as "needs confirmation" any story missing two or more of those parts.

### 5. Score Like an Interviewer

Prioritize stories that score well on at least three dimensions:

- Business or user relevance: the answer explains why the work mattered beyond "I used technology X."
- Ownership clarity: the answer says what the candidate did, not just what the app contains.
- Technical depth: the interviewer can ask follow-ups about design, data flow, edge cases, failure modes, and tradeoffs.
- Complexity under constraints: the work involved ambiguity, scale, integration, reliability, performance, security, UX, migration, or maintainability pressure.
- Outcome credibility: the result is specific and defensible, even if not numeric.
- Reflection: the answer includes what changed, what was learned, and what would be improved next.

Downgrade stories that are mostly CRUD, library setup, cosmetic UI, copied boilerplate, or claims with no evidence unless they can be reframed around real constraints or outcomes.

Completion criterion: select the strongest stories by score, then strip or downgrade any individual claim that lacks proof. For each selected story, name the interview dimension it demonstrates best and the weakest claim an interviewer is likely to challenge.

### 6. Challenge the Claims

Run a red-team challenge pass before final output. Use separate subagents when available; otherwise run both roles sequentially and keep their objections separate.

- Reviewer challenge: attack technical accuracy, missing evidence, inflated ownership, framework-default claims, unsupported metrics, architecture misunderstandings, and shallow tradeoffs.
- Interviewer challenge: attack business value, seniority signal, story clarity, follow-up durability, credibility under pressure, and whether the answer sounds like real ownership.

For each claim, ask:

- What exact follow-up would expose this as vague, inflated, or unsupported?
- What file, commit, test, behavior, or user flow proves it?
- Is this candidate-owned, team-owned, framework-default, or merely app-contained?
- What is the strongest defensible version of the claim if metrics or ownership are missing?
- What limitation, tradeoff, or failure mode should the candidate be ready to admit?

For every major claim, choose one disposition:

- Keep: evidence is strong and the claim is interview-worthy.
- Narrow: claim is directionally true but wording overreaches.
- Move to gaps: claim needs user confirmation, metric data, or stronger proof.
- Drop: claim is generic, unsupported, or not useful for the target role.

Completion criterion: no resume bullet, STAR/CAR answer, or deep-dive point survives unless it has passed both reviewer and interviewer challenge, been narrowed to a defensible version, or is explicitly labeled "needs confirmation."

### 7. Deepen and Package the Experience

Package the project into an eye-catching interview experience. Do not stop at defensive accuracy. Summarize, expand, and deepen the raw work into a stronger narrative by surfacing the problem, constraints, hidden complexity, design choices, tradeoffs, learning, and role-relevant capability signals. Keep the packaging defensible: do not invent scale, ownership, metrics, users, revenue, latency, or production impact.

Use these deepening moves:

- Lift raw work into a project narrative: requirement -> constraint -> technical difficulty -> decision -> implementation -> outcome -> reflection.
- Turn implementation details into capability signals: debugging, decomposition, integration, system design, reliability thinking, product sense, testing discipline, learning speed, or cross-layer ownership.
- Add adjacent depth the user can discuss: plausible alternatives, rejected approaches, tradeoffs, failure modes, future improvements, and metrics that would prove impact.
- Translate weak results into honest outcomes: enabled a workflow, reduced manual steps, clarified system behavior, improved maintainability, added a safety check, or made future work easier.

For each selected story, produce four layers:

- Polished story: the strongest concise version suitable for resume or interview.
- Deepening angles: technical, product, architecture, reliability, or collaboration angles that make the work more memorable.
- Follow-up depth: concrete implementation details, tradeoffs, failure modes, and next improvements the candidate should be ready to explain.
- Boundary: what not to claim, what to say if asked about missing scale/metrics/ownership, and which facts need user confirmation.

If the project is not inherently impressive, still make it valuable. Reframe it around practical signals and thoughtful engineering. A modest project can become strong interview material when the candidate clearly explains the problem, why the implementation was non-trivial, what tradeoffs were made, how quality was protected, and what would be improved next.

Completion criterion: every final story must feel intentionally shaped, not merely summarized. It should include a polished narrative, at least one deepening angle, and a safe boundary. The user should be able to sound impressive without being trapped by a realistic follow-up.

### 8. Tailor to the Target Role

Map the same evidence differently by role:

- Backend: data modeling, API design, consistency, throughput, reliability, security, observability, operational simplicity.
- Frontend: product thinking, interaction quality, state management, accessibility, performance, design-system consistency, user feedback loops.
- Full-stack: end-to-end ownership, integration boundaries, product delivery, data flow, deployment, cross-layer debugging.
- AI/ML or agent roles: evaluation, prompt/tool architecture, retrieval, data pipelines, model constraints, failure analysis, safety, measurement.
- Platform/infra: deployment, automation, CI/CD, scalability, cost, security, developer experience, incident prevention.
- Early-career roles: learning velocity, decomposition, testing discipline, debugging, collaboration, and ability to explain fundamentals.
- Senior roles: ambiguous problem framing, architecture tradeoffs, mentoring, cross-team impact, risk management, and long-term maintainability.

Use the requested output language. If the user writes or asks in Chinese, produce Chinese interview material; if the user asks for English, produce English. Keep evidence labels and code identifiers unchanged when translating.

Completion criterion: each final story must make the role-relevant capability explicit. Avoid generic "full-stack project" phrasing when the target role implies a sharper capability.

## Output Structure

Adapt the format to the request, but default to this structure:

```markdown
## Interview Positioning
[2-4 sentences: what this project proves about the candidate for the target role.]

## Best Stories
### 1. [Story title]
- Interview use: [behavioral / technical deep dive / resume / system design / leadership]
- Capability signal: [what this proves for the target role]
- What I built: [candidate-centered claim]
- Business/user context: [why it mattered]
- Technical substance: [architecture and implementation depth]
- Result/effect: [measured or defensible observed outcome]
- Evidence: [files, tests, docs, commits, or observed behavior]
- Challenge result: [kept / narrowed / needs confirmation, and why]
- Strong answer: [60-90 second answer in STAR/CAR form]
- Deepening angles: [ways to make the story more memorable: architecture, tradeoffs, failure modes, alternatives, product value, metrics to confirm]
- Safe boundary: [what not to overclaim, and how to answer if asked about missing metrics, scale, ownership, or production usage]
- Skeptical follow-ups: [3-5 questions that test ownership, tradeoffs, edge cases, scale, failure modes, and whether the claim is inflated]
- Defensible answers: [specific talking points, evidence, and what not to overclaim]

## Resume Bullets
- [Action verb + technical contribution + business/result evidence]

For each bullet, verify action, mechanism, scope, result, and proof. Do not output bullets that are only action + technology with no mechanism or effect.

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

For a quick request, shorten the output to the strongest 3-5 stories and best resume bullets, but still complete the evidence ledger gate before drafting. For a thorough request, include all sections.

Completion criterion: before final output, run a claim audit. Every polished claim must be marked as Fact, Inference, or Suggested Wording. Facts need evidence; inferences need reasoning and caveats; suggested wording must avoid unsupported ownership, metrics, scale, users, revenue, latency, and production usage.

## Answer Quality Rules

- Lead with the problem and outcome before naming tools.
- Replace vague claims with concrete mechanisms: not "improved performance," but "reduced redundant client fetches by centralizing cache invalidation" if the code supports it.
- Separate facts, inferences, and suggested wording. Mark uncertain claims as "needs confirmation."
- Prefer "I designed/implemented/debugged/validated" only when ownership is supported by the user's prompt, commit history, or explicit instruction.
- If no real metrics exist, offer metric-ready phrasing such as "reduced manual review steps" or "made X workflow possible," and list what data would quantify it.
- Every polished claim must cite at least one concrete file, component, test, commit, decision, or observed behavior; otherwise mark it as inference or needs confirmation.
- Include at least one tradeoff or limitation for each major story; perfect-sounding answers are less credible.
- Do not overfit to buzzwords. Use role keywords only when the available evidence supports them.
- Prefer fewer strong stories over many weak ones. A story that cannot survive reviewer and interviewer challenge should become a gap or be dropped.
- Deepen ordinary work through context, mechanism, tradeoff, alternatives, failure modes, and reflection. The goal is impressive framing grounded in reality, not flat conservatism.

## Common Gotchas

- Do not summarize the materials like documentation. Convert facts into interview value.
- Do not output only "亮点." Also produce the reasoning, evidence, answer scripts, follow-up preparation, resume wording, and missing proof.
- Do not assume production scale, users, revenue, latency, or business impact from code alone.
- Do not bury weak evidence. Say what is observed and what the candidate should confirm.
- Do not treat framework defaults as candidate achievement unless the candidate customized, integrated, operated, or made a meaningful decision around them.
- Do not hand the user impressive wording they cannot defend from their actual work. Pair strong packaging with safe fallback answers for likely follow-ups.
