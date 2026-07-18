---
id: ADR-0020
title: Attention ranks work in flight; the cursor reads the plan as found
status: accepted
date: 2026-07-17
replaces: [D-314, D-315, D-317]
---

## Decision

Attention never ranks the operator's backlog or the plan's milestones: the plan's ordering belongs to the plan — engine-authored and living, with the operator's authority sitting upstream in the spec they accepted and locked and at their selection of what to build — and attention ranks only the in-flight native work record plus the open engine-tracked debt register. The state cursor's milestone field reads rather than infers: it carries the open milestone set as found — the one when exactly one is open, all of them named when several are, "none set" when none are (a claim about open state, never that the project keeps none) — and the engine never elects a single "current" by a heuristic of its own; where a build-plan drives, its phases are those milestones, so the open set already is the open phase. The operator's "now and next" travels on two channels: boot pushes the now, the next is pulled on demand and stated conditionally with the resting state named plainly — "nothing is next until you name one" — never rendered as an empty ranking, and status surfaces name the source of "what's next" in plain language. This supersedes the older formulation, still carried in earlier engine canon text, that the whole native work record is "ordered by attention".

## Rationale

A backlog item nobody is working on is a plan, not a cold session's context, and the pinned ranking form has no slot for it — ranking a large backlog was measured to produce byte-identical output to ranking none: dormant code. Electing a "current" milestone by due date was killed by its own audit — the date field is optional so the rule selects nothing in the common case, the join back to the plan was never pinned, and a stalled past-due milestone would pin as current forever. A rule that reads what the platform has beats one that infers what it lacks, and it is smaller.

## Anti-choice

A sixth ranking category for the backlog was rejected as re-litigating the pinned form to spend bounded context on deferred work; surfacing the backlog outside the ranking form was rejected; the due-date election was rejected as inference over an absent field; silently narrowing "what's next" was rejected because it creates the false belief the backlog was considered and ranked below.
