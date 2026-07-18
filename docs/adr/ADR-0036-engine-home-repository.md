---
id: ADR-0036
title: The engine manifest records the engine's home repository
status: accepted
date: 2026-07-17
replaces: [D-281]
---

## Decision
The engine manifest records the engine's home repository — the single coordinate from which both the
updater resolves its release source and the upstream escalation resolves its filing target: one
coordinate, two readers. It is seeded from the template's own committed manifest as data, never a code
constant, carried forward by the instantiator, and preserved across upgrades — updated in place, never
overlaid. Resolution is three-state: resolvable, so fetch; recorded but unresolvable, so refuse loudly,
naming the home; absent, so refuse with a cause-matched reason and remedy — and it never falls back to
the deployed repository's own origin, which for a template-generated repository is its own release-less
copy. Because the home selects where executable engine code is fetched from, repointing it is a
guardrail-weakening-class change requiring the operator's distinct acknowledgment that this changes where
their engine's code comes from. The engine's home is distinct from a fork-native deployment's
product-project upstream, which is never the escalation target.

## Rationale
Deployed copies could never receive engine updates because the template repository's identity was
unstated and origin resolution pointed a generated repository at itself — the live failure this fixes.
A single recorded coordinate with loud three-state refusal keeps a wrong-but-present home from silently
masquerading as an unreachable one.

## Anti-choice
Rejected: a new operator-tunable release-source knob — the source never changed, only its resolution was
unstated; keying on origin or a template-repository marker, foreclosed by the two-senses-of-upstream
distinction and the spoofable-verdict rejection; two-state present-or-absent resolution, since
present-but-wrong must refuse loudly; and overlay-carried refresh of the coordinate.
