---
id: ADR-0051
title: The cold-start invocation law
status: accepted
date: 2026-07-17
replaces: [D-200]
---

## Decision

The operator-presentation relay (recorded with the lifecycle decisions) means routine status reaches the operator through a typed status verb. On the live platform, cold-start menu visibility and model-invocability are mutually exclusive for a single skill; the law follows: any verb the operator must be able to reach at a cold session start is operator-typed. The status verb — wanted precisely at session start — is therefore operator-typed; the assistant loses nothing, because it relays the same status by running the underlying tool directly, with the offer-on-relevance cue living in standing context rather than a resident skill description. The invocation axis stays load-bearing: the help listing derives from it, and a coherence check enforces that the declared invocation and the platform flag agree.

## Rationale

The platform renders no engine channel to the operator's screen, so the relay is the only honest delivery model — and the push/pull split keeps critical alarms from drowning in routine status. The cold-start law rests on the operator's live verification, which falsified the platform's documentation; an invariant the operator depends on at the moment they most need it can rest only on observed behavior.

## Anti-choice

Trusting the documentation over the live test was rejected. Keeping the status verb model-invocable was rejected — it would vanish from the menu at exactly the cold start it exists for. Removing the invocation axis was rejected (the help listing and the coherence check both derive from it), as was a both-modes skill — impossible on the platform and unnecessary given the direct-tool relay.
