---
id: ADR-0062
title: A depends edge is derived from what the module inspects
status: accepted
date: 2026-07-17
replaces: [D-129]
---

## Decision

A module's declared dependency is a presence assertion determined by the inspection-target axis: what its checks actually inspect and presuppose. Modules that inspect the operator's product artifacts presuppose no engine-self-validation corpus and depend only on core's check engine; only capability that genuinely rests on the guarantee that the engine's own self-validation floor holds takes the edge onto the rule-corpus package. The discriminator is reusable: every future module's dependency is re-derived from its inspection target, never inherited from a sibling's phrasing.

## Rationale

An over-asserted edge is not harmless bookkeeping: it fabricates a build-order layer resting on nothing real and leaves module documentation in live contradiction. Deriving the edge from what is actually presupposed keeps the dependency graph a statement of truth rather than of resemblance.

## Anti-choice

Rejected: keeping a product-inspecting module on the corpus package under a borrowed "floor-holds" rationale — the edge asserted a presence its checks never consume.
