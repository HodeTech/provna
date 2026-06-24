# ADR-0002: Vertical FS back-office beachhead

**Status:** Accepted
**Last updated: 2026-06-24**
**Related:** [../positioning.md](../positioning.md), [../business/icp-and-gtm.md](../business/icp-and-gtm.md), [../compliance/regulatory-mapping.md](../compliance/regulatory-mapping.md), [0001-atomic-unit-guarded-saga-step.md](0001-atomic-unit-guarded-saga-step.md)

## Context

Provna's atomic unit (see [0001-atomic-unit-guarded-saga-step.md](0001-atomic-unit-guarded-saga-step.md)) is vertical-agnostic in principle - any regulated write could be governed. But "governs any agent action anywhere" is exactly the horizontal position that a hyperscaler ships for free. We have to choose a beachhead narrow enough to win and deep enough to defend, and the choice is forced by where the buyer's pain is unavoidable, budgeted, and deadline-bearing.

Five properties make EU-exposed financial-services back- and middle-office the sharpest wedge. (R1) **Errors are irreversible and pre-budgeted**: money movement cannot be un-sent, and SOX / four-eyes controls mean the buyer already funds this category. (R2) **The densest date-stamped regulation**: EU AI Act Article 12 (forensic reproducibility) and Article 14 (human oversight), plus DORA and MiFID II, create a continuous evidence obligation rather than a one-off. (R3) **A live business pull**: banks are deploying reconciliation, accounts-payable, and close agents but have no safe write layer, so the projects stall in read-only pilots. (R4) **Integration is idempotency-native**: payment rails and ERPs already expose void/reversal/refund primitives, which is what compensation needs. (R5) **Highest founder-fit**: saga design, compliance mapping, and FS-domain ground-truth (did the agent actually close the reconciliation correctly) line up.

## Decision

**Narrow the initial market to the EU-exposed financial-services back- and middle-office vertical - the wedge being payment / supplier-payment approval or reconciliation-break correction - and explicitly reject horizontal agent-governance as a position.**

Considered: **horizontal agent-governance** (govern any agent action across any vertical - rejected: Microsoft ships horizontal governance free and open-source; the horizontal position is dead on arrival, and the same shallowness that makes the horizontal substrate free is what validates our vertical-depth thesis); **IT / cloud-ops** (govern infrastructure-mutating agents - rejected as a strong #2: the forcing function is weaker because the buyer has no date-stamped regulator demanding per-action forensic proof); **healthcare revenue-cycle management** (regulated, irreversible, real pull - rejected as a #2: the integration surface is hostile, with fragmented and PHI-laden systems that lack the clean void/reversal primitives FS rails already expose); chose **EU-exposed FS back-office** because it is the only candidate that satisfies all five properties at once - irreversibility plus existing budget plus continuous regulatory forcing plus idempotency-native integration plus founder-fit.

We do not pitch the EU AI Act deadline as a one-time finish line; that framing collapses against a sophisticated buyer the day after the date passes. The durable selling engine is the **recurring** obligation: DORA's ongoing operational-resilience duties, the evidence demand that repeats every audit cycle, and the permanent risk appetite around irreversible money movement. The deadline is a conversation-starter; the recurring obligation is the contract.

## Consequences

### Positive

- A single, sharp ICP for GTM (see [../business/icp-and-gtm.md](../business/icp-and-gtm.md)): EU-exposed bank / payments / fintech / treasury, 1000+ employees, with a blocked agent project in finance-ops.
- Depth becomes the moat: vertical-FS connectors with verified inverses plus Article 12/14 evidence packs are a domain depth a horizontal security firm cannot reach, which is the structural counter to absorption.
- The regulatory mapping (see [../compliance/regulatory-mapping.md](../compliance/regulatory-mapping.md)) becomes a deal-unblocker dossier rather than a checkbox.

### Negative

- We forgo the larger horizontal TAM and the easier "works everywhere" marketing story.
- Concentration risk: if FS back-office adoption stalls, the whole beachhead stalls; the #2 verticals (healthcare/insurance) are deliberately deferred to a later phase, so there is no near-term fallback market.
- The vertical demands real domain investment (connector inverses, FS ground-truth, EU compliance depth) before the first dollar, raising the cost of the first proof.
