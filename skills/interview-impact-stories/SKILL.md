---
name: interview-impact-stories
description: "Interview project stories from evidence. Use when the user wants to turn repositories, project notes, resumes, job descriptions, PRDs, docs, screenshots, metrics, demos, or other materials into impressive, defensible interview material. First reconstructs and, when necessary, clarifies the actual project type and requested analysis boundary; only then benchmarks the comparable project or subsystem against a blind best-practice reference design. Outputs a paste-ready resume project block, a deep-dive defense bank, and labeled extension items（可拓展项）with the cost to make each solid."
---

# Interview Project Stories

Turn project evidence and the user's prompt into interview material that survives a strong interviewer: clear problem framing, technical depth, impact, tradeoffs, and crisp answers under follow-up. Convert facts into interview value — never summarize the materials like documentation.

Evidence is the floor, not the goal. Anchoring and pruning exist to prevent collapse under grilling; the goal is material that is rich and substantial — every kept claim gains context: why it was needed, what it replaced, what the mainstream alternative is, what it teaches. A deliverable that is merely defensible but thin has failed.

## Analysis Scope and Ownership

Separate the object being analyzed from the experience being attributed:

- **Project-level analysis** — when the user asks about a whole project, module, or feature, cover that requested object regardless of commit authorship. Use git history to reconstruct requirements, evolution, and incidents — not to infer personal ownership.
- **Candidate-level packaging** — use first-person ownership wording only for the scope the user says they owned. Take the user's scope at face value; do not run authorship forensics or infer ownership from commit authors. Keep whole-project capabilities at project level until the user asks to convert them into personal resume claims.

Robustness under grilling comes from mastery of every claimed mechanism, decision, and failure. Framework defaults still are not achievements unless the project made a real decision around them.

## Claim Tiers

Every claim in the output belongs to one of three tiers. The tier label is for the user's eyes; it never appears in resume text.

- **Fact** — anchored to a file, commit, test, doc, metric, or user-confirmed context. Numbers cite their source or degrade to a magnitude word.
- **Reframe** — a fact packaged stronger: sharper mechanism, honest outcome wording ("enabled X workflow", "removed Y manual step", metric-ready phrasing). Never introduces a new fact.
- **Extension（可拓展项）** — goes beyond current facts. When real highlights fall short, do not stop at the facts: propose extensions the project could credibly support — features spoken as designed/planned/partially built, metrics not yet measured, hardening or scale-up work framed as roadmap. Each extension states: (1) suggested wording calibrated to distance from reality（已设计 / 规划中 / 已在小范围验证）, (2) 坐实成本 — the smallest concrete action (a script, a measurement, a design writeup, a rehearsal) that promotes it to Fact, (3) the follow-up an interviewer would ask and how to answer it today.

Extensions are a deliverable, not a compromise: a thin project plus well-chosen extensions with closing costs is exactly what this skill is for. The one hard line: metrics, users, revenue, incidents, and production usage that never happened are flagged as such to the user — the user decides how far to push the wording.

An adjacent capability that lies outside the requested object or available evidence is **Unknown / Out of scope**, not automatically a gap or Extension candidate.

## Workflow

1. **Intake** — Identify target role, seniority, output language, available materials (repo, notes, PRD, resume draft, JD), requested analysis object (whole project / subsystem / module / feature), and whether the output is project-level analysis or candidate-level packaging. The user's explicit scope is binding; expand it only after user confirmation. Separate classification-blocking questions from packaging-only questions: ownership, metrics, seniority, and other facts that affect wording but not project classification can wait until packaging. Ask only when an answer would materially change the current stage.
2. **Recon before classification** — Explore the materials before committing to a project type. For a thorough pass, run independent lanes (subagents when available; sequential otherwise, keeping notes separate): product/domain (users, jobs, workflows, business value), implementation (architecture, boundaries, one end-to-end vertical trace, non-trivial mechanisms), quality/evolution (tests, evals, observability, deploy, git stages, incidents). Each lane returns what the requested object actually does, what evidence sources cover, plausible classifications with confidence, claim candidates, and weak spots. Follow the requested object's dependency closure only as far as needed to explain it: direct dependencies are supporting evidence; unrelated consumers, neighboring modules, and broader platform capabilities remain outside scope.
3. **Classification gate** — Build an evidence-backed project frame with five fields: (a) requested analysis object, (b) target users or consumers, (c) primary job or outcome, (d) system/subsystem kind, and (e) material coverage and boundaries. A label in the prompt is a clue, not sufficient classification by itself.
   - If recon supports one frame strongly and alternatives would not change the reference design or story ranking, state the frame and continue.
   - If two or more plausible frames would produce materially different core-value lists, or the requested object/boundary is unclear, ask 1–3 concise clarification questions and wait. Do not launch the blind reference yet.
   - Resolve uncertainty from local evidence first; interact with the user when it cannot be resolved safely. Never turn absence from one artifact into absence from the whole project.
   - Treat two or more independent, consistent evidence sources (for example code structure plus design docs or tests) as sufficient when no competing classification would change the ranking. Do not ask the user to reconfirm evidence that is already clear.
   - Check evidence coverage separately from classification. If the requested object is broader than the materials, ask the user to choose among supplying more evidence, narrowing the analysis object, or continuing project-level analysis with the uncovered areas explicitly marked Unknown. This choice is required only when coverage would materially distort the comparison or deliverable.
