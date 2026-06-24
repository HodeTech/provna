# Glossary

**Status:** Living reference (pre-build)
**Last updated: 2026-06-24**
**Related:** [vision.md](vision.md), [positioning.md](positioning.md), [architecture/overview.md](architecture/overview.md), [tech-stack.md](tech-stack.md)

This glossary defines the load-bearing terms used across Provna's documentation. Each entry gives a short definition plus the pillar (S1 IFC, S2 Compensation, S3 Authorization, S4 Audit) or context it belongs to. Where a term is canonical in a dedicated doc, the pillar link is the place to go deeper. Terms are alphabetical.

---

**ActionGuard seam** — The vendor-neutral integration contract through which a host agent runtime hands a side-effecting call to Provna. A three-method protocol: `decide()` -> `commit()` -> `compensate()` (out-of-band). Host-injected, optional, default-OFF. Relavium is the first reference integration; the same seam is exposed via SDK, MCP hook, and proxy. See [architecture/integration-surfaces.md](architecture/integration-surfaces.md).

**AgentDojo** — The benchmark Provna consumes to measure information-flow defense. Provna publishes ASR and utility-tax *together* so a low ASR cannot be bought by blocking everything. Context: S1 evaluation discipline. See [architecture/pillar-1-information-flow-control.md](architecture/pillar-1-information-flow-control.md).

**AND-gate** — The core S3 authorization rule: an action is allowed only if agent AND user AND delegation AND intent all permit it. The user and intent axes are the differentiator competitors omit. Context: S3. See [architecture/pillar-3-runtime-authorization.md](architecture/pillar-3-runtime-authorization.md).

**ASR (Attack Success Rate)** — The fraction of prompt-injection / adversarial attempts that succeed in reaching a sensitive sink. Provna's measured ASR reflects the lattice + sink-policy guarantee, not classifier luck. Context: S1 evaluation. Always reported alongside utility-tax.

**Attenuation** — Irreversibly narrowing a credential's authority by adding a constraint (e.g. an amount cap) that can never be removed downstream. Provna implements real caveat-attenuation, not exact-match subset selection. Context: S3 / delegation. See [architecture/pillar-3-runtime-authorization.md](architecture/pillar-3-runtime-authorization.md).

**Attestation / witness** — See *witness*.

**Audit (tamper-evident)** — See *tamper-evident*.

**BAR (governance-failure signal)** — A signal that enforcement itself failed or was bypassed. Provna persists it as a signed audit event (a `compliance_finding`), turning "is enforcement actually on?" into forensic evidence rather than an ephemeral alert. Context: S4. See [architecture/pillar-4-tamper-evident-audit.md](architecture/pillar-4-tamper-evident-audit.md).

**Behavioral / temporal admission** — The S3 "5th dimension": a context-scoped, integer-only deterministic risk layer (history + anomaly + cooldown) that runs *after* the AND-gate to catch a harmful pattern made of individually-valid requests. It is an orthogonal post-AND-gate layer (not the 5th AND-member) and its default action is ESCALATE / dry-run / HITL, not categorical block. State-mixing is prevented from the start via `PatternKey = hash(agent || capability || resource || intent)`. Context: S3. See [architecture/pillar-3-runtime-authorization.md](architecture/pillar-3-runtime-authorization.md).

**Biscuit** — A decentralized, attenuable token format (offline-verifiable, caveat-based) Provna can use for delegation. Adding a caveat irreversibly narrows authority. Context: S3 / delegation.

**CAEP (Continuous Access Evaluation Profile)** — A standard for streaming access-change/session events between systems so authorization can be re-evaluated continuously. Relevant because the S3 market (CrowdStrike acquired SGNL) is built around it; Provna aligns and consumes rather than competes. Context: S3 ecosystem.

**CaMeL** — The dual-LLM isolation pattern Provna builds as the S1 core: a privileged P-LLM that plans and may call tools, and a quarantined Q-LLM that processes untrusted data, cannot call tools, and returns only typed values. Context: S1. See [architecture/pillar-1-information-flow-control.md](architecture/pillar-1-information-flow-control.md).

**Caveat** — A constraint attached to a delegated credential (e.g. amount <= 10000). In Provna, caveats are genuinely evaluated by the engine, not merely carried along. Context: S3 / delegation.

