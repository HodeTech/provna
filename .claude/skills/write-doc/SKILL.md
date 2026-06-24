---
name: write-doc
description: >
  Add or update a page in the docs/ tree (architecture, business, compliance, roadmap,
  standards, a pillar, the glossary) so it obeys Provna's conventions and the one-canonical-home
  rule. USE FOR: writing a new public doc, restructuring or expanding an existing one, adding a
  Mermaid-first architecture page. DO NOT USE FOR: recording a decision (use ../write-adr/SKILL.md),
  propagating a settled decision tree-wide (use ../apply-decision/SKILL.md), or writing internal
  competitive analysis (use ../competitive-teardown/SKILL.md, which targets docs/private/).
---
# Write or update a doc

## Purpose
Produce a public Provna doc that is English, self-contained, conventionally formatted, and lives
in its one canonical home — so the tree stays navigable and never contradicts itself. Assumes
you have read `CLAUDE.md` and `docs/standards/documentation-style.md`.

## When to use
- Adding a new page under `docs/` or materially rewriting an existing one.
- Adding an architecture/topology page (lead with a Mermaid diagram).

## When not to use
- It is a decision record → `../write-adr/SKILL.md`.
- It is internal competitive/teardown analysis → `../competitive-teardown/SKILL.md` (writes to
  `docs/private/`, which public docs never reference).

## Inputs
| Input | Description |
|-------|-------------|
| Topic & section | What the doc is about and which `docs/` folder it belongs in. |
| Canonical-home check | Whether the topic already has a home elsewhere (then link, don't restate). |
| Source facts | The content; mark `[OPINION]` and `UNVERIFIED` honestly; never invent numbers. |

## Workflow
1. **Find the one canonical home.** Decide the single file this content belongs in (concept →
   root; design → `architecture/`; decision → an ADR; money → `business/`; rules →
   `standards/`). If the topic is already owned elsewhere, **link to it — do not restate it**.
2. **Header + metadata.** Single H1 (`# Title`), then bold **Status**, **Last updated:
   2026-06-25**, and **Related** (relative links). **No YAML front-matter.**
3. **Lead architecture/flow docs with a Mermaid diagram.** Keep labels **ASCII-safe**: no
   apostrophes in flowchart labels; use `<br/>` (never `\n`) for line breaks; inside
   `sequenceDiagram` notes avoid `<br/>`, double-quotes, `;`, and in-message `->`.
4. **Write the body.** English only. Concrete and opinionated; cite competitors by name where
   useful but **never reference `docs/private/`** — restate the fact instead. Keep the
   gate↔pillar mapping straight (Gate 1 = S1, Gate 2 = S3, Gate 3 = S2, Gate 4 = S4). Honor the
   pinned-decision terminology (Go-first; DBOS / SagaCoordinator; Cedar-only / relationship-resolver;
   Tessera + internal RFC3161 TSA + cross-org witness; SeaweedFS / Valkey / OpenBao).
5. **Links only to the public tree, relative.** Reference `tech-stack.md` for versions; reference
   an ADR for a decision; reference the glossary for a term — don't duplicate any of them.
6. **Register it.** If you added a new file, add it to the section's `README.md` index (and, for
   a new top-level area, the root `docs/README.md` layout table) so it is discoverable.
7. **Gate.** Run `../docs-check/SKILL.md` and confirm PASS. For a substantial change, also run
   `../review-docs/SKILL.md`.

## Outputs
- A new or updated `docs/**/<file>.md` that passes `docs-check`.
- An updated section index if a new file was added.

## Done criteria
- [ ] One H1 + bold Status / Last updated / Related; no front-matter.
- [ ] English only; no Turkish leak; no `docs/private` reference.
- [ ] Mermaid (if any) is ASCII-safe; architecture/flow docs lead with a diagram.
- [ ] One canonical home — links instead of restating content owned elsewhere.
- [ ] `[OPINION]` / `UNVERIFIED` used honestly; no invented numbers.
- [ ] New file registered in its section index (and root layout table if a new area).
- [ ] `docs-check` passes.

## Common pitfalls
- Restating a spec/decision/term that already has a canonical home (it will drift).
- An apostrophe or a literal `\n` in a Mermaid label (breaks rendering — `docs-check` catches it).
- Adding a file but forgetting the index row, so navigation can't reach it.
- A stale pinned-technology name (e.g. "MinIO", "Rekor/Trillian" as Provna's choice).

## Related
- ../../../docs/standards/documentation-style.md, ../../../docs/standards/architectural-principles.md
- ../docs-check/SKILL.md, ../review-docs/SKILL.md, ../write-adr/SKILL.md, ../apply-decision/SKILL.md
