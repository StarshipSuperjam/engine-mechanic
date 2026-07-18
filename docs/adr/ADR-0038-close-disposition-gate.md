---
id: ADR-0038
title: Turn close is ambient capture plus a finding-disposition gate
status: accepted
date: 2026-07-17
replaces: [D-072]
---

## Decision

Turn close does exactly two things: it triggers ambient memory capture (memory's mechanism — close
never gates it, and content survives an ungraceful exit via a boot-time recovery sweep, never a
best-effort session-end event) and it runs the finding-disposition gate. The gate mechanically blocks
the end of a turn while any recorded concern lacks a disposition — fixed in line, logged as a tracked
follow-up, or escalated — reading an ephemeral, session-scoped findings record that is never committed
and never read across sessions; recording a concern in the first place is the assistant's discipline,
so the operator promise is "everything I flagged this turn is handled," never "nothing the engine
noticed is dropped." When the bounded block budget is exhausted, a still-open recorded finding degrades
to logged — never lost — via an out-of-band promotion path that never re-enters the gate; the gate
itself fails open, auto-logging its own failure through that same path and telling the operator in
plain words the same turn. An unattended run satisfies the gate without a human via the log-it
disposition, so it can never deadlock.

## Rationale

A heavy close ritual makes finishing work cost more than doing it, and a persisted findings ledger
would resurrect the dissolved session archive while duplicating the open-issues debt register — the
durable dispositions already live in the edit, the Issue, or the escalation. The degradation and
fail-open paths must bypass the gate they serve, or exhaustion and failure would loop forever. The
honest promise is scoped to what the mechanism can actually keep: the recorded subset.

## Anti-choice

A committed or gitignored findings ledger (resurrects the dissolved archive and double-books the debt
register); claiming the gate catches concerns the session never recorded (a promise the mechanism
cannot keep); routing gate failures or cap overflow back through the gate that just failed (deadlock).
