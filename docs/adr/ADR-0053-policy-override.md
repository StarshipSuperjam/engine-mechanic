---
id: ADR-0053
title: Per-deployment override of policy tuning values — retune within the laws, never weaken them
status: accepted
date: 2026-07-17
replaces: [D-167]
---

## Decision

A deployment may keep its own calibrated values for a policy's tunable knobs across engine upgrades through a committed operator-config override — preserved where engine machinery is overlaid wholesale — absent until the operator first sets a value. Only genuine tuning values are eligible: fields that encode a structural law and all enforcement or guardrail configuration are ineligible by construction, so an override retunes within the laws and can never weaken one, and a trust-critical signal promotes regardless of any tuned threshold. The merge is sparse and per-key at read time — an unset or stale key falls back to the shipped default and is surfaced — and the merged value is one more static recorded input, so deterministic consumers stay deterministic. Overrides are authored through an engine-mediated operator verb and validated by the policy's own value schema, never a hand-edit.

## Rationale

Without a preserved lane, every engine upgrade silently reverts the operator's calibration — a standing limitation in every deployment, cheapest to seat before deployments accumulate. Restricting eligibility by construction rather than by review vigilance is what keeps the safety laws inviolable under operator tuning; the ratifying follow-up confirmed the bound holds — tuning a triage threshold adjusts only the latency of benign-debt surfacing, never a governance alarm.

## Anti-choice

Deferring the lane was rejected — the limitation is present in every deployment from day one. Telemetry-driven auto-calibration was rejected: no evidence for it, and it collides with determinism. Classifying the override as overlaid engine infrastructure was rejected — it would be clobbered by the very upgrades it exists to survive.
