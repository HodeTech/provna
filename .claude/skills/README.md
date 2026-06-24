# Provna skills

Recurring agent procedures for the Provna repo. Each skill is a directory with a `SKILL.md`
(YAML frontmatter + a step-by-step procedure); the **directory name is the `/command`**. When
the maintainer names a recurring task, read the matching `SKILL.md` **in full** and check its
done-criteria before finishing. Skills cite the [standards](../../docs/standards/README.md) and
[decisions](../../docs/decisions/README.md) — they never duplicate them.

Provna is **pre-build**: the repository is a documentation tree, so today's recurring work is
**documentation and planning**, and the quality gate is the `docs-check` skill, not a compiler.
See [CLAUDE.md](../../CLAUDE.md) for the non-negotiable rules every skill assumes — especially
the **English-only public docs** policy and the **no-`docs/private`-reference** rule.

## Implementation

| Skill | Use it to |
|-------|-----------|
| [implement-task](implement-task/SKILL.md) | **Primary entry point.** End-to-end discipline for any non-trivial workstream: scope → align → inspect → plan → do → gate → docs → commit → review prompt. Today a PoC/spec; structured for code when the monorepo lands. |

## Process & governance

| Skill | Use it to |
|-------|-----------|
| [write-adr](write-adr/SKILL.md) | Record a settled non-trivial decision as a new condensed-MADR ADR in `docs/decisions/` and update the index. |
| [supersede-adr](supersede-adr/SKILL.md) | Reverse an Accepted decision: write a new ADR and mark the old one `Superseded` (never rewrite it). |
| [apply-decision](apply-decision/SKILL.md) | Propagate a settled decision (e.g. a tech choice) across the whole tree — canonical docs, ADRs, and stale terminology — consistently and verifiably. |

## Authoring

| Skill | Use it to |
|-------|-----------|
| [write-doc](write-doc/SKILL.md) | Add or update a `docs/` page (architecture, business, compliance, roadmap, …) that obeys the conventions: H1 + bold metadata, ASCII-safe Mermaid, relative links, one-canonical-home. |

## Quality & review

| Skill | Use it to |
|-------|-----------|
| [docs-check](docs-check/SKILL.md) | **Run before finishing any docs change.** Fast machine gate: no `docs/private` leak, English-only, links resolve, ASCII-safe Mermaid, no front-matter. |
| [review-docs](review-docs/SKILL.md) | Deep, multi-dimension adversarial review of a change or the whole tree; may delegate to the `provna-docs-reviewer` agent. |

## Research (planning phase)

| Skill | Use it to |
|-------|-----------|
| [competitive-teardown](competitive-teardown/SKILL.md) | Deeply review a competitor/reference (a repo or a product) and write a structured teardown + Provna-implications synthesis **into `docs/private/`** (never referenced from public docs). |

## Reviewer subagent

The project-aware reviewer lives at [../agents/provna-docs-reviewer.md](../agents/provna-docs-reviewer.md)
— invoke it (or the [review-docs](review-docs/SKILL.md) skill) to audit a change against the
Provna non-negotiables.
