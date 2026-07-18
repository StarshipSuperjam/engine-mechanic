---
id: ADR-0043
title: The assistant's chat is the sole in-session operator channel
status: accepted
date: 2026-07-17
replaces: [D-187]
---

## Decision

On the current platform, nothing the engine injects reaches the operator's screen — every briefing,
notice, and alarm reaches the assistant alone — so the assistant's own chat message is the sole
in-session operator channel. This is homed as a version-contingent platform constraint, deliberately
not a principle. Three consequences are law: the engine's briefing carries imperative relay markers on
its must-push subset, because the assistant cannot otherwise know the operator is blind to injected
content; the safety-critical subset — governance alarms, a grounding-failure tell, a needs-attention
headline, consent-critical prompts such as the pre-spend risk assessment and the close gate — is pushed
in plain language every session it applies, while routine status is pulled on demand through a status
verb; and the operator's did-it-ground check is a named orientation block the assistant renders first
every session, whose presence is a binary check a first-time non-engineer can apply. The relay is
posture: the merge wall stays the real guarantee, and a skipped governance relay is visible as the
missing first block.

## Rationale

Injected content reads as if written to the operator yet is delivered only to the model, so an
unmarked briefing invites the assistant to act as though the operator already saw it. The hook output
channels were live-verified invisible to the operator, so any design that parks an alarm there parks it
where no one looks; and a pull-only surface misses exactly the operator who did not know to ask.

## Anti-choice

Hook output channels as the operator surface (tested invisible); pull-only status dashboards (alarms
missed by the operator who never pulls); a telemetry-side detector for skipped relays (the relay is
model-internal and unobservable to telemetry — the observable check is the missing first block).
