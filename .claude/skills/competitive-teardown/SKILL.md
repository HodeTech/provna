---
name: competitive-teardown
description: >
  Deeply review a competitor or reference (an open-source repo or a product) and write a
  structured, evidence-cited teardown plus a Provna-implications synthesis INTO docs/private/.
  USE FOR: a code-level or doc-level intelligence dossier on a rival/reference (e.g. an agent-
  governance toolkit, an IFC engine, a durable-execution substrate) mapped to Provna's four
  pillars. DO NOT USE FOR: writing public docs (use ../write-doc/SKILL.md) — teardowns are
  internal and public docs never reference them.
---
# Competitive teardown

## Purpose
Turn a competitor or reference into a rigorous, Provna-oriented dossier: what it is, how it is
built, and — pillar by pillar — what Provna can learn, consume, or must out-build. Output lives
**under `docs/private/`** (gitignored), where Turkish is allowed; it is never cited from a public
doc. Bringing a finding into the public tree means *restating it self-contained* via `write-doc`
or `apply-decision`, never linking the teardown.

## When to use
- Sizing a competitor/reference repo (clone-and-read) or a product (docs/whitepaper-level).
- Validating where Provna's moat (S2 compensation, S1 IFC fusion) is genuinely open vs closed.

## When not to use
- Producing anything public — teardowns are internal only (rule #2).
- Re-running an existing teardown's conclusions across docs — use `../apply-decision/SKILL.md`.

## Inputs
| Input | Description |
|-------|-------------|
| Target | A repo URL (clone-able) or a product (name + docs/site). |
| Output dir | `docs/private/<short-name>/` (kebab; the product's own short name). |
| Depth | "doc-level" (closed/commercial) or "code-level" (open-source, clone and read). |

## Workflow
1. **Acquire — to a temp dir, never the repo.** Shallow-clone an open-source target to a scratch
   dir (e.g. `/tmp/teardown/<name>`); for a product, gather its docs/whitepapers. For current
   facts (funding, license, 2026 maturity) use WebSearch/WebFetch — do not trust memory; mark
   unconfirmed claims `DOĞRULANMADI`/`UNVERIFIED`.
2. **Map the structure.** File counts, languages, top-level layout, the subsystems. Decide the
   review breakdown (one section per meaningful subsystem).
3. **Review subsystem by subsystem** — for a code-level teardown, read the actual source and
   cite evidence as `path:line`. For breadth, fan out (parallel readers / a Workflow) so each
   subsystem gets a focused, thorough pass; be concrete (real names, counts, dependencies), not
   marketing-level. Flag everything that touches Provna's four pillars (S1 IFC / taint, S2
   transactional compensation / saga, S3 authz / delegation, S4 tamper-evident audit / anchor),
   plus prompt-injection, MCP, and EU-FS regulation.
4. **Synthesize the Provna implications** — the most valuable doc. Map the target to Provna's
   four pillars (present / partial / absent, with code evidence and maturity); assess it as a
   *threat* vs a *reference/consume-substrate*; call out, honestly, whether it closes either
   moat (S2 compensation library; runtime-tracked deterministic IFC). End with concrete,
   actionable conclusions and any suggested edits to the founding thesis.
5. **Write the dossier into `docs/private/<name>/`** — a numbered set of section docs plus the
   implications synthesis as the final doc, and a `README.md` index. Match the language and
   style of the existing private analysis (Turkish prose with English technical terms;
   `[GÖRÜŞ]`/`DOĞRULANMADI` markings; evidence by path).
6. **Clean up** the temp clone. **Do not** add any reference to `docs/private/<name>/` from a
   public doc — verify with `python3 .claude/hooks/docs-check.py` that nothing leaked into the
   public tree.

## Outputs
- `docs/private/<name>/` — section docs + a Provna-implications synthesis + a README index.
- (Optional) a short memo to the maintainer recommending which findings to fold into the public
  thesis via `apply-decision` / `write-doc`.

## Done criteria
- [ ] Output lives entirely under `docs/private/<name>/`; the temp clone is removed.
- [ ] Each load-bearing claim is evidence-cited (`path:line` for code; URL for facts); unconfirmed marked `DOĞRULANMADI`/`UNVERIFIED`.
- [ ] A pillar-by-pillar Provna-implications synthesis is the final doc, with an honest threat/reference verdict.
- [ ] `docs-check` confirms **no public doc references** the teardown.

## Common pitfalls
- Leaking a teardown path/filename into a public doc (the cardinal rule — `docs-check` blocks it).
- Marketing-level summary instead of code-level evidence on an open-source target.
- Stating 2026 facts (funding, license, maturity) from memory instead of the web.
- Forgetting to remove the temp clone, or writing the dossier into the public `docs/` tree.

## Related
- ../apply-decision/SKILL.md, ../write-doc/SKILL.md, ../docs-check/SKILL.md
- The private analysis already in docs/private/ (style reference; never linked publicly).
