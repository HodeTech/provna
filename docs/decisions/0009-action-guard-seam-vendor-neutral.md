# ADR-0009: ActionGuard Seam and Vendor-Neutral Integration Surfaces

**Status:** Accepted
**Last updated: 2026-06-24**
**Related:** [../architecture/integration-surfaces.md](../architecture/integration-surfaces.md), [../architecture/action-lifecycle.md](../architecture/action-lifecycle.md), [0001-atomic-unit-guarded-saga-step.md](0001-atomic-unit-guarded-saga-step.md), [0010-fail-closed-everywhere.md](0010-fail-closed-everywhere.md), [../positioning.md](../positioning.md)

## Context

Provna's defensibility rests on being **vendor-neutral**: a control plane that any agent runtime can call, not a feature locked inside one runtime. Two failures must be avoided simultaneously:

- **Lock-in collapses the thesis.** If Provna is embedded inside a single runtime, the vendor-neutrality principle — and the reason Provna is not just "governance for one platform" — evaporates. A developer will not adopt governance bound to one runtime; a CISO will not buy a control plane that only governs one vendor's agents.
- **The host owns the decision boundary.** The clean place to intercept a side effect is at the host runtime's side-effecting tool boundary, where untrusted/secret taint and the call intent are already available. Provna must plug in there as an *optional, host-injected, default-OFF* seam — present when the host opts in, invisible otherwise — so adoption is incremental (audit-only → policy → compensate) and the host never loses control.

The seam must map cleanly onto the guarded saga step: an in-band decision, an in-band commit, and an out-of-band compensation.

Considered: **single-runtime embedding** (simplest to ship first; rejected: lock-in, vendor neutrality collapses, and Provna degrades into "one runtime plus a bit of governance" — the defensibility-killing drift). **MCP-only integration** (clean and standard; rejected: too narrow a surface — it misses SDK-direct and proxy integrations and the runtimes that do not expose everything over MCP). We reject both single-surface options in favor of one protocol exposed over several surfaces.

## Decision

A single **ActionGuard seam** with a three-method protocol, exposed over vendor-neutral surfaces:

- **Protocol: `decide() -> commit() -> compensate()`.**
  - `decide(intent, taint)` runs Gate 1 (IFC) + Gate 2 (AND-gate authz) + risk tiering and returns a verdict: allow / block / require-approval / transform.
  - `commit(plan, commitThunk)` runs Gate 3 (idempotent execution via a semantic effect key, with the compensation recorded) + Gate 4 (tamper-evident audit emit).
  - `compensate(receipt)` runs the reverse-saga out-of-band on later-violation or saga failure.
- **Host-injected, optional, default-OFF.** The host runtime invokes the seam at its side-effecting tool boundary only when configured; with no guard injected, behavior is unchanged. This enables the "govern in two lines" progression: Layer-0 audit-only but signed+anchored (NOT plain logging) → Layer-1 policy (deny + dry-run) → Layer-2 compensate.
- **Vendor-neutral surfaces: SDK (Python/TS) + MCP hook + proxy.** The same ActionGuard logic is offered through all three so no integration is privileged. For Claude Code, the integration uses a real PreToolUse deny, not an observe-only post-hook (see [0010-fail-closed-everywhere.md](0010-fail-closed-everywhere.md)).
- **Relavium is the FIRST reference integration, not the only one.** Relavium's side-effecting tool boundary is the first concrete ActionGuard implementation and gives the MVP a head start (durable human-gate, run-events journal for replay-safe idempotency, existing untrusted/secret taint). LangChain, the OpenAI SDK, and custom runtimes are ROADMAP surfaces — not yet proven [OPINION]; proving them is the open vendor-neutrality validation item.

## Consequences

### Positive

- One protocol, many surfaces: vendor neutrality is structural, and lock-in fear is removed for both the developer (bottom-up wedge) and the CISO (top-down buyer).
- Default-OFF + layered opt-in mirrors the enterprise shadow-mode → enforce journey and lets a developer earn trust by observing (with signed audit) before enforcing.
- The `decide/commit/compensate` mapping keeps the seam aligned 1:1 with the four gates, so the integration contract is small and the same regardless of host.
- Reusing the host's existing boundary (taint, human-gate, idempotency journal) lets the MVP plug only the real IP (IFC engine, compensation library, S3 resolver, S4 audit) into the seam.

### Negative

- A stable seam across heterogeneous runtimes is harder to keep correct than one embedding; each surface (SDK, MCP, proxy) is a contract to maintain.
- Vendor neutrality beyond Relavium is asserted, not proven — until LangChain/OpenAI/custom integrations exist, the thesis carries risk.
- Default-OFF means value is zero until the host opts in; activation and the audit-only → enforce upgrade must be made frictionless or the wedge stalls.
