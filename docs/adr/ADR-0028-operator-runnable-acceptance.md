---
id: ADR-0028
title: The review record offers the operator runnable acceptance steps
status: accepted
date: 2026-07-17
replaces: [D-252]
---

## Decision

At submission, a change's review record carries the operator-runnable acceptance steps for that change — rendered verbatim from the locked spec's operator-runnable verification rows — or a bounded, reason-named no-op; never a silent absence. Rendering is plain-language: steps are grouped as things the operator can confirm themselves versus things the engine checked for them; an unrun recipe is presented as a promise, not proof, with that caveat beside the list; the steps are an offer, never a per-merge duty; and a no-op states its cause plainly and never leans on passing tests as if equal to the operator seeing the thing work. The slot is posture, not a new hard gate, and engine-run demonstrations are a distinct, engine-mediated tier never dressed as the operator-runnable class.

## Rationale

Canon fixes that consent rests on evidence with a non-engine correlate, with the behavioral demonstration the operator runs themselves as its strongest class (eADR-0013); this decision surfaces that class at the merge moment where consent actually happens. It cannot be a hard gate because choosing the no-op class is uncorroborable self-judgment — a machine tier on it would over-claim — so the mechanical correlate remains the spec coverage check, and the slot stays honest posture.

## Anti-choice

A merge gate that runs a scripted demonstration and passes on success was rejected because a demonstration must be able to fail, and a self-scripted one shows only its chosen path; homing the steps in the validation results was rejected because it would deepen the all-green collapse this slot exists to counter.
