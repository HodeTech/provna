# Architectural Principles

**Status:** Accepted
**Last updated: 2026-06-24**
**Related:** [../vision.md](../vision.md), [../architecture/overview.md](../architecture/overview.md), [../decisions/0010-fail-closed-everywhere.md](../decisions/0010-fail-closed-everywhere.md), [adr-template.md](adr-template.md)

These are the five first-class product principles of Provna. They are not aspirations; they are constraints. Every design choice, every connector, every ADR must be consistent with all five, or must explicitly argue the trade-off in its `### Negative` consequences. Each principle exists because it is the direct antidote to a specific weakness in the systems Provna competes against. Scope discipline (the sixth section) is what keeps the five honest.

Provna is a vendor-neutral runtime control plane: it turns every write an agent makes in a regulated system into a contract that is reversible, authorized, information-flow-controlled, and regulator-grade provable. The atomic unit is the **guarded saga step** — every side-effecting call passes four gates (IFC, AND-gate authorization plus behavioral admission, action contract, audit). These principles describe how that unit must behave.

## 1. Fail-closed everywhere

**The rule.** Any error, ambiguity, missing label, expired credential, or unreachable dependency resolves to **BLOCK**. There is no silent downgrade path, no "log and continue", no fallback to permissive behavior. Specifically:

- An unlabeled value in the information-flow lattice is treated as **untrusted**, not as trusted-by-default.
- Revocation is fail-closed: if we cannot confirm a credential is still valid, we treat it as revoked.
- The agent-integration hook is a **real deny**, not an advisory signal. For Claude Code this is a genuine `PreToolUse` deny that stops the call; not a warning the host may ignore.
- If the control plane cannot reach its policy or evidence store, side-effecting actions do not execute.

**The weakness it antidotes.** Guardrail and classifier-based competitors lean on heuristics that fail *open* — when the classifier is unsure or the detector misses, the action proceeds. A flow engine whose injection detector is admittedly "just a heuristic" cannot promise a regulator anything, because the failure mode is silent permission. Provna inverts the default: uncertainty costs throughput, never safety.

**Where it applies.** Universally, but most sharply at: the IFC sink gate, the authorization AND-gate, credential/revocation checks, and the host integration seam (`decide()` / `commit()` / `compensate()`). See [../decisions/0010-fail-closed-everywhere.md](../decisions/0010-fail-closed-everywhere.md).

## 2. Deterministic-guarantee honesty

**The rule.** We state exactly what we guarantee and exactly what we do not. The deterministic information-flow guarantee is anchored **only** in the typed lattice plus the sink policy — never in a machine-learning classifier. ML classifiers may run as an **optional pre-filter**, but they never carry the guarantee. We make one honest promise and refuse to inflate it:

> Untrusted data cannot reach a sensitive sink unless an explicitly typed policy authorizes that flow.

We explicitly do **not** claim to stop implicit-flow or side-channel leakage. Where a claim is unproven we mark it `UNVERIFIED` (for example, "court-admissible" is case-by-case and is marked as such; the honest claim is "regulator-grade, forensically reproducible"). Declassification happens only through a signed, principal-bound `trust_boundary` node — never implicitly.

**The weakness it antidotes.** Competitors conflate "our model usually catches injection" with "flows are controlled", and conflate chronological ordering with information flow. That over-claim is exactly what a CISO, an internal auditor, and a regulator will not accept. Provna's narrower, provable claim is worth more than a broad, unprovable one because it survives audit.

**Where it applies.** The IFC pillar's public claims, the evidence pack's wording, the regulatory mapping, and every customer-facing statement of what Provna prevents. The lattice and sink policy are the guarantee; the classifier is a convenience.

## 3. Signed and externally-anchored evidence is the system of record