**commit** — The second ActionGuard method: idempotently execute the side effect (keyed by the semantic effect key), record the compensation, and emit the tamper-evident audit event. Context: S2 + S4. See [architecture/action-lifecycle.md](architecture/action-lifecycle.md).

**Compensation** — The S2 act of undoing a side effect after it executed (or after a later violation) by running its recorded inverse via a reverse saga. Semantic, per-connector, and sometimes impossible — for irreversible actions Provna prefers two-phase (auth -> capture -> void) instead of promising "undo everything". Context: S2 (the real moat). See [architecture/pillar-2-transactional-compensation.md](architecture/pillar-2-transactional-compensation.md).

**compensate** — The out-of-band ActionGuard method that triggers the reverse saga when a saga fails or a violation is detected after commit. Context: S2.

**Connect (Connect-ES / buf)** — The RPC stack Provna uses off the inline money-path: Connect-ES for TypeScript and browser clients, with `buf` as the single schema source-of-truth for the protobuf/gRPC contracts; gRPC stays on the inline money-path and connect-python is deferred to its 1.0. Context: SDK / wire. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [tech-stack.md](tech-stack.md).

**constrained decoding (typed declassification)** — The default S1 declassification channel: a FIDES-style technique that forces a quarantined Q-LLM to emit only a low-capacity, typed output (bool / enum / small dict) via constrained/typed decoding, bounding how much untrusted information can cross a label boundary. The signed, principal-bound `trust_boundary` node is reserved for high-capacity declassification. Context: S1. See [architecture/pillar-1-information-flow-control.md](architecture/pillar-1-information-flow-control.md).

**Control-plane** — The portion of Provna that runs in the customer VPC and holds orchestration, not the hot path: the AuthZ PDP resolver, compensation orchestration, and the audit assembler. Written in Python/TS. Contrast *data-plane*. See [tech-stack.md](tech-stack.md), [project-structure.md](project-structure.md).

**Data-plane** — The inline, hot-path Policy Enforcement Point: the PEP, IFC engine, and action-contract logic that sit synchronously in front of every side-effecting call. Written in Go/Rust for latency. Contrast *control-plane*. See [tech-stack.md](tech-stack.md).

**decide** — The first ActionGuard method: run the IFC gate, the AND-gate authorization, and risk tiering, returning a verdict (allow / block / require-approval / transform; transform = allow but with the arguments rewritten or narrowed first, e.g. redacting an untrusted field before the sink). Context: S1 + S3. See [architecture/action-lifecycle.md](architecture/action-lifecycle.md).

**Delegation** — One axis of the AND-gate: authority passed from a user to an agent (and agent-to-agent), carried as an attenuable, verifiable credential chain with transitive revocation. Context: S3. See [architecture/pillar-3-runtime-authorization.md](architecture/pillar-3-runtime-authorization.md).

**Design partner** — An early customer (EU-exposed bank / payments / fintech / treasury with a blocked agent project) who co-validates Provna in shadow-mode and toward a payment-intent pilot. The 90-day single metric: a blocked agent project ships to limited prod with risk-committee approval because of Provna. See [business/design-partner-plan.md](business/design-partner-plan.md).

**DORA (Digital Operational Resilience Act)** — EU regulation imposing ongoing operational-resilience and evidence obligations on financial entities. A continuous forcing-function (not a one-time deadline) Provna's S4 evidence pack maps to. Context: compliance. See [compliance/regulatory-mapping.md](compliance/regulatory-mapping.md).

**dromedary (CaMeL implementation)** — Microsoft's MIT-licensed reference implementation of the CaMeL pattern (a privileged LLM plus a quarantined `query_ai_assistant`, a custom interpreter, and OPA policy) that Provna treats as the interpreter/capability reference for its S1 build. Provna also adopts the 2026 CaMeL side-channel hardening (loop clamping, structured/constant-time error handling) into its interpreter. Context: S1 reference. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-1-information-flow-control.md](architecture/pillar-1-information-flow-control.md).

**Dry-run** — An effect-free preview of an action before it touches the money path, so high-value or irreversible actions are previewed and can be routed to HITL. On by default for irreversible actions. Context: S2. See [architecture/pillar-2-transactional-compensation.md](architecture/pillar-2-transactional-compensation.md).

