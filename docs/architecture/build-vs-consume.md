# Build vs Consume

**Status:** Planned (pre-build)
**Last updated: 2026-06-24**
**Related:** [overview.md](overview.md), [../product-scope.md](../product-scope.md), [../positioning.md](../positioning.md), [pillar-1-information-flow-control.md](pillar-1-information-flow-control.md), [pillar-2-transactional-compensation.md](pillar-2-transactional-compensation.md), [pillar-3-runtime-authorization.md](pillar-3-runtime-authorization.md), [pillar-4-tamper-evident-audit.md](pillar-4-tamper-evident-audit.md)

This is the canonical build-vs-consume doc. It is the discipline that keeps Provna thin-but-deep: build only the white space the market leaves open, consume everything that is commoditized or being absorbed by larger players. The decision is pinned in [../decisions/0003-build-vs-consume-boundary.md](../decisions/0003-build-vs-consume-boundary.md).

```mermaid
flowchart TB
    subgraph BUILD["BUILD -- real IP and moat"]
        B2["S2 compensation library plus round-trip harness -- the real moat"]
        B1["S1 CaMeL P/Q isolation plus runtime-taint lattice fusion"]
        B3["S3 AND-gate resolver plus caveat-attenuation plus 5th-dimension admission"]
        B4["S4 Article 12 and 14 evidence pack plus external anchor binding"]
    end
    subgraph CONSUME["CONSUME or ASSEMBLE -- commoditized or being absorbed"]
        C0["S1 IFC reference -- FIDES plus dromedary as prototype substrate"]
        C1["Saga mechanism -- DBOS Transact now, Temporal contingency"]
        C2["PDP -- Cedar-embedded now, OpenFGA deferred, AuthZEN 1.0"]
        C3["Audit infra -- OTel, Tessera, internal RFC3161 TSA, cross-org witness, RFC8785 JCS"]
        C4["Probabilistic pre-filter -- self-hosted Llama Prompt Guard 2"]
        C6["Data -- Postgres, Valkey, SeaweedFS or customer in-VPC S3"]
        C5["Eval -- AgentDojo, ASR plus utility-tax"]
    end
    BUILD ==>|"sits on top of"| CONSUME
```

The shape is deliberate: **BUILD sits on top of CONSUME.** Provna never rewrites the commodity substrate; it assembles it and pours its years of effort into the narrow white space the substrate cannot fill.

## What Provna BUILDS

| Built capability | Pillar | Why build it (not consume) |
|---|---|---|
| **Per-connector inverse library + round-trip test harness + observe-probe + API-version-pinned auto-runnable catalog** | S2 | The four-way white space. No horizontal, durable-execution, or security vendor builds this — they treat reversal as a "developer problem." The saga *mechanism* is commodity, but the *content* (validated, version-pinned, domain-specific inverses for FS back-office) requires multi-year accumulation. This is the real moat — **conditional** on that accumulation genuinely being hard (the single most critical assumption, to be validated with design partners). |
| **S1 CaMeL P/Q-LLM isolation + runtime-taint dual-lattice fusion** | S1 | The reference IFC primitives are now consumable (see the CONSUME table: Microsoft FIDES + dromedary), but the inline, fail-closed reference-monitor on the synchronous money-path stays BUILD: the immutable server-side label store, the signed principal-bound declassification node, the per-connector sink-policy catalog, and the S1<->S4 forensic declassification bridge. The deterministic guarantee must be anchored in our own lattice + sink-policy; it cannot be outsourced to a classifier or to a prototype substrate. |
| **AND-gate resolver + real caveat-attenuation + transitive revocation + 5th-dimension behavioral admission** | S3 | The PDP itself is consumed; what is built is the *thin* resolver fusing four axes (user and intent are absent in competitors), genuinely-implemented attenuation (irreversibly add a constraint, not exact-match subset), and the context-scoped behavioral admission layer with `PatternKey` partitioning to avoid state-mixing. |
| **EU AI Act Article 12/14 evidence pack + external-anchor binding + portable witness + policy_snapshot_ref** | S4 | The crypto mechanisms are assembled, but the *regulator-grade FS evidence pack* (Article 12 forensic reproducibility, Article 14 human oversight, DORA, MiFID II mapping) and the binding of governance-failure signals into the signed ledger are domain depth no horizontal player carries. |

## What Provna CONSUMES or ASSEMBLES

