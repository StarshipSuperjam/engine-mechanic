---
id: ADR-0046
title: Boot's standing findings — a bounded intent-exit, and honest milestone rendering
status: accepted
date: 2026-07-17
replaces: [D-306, D-319]
---

## Decision

Two boot surfacing laws. First, the leftover-template-license finding is surfaced in plain language —
leading with the private-by-default reassurance, framed as provenance rather than a problem, ranked
below governance-critical alarms — and carries a bounded third disposition beyond fix-or-decline: a
plain decline collapses it to a terse, never-fully-silent reminder, while an explicit "I meant to keep
this" records a retired marker and the finding stops surfacing from that checkout. Whether a retired
marker is honored is decided by the deterministic hook from the finding class of the live producing
detector — retire-eligibility is a fixed per-class constant, never a model-asserted or co-written
label — so a mis-written or injection-planted marker can never silence a governance alarm: governance
conditions can be declined into a terse line but never retired. Second, boot relays the state system's
milestone-selection bound by name and restates none of it; and the rendering law is boot's: no open
milestone renders as the honest normal state — no milestone is open, never a claim the project keeps
none — and several open milestones render as the several they are, named, never silently promoted to a
single "current" the engine did not elect.

## Rationale

Without an intent-exit, the engine nags a deliberately kept license forever, which teaches the
operator to ignore standing findings; but model-side retire-eligibility would let one slip or one
injected sentence silence a governance alarm, so the eligibility check must live in the mechanism the
model cannot falsify. The several-open rendering is the entire operator-facing content of the
milestone ruling — a wording leaf cannot be relied on to invent it — and stating the bound once, in its
owner, leaves one site to change if the bound moves.

## Anti-choice

Never-fully-silent with no intent-exit (permanent nagging over a deliberate choice); model-side or
ledger-carried retire-eligibility (an injection could silence a governance alarm); the state system
legislating boot's rendering (ownership inversion); silently promoting one of several open milestones
to "current."
