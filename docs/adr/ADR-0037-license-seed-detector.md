---
id: ADR-0037
title: Standing license-seed detector with a reviewed-PR fix path
status: accepted
date: 2026-07-17
replaces: [D-302, D-303]
---

## Decision
A standing detector catches a product-root license file still holding the engine's own traveled seed —
repositories generated before the first-run clear shipped, or drifted back to the seed: boot-invoked,
offline, read-only, consent-gated detect-and-offer, reading the committed state of the default branch. It
fires only on a positive self-seed match over the append-only set of all historically-shipped seeds, each
recognized by its body plus a per-era distinctive template-author anchor — the engine holds no notion of
the operator's legal identity, only its own seeds — conservative, preserving on any doubt, and scoped to
the license file only. On consent the removal lands as a reviewed pull request the operator merges,
through the build layer's trivial fast path — never a boot-time write, which in a protected,
fully-provisioned repository is either non-durable or strands the checkout; the detector dedupes against
an already-open removal proposal and names the bounded staleness residual of a not-yet-synced local
checkout. Topology's ownership law gains exactly one narrow standing exception: the engine may propose,
through a reviewed pull request, removal of its own still-recognizable seed from the product-root license
— never a direct reconcile-write, so product ownership of the root is untouched. Decline is an
intent-exit: a plain decline collapses the surfacing to a terse standing line, while an explicit
kept-on-purpose acknowledgment retires the finding — a terminal state scoped to findings with a
legitimate operator-intended outcome, never to governance alarms.

## Rationale
The first-run clear fires once, so repositories generated before it shipped carry a foreign copyright
governing the adopter's own product; self-seed recognition dissolves the identity problem, since the
engine need only recognize what it itself shipped. The audited boot-time clear proved infeasible against
a protected branch, and routing the fix through the reviewed gate makes the operator's merge the consent.

## Anti-choice
Rejected: a boot-time working-tree delete (non-durable, dirties the checkout) and a direct default-branch
commit (rejected by protection, or strands the checkout); a marketing-readme sibling detector arm, as
over-build; and generalizing the topology exception to a plural corrections-of-engine-residue category —
an open category inviting self-authorizing members, reverted to keep the exception singular.
