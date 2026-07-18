---
id: ADR-0023
title: The audit reads its own history as corroboration, never as the judgment
status: accepted
date: 2026-07-17
replaces: [D-233]
---

## Decision

The periodic audit may read the history of its own committed digest as over-time corroboration, under four bounds. History corroborates but never decides: every keep-or-retire call still rests on a fresh probe run this cycle, and quiet is never read as dead. The audit may cite only conditions it previously observed, never its own prior recommendations or leanings. Recurrence may direct where the audit looks, but nothing is counted, weighted, or persisted; and when the history is unreadable, the audit degrades to a point-in-time review and says so plainly, never fabricating a trend. The digest presents a finding's fresh-probe basis and any corroborating-history note as distinct, and a recurring retire-candidate re-presents its case without escalating the ask — a prior operator decline stands.

## Rationale

Persistence of a condition across cycles distinguishes genuinely stale local state from a one-cycle blip, but feeding the audit its own past judgments would compound single-project bias and undo the cold-context defense engine canon fixes (eADR-0028). Reading existing committed history adds no new artifact and no ledger, so telemetry's native record stays the durable signal-of-record and the judgment ladder is untouched.

## Anti-choice

A committed trend ledger was rejected because it would rebuild the dissolved session archive telemetry deliberately avoids; statistical retirement (thresholds, decay scores) was rejected as judgment delegated to arithmetic; the self-tuning learning loop remains deferred, not smuggled in through history reads.
