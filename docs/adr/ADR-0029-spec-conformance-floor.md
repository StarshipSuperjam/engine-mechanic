---
id: ADR-0029
title: Conformance to the operator's frozen spec — a mechanical denominator and a standing sweep
status: accepted
date: 2026-07-17
replaces: [D-287, D-296]
---

## Decision

Conformance to the operator's locked spec gets a durable mechanical denominator: a derived obligation matrix, one row per obligation, pinned to its source span by content digest so a reworded obligation re-opens as changed; the matrix is an index, never a trusted second referent — reviewers and sweeps re-derive from the human-readable spec span itself. The whole conformance-enforcement floor travels to deployed repos conditionally, per locked row: with nothing locked it is a disclosed no-op, never a recurring nag that pressures an operator to freeze a staged or MVP spec. The audits rung runs the floor's standing cadence to catch what the introduction-time gate structurally cannot — drift after merge: report-only, forward divergence only (does each locked criterion's built code still meet it), prioritized rather than exhaustive with partial coverage disclosed, and deduplicated by row identity so recurring drift updates one draft. A standing finding is engine judgment carrying no behavioral correlate at that cadence, its warrant says exactly that, and adjudication is the reconcile merge; the sweep checks conformance to the spec the operator froze, never product quality — the engine-product wall holds (eADR-0007).

## Rationale

The silent under-build class — obligations never realized and never noticed — closes mechanically once a coverage denominator exists, while the correctness residuals (self-consistent divergence, faithfully building the wrong spec) are irreducible and are named rather than absorbed. A per-merge gate sees only what a change introduces; only a standing sweep sees a re-litigated row, accumulating small divergences, or code that predates its criterion's lock.

## Anti-choice

A hand-authored criterion-ID scheme was rejected as a parallel namespace that rots; unconditional travel of the floor was rejected because it would nag products whose operator deliberately keeps scope open; an exhaustive whole-repo sweep each cycle was rejected for its false-positive storm and run cost — prioritized coverage, honestly disclosed, is the surviving shape.