| Consumed component | Used for | Why consume it (commoditization / absorption) |
|---|---|---|
| **Microsoft FIDES + dromedary** (MIT) | S1 IFC reference + prototype substrate | The old premise that no production IFC plane exists is outdated. FIDES (in microsoft/agent-framework, provider-agnostic Python) is consumed as the Q-LLM-isolation + label-propagation reference and the prototype substrate for the MVP PoC and the AgentDojo eval; dromedary (a CaMeL implementation: privileged LLM + quarantined `query_ai_assistant` + custom interpreter + OPA policy) is the interpreter/capability reference. They are a reference and a prototype, not the production guarantee — the inline fail-closed reference-monitor (the BUILD row above) is never delegated to them. See [tech-stack-analysis.md](tech-stack-analysis.md). |
| **DBOS Transact** (Temporal as a contingency) | The saga execution mechanism | Resumability and exactly-once are commoditized substrate. Ship on DBOS Transact + Postgres for the MVP and early production; keep the substrate behind the gRPC ActionGuard seam plus a thin SagaCoordinator interface and pre-write a Temporal adapter spike, but migrate only if a concrete trigger fires (multi-tenant fan-out, a Postgres throughput/latency ceiling, or a buyer mandate). This is not a scheduled migration. The compensation *content* is the moat, independent of the substrate. See [tech-stack-analysis.md](tech-stack-analysis.md). |
| **Cedar (embedded), OpenFGA (deferred) + AuthZEN 1.0** | The PDP behind the AND-gate | S3 is a saturated market (CrowdStrike acquired SGNL for roughly 740M USD). For the MVP the PDP is embedded Cedar only (formally verified, single failure domain, lowest latency, best air-gap story) with relationships modeled as Cedar entities; OpenFGA is deferred behind a relationship-resolver interface and added only when a design partner's entitlements are provably ReBAC. AuthZEN 1.0 alignment is a real differentiator because the leading horizontal substrate does not implement it; biscuit for caveat-attenuation and IETF transaction-tokens for delegation wire-format. See [tech-stack-analysis.md](tech-stack-analysis.md). |
| **OpenTelemetry + Tessera + internal RFC3161 TSA + cross-org witness + RFC8785 JCS** | Audit transport, transparency log, timestamp anchor, third-party non-repudiation | The format is open and the mechanism is commodity. Air-gapped anchoring uses a self-hosted transparency log (Tessera, the Go successor to Trillian) plus an internal HSM-backed RFC3161 TSA, with the log checkpoint countersigned (tlog-witness / cosignature) by an independent trust domain pre-provisioned on both sides of the air gap — third-party non-repudiation without public-network egress. RFC8785 JCS canonicalization with a kid-embedded portable witness; Rekor v2 as a reference design; optional ML-DSA (FIPS 204) for long retention. Value accrues from being the system of record and the FS mapping, not from reinventing the log. See [tech-stack-analysis.md](tech-stack-analysis.md). |
| **Self-hosted Llama Prompt Guard 2** | Optional probabilistic pre-filter | A classifier is only an optional pre-filter, explicitly OFF the deterministic guarantee path, never the architectural guarantee. Self-hosted (86M multilingual / 22M low-latency); do not depend on any SaaS detector. Selling a classifier as a guarantee is exactly the weakness the IFC fusion is designed to avoid. See [tech-stack-analysis.md](tech-stack-analysis.md). |
| **Postgres + Valkey + SeaweedFS or customer in-VPC S3** | State, ledger, cooldown/rate counters, object storage | Commodity data substrate. Postgres for state + ledger (partitioning, logical decoding for the audit stream, row-level security, encryption-at-rest); Valkey (BSD, Linux Foundation fork) instead of Redis, or fold cooldown/rate counters into Postgres where feasible. Object storage defaults to SeaweedFS (Apache-2.0, single-binary) behind a swappable S3 API seam, and can target the customer's existing in-VPC S3 endpoint (Ceph / Dell ECS / NetApp) as a config switch; MinIO is dropped (AGPLv3 + archived). See [tech-stack-analysis.md](tech-stack-analysis.md). |
| **AgentDojo** | Evaluation: attack success rate (ASR) plus utility-tax, measured together | Measurement infrastructure is commodity. What Provna owns is the discipline of publishing ASR and utility-tax together (so "block everything" is not a hidden win) plus FS-domain ground-truth. |

## The reasoning behind the boundary

Two forces decide every row:

- **Commoditization.** Anything where the mechanism is open, standardized, or weekend-buildable (saga execution, PDP, audit transport, eval harness) is consumed. Owning it adds no defensibility and burns the runway.
- **Absorption.** Anything a larger player is actively absorbing (the PDP market by identity giants; horizontal governance by Microsoft) is consumed and aligned with, never contested head-on. The pitch always rests on the two genuinely defensible pillars, S1 and S2.

Defensibility is in **substance (S1 + S2)**, not in **position (S3 + S4)** — roughly a 12 to 24 month window. The build list is therefore narrow on purpose. Absorption vectors and the counter-moves (S2 vertical-FS connectors, Article 12/14 depth, IFC fusion) are in [../positioning.md](../positioning.md).

## Tie to scope discipline

The single scope test, from [../product-scope.md](../product-scope.md): *does this make one guarded saga step more secure, more reversible, or more provable — or does it turn Provna into an agent platform?* If the latter, reject or consume it. Three concrete guards:

1. **Build only the white space the fusion does not close** (S2 compensation + S1 capability-IFC); the rest (PDP, durability, audit infra, eval) is consumed or assembled.
2. **Expand in the vertical, never horizontally** — add a second vertical (healthcare/insurance), never a second product category (gateway, framework).
3. **Pitch always rests on S1 + S2** — becoming "a runtime plus a bit of governance" is fatal.
