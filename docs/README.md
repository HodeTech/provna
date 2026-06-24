# Provna documentation

> **Status:** Living · **Last updated: 2026-06-24**

**Provna is a vendor-neutral runtime control plane that turns every WRITE action an agent takes in regulated enterprise systems into a contract that is reversible, authorized, information-flow-controlled, and regulator-grade provable.** Its atomic unit is the *guarded saga step*: every side-effecting call passes four gates — information-flow control (S1), runtime authorization (S3), the transactional action contract / compensation (S2), and tamper-evident audit (S4). It does not sell a security tool; it sells the gate that lets a blocked agent project ship.

This tree is the **planning and roadmap documentation** for Provna (currently pre-build). It is organized by *the kind of question each section answers*, not by which subsystem the answer touches — when you have a question, you should know which folder to open before you know which part of the system is involved.

## Layout

| Folder / File | Answers the question |
|---|---|
| [vision.md](vision.md) | **What are we building, and why?** The problem, the category, the atomic unit. Read this first. |
| [product-scope.md](product-scope.md) | **What are the hard rules?** What Provna will be and — just as important — what it will *not* be, plus the scope-discipline test. |
| [positioning.md](positioning.md) | **Why this over the alternatives?** The four-way white space, the competitor contrast, defensibility and absorption. |
| [glossary.md](glossary.md) | Project-specific terminology used throughout the tree. Skim it first so the rest reads cleanly. |
| [tech-stack.md](tech-stack.md) | **What is it built with?** The pinned, polyglot technology choices and the MVP-vs-production split. |
| [project-structure.md](project-structure.md) | **Where will code live?** The planned monorepo layout and build order. |
| [architecture/](architecture/README.md) | **How is Provna designed?** The control-plane topology, the action lifecycle, the build-vs-consume boundary, the integration surfaces, and the four pillars (S1–S4) in depth. |
| [roadmap/](roadmap/README.md) | **What ships, and when?** The phase map, phases 0 → 2, and what is active right now. |
| [decisions/](decisions/README.md) | **Why is it built this way?** Architecture Decision Records (ADRs) in condensed MADR format — one per non-trivial choice. |
| [standards/](standards/README.md) | **How should things be written?** Documentation style, the ADR template, and the architectural principles. |
| [business/](business/README.md) | **Who is it for, and how is it sold?** The ICP and GTM motion, the design-partner plan, and pricing/packaging. |
| [compliance/](compliance/regulatory-mapping.md) | **What must we satisfy?** How the evidence pack maps to EU AI Act Article 12/14, DORA, MiFID II, and ISO 42001. |
| [risks/](risks/risk-register.md) | **What could dilute or kill it?** The risk register and the red lines. |

## Reading order for newcomers

1. [glossary.md](glossary.md) — the terms used throughout; read this first so the rest makes sense.
2. [vision.md](vision.md) — what Provna is and the problem it solves.
3. [product-scope.md](product-scope.md) — the hard rules (what it will and will not be) that shape every decision.
4. [positioning.md](positioning.md) — why Provna over the alternatives, and why it is deliberately not horizontal.
5. [decisions/](decisions/README.md) — the numbered ADRs, in order; the fastest way to understand *why* things are the way they are.
6. [architecture/overview.md](architecture/overview.md) — the system topology, then dive into the [four pillars](architecture/README.md).
7. [roadmap/current.md](roadmap/current.md) — what is active now and the immediate next steps, then [roadmap/README.md](roadmap/README.md) for the whole shape of the work.

## Conventions in this tree

- **Language:** English only.
- **File names:** `kebab-case.md`. ADRs are `NNNN-slug.md` with a 4-digit number.
- **No front-matter:** every file starts with a single H1 title; metadata goes in bold key lines directly under the H1 (**Status**, **Last updated**, **Related**). Living docs carry a `> Status:` line.
- **Links:** relative markdown paths within this tree, so they resolve on GitHub.
- **Diagrams:** Mermaid, embedded as inline fenced code blocks, with ASCII-safe labels (no apostrophes, double-quotes, `;`, `<br/>` or `->` inside sequence-diagram notes/messages). Architecture docs lead with a diagram where a topology or flow exists.
- **ADRs:** condensed MADR — `## Context`, `## Decision` (alternatives inline), `## Consequences` (`### Positive` / `### Negative`). See [standards/adr-template.md](standards/adr-template.md).
- **One canonical home per artifact:** each topic lives in one file; everything else links to it rather than copying.
- **Phasing:** milestones are phase-relative, never calendar dates; pre-build durations are indicative.
- **Marking:** opinions are tagged `[OPINION]`; unverified claims are tagged `UNVERIFIED`.

The binding style rules live in [standards/documentation-style.md](standards/documentation-style.md).