**The rule.** Audit output is not a log. Every governed action produces a tamper-evident record: hash-chained events, a Merkle root, an **external anchor** (a self-hosted transparency log (Tessera) plus an internal HSM-backed RFC3161 TSA plus a cross-organization witness cosignature, with Rekor v2 as the reference design), RFC8785 JCS canonicalization, a `kid`-embedded portable witness, and a `policy_snapshot_ref` pinning the exact policy in force. A governance-failure signal is itself persisted as a **signed audit event**. This signed, anchored evidence — not any internal database, not any plaintext log — is the authoritative system of record, and it maps to EU AI Act Article 12 (forensic reproducibility) and Article 14 (human oversight), plus DORA and MiFID II obligations.

**The weakness it antidotes.** Substrate and guardrail competitors emit **unsigned, un-anchored** audit trails — logs that the operator could in principle alter, and that therefore prove nothing to an external party. An auditor cannot rely on evidence the audited party can edit. Provna's evidence is verifiable by a third party who trusts none of the infrastructure, which is the only kind of evidence that turns a blocked agent project into a shippable one.

**Where it applies.** The audit pillar, the evidence-pack format, the compliance mapping, and any place where Provna asserts "this happened and here is the proof".

## 4. One-click reversal and dry-run by default

**The rule.** A governed write is a contract with an inverse. Before execution, the default path offers a **dry-run**; after execution, a **one-click compensation** can run the inverse (`A^-1`). The compensation library is per-connector, round-trip-tested, observe-probed, and API-version-pinned so the inverse is auto-runnable rather than a manual playbook. We never sell "undo everything": for irreversible actions we prefer a two-phase shape (auth -> capture -> void) so there is a real cancellation window. The action contract is the lifecycle `idempotent -> dry-run -> HITL -> execute -> compensate`.

**The weakness it antidotes.** The market is full of forward-only mechanisms: exactly-once execution with no undo, snapshot/restore at the system level rather than a per-action inverse, and durable-execution platforms where compensation is a *manual pattern the customer must write themselves*. None of these give an operator a tested, single-action reversal. This is Provna's real moat — and it is conditional: it holds only if building the compensation content genuinely requires multi-year accumulation ("buy < build"). That assumption is the single most critical one in the plan and is `[OPINION]` until validated with design partners.

**Where it applies.** The compensation pillar, every connector we ship, the action lifecycle, and the integration seam's `compensate()` contract.

## 5. Vendor neutrality (a goal)

**The rule.** Provna governs agent actions regardless of which framework, model provider, or host produced them. The control plane is reachable through neutral surfaces — an SDK (Python and TS), an MCP hook, and a proxy — and the `ActionGuard` seam (`decide()` -> `commit()` -> `compensate()`) is host-injected, optional, and default-OFF. The default model is Claude, but the system is provider-agnostic by design. This is stated as a **goal and a principle**, not a finished claim: today the first reference integration is proven, and broad framework support (LangChain, OpenAI SDK, custom hosts) is roadmap, marked `[OPINION]` until demonstrated.

**The weakness it antidotes.** A horizontal substrate vendor's governance is host-dependent and effectively single-ecosystem; a CISO buying it is betting on one vendor's stack. Provna's neutrality lets a regulated buyer adopt governance once and apply it across whatever agents they run, which is what an enterprise platform team actually needs.

**Where it applies.** The integration surfaces, the SDK and MCP and proxy entry points, and any positioning that claims breadth — which must remain honest about what is proven versus roadmap (Principle 2).

## Scope discipline: thin but deep

The four pillars are powerful only as a **fusion**. Split the atomic unit and the moat dilutes: IFC without compensation is just a guardrail; compensation without IFC is just durable execution; authorization alone is a saturated, already-owned market. So the discipline is **thin but deep** — a narrow surface (start with one connector and one action type), but each gate fully realized and genuinely fused.

The single test for any proposed scope addition:

> Does this make the guarded saga step deeper (a stronger, more provable inverse / flow-control / evidence guarantee on the actions we already govern), or does it just make the surface wider?

Depth wins. We will own a small number of write paths completely — reversible, authorized, flow-controlled, and provable — before we widen to more. A wide-but-shallow surface is exactly the position our competitors already occupy and exactly the position we are built to beat.
