---
id: ADR-0063
title: Named future modules with engine-observable triggers; no expression-contracts surface
status: accepted
date: 2026-07-17
replaces: [D-191, D-255, D-095, D-105]
---

## Decision

Two future optional modules are held as named catalog stubs — off the operator menu, absent from the build order — so their later build is additive rather than a refactor, and each carries an engine-observable commissioning trigger in place of operator intuition, with no detector, meter, or threshold shipped now. The product-side structural graph derives from whatever committed canonical structural artifact the project has — product code where it exists, the product's authored structural model where it does not, and where both exist, diffing the two yields an as-built versus as-designed drift check; it stays derived and fingerprint-gated, holds structure not belief, reads the product without ever editing it, and is commissioned when cold-session structural live-reads strain the bounded boot context budget. The code-style governance family — per-language standards injected into the worker agents plus a commit-boundary lint nudge, with CI the only unbypassable gate — is commissioned when recurring style divergence or repeated operator steers show posture and learned preference no longer hold consistency. No expression-contracts surface exists: the engine consumes its runtime as a black box, so an expression "contract" could only be posture or a check, and naming it a contract would dress posture as enforcement; prose organization is already governed, and internal AI-to-AI voice is dropped as unverifiable — logged honestly as dropped, not covered. Standing disclosure: while no automated code-style floor ships, the generated project's plain-language disclosure states that absence and names the planned remedy.

## Rationale

Holding the end-state slot now is what keeps the later build additive; a trigger the engine can observe beats a hunch for deciding when a deferred capability has earned its design session. A hand-authored structural graph rots silently and blurs the structure/belief wall, and a graph derived only from code is empty for non-code products.

## Anti-choice

Rejected: flipping the graph to hand-authored; naming a storage substrate now (taints a domain-general module); one shared generic trigger for both stubs (mis-fits both axes); encoding thresholds in advance; claiming the dropped expression classes are "covered".