4. **Reference design (blind, after the gate)** — Only after classification and evidence coverage are settled, run an independent agent that has NOT seen the implementation. Give it a scope contract: the confirmed project frame, requested object, material boundary, target role, known material constraints, and the object's major covered components — but no project solution details. It must design the **comparable object at the same abstraction level and functional coverage**, neither selecting only its most fashionable subpart nor expanding into an unconstrained whole system. Omit unknown team size, scale, or timeline unless they would materially change the reference; do not ask merely to fill the reference prompt. Source best-practice claims where possible; mark the rest as reasoning. Do not run this step in parallel with Recon or the Classification gate.
5. **Evidence ledger** — Before drafting, consolidate: claim / evidence / confidence / status / gap. Status distinguishes **Present**, **Missing within scope**, **Unknown**, and **Out of scope**. Only Missing within scope is a project gap by default; Unknown and Out of scope must not be rewritten as failure. An Unknown can become an Extension only after new evidence or explicit user confirmation establishes that it was designed, planned, or partially built.
6. **Select stories** — Rank candidates against the core-value list produced for the confirmed object. Prefer stories strong on at least three of: user or business relevance, candidate-centered decisions (for candidate packaging), technical depth under follow-up, complexity under constraints, credible outcome, reflection. Fewer strong stories beat many weak ones; downgrade CRUD/boilerplate/setup work unless real constraints make it substantive. Generate Extensions only from evidence-backed opportunities and Missing-within-scope gaps that directly improve the confirmed object's primary job or success condition. Never use neighboring code or Unknown capabilities to fill the story quota.
7. **Challenge** — Two adversarial passes (subagents when available): a reviewer attacks technical claims (real decision vs ordinary detail vs framework default; the one follow-up that would break each claim), an interviewer attacks the narrative (hook, role fit, seniority read, trap questions). Extensions go through the same passes. Disposition per claim: **Keep / Narrow / Extend / Drop**. Nothing ships unchallenged.
8. **Package and tailor** — Derive emphasis from the confirmed project frame, target role/JD, and evidence; do not use a fixed domain checklist as a substitute for exploration. Output in the user's language; keep code identifiers unchanged. Project-level analysis may cover the whole requested object; personal resume wording remains limited to user-confirmed ownership.
9. **Compliance audit** — Before shipping, verify: the first-screen framing matches the classification gate; the reference compared the same object and abstraction level; Unknown/Out-of-scope items were not presented as project gaps; every resume bullet has a deep-dive entry; extensions carry all three required parts; and the draft follows Output Language and Resume Writing Rules. Fix violations, then ship.

## What Counts as High Value

- Highlights are defined by the confirmed analysis object, its users, primary job, success conditions, and constraints — not by generic engineering merit or a domain label alone. The core list comes from the post-gate blind reference design, not from a hard-coded checklist or ad-hoc guessing.
- Whole-system success factors do not automatically become headline criteria for a subsystem. Compare like with like: project to project, subsystem to subsystem, module to module, feature to feature.
- Transplant test: a claim that could sit unchanged in an unrelated project's resume (deploy pipeline, login automation, logging, generic test counts) is supporting evidence — it hardens core claims but never leads the resume or takes a headline slot while core-domain material is still on the table.
- Slot order: core-domain decisions with their evals and incidents first; product judgment specific to this system next; generic reliability/delivery last, at most one slot. Role tailoring reorders within this ranking; it inverts it only when the target role is itself about the generic layer (platform/infra).

## Output Language

- Name the deliverable's parts by what they are for, in plain words. This skill's process vocabulary (story, bullet, layer, tier names) never appears in user-facing titles or prose.
- No self-coined compressed jargon: a label invented during the analysis to compress an idea does not ship — write out what the thing does in ordinary words instead. Established technical and architectural terms are not jargon and stay as-is; do not paraphrase them.
- The test: would the target interviewer already know this term without reading the document? Yes → keep it. It only means something because this document coined or implied it → replace it with its meaning.

## Output Structure

Two layers plus extensions and evidence to confirm. Layer 1 is the headline deliverable; every Layer 1 bullet maps to a Layer 2 entry. For a quick request: Layer 1 + the strongest Layer 2 entries + top extensions.

