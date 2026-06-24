---
name: docs-check
description: >
  The consistency gate for the docs tree — run before finishing ANY documentation change.
  Fast and mostly machine: no docs/private leak, English-only public docs, relative links
  resolve, ASCII-safe Mermaid, single H1 / no front-matter; then a short list of judgment
  checks the script cannot make. USE FOR: a pass/fail self-gate after editing docs. DO NOT USE
  FOR: a deep adversarial review (use ../review-docs/SKILL.md or the provna-docs-reviewer agent).
---
# Docs check

## Purpose
A fast, repeatable screen that catches Provna's load-bearing documentation rules *before* a
human or the reviewer agent spends attention. It is mostly a single script (`docs-check.py`)
plus a few judgment checks it cannot automate. Run it after any docs change and before
committing. A `PostToolUse` hook already runs the *private-leak* half of it automatically on
every `.md` edit; this skill is the full gate.

## When to use
- After editing or adding any `docs/` page or root guide, before finishing.
- As the final step of `write-adr`, `supersede-adr`, `write-doc`, and `apply-decision`.

## When not to use
- For a thorough correctness/consistency review — that is `../review-docs/SKILL.md` and the
  `provna-docs-reviewer` agent.

## Inputs
| Input | Description |
|-------|-------------|
| The change | The edited/added docs (or the whole tree). |
| Repo root | `$(git rev-parse --show-toplevel)`. |

## Workflow
1. **Run the machine gate.** It scans every public doc (the `docs/` tree minus `docs/private/`,
   plus the root guides) and exits non-zero on any error.
   ```bash
   python3 .claude/hooks/docs-check.py
   ```
   It reports, by `file:line`: `private-ref` (a `docs/private` leak), `lang-leak` (`Md.` or
   Turkish `madde` in a public doc), `broken-link`, `mermaid` (apostrophe / literal `\n` /
   unsafe sequenceDiagram note), `front-matter` / `no-h1`. Fix every ERROR and re-run until it
   prints **RESULT: PASS**. Treat WARNINGS (`/Users/…`, `teardown`) as "review — usually a real
   leak to reword".
2. **Judgment checks the script cannot make** — read for these on the changed docs:
   - **Gate↔pillar mapping** is Gate 1 = S1, Gate 2 = S3, Gate 3 = S2, Gate 4 = S4 (a recurring
     error). The four-gate framing must list all four pillars, including S2.
   - **Pinned-decision terminology** is current (Go-first; DBOS / SagaCoordinator, Temporal a
     contingency; Cedar-only / relationship-resolver, OpenFGA deferred; Tessera + internal
     RFC3161 TSA + cross-org witness; SeaweedFS not MinIO; Valkey not Redis; OpenBao not Vault) —
     **unless** the passage is describing the commoditized *market* (naming Rekor/OpenFGA as
     examples is fine there).
   - **Quantitative consistency** — a figure (ACV band, utility-tax, a count like "three proofs")
     reads the same everywhere and matches its list.
   - **One canonical home** — the change links to the owner of a fact rather than restating it.
   - **Honesty** — statistics/prices/dates cited or `UNVERIFIED`; opinions `[OPINION]`; "evidence
     is regulator-grade forensic-reproducible", never "court-admissible".
3. **Summarize** pass/fail with `file:line` for each remaining issue. A single unresolved ERROR
   blocks finishing until fixed or explicitly justified.

## Outputs
- `RESULT: PASS` from `docs-check.py`, plus a short note on the judgment checks.

## Done criteria
- [ ] `docs-check.py` prints `RESULT: PASS` (zero ERRORS).
- [ ] No `docs/private` reference, no Turkish leak, in any public doc.
- [ ] Relative links resolve; Mermaid ASCII-safe; one H1, no front-matter.
- [ ] Gate/pillar mapping and pinned-decision terminology correct (not a market description).
- [ ] Quantitative figures and counts consistent; honesty markings present.

## Common pitfalls
- Treating a WARNING as ignorable — `/Users/…` or `teardown` in a public doc is usually a real leak.
- "Fixing" a market-description by forcing Provna's pinned name into it (changes meaning).
- Forgetting the script can't judge meaning — the gate/pillar and quantitative checks are manual.
- Editing `CLAUDE.md`/`AGENTS.md`: they may name `docs/private` to *state the rule* (exempted).

## Related
- The script: ../../hooks/docs-check.py · The hook: ../../settings.json (PostToolUse)
- ../review-docs/SKILL.md, ../../agents/provna-docs-reviewer.md
- ../../../docs/standards/documentation-style.md
