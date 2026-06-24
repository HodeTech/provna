---
name: implement-task
description: >
  The primary end-to-end flow for delivering a non-trivial Provna roadmap workstream — scope,
  align, inspect, plan, do the work, gate it, update the canonical docs, commit, and hand off to
  review. USE FOR: a Phase-0 PoC or a substantial planning/spec/deliverable from
  docs/roadmap/current.md (and, once the monorepo lands, a feature/fix in the data-plane or
  control-plane). DO NOT USE FOR: a one-line edit, recording a decision (use write-adr), a
  quick docs gate (use docs-check), or reviewing someone else's work (use review-docs).
---
# Implement a task

## Purpose
Make every non-trivial Provna workstream land the same disciplined way: aligned with the
[CLAUDE.md non-negotiables](../../../CLAUDE.md), scoped from the roadmap, built within scope and
the build-vs-consume boundary, gated green, documented in its one canonical home, committed, and
handed to review. This skill is the spine; it cites the standards and delegates the gate and the
review — it does not restate them.

> **Phase note.** Provna is pre-build. Today a "task" is usually a **Phase-0 PoC** (the S2
> compensation-harness, the S1 fusion + AgentDojo, the S4 signed-anchored evidence pack) or a
> substantial planning/spec deliverable — so the gate is the **PoC's own success metric + the
> `docs-check` gate**, not a full toolchain. The code path below (steps 4–6) activates when the
> monorepo lands; until then, follow its *spirit* (fail-closed, the seams, boundary validation)
> in the PoC and capture the result as a doc/spec.

## When to use
- Delivering a workstream from [docs/roadmap/current.md](../../../docs/roadmap/current.md) or a
  phase file — a PoC, a spec, a structural plan.
- Once code exists: a feature/fix/refactor in the data-plane (Go) or control-plane (Python/TS).

## When not to use
- Trivial edits — just make them and run `../docs-check/SKILL.md`.
- Recording a decision → `../write-adr/SKILL.md`. Reviewing a change → `../review-docs/SKILL.md`.

