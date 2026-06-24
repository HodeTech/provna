# ADR-0007: S4 Tamper-Evident Audit — Merkle Root, External Anchor, JCS, Embedded Witness

**Status:** Accepted
**Last updated: 2026-06-24**
**Related:** [../architecture/pillar-4-tamper-evident-audit.md](../architecture/pillar-4-tamper-evident-audit.md), [0001-atomic-unit-guarded-saga-step.md](0001-atomic-unit-guarded-saga-step.md), [0006-s3-and-gate-attenuation-behavioral-admission.md](0006-s3-and-gate-attenuation-behavioral-admission.md), [0010-fail-closed-everywhere.md](0010-fail-closed-everywhere.md), [../compliance/regulatory-mapping.md](../compliance/regulatory-mapping.md), [../tech-stack.md](../tech-stack.md)

## Context

Gate 4 of the guarded saga step produces the evidence: for every action (allowed, blocked, dry-run, executed, compensated) a structured, tamper-evident record. The Verifier persona (Internal Audit / SOX) does not buy Provna — they *veto* it, and their approval is a precondition for the CISO's "yes." Six months after an action, a regulator asks: *why, who authorized it, with what data, and was the log altered?* The audit trail must answer this in a way that survives the threat model of an **insider or key-holder who wants to rewrite history**.

That threat model is exactly where the field is weak. Competitor implementations show two recurring failure modes:

- **Unsigned hash-chains / plain trace push.** A horizontal governance substrate emits unsigned HTTP traces; a hash-chain with no signature does not bind the record to a key. An insider can recompute the chain after editing an entry. This fails an audit.
- **Signed but self-clocked, unanchored.** Even with signatures, if timestamps come from the system's own clock (`datetime.now`), a key-holder can backdate and re-sign a *consistent* alternate history — the chain still verifies, but against a forged timeline. There is no independent third party to contradict the operator.

A further gap: governance-failure signals (e.g. a behavioral monitor firing) are often returned as transient alerts and never bound into the ledger, so there is no forensic proof that enforcement was actually active.

**The air-gap-vs-public-anchor tension.** The obvious way to inject an independent clock and an independent verifier is a *public* transparency log and a *public* TSA — the operator cannot forge what a third party already witnessed. But Provna ships into the customer's VPC and into **air-gapped, fail-closed** deployments where outbound egress is forbidden by policy. A public anchor requires that forbidden egress at the exact moment of anchoring, so it is unavailable precisely where the regulated buyers live. We therefore reject "public transparency log / public TSA" as the anchoring substrate: it cannot satisfy the air-gap constraint, and an anchor that only works with internet egress is an anchor the regulated deployment will turn off. The independence the threat model demands must instead come from a witness in a *different trust domain* that is reachable without leaving the air gap.

