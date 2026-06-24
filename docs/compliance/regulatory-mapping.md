# Regulatory Mapping

**Status:** Draft / pre-build reference
**Last updated: 2026-06-24**
**Related:** [../architecture/pillar-4-tamper-evident-audit.md](../architecture/pillar-4-tamper-evident-audit.md), [../architecture/pillar-3-runtime-authorization.md](../architecture/pillar-3-runtime-authorization.md), [../architecture/pillar-1-information-flow-control.md](../architecture/pillar-1-information-flow-control.md), [../business/icp-and-gtm.md](../business/icp-and-gtm.md), [../positioning.md](../positioning.md)

This is the canonical home for how Provna's architecture maps onto the regulatory obligations that the ICP (EU-exposed financial-services back/mid-office) must satisfy. It is the **deal-unblocker dossier**: the Verifier persona (Internal Audit / SOX) does not buy Provna, but a single "no" from them kills the deal, and their "yes" is the precondition for the Economic Buyer's "yes". This document is what turns "we deployed an agent" into "we can prove, to a regulator, what the agent did, who authorized it, with which data, and that the record was not altered".

Provna sells **permission to ship**, not security. The frame here is the same: each regulation below is a continuing obligation that recurs every audit cycle. Provna does not promise to make the deadline (the product is pre-build and the EU AI Act Article 12/14 application date (commonly cited as 2 Aug 2026, UNVERIFIED) is near-term); it solves the **permanent** obligation that survives every deadline.

---

## The honesty anchor (read this first)

> Provna's evidence is **regulator-grade / forensic-reproducible**. "Court-admissible" is **case-by-case and jurisdiction-dependent** UNVERIFIED. EU AI Act Article 12 forensic-reproducibility is **not** a guarantee of evidentiary admissibility in any specific court; the two must never be conflated. Overstated guarantees are punished by the Audit persona, who trusts the vendor that draws the boundary honestly.

Likewise, the S1 information-flow guarantee is bounded: untrusted data cannot reach a sensitive sink unless an explicitly-typed policy authorizes the flow, and all flows are deterministically enforced pre-execution and tamper-evident logged. **Implicit-flow and side-channel leakage are NOT guaranteed.** Every compliance claim below inherits these two boundaries.

---

## How the pillars satisfy obligations (the three load-bearing primitives)

Three architectural primitives carry almost every mapping below:

- **S4 evidence pack** — OpenTelemetry capture + hash-chain + Merkle root + external anchor (a self-hosted transparency log (Tessera) + an internal HSM-backed RFC3161 TSA + a cross-organization witness cosignature, with Rekor v2 as the reference design) + RFC8785 JCS canonicalization + `kid`-embedded portable witness + `policy_snapshot_ref` on every decision + a signed, persisted governance-failure (BAR-style) audit event. This is what makes the record **forensic-reproducible** and insider-rewrite resistant: even a key-holder or operator cannot rewrite history consistently, because the external anchor provides independent time and third-party verification.
- **S3 human oversight** — risk-tiered HITL with dry-run preview, four-eyes approval on high-value / irreversible actions, and the AND-gate (`agent AND user AND delegation AND intent`) that records *who* authorized each action under *what* delegation for *what* intent.
- **S1 fail-closed information-flow control** — unlabeled data is treated as untrusted; on any error the action is BLOCKED; there is no downgrade path. This is the architectural (not probabilistic) defense that lets a CISO sign off on a money-path agent.

---

## Mapping table

