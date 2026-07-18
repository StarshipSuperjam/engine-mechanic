---
id: ADR-0004
title: Derived-committed artifacts are source-deterministic; conflicts are spurious
status: accepted
date: 2026-07-17
replaces: [D-217]
---

## Decision
A derived-committed artifact — a committed file whose entire content is a deterministic function of the committed source tree — is source-deterministic: the same tree yields byte-identical output under canonical serialization. A merge or rebase conflict on one is spurious and has exactly one sanctioned resolution: clear the conflict and regenerate from the reconciled tree — never a hand-merge, never a side-pick, and never the operator's job; an AI session resolves it, and a build's integrate step regenerates every member from the reconciled tree as its final authoring step. Membership is by property, not a frozen list: an artifact with any authored content, or any dependence beyond the committed sources, is not a member — which is why authored governance catalogs are excluded and their conflicts are real. The fingerprint gate exercises determinism; an explicit regenerate-twice round-trip test enforces it.

## Rationale
A live merge conflict on a committed derived artifact stranded a non-engineer gate-holder. Given a clean source reconciliation, both sides of such a conflict are valid regenerations of one tree, so regeneration loses nothing and removes the operator from conflict resolution entirely. Honesty requires "spurious and recoverable," not "impossible": a transient conflicting state can still arise mid-flight; it is only operator-invisible to resolve.

## Anti-choice
Rejected de-committing the artifacts (loses offline cold-start and reviewable diffs), blocking merges until branches are current (hostile to a non-engineer), and merge drivers that silently keep a stale side.