Considered: **unsigned hash-chain** (the substrate/concept-twin weakness; rejected: an insider rewrite is undetectable — fails the core threat model). **Signed but unanchored, self-clocked** (rejected: backdating attack — the operator's own clock is not trustworthy, and a re-signed alternate history verifies cleanly). **Public transparency log / public TSA** (rejected: requires forbidden egress, so it is unavailable in the air-gapped, fail-closed deployments that are the EU-FS target). We reject all three in favor of an internally-anchored, cross-org-witnessed, independently-verifiable design.

## Decision

S4 = **assemble** commodity infrastructure (we do not invent crypto) and **build** the EU-FS evidence pack, with anchoring that is **air-gap-native**:

1. **Per-action structured record → Merkle root.** Records are batched into a Merkle tree; the root is the commitment over the batch. Each record carries `policy_snapshot_ref` (the S3 policy hash) so the decision is forensically reproducible.
2. **Internal anchor + cross-org witness (air-gapped non-repudiation).** The Merkle root is anchored to a **self-hosted transparency log — Tessera (the Go successor to Trillian)** — co-located in the deployment, and timestamped by an **internal HSM-backed RFC3161 TSA**. Independence is supplied not by the internet but by a **cross-organization witness cosignature (tlog-witness)** from an *independent trust domain* (e.g. the customer's separate audit org, or a counterparty/regulator domain), **pre-provisioned on both sides of the air gap** so the witness keys are already present and no egress is needed at anchoring time. The witness cosigns the log's checkpoint/root; an insider rewrite is detectable because the rewritten root no longer matches the root the independent witness already cosigned. This cross-domain cosignature — not a public clock — is the single line that closes the insider/key-holder threat under the air-gap constraint. **Rekor v2** is cited as the reference design for the log+witness pattern.
3. **RFC8785 JCS canonicalization.** All signed payloads are canonicalized (JSON Canonicalization Scheme) so signatures are reproducible byte-for-byte across implementations and an independent auditor can re-verify.
4. **`kid`-embedded portable witness.** Every record embeds the key id (`kid`) plus the public key / certificate, so the witness is verifiable by an independent auditor with an offline verifier — not bound to a local secret. (This is the gap where competitors embed neither, leaving the witness tied to a local key.)
5. **Persist the BAR-style governance-failure signal.** A behavioral/governance monitor firing is written as a *signed* `compliance_finding` audit event, bound into the ledger — not returned as a transient alert. This is the forensic proof that enforcement was active.
6. **Optional ML-DSA (FIPS 204) for long retention.** For evidence whose retention horizon outlives classical-signature assumptions, signatures may additionally use the post-quantum ML-DSA scheme (FIPS 204), so the long-tail dossier remains verifiable against a future cryptanalytic threat.
7. **Regulatory mapping (BUILD).** The evidence is mapped to EU AI Act Article 12 (forensic reproducibility) and Article 14 (human oversight), plus DORA and MiFID — the deal-unblocking dossier no competitor offers at EU-FS depth. See [../compliance/regulatory-mapping.md](../compliance/regulatory-mapping.md).

Underneath, the assembled stack is OpenTelemetry → hash-chain → Merkle → Tessera (self-hosted) + cross-org tlog-witness → internal HSM-backed RFC3161 TSA → RFC8785 JCS, with optional ML-DSA for long retention (see [../tech-stack.md](../tech-stack.md)).

**Honesty anchor (stated as sold):** the evidence is *regulator-grade, forensic-reproducible*. "Court-admissible" is case-by-case and jurisdiction-dependent UNVERIFIED — Article 12 forensic reproducibility is not a guarantee of evidentiary admissibility, and the two must never be conflated; the Verifier persona punishes overclaiming.

## Consequences

### Positive

- The cross-org witness cosignature closes the insider/key-holder rewrite threat that unsigned and self-clocked designs leave open — **and does so inside the air gap**, which a public-anchor design cannot. This resolves the air-gap-vs-public-anchor tension: independence comes from a different trust domain reachable without egress, not from internet connectivity, so the strongest S4 differentiator survives in exactly the fail-closed deployments the EU-FS buyers mandate.
- Self-hosted Tessera + internal HSM-backed RFC3161 TSA keep the entire anchoring path within the deployment boundary, so anchoring never depends on forbidden egress and cannot be silently disabled in regulated environments.
- JCS + `kid`-embedded witness make the evidence independently verifiable offline, which is what an auditor actually needs; optional ML-DSA (FIPS 204) keeps the long-retention dossier verifiable against a future post-quantum threat.
- The signed evidence store becomes the agent-action system-of-record: leaving Provna means losing audit history, the strongest switching cost.
- The Article 12/14 + DORA + MiFID mapping is the dossier that turns the Verifier from a veto into a sign-off.

### Negative

- S4 is mechanism-commodity (OTel/Tessera/tlog-witness/RFC3161); our edge is assembly + air-gap-native anchoring + FS regulatory mapping, not a cryptographic breakthrough — it is not defensible in isolation.
- The cross-organization witness carries a real **onboarding and governance cost**: an independent trust domain must agree to act as witness, witness keys must be pre-provisioned and rotated on both sides of the air gap, and the relationship needs governance (who the witness is, what they attest, how a witness outage or compromise is handled). This is operational overhead and a customer-side dependency, not a drop-in.
- Internal anchoring still adds latency and a dependency on the self-hosted log / TSA availability; anchoring must be batched and must fail-closed without becoming a money-path bottleneck.
- The honesty boundary ("regulator-grade, not court-admissible") must be held in every sales surface; the discipline is a constraint, not a feature.
