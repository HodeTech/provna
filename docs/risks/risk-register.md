# Risk Register & Red Lines

**Status:** Draft / pre-build reference
**Last updated: 2026-06-24**
**Related:** [../positioning.md](../positioning.md), [../roadmap/README.md](../roadmap/README.md), [../roadmap/current.md](../roadmap/current.md), [../decisions/0014-name-provna-trademark-clearance.md](../decisions/0014-name-provna-trademark-clearance.md), [../compliance/regulatory-mapping.md](../compliance/regulatory-mapping.md)

This is the canonical home for the things that can dilute or kill Provna, and the **rule** bound to each one. The format is deliberate: a risk is not actionable until it has a one-line rule the team can enforce in a design review or a sales call. Some of these are **red lines** — crossing them is not a degraded outcome, it is a different (and losing) company.

The single most important framing: Provna is **defensible in substance (S1 information-flow fusion + S2 transactional compensation), not in position (S3 authorization + S4 audit infrastructure are commodity)**. The clock is roughly 12-24 months [OPINION]. Every rule below ultimately serves one goal: keep the pitch anchored to S1+S2 and spin the compensation flywheel before the absorption window closes.

---

## Red lines (crossing one is fatal)

| Risk / red line | Why it is fatal | Rule |
|---|---|---|
| **Horizontal drift** — repositioning as a generic "agent governance control plane" | Microsoft (MGAT) is embedding horizontal governance for free; on the horizontal axis Provna gets crushed. The horizontal dream is dead; the same MGAT weaknesses (S2 stub, host-dependent IFC, unsigned audit, non-EU compliance) actually validate the vertical-depth thesis. | Pitch is always S1+S2 substance. Expand on the vertical axis (second vertical: healthcare/insurance), never on the horizontal axis (never add a second product category). |
| **Scope creep** — building a gateway, an agent framework, or a generic PDP | The buyer (CISO) does not buy a framework; building adjacent platform layers dilutes the moat and burns the runway that should go into the compensation library. | One test for any feature request: "Does this make a single guarded saga step safer / more reversible / more provable, or does it turn Provna into an agent platform?" If the latter — reject or consume. Build only the white space the fusion does not close (S2 compensation + S1 capability-IFC); consume/assemble everything else (PDP, durability, audit infra, eval). |
| **Becoming "Relavium for enterprises"** | Vendor neutrality is the actual defensibility; collapsing onto a single runtime destroys it. The reason to choose Provna was *not being horizontal* and *owning the hard pillars* — "Relavium plus a little governance" throws that away. The cultures are opposite (local-first / BYOK vs enterprise-VPC / compliance); early focus-drift is fatal. | `govern()` must work for LangChain / OpenAI-SDK / custom runtimes too. Relavium is the **first reference** integration (one door), never the only door. Prove vendor neutrality beyond Relavium on the roadmap. |
| **Fail-open / observability-shim** | A PostToolUse log with `enforcement_mode=observe` and `sys.exit(0)` gives the *feeling* of security with no real deny — it collapses under audit. This is precisely the competitor weakness Provna torpedoes (Invariant fails open on a crashed policy check; an observability-shim is not a reference monitor). | Fail-closed everywhere: unlabeled => untrusted, error => BLOCK, no downgrade path, revocation/CRL fail-closed. For Claude Code use a **real PreToolUse deny** (exit-2 / `permissionDecision: deny`), never audit-only-masquerading-as-control. |
| **Overstating compensation** — "undo everything" | Compensation is semantic and sometimes impossible; "undo everything" is a lie that destroys trust the moment it fails. | Never sell "undo everything". Prefer two-phase (auth -> capture -> void) for irreversible actions; gate the irreversible on HITL; state the guarantee boundary honestly. In the developer wedge say "risky actions are prevented, connector-backed actions are reversed" — not "everything is reversible". |
| **Name connotation** [OPEN — must close before finalizing the brand] | RU/UK *provina* means roughly "fault / guilt"; for EU-FS selling this could be fatal. A "final" brand must not ship with an open trademark/connotation risk. | Native-speaker check (5 minutes, critical path, has been pending) + provna.com/.ai/.io + USPTO/EUIPO class 9/42. Do not commit the brand to domain/code/marketing until cleared; record the outcome. See [../decisions/0014-name-provna-trademark-clearance.md](../decisions/0014-name-provna-trademark-clearance.md). |

---

## Strategic risks (manage, do not necessarily avoid)

