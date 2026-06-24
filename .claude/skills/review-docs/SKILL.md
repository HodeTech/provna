---
name: review-docs
description: >
  Deep, multi-dimension adversarial review of a docs change or the whole tree — terminology,
  quantitative consistency, technical accuracy vs the pinned decisions, cross-references, scope
  discipline, the no-docs/private rule, honesty, and conventions — with each candidate finding
  verified before it is reported. USE FOR: a thorough review before a milestone or after a large
  change. DO NOT USE FOR: the quick pass/fail gate (use ../docs-check/SKILL.md) or writing/fixing
  docs (this produces findings, it does not edit).
---
# Review docs

## Purpose
Find the issues the fast gate cannot: contradictions between docs, a thesis stated wrong in a
high-traffic file, a quantitative figure that drifted, a stale pinned-decision claim, a scope
drift, an over-claim. This is the discipline behind a real review pass — fan out across
dimensions, then **verify each candidate finding before reporting it** so the output is
trustworthy, not noisy.

## When to use
- Before a planning milestone, or after a large multi-doc change.
- When the maintainer asks for a "review" of the documentation.

## When not to use
- As the routine self-gate after a small edit — that is `../docs-check/SKILL.md`.

## Inputs
| Input | Description |
|-------|-------------|
| Scope | A change (`git diff`), a named set of docs, or the whole tree. |
| Depth | "quick" (the key dimensions) or "thorough" (every dimension + adversarial verification). |

## Workflow
1. **Run the machine gate first** so the deep pass is not wasted on mechanical issues:
   `python3 .claude/hooks/docs-check.py`. Fix or note its ERRORS.
2. **Delegate to the project-aware reviewer.** Invoke the `provna-docs-reviewer` agent (or
   `@provna-docs-reviewer`) on the scope; it knows the CLAUDE.md non-negotiables and returns
   severity-sorted `file:line` findings plus what it verified clean.
3. **Review across these dimensions** (the agent covers them; for a "thorough" pass, sweep each
   deliberately):
   - **Terminology** — glossary terms used consistently; load-bearing terms defined.
   - **Quantitative consistency** — every recurrence of a figure (ACV, utility-tax, a milestone
     count, a funding number) agrees; an "N proofs/steps" count matches its list.
   - **Technical accuracy** — claims match the pinned decisions; no stale pin presented as
     Provna's choice (vs a legitimate market description).
   - **Cross-references** — links resolve and are bidirectional where they should be (ADR ↔
     pillar; milestone ↔ phase file).
   - **Architecture coherence** — the gate↔pillar mapping (1=S1, 2=S3, 3=S2, 4=S4) and the
     four-gate framing are correct everywhere, especially in high-traffic files (the docs index,
     the seam ADR).
   - **Scope & strategy** — nothing drifts Provna horizontal; build-vs-consume is respected.
   - **Conventions & honesty** — one-canonical-home; `[OPINION]`/`UNVERIFIED`; no invented
     numbers; "regulator-grade forensic-reproducible" not "court-admissible".
4. **Adversarially verify before reporting.** For each candidate finding, re-check the actual
   text (and, for a "this is wrong" claim, the source it supposedly contradicts). Drop anything
   you cannot confirm; a wrong finding costs more than a missed nit. Note any you could not
   resolve under `Needs confirmation`.
5. **Report** severity-sorted (`Blocker / High / Medium / Low`) with `file:line`, impact, and a
   concrete fix; end with what was verified clean. **Do not edit** — hand the findings back so
   the maintainer (or a follow-up `write-doc` / `apply-decision`) applies them.

## Outputs
- A severity-sorted findings report (`file:line`, impact, fix) + a "clean" list, ready to act on.

## Done criteria
- [ ] Machine gate run; its ERRORS addressed or noted.
- [ ] Reviewer agent invoked; all dimensions covered (every dimension for a "thorough" pass).
- [ ] Each reported finding verified against the actual text; unconfirmed ones moved to `Needs confirmation`.
- [ ] Findings are `file:line`, severity-rated honestly (Blocker only for a non-negotiable), with fixes.
- [ ] No edits made by this skill.

## Common pitfalls
- Reporting plausible-but-unverified findings (verify against the text first).
- Over-rating severity — a separator nit is Low, not Blocker.
- Flagging a market description as a stale pin.
- Editing instead of reporting — this skill is review-only.

## Related
- ../../agents/provna-docs-reviewer.md, ../docs-check/SKILL.md
- ../write-doc/SKILL.md, ../apply-decision/SKILL.md (to apply the findings)
