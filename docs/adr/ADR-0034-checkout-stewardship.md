---
id: ADR-0034
title: Operator-checkout stewardship — two-stage strand detection and the harness-exhaust boundary
status: accepted
date: 2026-07-17
replaces: [D-275, D-239]
---

## Decision
Strand detection over the operator's top-level checkout is branch-agnostic and two-stage, because the
harmful essence is missing your merged main line of work, not sitting on a branch. Stage one is an
offline, every-boot, collapse-managed gentle signal the moment the checkout parks off the default branch,
classified against the persisted record of the default branch's name — never a remote pointer that is
frequently unset. Stage two is a network- and consequence-gated escalation once the checkout is missing
merged main-line work, on any branch; states the engine cannot compute degrade honest-silent, never a
false all-clear. Any fix runs only when it is offline-decidably lossless; whether parked work is already
merged is a best-effort advisory read that shapes the offer's tone only, never its safety — its
uncertainty errs toward over-reporting unfinished work, so the engine errs to the keep-your-work-safe
framing — and the operator surface carries no git vocabulary, reduces to one decision, and the first full
relay owns the disclosure gap that earlier sessions could not spot this. Boundary: accumulated local
session worktrees and branches are the assistant platform's exhaust, not an engine surface — the engine
builds no standing machinery to reconcile them; remediation belongs at the local and platform layer and
retires when the platform ships its own cleanup.

## Rationale
The off-main park is caught in the only window it is cheap to fix; consequence-only detection is silent
exactly then. An engine-owned reconciler fails structurally: offline merged-detection is defeated by
squash merges, making it a silent no-op against its own targets; autonomous mutation of standing state
contradicts the recommend-never-remediate charter; and mopping up version-contingent platform exhaust is
a layer violation.

## Anti-choice
Rejected: a third always-on binary off-main alarm (structure inflation, false positives on intentional
brief checkouts); consequence-gated-only detection, silent at the moment the park is free to fix; the
engine-owned git-hygiene reconciler; and an auto-clean-every-boot toggle, which has no legal home in a
tuning-values-only override scope.
