---
id: ADR-0049
title: Agent integrity — engine-prefixed names, a mechanical read-only floor with honest limits
status: accepted
date: 2026-07-17
replaces: [D-313]
---

## Decision

Agent instance names carry the engine prefix: the identifier law is universally quantified over every surface instance with a human-facing identifier, and living in a tool-dictated corner does not discharge it — an agent name is a knowledge-graph entity id and a bare typed token, exactly the class the law covers. The read-only posture is gated mechanically at the native write-tool floor: a merge-gating check asserts that a persona declaring itself read-only carries an explicit denial — or a write-excluding allowlist — of the platform's native write tools, closing the trap where a persona naming no restriction silently inherits write access. Two honest limits are part of the law: the check confirms the denial is declared while the platform is what honors it, and the floor polices native write tools only — shell and write-capable external calls are confined by the execution environment and the merge gate — so no engine text may claim "read-only" means cannot-cause-a-write-by-any-route.

## Rationale

Path confinement answers where a file lives, not what its bare name collides with — a bare identifier has no path, so the identifier law must reach it explicitly. A read-only claim held only by prose is posture dressed as enforcement; the declared-denial check makes it bite at the one point the engine controls. Stating the mechanism's limits inside the law prevents documentation from asserting more than the mechanism evaluates.

## Anti-choice

Discharging the identifier law by path confinement ("the platform corner is already the engine's") was rejected — the law's whole point is that identifiers travel where paths do not. Claiming full read-only enforcement was rejected as dishonest: the check speaks for the declaration, never for the platform's obedience or for routes outside the native tools.
