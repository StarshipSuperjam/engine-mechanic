---
id: ADR-0059
title: Review ships as two lens-roster suites; judgment above mechanics, disclosed when idle
status: accepted
date: 2026-07-17
replaces: [D-066, D-291]
---

## Decision

Product review ships as two optional agent-suite modules mirroring design-versus-QA, filling the build workflow's two gates with additive lens values on the existing reviewer roles — no new grammar, and installable per stage. The plan-review suite carries the product-intent, architecture, feasibility, and risk-governance lenses; the pre-submission suite carries spec-conformance, usability, technical-integrity, security-governance, and the divergence-hunter. Spec-conformance reviews systematically — derive each obligation from the locked spec, mark met, diverged, or untested, no charity — while the divergence-hunter is its coupled adversarial twin, always run beside it as a second decorrelated cold context that assumes a divergence exists and hunts it; both re-derive from the spec itself, judge only locked criteria, and on a spec-less change are a disclosed no-op, never a silent green. The divergence-hunter owns only narrow, diff-introduced over-build, surfaced as a grounded question — whole-repo dead-code health stays with the technical-integrity lens. Lenses are the judgment layer above mechanical validation and CI — complementing, never duplicating — and a lens may exercise code in an ephemeral, discarded copy: read-only means no mutation of authoritative state, not no execution. The suites review all build work and are never gated behind the intake module; the lens axis stays open and additive, so a new lens is a file drop.

## Rationale

The roster is the product-facing analogue of the engine's own cold-audit discipline — a traveled lane. The semantic misbuild is the one residual the floor's mechanical legs structurally cannot catch, which is what earns a second decorrelated judgment context on conformance specifically.

## Anti-choice

Rejected: bundling the lenses into the intake module (gates general review behind a product-layer choice); single umbrella design and QA personas (cannot carry the breadth); one undifferentiated review module (loses install-by-stage); the adversarial brief folded into a posture on one lens; a whole-repo over-build sweep (false-positive storm with no denominator).
