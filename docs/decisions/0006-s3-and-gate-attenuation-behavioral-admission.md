# ADR-0006: S3 Runtime Authorization — Four-Axis AND-Gate, Real Caveat-Attenuation, Behavioral Admission

**Status:** Accepted
**Last updated: 2026-06-24**
**Related:** [../architecture/pillar-3-runtime-authorization.md](../architecture/pillar-3-runtime-authorization.md), [0001-atomic-unit-guarded-saga-step.md](0001-atomic-unit-guarded-saga-step.md), [0003-build-vs-consume-boundary.md](0003-build-vs-consume-boundary.md), [0007-s4-merkle-external-anchor-jcs.md](0007-s4-merkle-external-anchor-jcs.md), [0010-fail-closed-everywhere.md](0010-fail-closed-everywhere.md), [../tech-stack.md](../tech-stack.md)

## Context

Gate 2 of the guarded saga step answers a single question before any side effect executes: *is this specific actor, acting for this specific principal, under this specific delegation, for this specific declared intent, allowed to perform this action right now?* This is per-action runtime authorization (S3), distinct from coarse build-time allow-lists.

Three forces shape the decision:

- **S3 is the most saturated layer in the landscape.** Identity incumbents have consolidated agent authorization (e.g. CrowdStrike's acquisition of SGNL, ~$740M UNVERIFIED; Microsoft, Okta/Entra agent identity). A Policy Decision Point (PDP) is a commodity: Cedar, OpenFGA, and the AuthZEN 1.0 interop standard are mature and free. Trying to *own* the PDP is a losing bet.
- **The differentiated content is thin but real.** Competitor implementations show consistent gaps: per-action authz engines gate on `agent ∩ resource` but omit the *user* and *intent* axes; delegation is modeled as exact-string capability matching (no genuine attenuation); transitive revocation is specified normatively but implemented as a leaf-only nonce check, leaving "zombie delegations" alive, and signature verification is sometimes never actually invoked.
- **Single-shot authorization is insufficient.** A stream of individually-valid requests can compose into a harmful pattern (e.g. many small reads that together exfiltrate, or repeated borderline transfers). A behavioral/temporal layer is needed — but a naive global request counter mixes unrelated state and produces availability attacks (benign reads contaminating a sensitive action into a false-DENY).

Considered: **exact-match subset attenuation** (the prior-art approach — a child capability is valid only if its string is a member of the parent's set; rejected: cannot express `financial.*` narrowing to `financial.payment` with an amount cap, so delegation is decorative, not enforced). **Static AND-gate only, no behavioral layer** (rejected: cannot catch the composed-pattern attack class; each request passes, the aggregate is malicious). **Cedar-only / consume the whole PDP with no resolver** (rejected: Cedar gives policy evaluation but has no opinion on the user axis, the intent axis, real attenuation, or transitive revocation — exactly the thin slice that is our differentiation).

## Decision

S3 = **consume the PDP, build a thin resolver around it**, composed of three built parts plus one orthogonal layer:

1. **Four-axis AND-gate: `agent AND user AND delegation AND intent`.** All four legs must independently authorize the action; any single denial blocks. The *user* leg (on whose behalf the agent acts) and the *intent* leg (the declared business purpose, bound to the action contract) are the axes competitors omit — they are the cheapest part to add and the clearest functional difference. The PDP (Cedar embedded + OpenFGA for relationship-based checks, surfaced over AuthZEN 1.0) is consumed to evaluate the agent and resource policy; the resolver fuses the four verdicts.

2. **Real caveat-attenuation via biscuit/macaroon tokens.** Delegation irreversibly *adds constraints* — attenuation is monotonic narrowing (e.g. attach an amount limit, a resource scope, a time window), never exact-match subset selection from a fixed set. Constraints (caveats) are carried in the token *and evaluated at the engine level* at decision time, not merely transported. Chain integrity uses `parent_hash = SHA-256(JCS(parent))` so the delegation chain is itself tamper-evident.

3. **Genuinely-implemented transitive revocation.** Revocation walks the full delegation chain recursively (not a leaf-only nonce lookup), so revoking a parent invalidates all descendants — no zombie delegations. Per-hop signature verification (Ed25519) is mandatory and actually invoked on every hop; a missing or invalid signature blocks. Revocation is fail-closed: a revocation-store lookup error denies (see [0010-fail-closed-everywhere.md](0010-fail-closed-everywhere.md)).

4. **Context-scoped behavioral/temporal admission (the "5th dimension").** A *post-AND-gate orthogonal* risk layer (explicitly NOT a fifth AND member): after authorization passes, it evaluates history + anomaly + cooldown to catch the composed-pattern attack. It is **integer-only and deterministic** (no probabilistic scoring on the hot path), and its default action is **ESCALATE** (dry-run / HITL), never categorical block — it raises friction, it does not silently deny. State-mixing is prevented from the start: admission is keyed by `PatternKey = hash(agent || capability || resource || intent)`, so unrelated request streams never contaminate each other (a global per-agent counter is rejected as the known availability-attack vector). Cooldown is not a silent throttle: it is persisted as a signed `AGENT_STATE_CHANGE` audit event (see [0007-s4-merkle-external-anchor-jcs.md](0007-s4-merkle-external-anchor-jcs.md)).

Each decision emits a `policy_snapshot_ref` (hash of the evaluated policy) so the verdict is forensically reproducible and bridges S3 to S4.

We align with the saturated market rather than fight it: AuthZEN 1.0 is a genuine differentiator because a major horizontal substrate does not implement it. Patent caution: the behavioral-admission concept is treated as prior-art; our originality is the context-scoping correction, and primitives are re-implemented from open foundations (Ed25519, capability/macaroon literature) without using third-party trademarks.

## Consequences

### Positive

- The `user` and `intent` axes give a defensible functional gap over per-action authz that gates only on agent and resource.
- Real attenuation + recursive revocation + mandatory per-hop verification turn delegation from a decorative claim into an enforced, audit-visible guarantee — directly answering the Verifier persona's "who authorized this, and could it have been revoked?".
- `PatternKey`-scoped admission catches the composed-pattern attack without the global-counter availability bug.
- Consuming Cedar/OpenFGA/AuthZEN keeps engineering focused on the thin differentiating resolver and avoids competing with $740M-class incumbents.

### Negative

- Building the resolver around a consumed PDP adds an integration seam and a fusion-logic surface we must keep correct as AuthZEN evolves.
- Real caveat-evaluation and recursive revocation are more code and more latency than leaf-only checks; the behavioral layer adds per-action state reads on the hot path.
- S3 is not a defensible position — it is table-stakes alignment; the pitch must always lean on S1+S2, never on "better authorization," or we get crushed by identity incumbents.
