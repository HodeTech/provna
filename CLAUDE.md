# Claude agent guide — Provna

This file is the entry point for Claude-based AI agents (Claude Code, the Claude API,
subagents) working in this repository. **Read it fully before taking any action.** Other
AI agents should read [AGENTS.md](AGENTS.md), which points back here.

## What this project is

**Provna** is a **vendor-neutral runtime control plane** that turns every WRITE action an
agent takes in regulated enterprise systems into a contract that is *reversible, authorized,
information-flow-controlled, and regulator-grade provable.* Technically it is a Policy
Enforcement Point (PEP) + a transaction (saga) coordinator + a tamper-evident evidence
ledger. Metaphor: **escrow for agent actions.** Frame: it does not sell a security tool, it
sells **permission to ship** an agent into a system where a wrong write has consequences.
Tagline: *Provna — every agent action, proven.*

**The atomic unit is the *guarded saga step*** — every side-effecting call passes four gates
in a fixed order:

| Gate | Pillar | What it does |
|---|---|---|
| **Gate 1** | **S1 — Information-Flow Control** | Deterministic, architectural defense against prompt injection (lattice + sink-policy; not a classifier). |
| **Gate 2** | **S3 — Runtime Authorization** | AND-gate (agent AND user AND delegation AND intent) + behavioral/temporal admission. |
| **Gate 3** | **S2 — Transactional Action Contract** | idempotent → dry-run → HITL → execute → compensate. **The real moat.** |
| **Gate 4** | **S4 — Tamper-Evident Audit** | Merkle + external anchor + signed portable witness, mapped to EU AI Act Article 12/14, DORA, MiFID II. |

> Note the gate↔pillar mapping: **Gate 1 = S1, Gate 2 = S3, Gate 3 = S2, Gate 4 = S4.** It is
> deliberate (authorization precedes the action contract) and easy to mis-state — keep it
> straight. The canonical walk-through is [docs/architecture/action-lifecycle.md](docs/architecture/action-lifecycle.md).

**Status: pre-build / planning phase.** There is **no product code yet.** This repository is
currently a **documentation tree** under [docs/](docs/) — the vision, the four-pillar
architecture, the roadmap, the ADRs, the standards, the business case, the compliance map,
and the risk register. The first build steps (the Phase-0 PoCs) are in
[docs/roadmap/current.md](docs/roadmap/current.md). The planned polyglot monorepo layout is in
[docs/project-structure.md](docs/project-structure.md) and the pinned stack in
[docs/tech-stack.md](docs/tech-stack.md).

The settled technology decisions (2026-06-24) — these are pinned, do not re-open them without
an ADR: **Go-first** data-plane (Go ≥ 1.24, FIPS-in-stdlib); **DBOS** now behind a
`SagaCoordinator` seam with **Temporal** as a triggered contingency; **Cedar-only** PDP for
the MVP with **OpenFGA** deferred behind a `relationship-resolver` seam; **Tessera + an
internal RFC3161 TSA + a cross-org witness** for the S4 anchor; **SeaweedFS** (not MinIO),
**Valkey** (not Redis), **OpenBao** (not Vault); **FIDES/dromedary** consumed as the S1
reference substrate; **gRPC + Connect + buf** for the seam. Rationale lives in
[docs/architecture/tech-stack-analysis.md](docs/architecture/tech-stack-analysis.md).

## Non-negotiable rules for AI agents

These apply to every AI agent in this repo, regardless of model or tool.

1. **Language policy — the distinctive rule.** All committed/public work is in **English**:
   every doc under `docs/` (except `docs/private/`), every file name, every directory name,
   and all future code. Use **Turkish only** for (a) talking to the maintainer, and (b)
   documents the maintainer *specifically* asks for under `docs/private/`. Never mix Turkish
   into a public doc.
2. **`docs/private/` is gitignored and is NEVER referenced from any public output.** It holds
   the internal competitive teardowns, the framing charter, and the founding report (and they
   are in Turkish). You may *read* it for context, but anything you write into the public tree
   must be **self-contained** — never link to it, never name its files (`provna-cerceve`,
   `initial-report`, the teardown dirs), never write the path `docs/private`. Restate the fact
   instead of citing the source.
3. **Scope discipline — thin but deep.** Provna owns the agent action lifecycle's four gates
   and goes infinitely deep there; it never drifts horizontal. The single test for any feature:
   *"does this make one guarded saga step safer / more reversible / more provable, or does it
   turn Provna into an agent platform?"* If the latter, reject it or consume it. Provna is **not**
   an LLM gateway, an agent framework, a generic PDP, a durable-execution engine, a KYC/AML
   tool, a guardrail/inspection product, or a plain-logging audit tool. See
   [docs/product-scope.md](docs/product-scope.md).
4. **Build vs consume.** BUILD only the white space — the S1 IFC fusion and the S2 compensation
   content (the moat). CONSUME or assemble everything commoditized (durability, the PDP, audit
   infrastructure, eval). **No core dependency or stack change without an ADR.** The canonical
   boundary is [docs/architecture/build-vs-consume.md](docs/architecture/build-vs-consume.md).
5. **Fail-closed and honest by construction.** When designing or describing: fail-closed
   everywhere (an error implies BLOCK, no downgrade path); the deterministic guarantee lives
   *only* in the lattice + sink-policy (an ML classifier is an optional pre-filter, never the
   guarantee); evidence is **regulator-grade forensic-reproducible**, never claimed
   "court-admissible". See [docs/standards/architectural-principles.md](docs/standards/architectural-principles.md).
