# Architecture Decision Records

**Status:** Living index
**Last updated: 2026-06-24**
**Related:** [../standards/adr-template.md](../standards/adr-template.md), [../standards/documentation-style.md](../standards/documentation-style.md), [../architecture/build-vs-consume.md](../architecture/build-vs-consume.md)

This directory holds the load-bearing decisions that define what Provna is, what it deliberately is not, and where its real engineering effort goes. An ADR (Architecture Decision Record) captures a single decision: the **Context** that forced a choice, the **Decision** itself (with the alternatives we considered and rejected written inline), and the **Consequences** we accept as a result. ADRs are append-only history: we do not delete a decision, we supersede it with a newer one and update the status.

We use a condensed MADR format. Each record leads with the same three sections so a reader can scan Context to Decision in seconds. Alternatives are not a separate section: they are written inline in the Decision as `Considered: A (rejected: ...), B (...); chose X because ...`. Consequences split into `### Positive` and `### Negative` because every real decision costs us something, and naming the cost is how we keep ourselves honest. See [../standards/adr-template.md](../standards/adr-template.md) for the exact shape.

## When to write an ADR

Write one when a decision is (a) hard to reverse, (b) cross-cutting (it constrains more than one component), or (c) likely to be questioned later ("why didn't you just use OPA / undo everything / go horizontal?"). A decision that only affects one file's internals does not need an ADR; a decision that shapes the moat does.

## Status values

- **Proposed** - decision drafted, not yet ratified (often blocked on an external dependency such as trademark clearance).
- **Accepted** - ratified; the codebase and plan must be consistent with it.
- **Superseded by NNNN** - replaced by a later ADR.
- **Deprecated** - no longer applies and not replaced.

## Index

| # | Title | Status |
|---|---|---|
| [0001](0001-atomic-unit-guarded-saga-step.md) | Atomic unit is the guarded saga step | Accepted |
| [0002](0002-vertical-fs-beachhead.md) | Vertical FS back-office beachhead | Accepted |
| [0003](0003-build-vs-consume-boundary.md) | Build-vs-consume boundary | Accepted |
| [0004](0004-s1-camel-pq-isolation-runtime-taint-fusion.md) | S1: CaMeL P/Q isolation + runtime-taint fusion | Accepted |
| [0005](0005-s2-dbos-substrate-compensation-library.md) | S2: DBOS substrate, BUILD the compensation library | Accepted |
| [0006](0006-s3-and-gate-attenuation-behavioral-admission.md) | S3: AND-gate + attenuation + behavioral admission | Accepted |
| [0007](0007-s4-merkle-external-anchor-jcs.md) | S4: Merkle + external anchor + JCS | Accepted |
| [0008](0008-polyglot-data-plane-control-plane.md) | Polyglot data-plane / control-plane split | Accepted |
| [0009](0009-action-guard-seam-vendor-neutral.md) | ActionGuard seam, vendor-neutral surfaces | Accepted |
| [0010](0010-fail-closed-everywhere.md) | Fail-closed everywhere | Accepted |
| [0011](0011-open-source-boundary-proprietary-core.md) | Open-source boundary, proprietary core | Accepted |
| [0012](0012-pricing-metered-governed-action.md) | Pricing: metered governed-action, no per-seat | Accepted |
| [0013](0013-deployment-vpc-airgapped-k8s-helm.md) | Deployment: customer VPC / air-gapped, K8s/Helm | Accepted |
| [0014](0014-name-provna-trademark-clearance.md) | Name "Provna" + trademark clearance | Proposed |

ADRs 0006 through 0014 are authored in adjacent clusters; this index is the canonical home for the full list. Each row links to the record; the records never restate this table.
