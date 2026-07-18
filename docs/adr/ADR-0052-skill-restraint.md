---
id: ADR-0052
title: Skill restraint — residence is earned, discovery is derived, routine entry is explicit
status: accepted
date: 2026-07-17
replaces: [D-087]
---

## Decision

A model-invocable skill's description is permanently resident in every session, so residence is rationed: a procedure earns model-invocation only for a genuine metacognition gap — a recurring procedure the model should reach for unprompted — and a procedure with a better home (a review lens, a flow-owned gate step, a capture step at its owning gate) routes there instead, so an empty model-invocable set is earned by demonstration, never asserted. Operator-typed verbs are rationed by discoverability instead: the discovery index derives its listing by presence — installed verbs always, optional ones as available-if-installed — and the orientation doc points at the index rather than enumerating verbs, so the two paths cannot disagree. A scheduled routine's firing only launches a prompt, so routine activation is an explicit entry verb validated against the live schedule, thin and delegating to an owned operation rather than carrying a step list.

## Rationale

Every resident description is paid on every session and mis-triggers when vague, so the empty-by-default posture must be justified candidate by candidate — and each prototype auto-invoked skill demonstrably had a better surface to route to. A hand-enumerated verb list and a derived index would drift apart; deriving the listing from presence removes the second source of truth. Treating a scheduled routine as self-activating is empirically false on the platform, so the activation must be an explicit, validated entry.

## Anti-choice

A model-invocable capture skill was rejected — capture is flow-triggered at its owning gate, not a metacognition gap a resident skill would fill. Treating routine firing as self-activating was rejected as empirically false. A hand-maintained verb enumeration in the orientation doc was rejected in favor of pointing at the derived index.