| Risk | Why it hurts | Rule |
|---|---|---|
| **Absorption** — Snyk moves down, Temporal moves up, Microsoft organic, Rubrik perception | ~12-24 month window; position is not defensible. If Temporal moves up, it stops being a substrate to consume and becomes a competitor. | Anchor to substance (S1+S2). **Snyk-down:** nail the S2 catalog to vertical-FS connectors (NetSuite/Stripe/SWIFT/ledger) + integrate Article 12/14 evidence — domain depth a horizontal S1 firm cannot reach. **Temporal-up:** pool value where Temporal does not / cannot go — IFC-aware compensation + signed/anchored regulator-grade compensation proof + vertical-FS connector content; horizontal durability is not the EU-FS forensic + IFC-fusion category. **Rubrik-perception:** counter-position "snapshots cannot un-send a sent email or un-trigger a payment" with a live demo. **Microsoft-organic:** do not race horizontally; narrow build to S2 + S1-runtime-IFC + Article 12/14; consume ACS as a PDP substrate; lead with DORA/MiFID II depth. Spin the flywheel fast. |
| **Flywheel assumption proves false** | The hardest moat (the per-connector compensation library) only holds **if** compensation content genuinely requires multi-year accumulation ("buy < build"). If compensation is easy, the flywheel is a weak moat. This is the single most critical unvalidated assumption. | Validate this FIRST with design partners (the S2 PoC, step 2 of the first five steps, is also the first measurement of "is compensation actually hard"). Until validated, present the moat as **conditional** — never sell it as certainty; lean harder on vertical-FS + IFC-fusion as the fallback. |
| **Patent conflict** — MVAR provisional patent (Feb 2026, combination claims on taint-laundering prevention / execution-witness binding) + ACP S3 stateful-admission prior-art | Combination claims and prior-art on the behavioral-admission "5th dimension" create legal exposure and naming risk. | Re-implement the primitives independently via prior art (Jif / FlowCaml / Capsicum / Ed25519). Position the 5th dimension as a "context-scoping-corrected implementation" (it fixes the state-mixing CVE), not as a novel invention. **Do not use the competitor brand names** (MVAR / MIRRA / QSEAL / ACP) in product, code, or marketing. |
| **Fake statistics** — unsourced percentage claims | If a CISO or auditor asks for the source and there is none, the entire document loses credibility. | Market statistics are either sourced or softened to "a large majority [UNVERIFIED]". False precision (e.g. "92.5%") is banned. |
| **Deadline over-promise** | The product does not make the EU AI Act application date (commonly cited as 2 Aug 2026, UNVERIFIED); claiming "we make it" gets caught by a sophisticated buyer. | Shift to the continuing forcing-functions — DORA's ongoing operational-resilience obligations + the evidence demand that recurs every audit cycle. Do not hang the sale on a single date; sell the permanent obligation. |
| **The standard threat (ACS)** [UNVERIFIED] | An "Agent Control Standard" could standardize interception and commoditize part of the surface. Note the triple confusion: ACS = Agent Control *Standard* (businesswire, UNVERIFIED adoption) vs *Specification* (Microsoft MGAT Rust PDP) vs ACP = Agent Control *Protocol*. | Embrace-implement-own-the-layer-above: ACS does not say *how an action is reversed* or *how absence-of-injection is proven* — own exactly that (S2 + S1). Always disambiguate Standard / Specification / Protocol in any material to avoid being mistaken for an "MGAT-ACS clone". The AuthZEN opportunity is real (MGAT does not implement it). |

---

## Early-warning triggers (moat-attack signals)

The first-mover advantage is in **content accumulation, not architecture** — the saga mechanism is a commodity. So the canary is not someone building a saga coordinator; it is someone building reversal *content*.

> **Trigger:** the strings `rollback`, `compensat`, `saga`, `inverse`, or `undo` appearing for the first time in a non-test path of a competitor repo (e.g. an `invariant-gateway` / `snyk-agent-scan` surface, MVAR, ACP, or a Temporal-adjacent project) is a **direct moat-attack signal**.

When this fires:
- Re-confirm the flywheel-validation status with design partners immediately.
- Accelerate vertical-FS connector coverage and the round-trip test harness (depth they cannot copy quickly).
- Reinforce the parts they are structurally unlikely to follow: IFC-aware compensation + signed/anchored regulator-grade evidence + EU-FS regulatory depth (Article 12/14 + DORA + MiFID II).

## Kill-criteria (when to stop)

Not every risk is recoverable. Abandon or hard-pivot if any of these hold during the design-partner phase:
- No path to a paying contract within 90 days.
- Partners say "we can build it with OPA in one sprint" (the compensation moat is not real for them).
- Money-path latency cannot be fixed.
- The champion lacks budget + urgency.

The single 90-day pilot metric that decides success: a blocked agent project ships to (limited) production with risk-committee approval **because of** Provna.
