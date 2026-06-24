# ADR-0010: Fail-Closed Everywhere

**Status:** Accepted
**Last updated: 2026-06-24**
**Related:** [../standards/architectural-principles.md](../standards/architectural-principles.md), [0001-atomic-unit-guarded-saga-step.md](0001-atomic-unit-guarded-saga-step.md), [0004-s1-camel-pq-isolation-runtime-taint-fusion.md](0004-s1-camel-pq-isolation-runtime-taint-fusion.md), [0006-s3-and-gate-attenuation-behavioral-admission.md](0006-s3-and-gate-attenuation-behavioral-admission.md), [0009-action-guard-seam-vendor-neutral.md](0009-action-guard-seam-vendor-neutral.md)

## Context

Provna is sold as *permission to ship*: a CISO transfers risk to a gate because the gate gives an architectural guarantee, not a best-effort one. That promise is only credible if the system behaves safely **under failure** — error, ambiguity, missing data, or an unexpected response. The buyer is regulated EU-FS, and the Verifier (Internal Audit / SOX) tests precisely the failure paths.

Competitor implementations are a catalog of trust holes opened at the failure boundary:

- A guardrail that, when its policy check throws, lets traffic through (fail-open).
- A confirmation step that silently returns "not confirmed" on an unexpected response — turning an error into an implicit allow.
- A shipped agent hook running in `observe` mode that always exits 0 — an observability shim presented as enforcement, not a reference monitor.
- A signature path that downgrades to a self-verifying HMAC when the real asymmetric key is unavailable (the verification flag is always true).
- Revocation / CRL lookups that fail-open, so a revoked credential keeps working when the store is unreachable.

Every one of these *feels* like security but provides no real deny, and every one fails an audit. The common root is an asymmetry: on the happy path the system enforces; on the error path it quietly downgrades.

Considered: **fail-open / observe-shim** (lower friction, fewer false blocks, easier rollout — the Invariant/MVAR-style posture; rejected: it is the exact weakness that fails an audit and breaks the permission-to-ship promise — a gate that opens on error is not a gate). We reject any downgrade-on-failure path.

## Decision

**Fail-closed is a cross-cutting, non-negotiable principle applied at every enforcement surface.** Concretely:

- **Unlabeled => untrusted (S1).** Data with no provenance label is treated as untrusted, not as a safe default; an unlabeled value cannot reach a sensitive sink. (See [0004-s1-camel-pq-isolation-runtime-taint-fusion.md](0004-s1-camel-pq-isolation-runtime-taint-fusion.md).)
- **Error => BLOCK.** Any gate that errors, times out, or returns an unexpected/ambiguous result denies the action. There is no path where a failure becomes an implicit allow.
- **No downgrade path.** Cryptographic verification never silently falls back to a weaker mode (no HMAC self-verify substitute for a missing asymmetric key); signature consistency holds across all PEP surfaces.
- **Revocation fail-closed (S3).** A revocation / CRL store lookup that fails denies; an unreachable store does not grant. (See [0006-s3-and-gate-attenuation-behavioral-admission.md](0006-s3-and-gate-attenuation-behavioral-admission.md).)
- **Real PreToolUse deny.** For Claude Code and equivalent host hooks, enforcement is a true pre-execution deny (exit-2 / `permissionDecision: "deny"`), never an observe-only post-hook that logs after the fact.

Note the one deliberate nuance that is *not* a violation: the ActionGuard seam ships **default-OFF** and supports an audit-only Layer-0 (see [0009-action-guard-seam-vendor-neutral.md](0009-action-guard-seam-vendor-neutral.md)). That is a host-controlled opt-in posture, and even Layer-0 produces signed + anchored evidence. Once a gate is *active*, it is fail-closed; the audit-only mode is an explicit configuration, never a silent downgrade.

## Consequences

### Positive

- A gate that denies on error is a gate the Verifier can sign off on — fail-closed is what makes the permission-to-ship promise survive an audit.
- It is the direct antidote to every cataloged competitor failure mode (fail-open policy checks, silent-false confirmations, observe-shims, HMAC downgrades, fail-open revocation).
- A single, uniform rule across S1-S4 and every integration surface is simple to state, test, and certify.

### Negative

- Fail-closed couples availability to the gate: an outage in a dependency (revocation store, anchor, IFC engine) can block legitimate actions. This must be mitigated with redundancy and tight latency budgets, and contained — e.g. behavioral admission defaults to ESCALATE/HITL rather than hard-block to avoid availability attacks (see [0006-s3-and-gate-attenuation-behavioral-admission.md](0006-s3-and-gate-attenuation-behavioral-admission.md)).
- More false blocks than a fail-open system, which raises onboarding friction; the layered default-OFF → audit-only → enforce path exists precisely to manage that.
- The discipline forbids convenient escape hatches under deadline pressure; it must be enforced in code review and tests, not left to intent.
