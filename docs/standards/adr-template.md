# ADR Template

**Status: Accepted**
**Last updated: 2026-06-24**
**Related:** [documentation-style.md](documentation-style.md), [architectural-principles.md](architectural-principles.md), [../decisions/README.md](../decisions/README.md)

Provna uses a condensed [MADR](https://adr.github.io/madr/) format. Copy the skeleton below into `decisions/NNNN-slug.md`, fill it in, and delete the guidance comments. Keep ADRs short: an ADR is a record of one decision and its trade-offs, not a design document.

## The skeleton

Copy everything inside the fence into a new file.

```markdown
# ADR-NNNN: Title

**Status: Proposed | Accepted | Deprecated | Superseded by [ADR-NNNN](NNNN-slug.md)**
**Date: YYYY-MM-DD**
**Related:** [../some/file.md](../some/file.md), [NNNN-other-decision.md](NNNN-other-decision.md)

## Context

The forces at play: the problem, the constraints, the requirement that forces a
choice. State what is true and what is uncertain. Mark unverified claims
UNVERIFIED and opinions [OPINION]. Do not pre-announce the decision here.

## Decision

The decision, stated in one or two sentences in the active voice ("We will ...").

Write the alternatives inline, each with the reason it lost:

  Considered: A (rejected: reason), B (rejected: reason); chose X because reason.

Do not repeat pinned version numbers; link [../tech-stack.md](../tech-stack.md)
instead.

## Consequences

### Positive

- What gets better, simpler, or newly possible.
- Which architectural principle this upholds.

### Negative

- What gets harder, what debt we take on, what we now must maintain.
- Any principle this strains, and why the trade-off is acceptable.
```

## Field rules

- **Title** — `ADR-NNNN: Title` as the single H1. `NNNN` is a 4-digit zero-padded sequence number; the file name is `NNNN-slug.md` with a kebab-case slug (e.g. `0005-s2-dbos-substrate-compensation-library.md`).
- **Status** — exactly one of:
  - `Proposed` — under discussion, not yet binding.
  - `Accepted` — binding; the codebase and other docs must conform.
  - `Deprecated` — no longer recommended, but not replaced by a specific decision.
  - `Superseded by [ADR-NNNN](NNNN-slug.md)` — replaced by a newer decision; always carry the forward link.
- **Date** — `YYYY-MM-DD`, the date the status last changed.
- **Related** — relative markdown links to files in the public tree only. Never link to anything outside it.

## Usage notes

- **Settled decisions are authored as Accepted.** Most Provna ADRs record choices already made during planning. Do not stage a fake `Proposed -> Accepted` history for them; write them directly as `Accepted` with the decision date.
- **Reserve `Proposed`** for decisions genuinely still open, where the doc exists to drive the discussion.
- **Never delete a superseded ADR.** When a decision is replaced, set the old ADR's status to `Superseded by [ADR-NNNN](...)`, give the new ADR a `## Context` that links back to what it replaces, and leave the old file in place. The decision trail is part of the record.
- **One decision per ADR.** If you are tempted to record two choices, write two ADRs and cross-link them in `Related`.
- **Alternatives belong inline in `## Decision`**, not in a separate section. The `Considered: ...; chose X because ...` form keeps the reasoning attached to the choice.
- **Honor the principles.** Every ADR must be consistent with [architectural-principles.md](architectural-principles.md). If a decision strains a principle, name the strain in `### Negative` and justify it.
