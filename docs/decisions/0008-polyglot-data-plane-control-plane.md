# ADR-0008: Polyglot Architecture — Go/Rust Hot-Path PEP, Python/TS Control Plane

**Status:** Accepted
**Last updated: 2026-06-24**
**Related:** [../tech-stack.md](../tech-stack.md), [../architecture/overview.md](../architecture/overview.md), [0003-build-vs-consume-boundary.md](0003-build-vs-consume-boundary.md), [0009-action-guard-seam-vendor-neutral.md](0009-action-guard-seam-vendor-neutral.md), [../project-structure.md](../project-structure.md)

## Context

Provna sits inline on the money path: the Policy Enforcement Point (PEP) runs the four gates of the guarded saga step before a side effect executes. This creates two contradictory engineering demands in one product:

- **The hot path is latency- and safety-critical.** The inline PEP adds latency to every governed action; for payment/ERP writes the latency SLO is a deal-validation item. It must be predictable (no GC pauses on the critical path), memory-safe, and deployable as a single small inline component into a customer VPC or air-gapped environment.
- **The control plane is iteration- and ecosystem-critical.** Policy resolution, compensation-library authoring, LLM orchestration (the Q-LLM, compensation-inverse suggestion, risk scoring), the evidence store, and the connector catalog all benefit from a fast-moving, AI-rich ecosystem and high developer velocity. The richest libraries for LLM orchestration and the design-partner SDKs live in Python and TypeScript.

Forcing both sides into one language sacrifices one of these demands.

Considered: **single-language TypeScript everywhere** (great velocity and one SDK story; rejected: a weak inline hot path — runtime characteristics are wrong for a low-latency, memory-safe, single-binary money-path PEP). **Python-only** (best LLM ecosystem and fastest control-plane iteration; rejected: a heavy, GC-paused inline PEP is unacceptable on the critical path and awkward to ship as a small air-gapped component). We reject monoglot in favor of placing each language where its constraints fit.

## Decision

A polyglot split aligned to the data-plane / control-plane boundary:

- **Hot-path PEP / data plane = Go or Rust (inline).** The inline enforcement point — the part that runs on every governed action and must meet the latency SLO — is a compiled, memory-safe binary. This is where fail-closed behavior and low, predictable latency are non-negotiable.
- **Control plane + LLM orchestration = Python / TS.** Policy resolution, the compensation library + round-trip test harness, Q-LLM and risk orchestration, the evidence store, and the connector catalog run in the control plane where iteration speed and the AI ecosystem matter most.
- **Web panel = TypeScript / React / Next.**
- **SDK = Python + TS, over gRPC.** Two first-class SDK languages match the design-partner stacks; gRPC is the wire contract between SDK, data plane, and control plane.

This split is phased (see [../tech-stack.md](../tech-stack.md)): the **MVP (0-3 mo)** runs a TS/Python single container (the inline-PEP performance work is deferred while validating product fit); the **production-target stack (6-12 mo)** moves the inline PEP to Go/Rust and hardens the rest. Pinned versions live in [../tech-stack.md](../tech-stack.md), not here.

## Consequences

### Positive

- Each tier uses the right tool: predictable low-latency, memory-safe enforcement inline; fast iteration and a rich AI/connector ecosystem in the control plane.
- The compiled inline PEP ships cleanly as a small component into customer VPC / air-gapped deployments.
- The data-plane / control-plane language boundary mirrors the build/consume and ActionGuard seams, keeping responsibilities crisp.

### Negative

- Polyglot raises operational and cognitive overhead: two toolchains, two build/test pipelines, and a typed gRPC contract that must stay in sync across the boundary.
- Talent must span Go/Rust and Python/TS, or the team must be partitioned by tier.
- The MVP-to-production rewrite of the inline PEP (TS/Python container → Go/Rust binary) is real migration work that must be planned, not assumed free.
