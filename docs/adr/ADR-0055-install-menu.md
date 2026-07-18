---
id: ADR-0055
title: The install menu shows only opt-outs, grouped under recognized disciplines
status: accepted
date: 2026-07-17
replaces: [D-067, D-068]
---

## Decision

The install walkthrough enumerates only the packages an operator can opt out of. The required spine is never presented as an install choice and is not disablable, but it is disclosed in plain language in the project README and the engine's self-map readout — hidden from the installer is not undisclosed. Optional packages group under recognized software-discipline umbrellas (product management, configuration management, verification and validation), carried as provisioning-side presentation data keyed by module id — deliberately not a manifest field — and each module carries a one-line plain-language gloss. An optional module earns a slot only if its use case is cross-cutting across project types and it adds capability nothing already provides; kept optional modules default to off. The dependency-closure invariant: hiding required internals is safe only while no operator-facing package depends on a hidden one; any such future dependency must surface at install confirmation.

## Rationale

A non-engineer choosing capabilities needs a short menu of real choices in terms they can look up, not an inventory of internals; recognized discipline names scale to dozens of modules where invented names would not. Over-coverage serving no quality attribute is scope creep, so the inclusion bar cuts bundles whose capability already has a surviving home. Keeping the grouping presentation-side leaves the locked manifest grammar untouched.

## Anti-choice

Rejected: a category field in the manifest (trips the locked grammar); coarse merged packages (recreates the grab-bag and re-couples deliberately decoupled capabilities); keeping every prototype bundle to be safe (re-imports the breadth that sank the prototype); default-on optional modules (the engine holds no default-on opinion for optionals).