The deliverable opens with two lines the user can veto at a glance: the confirmed analysis object and boundary, and the core-value list (from the comparable reference design) that selection was ranked against. A wrong framing must be visible on the first screen, not discoverable five bullets in.

### Layer 1 — Resume block（整体面，可直接粘贴）

```markdown
### [Project name]
[Positioning line: what it is + who uses it + verifiable scale]
[Candidate-level only: Role line 负责/独立完成 + user-confirmed parts] ｜ [optional 技术栈 line]
- [2-6 bullets per the Resume Writing Rules]
```

In project-level analysis without confirmed ownership, use a project-capability block and omit personal Role wording. Candidate-level packaging requires user-confirmed scope. One version per target role is produced by reordering and re-emphasizing bullets — new claims enter only through the Extension path.

### Layer 2 — Deep-dive bank（细节面）

One entry per Layer 1 bullet:

- 60-90 second spoken answer, problem and outcome first.
- Mechanism detail with file/commit anchors — what the candidate must explain without notes.
- Tradeoffs, rejected alternatives, and the trigger condition that would flip each decision. At least one limitation per story — perfect-sounding answers are less credible.
- Incidents as retellable root-cause timelines.
- Best-practice comparison (from the reference design): what the mainstream approach is, and whether this project matches it, deliberately diverges (say why under its constraints), or plans to catch up.
- Business context: why it mattered beyond the technology.
- 3-5 skeptical follow-ups with defensible answers.
- Boundary: what not to claim; the honest fallback when challenged on missing metrics, scale, or production usage.

### 可拓展项（Extensions）

The labeled extension list per Claim Tiers — suggested wording, 坐实成本, today's answer to the obvious follow-up. Order by impact-to-cost ratio.

### Quick-reference sheet（速查，optional but recommended for a thorough pass）

Interview-day material that belongs to no single bullet: a 30-second opening (one product-value version, one technical version), a usable-numbers table (each number: source + can/cannot use), red lines (things to fix or never say), prepared answers to the predictable cross-project questions (why no framework, small eval set, no business metrics, solo project, AI-assisted), and a pre-interview checklist.

### Evidence and facts to confirm

Unknown capabilities, missing evidence, ownership scope, or numbers needing the user's confirmation. Keep these distinct from Missing-within-scope project gaps.

## Resume Writing Rules

Distilled from community-validated practice (Google XYZ formula, Harvard/MIT guides, The Tech Resume Inside Out, Cracking the Coding Interview, Tech Interview Handbook, r/EngineeringResumes wiki, 掘金/牛客 STAR consensus). Apply to Layer 1 verbatim; rewrite any draft line that violates them.

### Positioning line

- One line, three things: what the system is, who uses it, at what verifiable scale. No defensible number → omit scale, don't pad.
- Role declared once here (负责 vs 参与 honestly, naming owned parts); bullets never restate the role.
- Personal projects carry a clickable link in presentable state; tutorial clones and coursework are not standalone projects.

### Bullets

- One sentence: strong verb + concrete mechanism + quantified result. XYZ/CAR/PAR/STAR are thinking frames — on paper each compresses to this single-sentence shape.
- Every bullet carries a verifiable number (%, time, count, scale) or a checkable qualitative result; otherwise delete it. Front-load the metric or most striking fact.
- 1-2 lines each, target one; no orphan-word wraps, no sub-bullets, no paragraphs.
- 2-6 bullets: 3-6 is preferred for a full project; 2 is acceptable for a narrow module or feature. Never expand the requested scope or use neighboring capabilities to reach a bullet count. Order of precedence: the High Value slot order first (core-domain before generic), then relevance to the target role, then strength — the first bullet is the strongest core claim.
- Name the technologies that did the real work inline; a separate 技术栈 line doesn't excuse tech-free bullets.
- No personal pronouns（I/we/我/我们）. No decorative adjectives/adverbs（成功地/高效地）— numbers carry the weight. Verifiable technical verbs (implemented, reduced, 设计, 定位修复); no weak verbs (helped, participated, 协助) or hype verbs (revolutionized, 颠覆) for ordinary changes.

### Anti-patterns (any occurrence fails the draft)

- Responsibility lists / job-description prose; paragraphs instead of bullets.
- Tech-name pileups with no mechanism.
- Action with no result, or a result with neither number nor checkable effect.
- Team achievements not split into personal contribution.
- Numbers without a Layer 2 entry stating measurement method and baseline.
- Skill self-rating tables（精通/熟悉/了解）as achievement content.

### zh/en divergences (resolved defaults)

- 负责/参与 lives in the role line; bullets start with verbs in both languages.
- Keep the 技术栈 line for Chinese-market resumes; embed working tech in bullets regardless.
- Where verb lists conflict, side with engineering communities: verifiable technical verbs over momentum verbs.
- STAR is for collecting material and spoken answers; on the resume it always compresses to the one-sentence formula.