**Dual-LLM** — The architectural split (privileged + quarantined) underlying CaMeL; the basis of Provna's S1 deterministic guarantee. See *CaMeL*, *P-LLM/Q-LLM*. Context: S1.

**ESCALATE** — The default outcome of the behavioral/temporal admission layer: instead of a categorical block, raise the action to dry-run / HITL / cooldown. A cooldown is not a silent throttle — it is written to the audit log as an `AGENT_STATE_CHANGE` event. Context: S3.

**EU AI Act Article 12** — Record-keeping / logging obligation for high-risk AI; Provna maps it to forensic-reproducibility of the evidence pack. Context: S4 / compliance. See [compliance/regulatory-mapping.md](compliance/regulatory-mapping.md).

**EU AI Act Article 14** — Human-oversight obligation for high-risk AI; Provna maps it to the dry-run + HITL + four-eyes approval flow. Context: S3/S2 + compliance.

**External anchor** — A third-party, independent attestation that a piece of evidence existed at a point in time, so even a key-holding insider cannot rewrite history consistently. Provna assembles this from a self-hosted Tessera transparency log + an internal RFC3161 TSA + a cross-organization witness cosignature (Rekor v2 is the reference design). Context: S4. See [architecture/pillar-4-tamper-evident-audit.md](architecture/pillar-4-tamper-evident-audit.md).

**FIDES** — Microsoft's MIT-licensed, provider-agnostic Q-LLM-isolation + label-propagation library (shipped in `microsoft/agent-framework`) that Provna CONSUMES as the reference and prototype substrate for the S1 MVP PoC and AgentDojo eval. The real BUILD moat (inline fail-closed reference monitor, immutable label store, signed declassification node, per-connector sink-policy catalog, S1<->S4 forensic bridge) sits on top; FIDES-style typed constrained decoding is the default declassification channel. Context: S1 (CONSUME). See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-1-information-flow-control.md](architecture/pillar-1-information-flow-control.md).

**FIPS 140-3** — The US cryptographic-module validation standard. Go >=1.24 ships a FIPS 140-3 validated crypto module in its standard library, buildable with `GODEBUG=fips140=on` for regulated/air-gapped deployments — a key reason the Go-first data-plane was chosen. Context: data-plane / compliance. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [tech-stack.md](tech-stack.md).

**Four-eyes** — A control requiring two distinct human approvers for a sensitive action; in Provna realized through the HITL gate and mapped to EU AI Act Article 14. Context: S2/S3.

**Guarded saga step** — Provna's atomic unit: every side-effecting call wrapped so it passes four gates in fixed order — (1) IFC, (2) AND-gate authorization + behavioral admission, (3) action contract (idempotent -> dry-run -> HITL -> execute -> compensate), (4) audit. Splitting the unit dilutes the moat; the fusion is the product. See [decisions/0001-atomic-unit-guarded-saga-step.md](decisions/0001-atomic-unit-guarded-saga-step.md).

**guarantee-kernel** — The narrow interface Provna carves out inside the Go data-plane PEP that holds the security-critical primitives — lattice label propagation, sink-policy decide, JCS canonicalization, and signing — so it CAN be reimplemented in Rust later (behind a proven trigger) without touching the rest of the PEP. Context: data-plane architecture. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [tech-stack.md](tech-stack.md).

**gVisor** — The user-space application kernel Provna uses to isolate the S2 harness runner, sandboxing connector round-trips during compensation-harness execution. Context: S2 harness. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-2-transactional-compensation.md](architecture/pillar-2-transactional-compensation.md).

**Hash-chain** — A sequence of audit records where each links to the prior record's hash, making any retroactive edit detectable. The base layer beneath the Merkle root and external anchor. Context: S4.

**HITL (Human-in-the-Loop)** — A durable approval gate where a human must approve before a high-risk or irreversible action executes. Provna consumes the host's durable human-gate rather than building its own suspend. Context: S2/S3, maps to EU AI Act Article 14.

