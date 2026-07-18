---
id: ADR-0025
title: A rule that does not bind a change says so — the disclosed not-applicable
status: accepted
date: 2026-07-17
replaces: [D-207]
---

## Decision

A check rule may declare, in its own data, an applicability boundary naming automated change-authors it does not bind. When the merge suite evaluates such a rule against a change from an exempt author, the result is a disclosed not-applicable — a genuine reported pass that names why the rule does not bind — never a silent skip (which reads as verified) and never a stuck pending check (which blocks the merge). The author identity is taken from the trusted event context, never from a spoofable actor field; the core check kinds stay author-agnostic; and introducing or widening an exempt set on a required rule is a guardrail-weakening event under the engine's weakening gate (eADR-0011), forcing fresh spoof-safety confirmation. The engine relays that a green exempt result means exempt, not verified.

## Rationale

An automated dependency change is not an engine build session, and forcing the engine's change-contract onto it would manufacture a false account; but a rule that quietly stops binding is exactly the silent weakening the guardrail ladder exists to prevent, so non-applicability must be a reported, named verdict. Keeping the boundary in rule data keeps the check kinds honest and the exemption reviewable like any other rule change.

## Anti-choice

A trusted-bot registry and a general applicability-predicate language were rejected as scope creep beyond the one proven need; making check kinds actor-aware was rejected because it would smuggle an author axis into every kind; keying on the spoofable actor field was rejected outright as a spoofing hole.
