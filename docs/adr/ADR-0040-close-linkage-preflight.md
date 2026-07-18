---
id: ADR-0040
title: Submit-time close-linkage pre-flight — detect and surface, disclosed defang
status: accepted
date: 2026-07-17
replaces: [D-283, D-284]
---

## Decision

At submit, before the pull request opens, the orchestrator compares what the PR will actually close —
the platform's computed will-close linkage plus any closing keywords in the commit messages being
integrated — against the closing intent the PR declares in its own structured scope, and surfaces the
result in the Review record. Two contradictions are machine-decidable without guessing intent: a
will-close on an issue the scope declares only part of, and an under-link where a compound closing line
silently links fewer issues than it names. On any contradiction the default is to surface it in plain
language; only an unambiguously accidental keyword — the scope declares partial work and carries no
deliberate close line — may be neutralized, and then only as a minimal keyword-only defang, disclosed
in the Review record, never a rewrite of the narrative. Adjudication is same-repo only: a close
reaching another repository, or one a cross-fork contribution would trigger upstream, is surfaced and
named, never silently passed and never defanged. The pre-flight is not a gate: it inherits the Review
record's posture-truthfulness tier, bounded on both paths by the operator's own independent will-close
view at the merge.

## Rationale

The platform auto-closes issues from any closing keyword buried in prose, and repeated real incidents
of PRs closing issues they only partly addressed were caught only by the operator's eye after an
authoring-discipline note demonstrably slipped. A silent auto-edit of what a PR closes would
reintroduce the exact scope-intent judgment and silent backlog change the pre-flight exists to prevent,
and would break the operator's independent view precisely where the engine acted alone. A recoverable
miss (reopen the issue) does not warrant a merge-blocking gate.

## Anti-choice

A soft CI check (reaches neither the assistant mid-session nor a walked-away operator); a hard merge
gate (disproportionate, and a merge denial on outage); a silent unilateral auto-edit; dropping the
defang entirely (a disclosed minimal defang preserves fix-at-the-source value); adjudicating cross-repo
closes on a guess about a scope line that does not exist.