**IFC (Information-Flow Control)** — S1: enforcing, at runtime, that untrusted data cannot reach a sensitive sink unless an explicitly-typed policy authorizes the flow. Typed and fail-closed (unlabeled => untrusted). Context: S1 (BUILD). See [architecture/pillar-1-information-flow-control.md](architecture/pillar-1-information-flow-control.md).

**Idempotency** — The property that re-executing the same action produces no additional side effect. Provna enforces it via a semantic effect key so retries and replays do not double-post. Context: S2.

**Inverse (A^-1)** — The per-connector operation that undoes a given action A (e.g. Stripe refund/void undoing a charge, a reversing NetSuite journal). The accumulating, version-pinned, round-trip-tested catalog of these inverses is the S2 moat content. Context: S2. See [architecture/pillar-2-transactional-compensation.md](architecture/pillar-2-transactional-compensation.md).

**ISO 42001** — The AI management-system standard Provna anchors its compliance legitimacy to (alongside the EU AI Act), preferred over self-interested vendor schemes. Context: compliance. See [compliance/regulatory-mapping.md](compliance/regulatory-mapping.md).

**JCS (RFC8785 JSON Canonicalization Scheme)** — A deterministic JSON serialization so the same logical record always hashes identically, making signatures and chain verification reproducible across implementations. Context: S4. See *RFC8785 JCS*.

**kid (key identifier)** — An identifier embedded in each signed audit record naming the signing key (with the public key / cert), so an independent auditor can verify a portable witness without access to local key material. Context: S4.

**Lattice** — The ordered set of security labels (e.g. an integrity x confidentiality dual-lattice) over which IFC decisions are computed. The deterministic S1 guarantee is anchored in the lattice + sink-policy, not in ML classifiers. Context: S1.

**Lethal trifecta** — The condition (private data + untrusted content + external communication) under which any agent is unconditionally exploitable; model vendors acknowledge it cannot be patched inside the model. Only architectural defense (IFC + sink policy) guarantees safety — the motivation for S1. Context: S1.

**Llama Prompt Guard 2** — A self-hosted probabilistic prompt-injection pre-filter (86M multilingual / 22M low-latency variants) Provna may run as a cheap first pass. It is explicitly OFF the deterministic guarantee path — the lattice + sink-policy still own the guarantee — and Provna avoids any SaaS detector dependency (e.g. Lakera). Context: S1 (off-path pre-filter). See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-1-information-flow-control.md](architecture/pillar-1-information-flow-control.md).

**Macaroon** — A bearer-token format supporting attenuation via caveats (constraints added downstream that only narrow authority). An alternative to biscuit for delegation. Context: S3.

**Merkle (root/tree)** — A tree of hashes whose root commits to a whole batch of audit records; publishing the root to an external anchor makes the entire batch tamper-evident with one attestation. Context: S4. See [architecture/pillar-4-tamper-evident-audit.md](architecture/pillar-4-tamper-evident-audit.md).

**MiFID II** — EU financial-markets regulation with record-keeping/reporting obligations Provna's S4 evidence pack maps to. Context: compliance. See [compliance/regulatory-mapping.md](compliance/regulatory-mapping.md).

**ML-DSA (FIPS 204)** — The NIST-standardized post-quantum (lattice-based) digital-signature algorithm Provna can optionally apply to S4 audit signatures for long-retention evidence, hedging against future cryptographic obsolescence. Context: S4 (optional). See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-4-tamper-evident-audit.md](architecture/pillar-4-tamper-evident-audit.md).

**MVAR** — A single-author, Apache-2.0 runtime-taint reference implementation (`mvar-security/mvar`): a real integrity x confidentiality dual-lattice with a two-layer fail-closed sink-gate. Provna treats it as a design reference (not a dependency); known gaps it must improve on are a mutable provenance node, no transactional/compensation side, and no external audit anchor — plus a US provisional patent (PATENT CAUTION: re-implement from prior art, avoid the brand). Context: S1 reference. See [architecture/pillar-1-information-flow-control.md](architecture/pillar-1-information-flow-control.md).

**NIST AI RMF (AI Risk Management Framework)** — A voluntary US framework for managing AI risk; a mapping target for Provna's governance evidence alongside the EU regime. Context: compliance.

