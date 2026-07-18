---
id: ADR-0033
title: First-run retirement is reference-closed, enforced by a hard closure check
status: accepted
date: 2026-07-17
replaces: [D-219]
---

## Decision
First-run retirement is reference-closed: no file that survives instantiation may statically reference a
retired first-run asset — by import, dynamic import, a subprocess invocation of its path, or a hard-coded
read of a retired path. A survivor that needs such machinery is itself a first-run asset, retired in the
same pass, or is removed; there is no guard-it-instead exemption, because a static check cannot certify
that a guarded reference keeps a generated repository's first CI run green — blessing a guard would be an
overclaim. The invariant is enforced by a mandated hard CI closure check that is honest about static
reach: computed path reads are a behavioral residual the invariant still forbids but the check cannot
see. Findings speak the operator-communication standard — the consequence, the concrete file and
reference, and a disposition — never engineer shorthand; and this single-instance invariant deliberately
mints no general numbered principle, promoting only if a second travel-closure instance appears.
Already-generated repositories remediate through the engine-upgrade overlay plus the boot relay's
plain-language account.

## Rationale
The motivating failure was surviving tests importing the deleted instantiator, turning an adopter's first
required CI run red at the ask-and-walk-away trust moment — the exact moment the engine must be most
trustworthy unattended. Property-total closure with no exemptions is the only shape a static check can
honestly enforce.

## Anti-choice
Rejected: a guard-the-reference exemption, because no static check can verify a guard actually keeps the
first CI run green, so the exemption dresses an unverifiable guard as enforcement; and promoting a general
travel-closure principle from one instance, which would inflate the principle set on a single data point.
