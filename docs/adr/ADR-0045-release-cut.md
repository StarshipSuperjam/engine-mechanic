---
id: ADR-0045
title: Engine releases are cut by an evidenced maintainer confirmation through the gate
status: accepted
date: 2026-07-17
replaces: [D-194]
---

## Decision

Engine versions are produced by a standing maintainer-side release-cut process — the complement of the
locked version-consumption machinery — replacing any implicit edit-and-tag habit. The bump rule is a
mechanical floor plus an evidenced, unconditional human confirmation: signals classified from the
changes since the last release set a minimum bump, and a contract-affecting change carries a
plain-language impact statement plus a behavioral break/no-break demonstration where one exists — the
maintainer consents on evidence against a plain-language change inventory, never by reading code, and
may raise but never lower the floor. The mechanism is a deliberate maintainer-invoked run: propose with
evidence, the maintainer confirms or raises, a release pull request passes the control-plane gate, and
the tag and release land at the exact reviewed merge commit, single-flighted, with every release gated
on the acceptance benchmark. The run is atomic or loudly incomplete. The contract-silent breaking
change is the named honest residual of the posture tier.

## Rationale

Version production had no owner: consumption (the manifest, tagged-release overlay, and version-keyed
migrations) was locked while versions themselves appeared by hand. Breaking-ness is a semantic
judgment no pure automation can make, so the human confirmation is unconditional — but it is only as
good as its evidence, hence the inventory and the demonstration. The tag must point at exactly what was
reviewed, or the release channel ships something the gate never saw.

## Anti-choice

Homing release production in the locked provisioning or control-plane laws (production is a
maintainer-side process, not deployed machinery); a fully automatic bump (delegates a semantic
judgment to a classifier); tagging outside the reviewed merge (ships ungated code down the upgrade
channel).