**oasdiff** — An OpenAPI diff tool Provna runs as a drift gate on its connected re-record station: when a connector's OpenAPI spec changes, oasdiff flags the drift before that connector is promoted back into the auto-runnable harness catalog. Context: S2 harness. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-2-transactional-compensation.md](architecture/pillar-2-transactional-compensation.md).

**OpenBao** — The MPL-licensed open-source fork of HashiCorp Vault (which moved to BSL) that Provna uses for secrets management, paired with the External Secrets Operator. Part of the deployment/supply-chain stack. Context: deployment / secrets. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [tech-stack.md](tech-stack.md).

**P-LLM / Q-LLM** — The two roles in the dual-LLM split. The **P-LLM** (privileged/planner) may call tools and emits the plan; the **Q-LLM** (quarantined) processes untrusted data, **cannot call tools**, and returns only typed values. This isolation is what makes the S1 guarantee architectural rather than probabilistic. Context: S1.

**PDP (Policy Decision Point)** — The component that evaluates authorization policy and returns allow/deny. Provna **consumes** the PDP (Cedar / OpenFGA + AuthZEN 1.0) and builds only the thin AND-gate resolver around it. Context: S3. See [architecture/build-vs-consume.md](architecture/build-vs-consume.md).

**PEP (Policy Enforcement Point)** — The inline component that intercepts a side-effecting call and enforces the PDP's decision (allow / block / dry-run / reverse). Provna's hot-path PEP is the heart of the data-plane. Context: core class. See [architecture/overview.md](architecture/overview.md).

**ReBAC (Relationship-Based Access Control)** — An authorization model where permissions derive from relationships between entities (the model OpenFGA implements). Provna defers OpenFGA behind a relationship-resolver interface and adds it only when a design partner's entitlements are provably ReBAC; the MVP PDP is Cedar-only. Context: S3. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-3-runtime-authorization.md](architecture/pillar-3-runtime-authorization.md).

**Rekor** — A Sigstore transparency log used as an external anchor: appending an evidence hash yields an independently-verifiable, append-only public record of existence-at-time. Context: S4. See *external anchor*.

**Rekor v2** — The newer Sigstore transparency-log design Provna keeps as a reference for its self-hosted S4 anchor (Tessera-based internal log + witness cosignature), rather than depending on the public Sigstore deployment in air-gapped settings. Context: S4 reference. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-4-tamper-evident-audit.md](architecture/pillar-4-tamper-evident-audit.md).

**RFC3161** — The Time-Stamp Protocol: a trusted Time-Stamping Authority signs a hash to attest it existed before a given time, giving an independent clock that an insider cannot backdate. Context: S4.

**RFC8785 JCS** — The JSON Canonicalization Scheme; canonical serialization that makes hashing and signing of audit records deterministic and cross-implementation reproducible. Context: S4. See *JCS*.

**Saga** — A long-running transaction expressed as a sequence of steps, each with a compensating action, so partial failure can be unwound. Provna **consumes** the saga mechanism (from DBOS Transact) and builds the compensation *content* on top. Context: S2.

**SagaCoordinator (interface)** — The thin internal interface Provna places in front of the S2 durable-execution substrate so the substrate stays swappable. The MVP ships on DBOS Transact + Postgres behind this interface (plus the gRPC ActionGuard seam); a Temporal adapter is pre-written as a contingency and adopted only if a concrete trigger fires (multi-tenant fan-out, a Postgres throughput/latency ceiling, or a buyer mandate). This is not a scheduled DBOS->Temporal migration. Context: S2. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-2-transactional-compensation.md](architecture/pillar-2-transactional-compensation.md).

**SeaweedFS** — The Apache-2.0, S3-compatible, single-binary object store Provna defaults to (replacing MinIO, which is AGPLv3 + archived). The S3 API is kept as a swappable seam so a customer's existing in-VPC S3 endpoint (Ceph / Dell ECS / NetApp) can be targeted by config. Context: data / storage. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [tech-stack.md](tech-stack.md).

**Semantic effect key** — A key derived from an action's meaning (not just its request bytes) used to enforce idempotency, so a retry or replay representing the same real-world effect executes at most once. Context: S2.