| Regulation / framework | What it requires (in scope for the ICP) | How Provna maps | Carrying pillar |
|---|---|---|---|
| **EU AI Act — Article 12 (record-keeping)** | Automatic logging of events over the system's lifetime; logs must enable identification of situations that may make the system risky or trigger substantial modification; traceability and forensic reproducibility of how an output was produced; log integrity. | Every guarded saga step emits a structured, signed, externally-anchored audit event with `policy_snapshot_ref` (the exact policy hash in force at decision time), inputs/labels, verdict, and outcome. The Merkle root + external anchor make the log integrity-verifiable by an independent auditor; the `kid`-embedded portable witness lets verification happen without access to the local signing key. "Why/what/when" is reproducible per action. | S4 (anchor + JCS + `kid` + `policy_snapshot_ref`) |
| **EU AI Act — Article 14 (human oversight)** | Effective oversight by natural persons; the ability to interpret output, to decide not to use it, and to intervene or interrupt ("stop" button); oversight proportionate to risk. | Risk-tiered HITL: high-value / irreversible actions are previewed via **dry-run** and gated on **four-eyes** approval before execution; the human verdict (approved / rejected) is itself a signed audit event. Behavioral/temporal admission can ESCALATE to human review rather than silently proceeding. Fail-closed means the default on uncertainty is to stop, not to proceed — the architectural form of an interrupt. | S3 (HITL, four-eyes, AND-gate) + S2 (dry-run) |
| **DORA (Digital Operational Resilience Act)** | **Continuing** operational-resilience obligations for financial entities: ICT risk management, logging, incident reproducibility, long-retention of records, and demonstrable controls over critical operations — re-evidenced every audit cycle, not once. | The evidence store is a long-retention, integrity-anchored system-of-record (object store (SeaweedFS, or the customer in-VPC S3 endpoint) + Merkle + external anchor). Reversibility (per-connector inverse + two-phase for irreversible actions) is an operational-resilience control: a faulty agent action can be compensated rather than leaving the system in a broken state. The signed BAR-style governance-failure event is forensic proof that enforcement was actually active. This is positioned as the **permanent** forcing-function (vs the one-time Article 12/14 application date). | S4 (long retention + anchor) + S2 (reversibility) |
| **MiFID II** | Record-keeping and reconstruction obligations for in-scope activities (e.g. order/transaction records, time-stamping, reproducibility of decisions affecting client-facing financial operations). | Independent, externally-anchored time-stamping (RFC3161 TSA — not a self-clock) and per-action reconstructible records satisfy the reconstruction/time-stamp expectations for governed financial actions. `policy_snapshot_ref` reconstructs the exact rule set under which a decision was made. | S4 (RFC3161 external time + reconstructible record) |
| **ISO/IEC 42001 (AI management system)** | An auditable AI management system: documented controls, risk treatment, monitoring, and continual improvement over AI systems. | Provna provides the **runtime control evidence** an ISO 42001 AMS needs: enforced policies (with versioned, tamper-evident policy snapshots), monitoring (the audit ledger), human-oversight records, and incident/governance-failure signals. Provna is a control-and-evidence layer inside the customer's management system, not the management system itself. | S4 (versioned policy + ledger) + S3 (oversight records) |
| **NIST AI RMF** | Voluntary risk-management functions — Govern, Map, Measure, Manage — for trustworthy AI; emphasis on measurement and documented risk treatment. | **Measure**: published AgentDojo results (ASR + utility-tax together) plus FS-domain ground-truth give measured assurance, not asserted assurance. **Manage**: fail-closed enforcement + compensation are concrete risk-treatment controls. **Govern/Map**: the AND-gate and IFC policies document who/what/which-data is authorized per action. | S1 (measured ASR) + S2/S3 (managed risk) |
| **SOC 2** | Trust-services controls (notably Security, Availability, Processing Integrity, Confidentiality) demonstrated to an external auditor over a period. | Provna's own audit ledger demonstrates processing-integrity and confidentiality controls over governed actions; fail-closed behavior and signed evidence support the Security and Processing-Integrity criteria. SOC 2 is started in the enforcement phase as part of becoming a trustworthy system-of-record. (SOC 2 is about Provna as a vendor; the rows above are about what Provna lets the *customer* prove.) | S4 (integrity evidence) + S1 (fail-closed) |

---

## A note on AIUC-1 and where primary legitimacy is anchored

AIUC-1 is a relevant industry assurance mapping and Provna will map to it as a secondary signal. However, AIUC-1 has a **conflict-of-interest critique** UNVERIFIED, so Provna does **not** anchor its primary regulatory legitimacy there. Primary legitimacy is anchored to **ISO/IEC 42001 + the EU AI Act** (Articles 12 and 14), with DORA and MiFID II as the continuing financial-services forcing-functions. AIUC-1 is mapped, not relied upon.

## Two boundaries restated (do not let the dossier overreach)

1. **Forensic-reproducible, not court-admissible.** The evidence reconstructs the action faithfully and resists tampering; whether a given record is admissible in a given court is case-by-case / jurisdiction-dependent UNVERIFIED. Never sell admissibility.
2. **Information-flow guarantee is bounded.** The deterministic guarantee covers explicit flows from untrusted source to sensitive sink; implicit-flow and side-channel leakage are not guaranteed. State this limit in every audit-facing conversation — the boundary is a trust-builder, not a weakness to hide.
