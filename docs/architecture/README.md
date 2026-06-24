# Architecture

**Status:** Planned (pre-build)
**Last updated: 2026-06-24**
**Related:** [../vision.md](../vision.md), [../product-scope.md](../product-scope.md), [../positioning.md](../positioning.md), [../tech-stack.md](../tech-stack.md)

This section is the technical canon for how Provna works. Provna is a vendor-neutral **runtime control plane** that turns every WRITE action an agent takes in regulated enterprise systems into a contract that is *reversible + authorized + information-flow-controlled + regulator-grade provable*. Technical class: a Policy Enforcement Point (PEP) + a transaction (saga) coordinator + an evidence ledger. Metaphor: escrow for agent actions. Frame: it does not sell security, it sells **permission to ship**.

The atomic unit of the whole system is the **guarded saga step**: every side-effecting call passes four gates in a single, fixed-order pass. Split the unit and the moat dilutes (IFC without compensation is a guardrail; compensation without IFC is durable-execution). The fusion is the product.

## Reading order

Read top to bottom on first pass; each doc assumes the one before it.

1. **[overview.md](overview.md)** — the control-plane topology. Where Provna sits between the agent and upstream systems; data-plane vs control-plane split; the four-gate chain end to end. **Start here.**
2. **[action-lifecycle.md](action-lifecycle.md)** — the guarded saga step in full: IFC gate, AND-gate authorization, behavioral admission, idempotency key, dry-run, risk tier, HITL, execute + record-compensation, audit, and the reverse-saga path on failure or later violation. This is the canonical description of the atomic unit.
3. **[build-vs-consume.md](build-vs-consume.md)** — the single most important strategic doc. What Provna BUILDS (the real IP) vs what it CONSUMES/ASSEMBLES (commoditized substrate), with a reason per row. This is the discipline that keeps the product thin-but-deep.
4. **[integration-surfaces.md](integration-surfaces.md)** — how an agent runtime plugs into Provna: the ActionGuard seam (decide/commit/compensate), the vendor-neutral surfaces (SDK, MCP hook, proxy), the govern-in-two-lines layered model, and Claude Code enforcement.

## The four pillars

Each pillar is canonical in exactly one file. The lifecycle and overview link to these; they do not restate them.

| Pillar | File | One line | Build/Consume |
|---|---|---|---|
| **S1 — Information-Flow Control** | [pillar-1-information-flow-control.md](pillar-1-information-flow-control.md) | Untrusted data cannot reach a sensitive sink unless an explicitly-typed policy authorizes the flow. | BUILD |
| **S2 — Transactional Compensation** | [pillar-2-transactional-compensation.md](pillar-2-transactional-compensation.md) | Per-connector inverse plus round-trip harness; the real moat. | BUILD (saga mechanism consumed) |
| **S3 — Runtime Authorization** | [pillar-3-runtime-authorization.md](pillar-3-runtime-authorization.md) | AND-gate (agent AND user AND delegation AND intent) plus a behavioral admission layer. | CONSUME + thin resolver BUILD |
| **S4 — Tamper-Evident Audit** | [pillar-4-tamper-evident-audit.md](pillar-4-tamper-evident-audit.md) | Hash-chain + Merkle + external anchor + portable witness, mapped to EU AI Act Articles 12/14. | ASSEMBLE + evidence-pack BUILD |

## Supporting docs in this section

- **[build-vs-consume.md](build-vs-consume.md)** — the boundary, canonical.
- **[integration-surfaces.md](integration-surfaces.md)** — the seam and the surfaces.
- **[tech-stack-analysis.md](tech-stack-analysis.md)** — the per-layer technology evaluation (alternatives, 2026 maturity, sources).

ADRs that pin these decisions live in [../decisions/README.md](../decisions/README.md). Architectural principles (fail-closed, deterministic-guarantee honesty, vendor neutrality) live in [../standards/architectural-principles.md](../standards/architectural-principles.md).
