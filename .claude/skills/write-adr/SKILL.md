---
name: write-adr
description: >
  Author a new Architecture Decision Record in docs/decisions/ using Provna's condensed-MADR
  form and register it in the index. USE FOR: recording a settled non-trivial
  architectural / product / process / tech decision, pinning a stack or seam choice, or
  justifying a new core dependency. DO NOT USE FOR: reversing an Accepted decision (use
  ../supersede-adr/SKILL.md), propagating an already-recorded decision across the tree (use
  ../apply-decision/SKILL.md), or writing a normal doc (use ../write-doc/SKILL.md).
---
# Write an ADR

## Purpose
Record *why* a non-trivial Provna decision was made, so a future contributor can follow the
reasoning and disagree by writing a new ADR rather than silently changing direction. This skill
produces one append-only file in `docs/decisions/` in the condensed MADR form the whole corpus
uses, and adds its row to the index. It assumes you have read `CLAUDE.md` and the relevant
standards.

## When to use
- A decision touches the architecture (a pillar), the build-vs-consume boundary, product scope,
  pricing/packaging, deployment, or the name/brand.
- You are pinning or changing a technology (a substrate, the PDP, the data-plane language, the
  audit anchor). A stack change or a new core dependency **requires** an ADR (CLAUDE.md §4).
- You are choosing between real alternatives and the loser deserves to be remembered.

## When not to use
- The decision overrides an already-Accepted ADR — use `../supersede-adr/SKILL.md`.
- The decision is already recorded and you only need it to ripple across docs — use
  `../apply-decision/SKILL.md`.
- The artifact is descriptive documentation, not a decision — use `../write-doc/SKILL.md`.

## Inputs
| Input | Description |
|-------|-------------|
| Decision statement | The plain "we will do X" you are recording. |
| Alternatives | The options weighed and why each lost. |
| Related ADRs / clauses | Sibling ADRs and the `product-scope.md` / `architectural-principles.md` clauses that frame it. |
| Settled? | `Accepted` if the decision is made (the common case); `Proposed` only if genuinely open. |

## Workflow
1. **Confirm it is a new decision, not a supersede.** If it overrides an Accepted ADR, stop and
   use `../supersede-adr/SKILL.md`.
2. **Compute the next free number dynamically** — zero-padded 4 digits, never reused or
   renumbered. Never copy a number from this skill's examples.
   ```bash
   R=$(git rev-parse --show-toplevel)
   NEXT=$(printf '%04d' $(( 10#$(ls "$R"/docs/decisions/ | grep -E '^[0-9]{4}-' | sort | tail -1 | cut -c1-4) + 1 )))
   echo "$NEXT"   # the next free ADR number — trust this
   ```
3. **Copy the template** and rename with a kebab slug:
   ```bash
   cp "$R"/docs/standards/adr-template.md "$R"/docs/decisions/"$NEXT"-your-slug.md
   ```
4. **Fill the H1 and metadata.** `# ADR-NNNN: Title` (your `$NEXT`), then the bold lines
   **Status** (`Accepted` when settled — no ceremonial `Proposed → Accepted` round-trip),
   **Last updated** (`2026-06-25`), and **Related** (relative links to sibling ADRs and the
   framing `../product-scope.md` / `../standards/architectural-principles.md` clauses).
5. **Write `## Context`.** The situation, the constraints (vertical-FS, fail-closed, air-gapped,
   thin-but-deep scope, build-vs-consume), and the stakes of getting it wrong. Mark opinions
   `[OPINION]` and unconfirmed facts `UNVERIFIED`.
6. **Write `## Decision`.** State "we will do X" plainly, then the alternatives **inline**:
   `Considered: A (rejected: …), B (rejected: …); chose X because …`. **Do not restate pinned
   versions** — link `../tech-stack.md`. **Cite specs, never paste them.**
7. **Write `## Consequences`** split into `### Positive` and `### Negative`, each negative paired
   with how you live with or mitigate it.
8. **Update the index.** Add a row to the table in `docs/decisions/README.md` in numerical order.
9. **Gate.** Run `../docs-check/SKILL.md` (or `python3 .claude/hooks/docs-check.py`) and confirm
   PASS: one H1, no front-matter, relative links resolve, English-only, ASCII-safe Mermaid, no
   `docs/private` leak, no spec restated.

## Outputs
- A new `docs/decisions/NNNN-your-slug.md` in condensed MADR form.
- An updated index row in `docs/decisions/README.md`.

## Done criteria
- [ ] Next free 4-digit number used; no existing ADR renumbered.
- [ ] H1 + bold Status / Last updated / Related; Status is `Accepted` when settled.
- [ ] `## Context`, `## Decision` (alternatives inline), `## Consequences` (Positive + Negative) all present.
- [ ] Versions reference `../tech-stack.md`; no spec body restated.
- [ ] Index table in `docs/decisions/README.md` updated, in order.
- [ ] Any new core dependency is justified by *this* ADR.
- [ ] `docs-check` passes.

## Common pitfalls
- Restating version numbers instead of linking `tech-stack.md`.
- Forgetting the README index row (the ADR then "does not exist" to navigation).
- A `Proposed → Accepted` round-trip for an already-settled decision.
- Mis-stating the gate↔pillar mapping (Gate 1 = S1, Gate 2 = S3, Gate 3 = S2, Gate 4 = S4).
- Leaving a Turkish term or a `docs/private` reference in the ADR.

## Related
- Template: ../../../docs/standards/adr-template.md
- ADR index & rules: ../../../docs/decisions/README.md, ../../../docs/standards/documentation-style.md
- Principles: ../../../docs/standards/architectural-principles.md
- Sibling skills: ../supersede-adr/SKILL.md, ../apply-decision/SKILL.md, ../docs-check/SKILL.md