6. **No false precision.** Market statistics, prices, and dates are cited or marked
   `UNVERIFIED`; opinions are marked `[OPINION]`. Never invent a percentage, a funding figure,
   a benchmark number, or a regulatory date. See the risk register's "fake statistics" red line.
7. **Record non-trivial decisions as ADRs** in [docs/decisions/](docs/decisions/) using the
   condensed MADR form. ADRs are **append-only** — to change one, write a new ADR that
   supersedes it (skill: `supersede-adr`); never rewrite a settled decision in place.
8. **Documentation conventions are binding.** Single H1 + bold metadata lines (no
   front-matter); `kebab-case.md`; **relative links only, never to `docs/private`**;
   `[OPINION]` / `UNVERIFIED` markings; one canonical home per artifact (link, never restate);
   phase-relative milestones, never calendar dates. Full rules:
   [docs/standards/documentation-style.md](docs/standards/documentation-style.md).
9. **Mermaid labels must be ASCII-safe — learned the hard way.** Inside `sequenceDiagram`
   notes/messages do NOT use apostrophes, double-quotes, `;`, `<br/>`, or in-message `->`;
   inside flowchart labels do NOT use apostrophes, and use `<br/>` (never literal `\n`) for line
   breaks. A single stray apostrophe breaks rendering in strict renderers. The `docs-check`
   skill verifies this.

## Where to find things

| Need | Path |
|------|------|
| What & why | [docs/vision.md](docs/vision.md) · [docs/product-scope.md](docs/product-scope.md) · [docs/positioning.md](docs/positioning.md) |
| The pinned stack + the evaluation | [docs/tech-stack.md](docs/tech-stack.md) · [docs/architecture/tech-stack-analysis.md](docs/architecture/tech-stack-analysis.md) |
| Planned monorepo layout | [docs/project-structure.md](docs/project-structure.md) |
| How it is designed (four pillars) | [docs/architecture/](docs/architecture/README.md) |
| Why it is built this way (ADRs) | [docs/decisions/](docs/decisions/README.md) |
| Binding writing rules | [docs/standards/](docs/standards/README.md) |
| What is active now + the phase plan | [docs/roadmap/current.md](docs/roadmap/current.md) · [docs/roadmap/](docs/roadmap/README.md) |
| Who buys it, pricing | [docs/business/](docs/business/README.md) |
| Compliance & risk | [docs/compliance/regulatory-mapping.md](docs/compliance/regulatory-mapping.md) · [docs/risks/risk-register.md](docs/risks/risk-register.md) |
| Recurring agent procedures | [.claude/skills/](.claude/skills/README.md) |
| Project terms | [docs/glossary.md](docs/glossary.md) |

## Reading order

1. [README.md](README.md) — what Provna is.
2. **This file (CLAUDE.md).**
3. [docs/glossary.md](docs/glossary.md) — the vocabulary used everywhere (PEP, IFC, saga, AND-gate, the four pillars).
4. [docs/product-scope.md](docs/product-scope.md) — the hard rules (what it will and will not be).
5. The ADRs in [docs/decisions/](docs/decisions/README.md) in numerical order.
6. [docs/roadmap/current.md](docs/roadmap/current.md) — what is active now.
7. The skill at `.claude/skills/<slug>/SKILL.md` matching your task.

## Build, test, lint

There is **no code yet** — this is a documentation repository in the planning phase. There is
nothing to build, test, or lint. When the monorepo lands, the build commands will live in
[docs/project-structure.md](docs/project-structure.md) and [docs/tech-stack.md](docs/tech-stack.md)
(Go data-plane, Python/TS control-plane, a gRPC `ActionGuard` seam). Until then, the recurring
work is documentation, and the quality gate is the `docs-check` skill, not a compiler.

## Skills

When the maintainer asks for a recurring task — write an ADR, add or update a doc, run the
consistency gate, do a deep review, tear down a competitor, propagate a settled decision —
there is usually a **skill** at `.claude/skills/<slug>/SKILL.md` describing the correct
procedure step by step. Read the skill in full and check its done-criteria before finishing.
Skills cite the standards and ADRs; they never duplicate them. See
[.claude/skills/README.md](.claude/skills/README.md) for the index.

A project-aware reviewer subagent lives at
[.claude/agents/provna-docs-reviewer.md](.claude/agents/provna-docs-reviewer.md).

## Before starting work

1. Read [docs/glossary.md](docs/glossary.md) and the relevant ADRs — they are the design
   language of the project.
2. If a change touches more than two or three docs, propose a plan first.
3. Honor the language policy (§1) and the `docs/private` rule (§2) on every file you write.
4. After any documentation change, run the `docs-check` skill before finishing.
5. When a settled decision needs to ripple across the tree, use the `apply-decision` skill so
   the canonical docs, the ADRs, and the stale terminology all move together.

## Escalation

If a requested change would violate a non-negotiable rule above — drift the scope horizontal,
leak `docs/private` into a public doc, break the language policy, re-open a pinned decision
without an ADR, or weaken the fail-closed/honesty posture — **stop and ask** before proceeding.
It is better to pause than to silently weaken a guarantee or a guardrail.
