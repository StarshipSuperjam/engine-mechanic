---
id: ADR-0060
title: Dependency and migration discipline: honest tiers, escalation over false gates
status: accepted
date: 2026-07-17
replaces: [D-097, D-098]
---

## Decision

Two optional configuration-management modules govern the product's dependencies and its data migrations, with each concern assigned the strongest tier it can honestly hold. Dependency governance: the security review gate is hard at CI, realized as a check rule relaying the platform's native dependency-review data through the existing required check — no new ruleset binding, no operator-privileged step, no third-party component in the pipeline; version pinning is a soft, ecosystem-detected nudge that is a disclosed no-op without a manifest; update cadence is posture by construction, since no committed seam can edit the platform floor's schedule. Migration governance rests on an honest premise — destructiveness is not mechanically decidable across ecosystems — so a destructive product migration routes to judgment-triggered human escalation through the always-present escalation policy, with recognition guidance and a recommended safer path, never a hard gate; its one soft presence check resolves three ways (artifact present, missing, or framework-has-no-concept, disclosed) and the module only ever reads — it never runs a product migration. Any firing hard gate must give the operator a plain-language next step, a remediation offer, and a recorded operator-informed accepted-exception path, and the ability to block merges is disclosed at install.

## Rationale

Degradation is full teeth where data exists and a disclosed no-op where it does not — never a claimed floor that does not actually travel. A hard gate with no exception path, or one resting on a detector that does not exist, would strand exactly the non-engineer the engine serves.

## Anti-choice

Rejected: a standalone gate workflow (killed on audit — an operator-privileged, third-party-bearing step); framing the gate as a floor that travels everywhere; hard-gating migrations without a real destructiveness detector.
