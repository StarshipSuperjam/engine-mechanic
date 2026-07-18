---
id: ADR-0044
title: The operator checkout is a surface, not a workspace — strand detection and lossless repair
status: accepted
date: 2026-07-17
replaces: [D-189]
---

## Decision

The top-level operator checkout is the operator's surface, never a build workspace, and the engine
guards that boundary four ways. Build work rests on the platform's native per-session worktree
isolation as its substrate — a strong default, never a guarantee — with no bespoke location guard
built. A never-strand posture floor rides the deployed grounding floor: the engine never mutates the
operator checkout's git state as build work, autonomously, or without consent — scoped to the
detach-and-strand class, not to commits reaching the default branch through the reviewed channel — with
the consented un-stranding repair the sole exception. A genuinely stranded checkout (a detached head,
missing engine files — binary offline checks only) is detected at boot and relayed read-only with an
offer to fix; being behind the main line is the normal state under the worktree-and-pull-request model
and never alarms on bare distance. The fix is lossless-or-it-does-not-run: offline predicates gate it,
a rescue branch precedes any risky re-attach, divergence is never silently fast-forwarded, and
losslessness is claimed only for the fix's own operations, with the version-control system's own
recovery log named as the backstop. The merge wall covers shipped history only, never local checkout
integrity.

## Rationale

An always-on, stance-independent location guard would re-open the settled decision that always-on
enforcement is not the stance system's concern, and would rest on fragile shell parsing. Alarming on
ordinary behind-ness would cry wolf on the normal state and teach the operator to ignore the one alarm
that matters. A repair that can guess is a repair that can lose work.

## Anti-choice

A bespoke always-on location guard (re-opens a settled drop; fragile); alarming on bare
behind-distance (habituates the operator to noise); a fix that silently fast-forwards divergence or
claims losslessness beyond its own operations.
