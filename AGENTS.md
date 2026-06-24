# Agent guide — Provna

This file is the entry point for non-Claude AI coding agents (and any tool that looks for
`AGENTS.md`). **The canonical, authoritative guide is [CLAUDE.md](CLAUDE.md) — read it in
full first.** This file only summarizes the load-bearing rules so an agent that lands here
does not miss them.

## What Provna is (one line)

A **vendor-neutral runtime control plane** that turns every WRITE action an agent takes in
regulated enterprise systems into a *reversible, authorized, information-flow-controlled, and
regulator-grade-provable* contract. The atomic unit is the **guarded saga step** (four gates:
S1 information-flow control → S3 authorization → S2 transactional action contract → S4
tamper-evident audit). **Status: pre-build / planning.** This repo is currently a
documentation tree under [docs/](docs/); there is no product code yet.

## The rules you must not break (full text in [CLAUDE.md](CLAUDE.md))

1. **Language policy.** All public/committed work is **English** (docs, file names, directory
   names, future code). Use **Turkish only** when (a) talking to the maintainer or (b) writing
   documents the maintainer specifically asks for under `docs/private/`.
2. **`docs/private/` is gitignored and is never referenced from public output.** Read it for
   context if needed, but anything you write into the public tree must be self-contained — no
   link, no file name, no `docs/private` path. Restate facts instead of citing the source.
3. **Scope discipline.** Provna owns the four gates of the agent action lifecycle and nothing
   horizontal. The test: *does this make one guarded saga step safer/more reversible/more
   provable, or does it turn Provna into an agent platform?* See [docs/product-scope.md](docs/product-scope.md).
4. **Build vs consume.** Build only the S1 IFC fusion and the S2 compensation content; consume
   the rest. No core dependency or stack change without an ADR in [docs/decisions/](docs/decisions/README.md).
5. **Honest by construction.** Fail-closed everywhere; the deterministic guarantee lives only
   in the lattice + sink-policy; evidence is "regulator-grade forensic-reproducible", never
   "court-admissible"; mark `[OPINION]` / `UNVERIFIED`; invent no statistic, price, or date.
6. **Docs conventions.** Single H1 + bold metadata (no front-matter); `kebab-case.md`; relative
   links only (never to `docs/private`); ASCII-safe Mermaid labels; one canonical home per
   artifact; phase-relative milestones. See [docs/standards/documentation-style.md](docs/standards/documentation-style.md).

## Where to start

[README.md](README.md) → **[CLAUDE.md](CLAUDE.md)** → [docs/glossary.md](docs/glossary.md) →
[docs/product-scope.md](docs/product-scope.md) → the ADRs in [docs/decisions/](docs/decisions/README.md)
→ [docs/roadmap/current.md](docs/roadmap/current.md).
