---
id: ADR-0042
title: Native plan mode — a yielding default, and acceptance that enters Build legibly
status: accepted
date: 2026-07-17
replaces: [D-185, D-270]
---

## Decision

The platform's native plan permission mode is posture layered on the engine's stance model, never the
safety guarantee and never conflated with it. Two laws. First, the shipped default: at install,
provisioning writes a recommended plan-mode default into this repo's committed settings as operator
config — only after reading, never writing, the operator's own user-level settings; an operator who
already prefers a different mode gets one conflict-only offer, and declining writes nothing, so their
own setting governs. Nothing static ships in the template; a later mode change is an ordinary
preference, not a guardrail-weakening event; and the unattended launch posture overrides the project
default so a scheduled run never stalls awaiting an acceptance no human will give. Second, acceptance:
approving a plan enters Build by setting the stance signal — the sole durable stance record, cleared at
every session start — and by injecting a turn-local, assistant-internal directive that triggers the
announced kickoff exactly once. The directive is machine context, never relayed and never a stance
record; the kickoff is guarded by a live re-read of the signal; so a directive replayed on resume over
a cleared signal triggers no write, no kickoff, and no stance misreport.

## Rationale

Project-scope settings override user-scope, so a statically shipped value would silently clobber the
operator's own preference — the yield must be computed at install time. On acceptance, the assistant
otherwise keeps acting on its stale session-start briefing, misreporting its stance or repeating entry
ceremony; pushing a turn-local directive while keeping the signal the sole durable record makes resume
safety hold by construction, with partial failure benign in either direction.

## Anti-choice

Shipping a static default in the template (defeats the yield); writing the operator's user-level
settings; shipping no default at all (loses the safe first-touch and cross-adopter consistency);
treating the injected directive or a replayed nudge as a durable stance record (a resumed session could
resurrect Build).
