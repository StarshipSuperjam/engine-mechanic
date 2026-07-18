---
id: ADR-0039
title: The build workflow — two-beat consent, single writer, honest gates
status: accepted
date: 2026-07-17
replaces: [D-073]
---

## Decision

The claim/plan surfaces and the merge-time contract gate are engine canon (eADR-0025, eADR-0021); this
record carries only the workflow laws atop them. Build follows one fixed gate shape — plan, plan
review, implement, integrate, pre-submission review, submit — with the review lenses at each gate
derived from what is installed; the shape is honest posture, its one mechanical hook the required
presence of the contract's Review record — truthfulness stays posture, and the record states in-block
that it is the engine's own account, the operator's approval the real gate. The plan gate runs in two
beats: consent before the spend (a plain-language headline that varies with the change, a
consequence-named depth choice in the operator's language, a cost-and-time estimate), then one
synthesized recommendation after the audit — always re-engaging the operator on an unresolved
blocking finding, every disposition surfaced, never silently absorbed. The orchestrator is the single
writer of final commits: workers produce mechanical work product in isolation and the orchestrator
reviews, revises, and authors the cohesive set — delegation buys cohesion under context pressure,
never speed. Validation must be green before the expensive judgment review and reruns on every change;
the cold audits run once at the agreed depth, the Review record stating any post-audit fixes as
validated but not re-reviewed. Depth scales to a genuine floor — a trivial change is one entry, one
glance, one merge — and Routine is this same workflow's implement phase distributed across unattended,
non-interactive, scheduler-serialized local sessions for decomposable bulk work only, never auto-merging.

## Rationale

A non-engineer's approval is only consent if cost and coverage are named before the spend and the
findings arrive as one synthesized call, not a panel to referee. The single writer exists because
generation at scale loses the whole; review-and-author keeps the PR cohesive so cold audits catch
substance. The shape is named as posture because nothing local can force a lens run before the merge.

## Anti-choice

Folding the Review record into the mechanical validation results (blurs the judgment/mechanical
line); framing the skeleton as mechanically always-running; workers as a speed play; cloud-hosted
routine runs, whose fully-autonomous fresh-clone model does not fit this design.
