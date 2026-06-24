# Standards

**Status: Accepted**
**Last updated: 2026-06-24**
**Related:** [adr-template.md](adr-template.md), [documentation-style.md](documentation-style.md), [architectural-principles.md](architectural-principles.md)

This directory holds the conventions that keep the Provna documentation tree coherent and the conventions that keep the product itself coherent. Two of these documents govern how we write; one governs what we build. Read all three before contributing a new doc or an ADR.

## What lives here

| File | Governs | Read it when |
| --- | --- | --- |
| [adr-template.md](adr-template.md) | The shape of every Architecture Decision Record. | You are about to record (or supersede) a decision. |
| [documentation-style.md](documentation-style.md) | The canonical style rules for the whole `docs/` tree: language, file naming, headings, links, Mermaid, marking conventions. | You are writing or editing any doc. |
| [architectural-principles.md](architectural-principles.md) | The five first-class product principles every design and ADR must satisfy, plus the scope-discipline test. | You are making a design choice, reviewing one, or writing an ADR. |

## How they relate

- **documentation-style.md** is the single source of truth for prose mechanics. Every other doc obeys it; none restate it.
- **adr-template.md** is the copyable skeleton for `decisions/NNNN-slug.md`. It applies the style rules to the specific case of a decision record.
- **architectural-principles.md** is the substance the decisions must honor. An ADR that violates a principle without explicitly arguing the trade-off in `## Consequences` is incomplete.

## The one rule that overrides all others

The documentation tree is **self-contained**. The internal competitive analysis and the founding charter are not part of this tree, are not tracked here, and are never cited or linked. Every public doc restates the content it needs in its own words. If a fact only exists in an untracked source, copy the fact in; do not point at the source. This is non-negotiable and is detailed in [documentation-style.md](documentation-style.md).
