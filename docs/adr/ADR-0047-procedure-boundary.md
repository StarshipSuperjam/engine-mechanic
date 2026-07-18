---
id: ADR-0047
title: The procedural-surface boundary — one procedure, one home
status: accepted
date: 2026-07-17
replaces: [D-042]
---

## Decision

Every engine behavior keeps to exactly one surface, routed by observable properties rather than taste. Deterministic executable behavior is a tool; a protocol contract a swappable implementation satisfies is an interface; operator-facing explanation is docs; and a procedure performed by reading-and-following routes by its invocation trigger and execution context — spawned into an isolated context it is an agent, invoked in-session it is a skill, and its shared body is an operation, which every invoker references and never restates. An operation earns standalone existence only when it is genuinely shared by more than one invoker or requires human-in-the-loop steps; a single-referrer operation is a fold-or-retire candidate under audit judgment, never a hard gate. "What a system is" is never a catalogued surface: the engine self-describes through derived output, so no hand-authored current-state specification is catalogued. The one deliberate floor: the docs surface never ships empty — a named operator orientation doc (what the engine is, how to direct it, how to discover commands, and that default-on self-audit is normal hygiene) ships from the first version as a self-sufficient discovery path.

## Rationale

The procedural surfaces are mutually defining — deciding each in isolation is exactly how the prototype's surface zoo regrew, so the boundary is one law routed by trigger and context, properties an author can check rather than argue. Hand-authored design documents drift while derived output cannot, so cataloguing specification would enshrine the one document class guaranteed to go stale. The docs floor exists because an empty operator-docs slot strands exactly the non-engineer the engine exists to serve.

## Anti-choice

Designing the procedural surfaces independently was rejected — the unprincipled split regrows sprawl. Cataloguing specification as a surface was rejected because hand-authored current-state docs inevitably diverge from the system they describe. A hard mechanical bar on operation promotion was rejected: a genuinely shared procedure awaiting its second referencer must not be deleted out from under the design.
