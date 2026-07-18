---
id: ADR-0026
title: Every hard check is proven able to fail
status: accepted
date: 2026-07-17
replaces: [D-256]
---

## Decision

Every hard check must be proven to bite: a standing, mandatory meta-check in the merge suite runs each hard logic-unit against a committed deliberately-broken example and asserts the expected hard finding by set-membership, never by order or count. The meta-check fails closed on any in-scope hard unit that lacks its broken example, and carries its own — a seeded unit whose example is missing or non-biting must turn it red — which terminates the regress without a checker-of-the-checker-of-checkers. The bespoke-script escape hatch's process-to-result contract is pinned fail-closed: a missing script, a failing exit, and an unreadable result each yield a hard finding, and each mode is itself exercised by a broken example. The only carve-out is a check with no statically-decidable failure path in the merge environment, which resolves to a disclosed not-applicable; and the operator rendering is fixed — a passing check means the gate was shown to catch a deliberately broken example, proof the gate works, never proof the change is correct.

## Rationale

Engine canon already fixes the obligation — a hard rule that can never fail is posture wearing a machine's name (eADR-0006); this decision supplies the standing mechanism that discharges it across the whole check corpus, accepting a permanent authoring tax as the price of an honest hard tier. Discovery by presence keeps the examples co-located with their owners so uninstalling a check removes its proof with it, stranding nothing.

## Anti-choice

Trusting declared hard tiers without a witnessed bite was rejected as the exact posture-dressed-as-enforcement canon forbids; an unbounded meta-meta-check regress was rejected by having the meta-check carry its own falsifying example; proving rule aim (as opposed to logic bite) was declined honestly — aim stays an after-the-fact never-fired signal, and the bound is stated, not papered over.
