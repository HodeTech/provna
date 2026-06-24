---
name: supersede-adr
description: >
  Reverse or replace an Accepted decision by writing a NEW ADR and marking the old one
  Superseded — ADRs are append-only and history is never rewritten. USE FOR: changing a
  decision that an Accepted ADR already records (a substrate swap, a reversed scope call, a
  new pinned technology that displaces an old one). DO NOT USE FOR: recording a brand-new
  decision (use ../write-adr/SKILL.md), or merely refining wording/propagating an unchanged
  decision across docs (use ../apply-decision/SKILL.md).
---
# Supersede an ADR

## Purpose
Change a recorded decision without erasing the reasoning that produced it. The old ADR stays in
place as history; a new ADR carries the new decision and explains why the old one no longer
holds. This preserves the decision trail (CLAUDE.md §7: ADRs are append-only).

## When to use
- A previously-Accepted decision is being reversed or replaced (e.g. a different substrate, a
  different audit anchor, a reversed scope boundary).

## When not to use
- The decision is genuinely new and overrides nothing — use `../write-adr/SKILL.md`.
- You are only fixing a typo or propagating an *unchanged* decision's terminology — use
  `../apply-decision/SKILL.md` or a direct edit.

## Inputs
| Input | Description |
|-------|-------------|
| Old ADR | The Accepted ADR being replaced (number + slug). |
| New decision | The "we will now do Y instead" statement and its rationale. |
| What changed | Why the old decision no longer holds (new evidence, a failed assumption, a partner mandate). |

## Workflow
1. **Write the new ADR** with `../write-adr/SKILL.md`. In its `## Context`, link back to the
   ADR it replaces and state plainly what changed since. Compute the next free number; do not
   reuse the old one.
2. **Mark the old ADR superseded — header only, body untouched.** Change *only* its Status line:
   ```
   **Status:** Superseded by [ADR-NNNN](NNNN-new-slug.md)
   ```
   Do **not** edit the old ADR's Context / Decision / Consequences — the original reasoning is
   the point.
3. **Cross-link.** The new ADR's `## Context` links to the old; the old ADR's Status links
   forward to the new. Bump the old ADR's **Last updated** to today.
4. **Update the index.** In `docs/decisions/README.md`, set the old row's status to `Superseded`
   (with the forward link) and add the new ADR's row in numerical order.
5. **Propagate, if the change ripples.** If the superseded decision was a pinned technology or a
   structural choice referenced across the tree, run `../apply-decision/SKILL.md` so the
   canonical docs, the affected ADRs, and the stale terminology all move together.
6. **Gate.** Run `../docs-check/SKILL.md` and confirm PASS.

## Outputs
- A new ADR carrying the replacement decision.
- The old ADR's Status changed to `Superseded by [ADR-NNNN]` (body preserved).
- An updated index reflecting both.

## Done criteria
- [ ] New ADR written and numbered (next free number, not the old one).
- [ ] Old ADR's Status → `Superseded by [ADR-NNNN](…)`; its body untouched; Last updated bumped.
- [ ] New ADR's Context links back; old ADR's Status links forward.
- [ ] Index updated for both rows.
- [ ] Ripple propagated with `apply-decision` if the decision was tree-wide.
- [ ] `docs-check` passes.

## Common pitfalls
- Editing the old ADR's body instead of only its Status header (history lost).
- Reusing the old ADR's number for the new one.
- Forgetting to propagate a pinned-technology change, leaving stale terminology tree-wide.
- Updating the new row but not flipping the old row's status in the index.

## Related
- ../write-adr/SKILL.md, ../apply-decision/SKILL.md, ../docs-check/SKILL.md
- ../../../docs/decisions/README.md, ../../../docs/standards/adr-template.md
