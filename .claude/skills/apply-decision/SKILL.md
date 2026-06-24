---
name: apply-decision
description: >
  Propagate a settled decision (e.g. a pinned-technology choice) consistently across the whole
  docs tree — the canonical docs, the relevant ADRs, and every stale terminology reference —
  and verify it. USE FOR: rippling an already-made decision so the tree stays self-consistent
  after a tech choice, a substrate swap, or a scope refinement. DO NOT USE FOR: recording the
  decision in the first place (use ../write-adr/SKILL.md) or reversing one (use
  ../supersede-adr/SKILL.md).
---
# Apply a decision

## Purpose
When a decision is made, it usually touches more than its ADR — the pinned stack, a pillar doc,
the build-vs-consume table, the roadmap phases, the principles, the compliance map, and ADR
diagrams may all reference the old choice. This skill rolls the decision across all of them from
**one shared decision statement**, distinguishing a *Provna pin* (update) from a *market
description* (keep), and verifies the result. It exists because a tech decision ripples wide and
a half-applied decision leaves the tree contradicting itself.

## When to use
- A pinned technology changed (a substrate, the PDP, the data-plane language, the audit anchor,
  the object store) and the rest of the tree must follow.
- A scope refinement or a build-vs-consume change needs to read consistently everywhere.

## When not to use
- The decision is not yet recorded — write/supersede the ADR first
  (`../write-adr/SKILL.md` / `../supersede-adr/SKILL.md`), then apply it.

## Inputs
| Input | Description |
|-------|-------------|
| Decision statement | The single source of truth: "we now do X (not Y); the seam is Z." |
| Old → new terms | The exact strings that change (e.g. `Rekor/Trillian` → Tessera + internal RFC3161 TSA + cross-org witness). |
| Pin vs market | Which usages are Provna's *pin* (update) and which are *market description* (keep — naming Rekor/OpenFGA as commodity examples is fine). |

## Workflow
1. **Write the decision statement once.** A compact, unambiguous block: the fork(s) decided, the
   recommended defaults, and an explicit *alignment map* of old→new terms. Everything downstream
   reads from this so it cannot drift.
2. **Update the canonical homes + the ADRs.** The pinned stack (`tech-stack.md`), the affected
   pillar doc(s), `build-vs-consume.md`, and the relevant ADRs (or a new ADR via `write-adr`).
   Add a "Decisions taken (date)" note to `tech-stack.md` and link the rationale doc if one
   exists. **Reproduce whole files — never a change-summary, never `...` placeholders.** (A
   common failure mode is an agent returning a summary of edits instead of the file body; always
   write the complete document.)
3. **Align stale terminology tree-wide.** Sweep the docs that merely *reference* the choice —
   the roadmap phases, `overview.md`, `project-structure.md`, `architectural-principles.md`,
   `regulatory-mapping.md`, and any ADR Mermaid diagrams. Replace each **Provna-pin** usage per
   the alignment map; **leave market/commodity descriptions intact** (a passage that says "the
   PDP is commoditized: Cedar/OpenFGA/AuthZEN" is describing the market, not Provna's pin).
4. **Reflect structural seams if the decision implies one.** A substrate-swap decision usually
   means a seam interface (e.g. `SagaCoordinator`, `relationship-resolver`) — make it first-class
   in `project-structure.md` (directory tree + package graph + the surface-boundaries note) so
   the swap is visibly an adapter change, not a rewrite.
5. **Update the glossary.** Add entries for new terms introduced by the decision; keep existing
   entries.
6. **Verify.** Run `python3 .claude/hooks/docs-check.py` (PASS) and grep that the old pin no
   longer appears *as a Provna pin* (only as a market example or in the rationale doc's
   pre-decision baseline). For a large ripple, run `../review-docs/SKILL.md`.

## Outputs
- The canonical docs, ADRs, structural docs, and glossary all consistent with the decision.
- A clean `docs-check`; no stale pin presented as Provna's choice.

## Done criteria
- [ ] One decision statement + alignment map drove every edit.
- [ ] Canonical homes + ADRs updated as **whole files** (no summaries/elisions).
- [ ] Stale Provna-pin terms replaced everywhere; market descriptions left intact.
- [ ] Structural seam (if any) made first-class in `project-structure.md`.
- [ ] Glossary updated; existing entries preserved.
- [ ] `docs-check` passes; the old pin survives only as a market example or pre-decision baseline.

## Common pitfalls
- **An agent returning a change-summary instead of the full file body** — always reproduce the
  whole document; verify it starts with `#` and has no `...`/placeholder.
- Over-applying — forcing Provna's pinned name into a passage that is describing the commodity
  market.
- Under-applying — leaving a stale pin in a roadmap phase, a diagram, or the compliance map.
- Forgetting the structural seam, so the decision reads as a one-way bet rather than a swappable
  interface.

## Related
- ../write-adr/SKILL.md, ../supersede-adr/SKILL.md, ../docs-check/SKILL.md, ../review-docs/SKILL.md
- ../../../docs/tech-stack.md, ../../../docs/architecture/build-vs-consume.md, ../../../docs/project-structure.md
