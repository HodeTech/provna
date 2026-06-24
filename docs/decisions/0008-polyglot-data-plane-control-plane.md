# ADR-0008: Polyglot Architecture — Go-First Hot-Path PEP, Python/TS Control Plane

**Status:** Accepted
**Last updated: 2026-06-24**
**Related:** [../tech-stack.md](../tech-stack.md), [../architecture/overview.md](../architecture/overview.md), [0003-build-vs-consume-boundary.md](0003-build-vs-consume-boundary.md), [0009-action-guard-seam-vendor-neutral.md](0009-action-guard-seam-vendor-neutral.md), [../project-structure.md](../project-structure.md), [../architecture/tech-stack-analysis.md](../architecture/tech-stack-analysis.md)

## Context

Provna sits inline on the money path: the Policy Enforcement Point (PEP) runs the four gates of the guarded saga step before a side effect executes. This creates two contradictory engineering demands in one product:

- **The hot path is latency- and safety-critical.** The inline PEP adds latency to every governed action; for payment/ERP writes the latency SLO is a deal-validation item. It must be predictable (no surprise GC pauses on the critical path), memory-safe, and deployable as a single small inline component into a customer VPC or air-gapped environment.
- **The control plane is iteration- and ecosystem-critical.** Policy resolution, compensation-library authoring, LLM orchestration (the Q-LLM, compensation-inverse suggestion, risk scoring), the evidence store, and the connector catalog all benefit from a fast-moving, AI-rich ecosystem and high developer velocity. The richest libraries for LLM orchestration and the design-partner SDKs live in Python and TypeScript.

Forcing both sides into one language sacrifices one of these demands.

Considered: **single-language TypeScript everywhere** (great velocity and one SDK story; rejected: a weak inline hot path — runtime characteristics are wrong for a low-latency, memory-safe, single-binary money-path PEP). **Python-only** (best LLM ecosystem and fastest control-plane iteration; rejected: a heavy, GC-paused inline PEP is unacceptable on the critical path and awkward to ship as a small air-gapped component). We reject monoglot in favor of placing each language where its constraints fit.

The remaining question is which compiled language owns the hot path. The choice is shaped by 2026 facts in regulated, air-gapped contexts:

- **Go ships FIPS 140-3 validated cryptography in the standard library.** As of Go 1.24, a FIPS 140-3 validated cryptographic module is built into the toolchain, switchable with `GODEBUG=fips140=on` for regulated/air-gapped builds — no third-party crypto, no separate validated module to vendor and track. For a product that must run inside customer compliance boundaries this collapses a large procurement and audit surface.
- **Go's observability and gRPC stories are stable.** OpenTelemetry traces and metrics for Go are stable, and `grpc-go` is the canonical, production-hardened gRPC implementation — directly aligned with our gRPC-as-wire-contract seam.
- **Rust's equivalents are not yet stable in 2026.** OpenTelemetry for Rust is still beta, and the `grpc`/`tonic` Rust ecosystem is mid-migration (`grpc-rust` reorganization in progress). FIPS-validated crypto in Rust means binding to a validated C module (e.g. an OpenSSL/aws-lc-fips backend) rather than a stdlib module. None of this is disqualifying for Rust long-term, but it raises the cost of choosing Rust as the default today.

Given that the MVP's binding constraints are FIPS-in-the-box, stable OTel/gRPC, and fast delivery into air-gapped customer VPCs — not yet sub-millisecond inline-proxy latency — Go is the better default for the hot path now, provided we keep a future Rust leaf cheap.

## Decision

A polyglot split aligned to the data-plane / control-plane boundary, with the hot path **Go-first**:

- **Hot-path PEP / data plane = Go-first (inline).** The inline enforcement point — the part that runs on every governed action and must meet the latency SLO — is a compiled, memory-safe Go binary. Target **Go >= 1.24** specifically for: the **FIPS 140-3 validated crypto module in the standard library** (`GODEBUG=fips140=on` for regulated/air-gapped builds), **stable OpenTelemetry traces + metrics**, and the **canonical `grpc-go`** implementation. This is where fail-closed behavior and low, predictable latency are non-negotiable.
- **Narrow guarantee-kernel interface.** The safety-critical core is factored behind a deliberately narrow interface — lattice label-propagation, sink-policy decide, JCS (RFC 8785) canonicalize, and sign — so that a future Rust reimplementation of the kernel is a contained leaf swap behind a stable boundary, not a rewrite of the whole data plane. The kernel does not leak Go-isms across the interface.
- **Rust reserved for proven triggers only.** Rust is introduced into the hot path only when one of three named triggers is demonstrated, not on a schedule: (1) a **sub-millisecond-p99 inline proxy datapath** where Go's tail latency is shown insufficient; (2) an **untrusted-connector sandbox-WASM host** needing a Rust WASM runtime embedding; or (3) a **constrained sidecar** where binary size / footprint forces it. Absent a triggered, measured need, the hot path stays Go.
- **Zig and C++ are dropped.** Neither earns a place: Zig lacks the validated-crypto and ecosystem story; C++ brings memory-unsafety onto the money path. They are out of scope for this architecture.
- **Control plane + LLM orchestration = Python / TS.** Policy resolution, the compensation library + round-trip test harness, Q-LLM and risk orchestration, the evidence store, and the connector catalog run in the control plane where iteration speed and the AI ecosystem matter most.
- **Web panel = TypeScript / React / Next.**
- **SDK = Python + TS, over gRPC.** Two first-class SDK languages match the design-partner stacks.
- **Seam = gRPC, not FFI.** The boundary between data plane and control plane is a typed gRPC contract (buf schema as source of truth), not in-process foreign-function-interface coupling. This keeps the tiers independently deployable, independently versioned, and independently swappable, and it is what makes the future Rust kernel leaf a contained change rather than an ABI negotiation.

This split is phased (see [../tech-stack.md](../tech-stack.md)): the **MVP (0-3 mo)** runs a TS/Python single container (the inline-PEP performance work is deferred while validating product fit); the **production-target stack (6-12 mo)** moves the inline PEP to the Go-first binary and hardens the rest. Pinned versions live in [../tech-stack.md](../tech-stack.md), not here. The full evaluation and source URLs live in [../architecture/tech-stack-analysis.md](../architecture/tech-stack-analysis.md).

## Consequences

### Positive

- Each tier uses the right tool: predictable low-latency, memory-safe enforcement inline; fast iteration and a rich AI/connector ecosystem in the control plane.
- Go-first collapses the compliance surface on the money path: FIPS 140-3 validated crypto comes from the standard library (`GODEBUG=fips140=on`), with no third-party validated module to vendor, audit, or track — a decisive advantage for regulated and air-gapped customer deployments.
- Stable OpenTelemetry traces+metrics and the canonical `grpc-go` mean the hot path's observability and wire contract rest on mature, production-hardened foundations today, matching our gRPC seam directly.
- The compiled inline PEP ships cleanly as a small component into customer VPC / air-gapped deployments.
- The narrow guarantee-kernel interface (label-propagation + sink-policy decide + JCS canonicalize + sign) keeps a future Rust reimplementation a contained leaf swap, so choosing Go now does not foreclose Rust later.
- Dropping Zig and C++ and reserving Rust for three measured triggers keeps the toolchain count down and avoids speculative complexity on the critical path.
- The data-plane / control-plane language boundary mirrors the build/consume and ActionGuard seams, keeping responsibilities crisp; the gRPC (not FFI) seam keeps the tiers independently versioned and swappable.

### Negative

- Polyglot raises operational and cognitive overhead: two toolchains, two build/test pipelines, and a typed gRPC contract that must stay in sync across the boundary.
- Talent must span Go and Python/TS, or the team must be partitioned by tier.
- The MVP-to-production rewrite of the inline PEP (TS/Python container -> Go binary) is real migration work that must be planned, not assumed free.
- Go-first defers, but does not eliminate, the cost of a possible Rust leaf: if a named trigger fires (sub-ms-p99 inline proxy datapath, untrusted-connector sandbox-WASM host, or constrained sidecar), the guarantee kernel must be reimplemented in Rust behind the same interface, including re-establishing FIPS-validated crypto via a validated C backend rather than a stdlib module.
- Betting the hot path on Go accepts Go's GC tail-latency characteristics; if the latency SLO tightens into the sub-millisecond-p99 regime, that becomes the trigger to move the kernel to Rust — a risk we carry deliberately rather than pre-pay.
