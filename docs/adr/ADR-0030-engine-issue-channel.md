---
id: ADR-0030
title: Engine-issue channel grammar and the conformance reroute gate
status: accepted
date: 2026-07-17
replaces: [D-183, D-235]
---

## Decision
The human issue templates are pinned-section guidance, never a gate: no required-field validation, a
plain-language floor that keeps engineer idiom off the filing surface, and a fault template that asks the
operator to narrate what happened — the engine supplies the diagnosis, never the filer. Every issue the
engine authors into its own labeled channel carries a loose plain-language body contract — what it is and
why, what if anything the operator must decide or what happens next, references as followable links —
filled by construction through one shared passive authoring helper each producer calls. Routing through
that helper is block-eligible: an engine-channel issue creation whose body lacks the contract's structural
markers is denied at the pre-action gate and redirected to the helper — a minimal-work-loss redirect, the
one admitted exception to the block budget's governance-critical-only membership, because it loses no work:
the issue still gets filed, through the conforming path. The gate keys on body shape, never on tool
provenance — shape is gated, truthfulness stays posture — and because the gate is honestly fallible with no
merge wall behind it, a repository-side backstop flags a slipped non-conforming engine-labeled issue with
the conforming skeleton: never a silent rewrite, never an operator chore. The operator's own issues,
unlabeled human issues, all reads, and drafts for un-owned upstreams are exempt; on an un-owned upstream
the engine follows the host repository's templates and conventions, falling back to its own shape only
where none exist.

## Rationale
The platform cannot gate issue creation the way a required check gates a merge, so enforcement is by
construction plus a fallible redirect plus an honest backstop. A redirect clears the friction test a
work-blocking refusal would not: the same action completes, conformant, with nothing lost. Templates that
gate strand a non-engineer behind a form, and a body contract held only as posture had proven insufficient
against malformed engine-authored issues.

## Anti-choice
Rejected: required-field issue forms; a standing validator over issue bodies; nudge-and-allow, which
leaves the malformed issue created; making the backstop the primary lever (a detect-and-remediate loop the
operator rejected); gating all issue creation; an active helper that edits content rather than formatting
it; and dressing the gate as an unbypassable wall.
