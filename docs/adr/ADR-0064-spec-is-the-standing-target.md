---
id: ADR-0064
title: The spec is the standing target — no construction milestone licenses an under-build
status: accepted
date: 2026-07-17
replaces: [D-266, D-267]
---

## Decision

The operator minted this as a standing law after observing build sessions hedging work as
"not needed until later" in ever-thinner passes: the spec is the complete final state, and
every deviation from it is driven to full conformance — in measured doses set by build
order, each dose complete, parking nothing. Four clauses govern: every build step drives the
slice it touches to full spec capability; no construction milestone or "once deployed"
horizon is a deferral license — a named owner is a concrete build step, never a milestone;
membership in the spec is decided by the spec itself (a settled document or a logged
decision scopes a capability out — a build session may not reclassify to dodge building);
and the law binds the engine to the engine's spec only — the operator alone decides how much
of their product is frozen ground. Conformance capability ships; only build apparatus
retires.

## Rationale

The hedging was build-session posture, not a spec defect: the spec mandates a stateless
builder that behaves identically template-side and deployed. Left unnamed, the deferral
grammar stretched to whatever the next milestone was, and each pass under-built a little
more. Making the tie-breaker a standing principle — rather than one decision among hundreds —
is what stops the pattern recurring.

## Anti-choice

Rejected: letting "deferred to a later named owner" admit milestones as owners (the exact
leak); treating the boundary as a build-session judgment call; and extending the law to
products the engine builds, which would freeze ground that belongs to the operator.
