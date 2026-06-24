# Documentation Style

**Status: Accepted**
**Last updated: 2026-06-24**
**Related:** [adr-template.md](adr-template.md), [architectural-principles.md](architectural-principles.md), [README.md](README.md)

This is the single source of truth for how every file in the Provna `docs/` tree is written. No other doc restates these rules; they all obey them. If a rule here conflicts with habit, the rule wins.

## Language

- **English only** — all content, headings, captions, and diagram labels. The internal working notes may be in another language; the published tree is English.
- **Keep product and technical terms as-is** — `Provna`, `ActionGuard`, `CaMeL`, `DBOS`, `Cedar`, `OpenFGA`, `Rekor`, `AuthZEN`, EU AI Act article numbers, etc. Do not translate or paraphrase a term that has a canonical name.
- **Tone** — founder to team: concrete, opinionated, justified. No marketing fluff, no hedging filler. The audience is the internal team building Provna, and the documents are a forward-looking plan, not a sales deck.

## File naming

- **kebab-case** for all file names: `action-lifecycle.md`, `icp-and-gtm.md`.
- **ADRs** are named `NNNN-slug.md` — a 4-digit zero-padded number plus a kebab-case slug: `0009-action-guard-seam-vendor-neutral.md`.
- One topic has exactly one canonical file (see *One canonical home* below).

## File header

Every file starts with a single H1 (`#`), and **no YAML front-matter**. Immediately under the H1, a block of **bold-key metadata lines**:

```markdown
# Page Title

**Status: Accepted**
**Last updated: 2026-06-24**
**Related:** [../vision.md](../vision.md), [../architecture/overview.md](../architecture/overview.md)
```

- `Status` — `Draft`, `Proposed`, `Accepted`, `Deprecated`, or `Superseded` as appropriate to the doc. (ADRs use the status vocabulary in [adr-template.md](adr-template.md).)
- `Last updated` — `YYYY-MM-DD`.
- `Related` — relative markdown links to other public docs. Omit the line if there are none.

There is exactly one H1 per file (the title). All other headings are H2 (`##`) and below.

## Links

- **Relative markdown only**, and only to files that exist in the public `docs/` tree: `[../tech-stack.md](../tech-stack.md)`, `[../architecture/pillar-2-transactional-compensation.md](../architecture/pillar-2-transactional-compensation.md)`.
- **Never** link to a file outside the public tree, to an absolute path, or to any untracked working note.
- If you reference a fact that lives only in an untracked source, **restate the fact**; do not link to the source. See *Self-containment* below.

## Diagrams (Mermaid)

Use Mermaid wherever it clarifies structure: topology, lifecycle, phase-dependency graphs, quadrants, flywheels. **Architecture docs that describe a topology or a flow lead with the diagram**, then explain it in prose.

Diagrams are fenced inline (```` ```mermaid ````). Labels must be **ASCII-safe**:

- In `sequenceDiagram` notes and messages, do **not** use `<br/>`, apostrophes, double quotes, semicolons, or an in-message `->`.
- In `flowchart` node labels, avoid apostrophes.
- Prefer plain words over punctuation that the renderer may choke on.

These constraints exist because the renderers in our toolchain are unforgiving about those characters; a diagram that fails to render is worse than no diagram.

## One canonical home

Each topic is canonical in **exactly one** file. Other files link to it; they do not copy it. If you find yourself explaining the same mechanism in two places, pick the canonical home, fully explain it there, and replace the duplicate with a one-line summary plus a link. This is what keeps the tree maintainable as it grows.

## Phasing and milestones

Roadmap and planning docs use **phase-relative milestones**, never calendar dates. Say "Phase-0 MVP" or "by the end of Phase-0 -> 1 Enforcement", not a quarter or month. Durations, when given, are labeled **indicative (pre-build)** because nothing has been built yet and estimates are unproven.

## Marking conventions

Keep the planning rigor visible in the text:

- **`[OPINION]`** — a founder or team judgment call that is not (yet) backed by evidence. Mark it so a reader knows it is a stance, not a fact.
- **`UNVERIFIED`** — a claim we believe but have not confirmed (a competitor detail, a legal characterization, a market number). Mark it so no one downstream treats it as settled.

Use these inline, next to the specific claim, not as a blanket disclaimer at the top of a file.

## Self-containment (the no-private-reference principle)

The public documentation tree is **self-contained and standalone**.

- The internal competitive analysis and the founding charter are **not part of this tree, are not tracked alongside it, and are never named, cited, quoted, or linked** from any public doc.
- When a public doc needs a fact, an argument, or a competitor characterization that originated in that internal work, the doc **restates it in its own words** and stands on its own.
- Naming competitors and describing their strategic gaps in a forward-looking, plan-oriented way is fine. Reproducing internal competitive-analysis evidence verbatim, or pointing a reader at non-public analysis, is not.

The test: a new team member should be able to read only the public tree, understand the entire plan, and never encounter a dangling reference to something they cannot open.

## ADRs

Decisions follow the condensed MADR format in [adr-template.md](adr-template.md): `## Context`, `## Decision` (alternatives written inline as `Considered: A (rejected: ...); chose X because ...`), `## Consequences` split into `### Positive` and `### Negative`. Do not repeat pinned version numbers in an ADR; link [../tech-stack.md](../tech-stack.md).