**Shadow-mode** — A deployment in which Provna observes and produces signed, anchored evidence without blocking, used in early design-partner engagements before enforcement is switched on. Note: shadow-mode is audit-only but signed + anchored — not plain logging. Context: GTM / roadmap. See [roadmap/phase-0-mvp.md](roadmap/phase-0-mvp.md).

**Sink** — A point where data leaves the controlled boundary into a real-world side effect (a payment rail, an ERP write, an outbound message). IFC decisions are about what may reach a sink. Context: S1.

**Sink-policy** — The explicit, typed rule governing which labeled data may flow to a given sink. The deterministic S1 guarantee is anchored in the lattice + sink-policy. Context: S1.

**SOC 2** — A trust/security attestation Provna pursues from the enforcement phase onward; a prerequisite for enterprise procurement. Context: GTM / roadmap. See [roadmap/phase-0-1-enforcement.md](roadmap/phase-0-1-enforcement.md).

**System-of-record** — A source whose data is treated as authoritative and original. Provna's signed + anchored evidence store is the system-of-record for agent actions; leaving Provna means losing the audit history — the strongest switching cost. Context: S4 / positioning.

**Taint** — A runtime label marking data as untrusted/sensitive, propagated through computation so a sink-gate can fail-closed when tainted data would reach a sensitive sink. The runtime-taint dual-lattice complements CaMeL isolation. Context: S1.

**Tamper-evident** — The property that any after-the-fact alteration of the audit record is detectable. Achieved via hash-chain + Merkle root + external anchor + JCS + portable witness. Context: S4. See [architecture/pillar-4-tamper-evident-audit.md](architecture/pillar-4-tamper-evident-audit.md).

**Tessera** — The Go successor to Trillian: the self-hosted, append-only transparency-log infrastructure Provna runs as its internal S4 anchor (alongside an internal HSM-backed RFC3161 TSA), suitable for air-gapped deployments. Context: S4. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-4-tamper-evident-audit.md](architecture/pillar-4-tamper-evident-audit.md).

**tlog-witness / witness cosignature** — The mechanism by which Provna's internal transparency-log checkpoint is countersigned by an independent trust domain whose root of trust is pre-provisioned on both sides of the air gap, yielding genuine third-party, cross-organization non-repudiation without public-network egress. Context: S4. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-4-tamper-evident-audit.md](architecture/pillar-4-tamper-evident-audit.md).

**Transaction token** — A short-lived, scoped credential (per the IETF transaction-tokens draft) carrying authorization context for a single action across services. Relevant to S3 delegation; the standards here are still draft, not RFC. Context: S3.

**Transitive revocation** — Revoking a delegation such that every credential derived from it downstream is also revoked, with mandatory signature verification at each hop (no "zombie delegations"). Provna implements this genuinely, fail-closed. Context: S3.

**Trillian** — The append-only verifiable-log infrastructure underlying transparency logs (e.g. Rekor); usable as a self-hosted external anchor in air-gapped deployments. Context: S4.

**trust_boundary node** — The only legitimate path to declassify data in Provna's IFC: a signed, principal-bound, audit-visible node that explicitly authorizes a flow across a label boundary. Labels are otherwise immutable. Context: S1.

**Utility-tax** — The drop in task utility (success on legitimate work) caused by an IFC defense. Reported together with ASR so the defense is not just "block everything"; a known reference is roughly 7 points [OPINION, to be validated with design partners]. Context: S1 evaluation.

**Valkey** — The BSD-licensed, Linux-Foundation Redis fork Provna uses (instead of Redis, whose license changed) for cooldown / rate counters and caching, where such state is not folded into Postgres. Context: data. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [tech-stack.md](tech-stack.md).

**VCR cassette** — A recorded request/response fixture that lets the S2 harness replay connector round-trips offline (air-gap-native). A separate connected re-record station refreshes the cassettes and runs oasdiff as a drift gate before a connector is promoted to the auto-runnable catalog. Context: S2 harness. See [architecture/tech-stack-analysis.md](architecture/tech-stack-analysis.md), [architecture/pillar-2-transactional-compensation.md](architecture/pillar-2-transactional-compensation.md).

**Witness** — A portable, self-contained verification artifact for an audit record: JCS-canonicalized content + signature + embedded `kid`/public-key/cert, so an independent auditor can verify it without local key access. Context: S4.