## Inputs
- The task / roadmap item with its acceptance criteria (the phase file's per-workstream acceptance).
- The pillar(s) and seam(s) it touches, and the ADRs/standards that frame it.
- Whether it touches a pinned decision, a scope/build-vs-consume boundary, a seam
  (`ActionGuard` decide/commit/compensate, `SagaCoordinator`, `relationship-resolver`), or
  introduces a dependency — these gate the plan step.

## Workflow
1. **Scope and align.** Read [CLAUDE.md](../../../CLAUDE.md) and locate the task in
   [docs/roadmap/current.md](../../../docs/roadmap/current.md) / its phase file; note its
   acceptance criteria. Read the ADRs it touches and the relevant
   [docs/architecture/](../../../docs/architecture/README.md) pillar(s). Confirm it stays **in
   scope** (it deepens one guarded saga step; it does not drift Provna horizontal) and on the
   right side of **build-vs-consume** (build only the S1 IFC fusion / S2 compensation content;
   consume the rest). Keep the gate↔pillar mapping straight: Gate 1 = S1, Gate 2 = S3, Gate 3 =
   S2, Gate 4 = S4.
2. **Inspect before building.** Find the nearest existing pattern and mirror it — the relevant
   pillar doc, an existing PoC/spec, the seam definitions in
   [project-structure.md](../../../docs/project-structure.md). Do not invent a new shape beside
   an established one.
3. **Plan — confirm only when it matters.** Write a short plan (what you will produce, the
   approach, the success criterion). **Stop and confirm with the maintainer** if it touches: a
   pinned decision (re-opening one needs an ADR first), a scope / build-vs-consume boundary, a
   seam contract (`ActionGuard` / `SagaCoordinator` / `relationship-resolver`), or a new
   dependency. Otherwise proceed.
4. **Do the work, honoring the architecture.** For a **PoC/spec**: build the smallest thing that
   proves the hard part (e.g. an A → A⁻¹ round-trip for S2; ASR + utility-tax on AgentDojo for
   S1; a JCS + Ed25519 + Tessera-anchored evidence pack for S4) and capture the result. For
   **code** (when it lands): write it per [tech-stack.md](../../../docs/tech-stack.md) — Go on
   the inline data-plane, Python/TS in the control-plane — keeping the substrate behind the
   `SagaCoordinator` seam and the PDP behind the `relationship-resolver` seam, validating
   untrusted input at the boundary, and keeping the design **fail-closed** (any error ⇒ BLOCK, no
   downgrade path). The deterministic guarantee lives only in the lattice + sink-policy; an ML
   classifier is an optional pre-filter, never the guarantee.
5. **Self-check against the non-negotiables.** Before the gate, walk your own output:
   - **Scope held** — it deepens a gate; it did not turn Provna into a platform.
   - **Seams held** — the substrate is reached only through `SagaCoordinator`; the PDP only
     through `relationship-resolver`; host runtimes only through the `ActionGuard` gRPC seam. No
     core dependency added without an ADR.
   - **Fail-closed** — no downgrade/observe-only/fail-open path; revocation fail-closed.
   - **Honesty & language** — `[OPINION]`/`UNVERIFIED` where due, no invented numbers; English in
     anything public; no `docs/private` reference.
6. **Gate.** Run `../docs-check/SKILL.md` (PASS) on any docs touched. For a PoC, state its
   **success metric result** plainly (met / not met, with the number). When the toolchain exists,
   run the data-plane/control-plane tests per `tech-stack.md`; a red gate is a blocker, not a
   warning.
7. **Update the canonical docs.** If the work settled a decision, write a new append-only ADR
   (`../write-adr/SKILL.md`). If it altered the stack or a structural seam, ripple it with
   `../apply-decision/SKILL.md`. Reflect a new concept in the relevant pillar doc or the
   [glossary](../../../docs/glossary.md). Update `docs/roadmap/current.md` / the phase file's
   status if a milestone moved. One canonical home — link, never restate.
8. **Commit.** A clear, imperative subject scoped to the area (`docs:` / `roadmap:` / `poc:` /
   later a package scope), a body saying what changed and why, ending with
   `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. (Branch first if on the default
   branch.) Commit/push only when the maintainer has asked.
9. **Summary + review prompt.** State what changed and why, which pillars/seams/ADRs it touches,
   the gate/PoC result, and what you deferred. Emit a copy-paste block for the
   `provna-docs-reviewer` agent (docs) — naming the change, the scope, the ADRs it implements,
   and any area to scrutinize.

## Outputs
- The delivered PoC/spec/doc (or, later, code with tests) that meets the workstream's acceptance.
- A green `docs-check` (and the PoC's success-metric result, or the toolchain green once it exists).
- Updated canonical docs / a new ADR where the work warrants it; the roadmap status moved.
- A commit (when asked) and a plain-language summary + a `provna-docs-reviewer` prompt.

## Done criteria
- [ ] Task located in the roadmap with its acceptance criteria; CLAUDE.md + relevant ADRs read.
- [ ] In scope and on the right side of build-vs-consume; gate↔pillar mapping correct.
- [ ] Inspected and mirrored the nearest pattern; wrote a plan; confirmed it if it touched a pinned decision / a boundary / a seam / a dependency.
- [ ] Work done fail-closed, through the seams, with boundary validation; the deterministic guarantee kept in the lattice + sink-policy.
- [ ] Self-checked scope / seams / fail-closed / honesty & language.
- [ ] `docs-check` PASS (and the PoC success metric stated, or the toolchain green once it exists).
- [ ] Canonical docs updated / ADR written where warranted; roadmap status moved.
- [ ] Committed with the `Co-Authored-By` trailer (only when asked); summary + review prompt produced.

## Common pitfalls
- **Scope drift** — solving a horizontal problem (a gateway, a framework, a generic PDP) instead
  of deepening a gate.
- **Reaching past a seam** — wiring DBOS/Cedar/a host runtime directly instead of through the
  `SagaCoordinator` / `relationship-resolver` / `ActionGuard` seam (kills the swappability and the
  vendor-neutrality thesis).
- **A fail-open/observe-only shortcut** — the exact weakness Provna is built to beat.
- **Adding a core dependency to get unblocked** — it needs an ADR first.
- **Leaning on review for the gate** — run `docs-check` (and the toolchain, later) yourself first.
- **A `docs/private` reference or a Turkish leak** in a public deliverable.

## Related
- ../write-adr/SKILL.md, ../apply-decision/SKILL.md, ../docs-check/SKILL.md, ../review-docs/SKILL.md
- ../../agents/provna-docs-reviewer.md
- ../../../docs/roadmap/current.md, ../../../docs/tech-stack.md, ../../../docs/project-structure.md, ../../../docs/architecture/build-vs-consume.md
