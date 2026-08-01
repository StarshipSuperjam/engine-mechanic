---
status: accepted
engine_record: true
---

# Admit actionlint as an advisory member of the security floor

*Decided 2026-08-01 in this repository, by the operator, in the wave-5 ruling round under
[decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md). Settles the
register item **infrastructure-U13**.*

## The decision

The built **actionlint workflow** — a committed advisory workflow-grammar lint that travels to
every generated repo, runs on every pull request against a pinned binary, and warns without ever
blocking a merge (its run can go red; the red never gates) — is admitted as an **advisory member of
the security floor** beside the four ratified
pillars (secrets, dependencies, code, disclosure). The
[control-plane](../spec/systems/infrastructure/control-plane.md) spec's security-floor section now
names it. Its job name stays deliberately **outside the required-check list**, so a finding it
raises is surfaced for the engine to address but can never block a merge a non-engineer cannot
clear — the same advisory shape as the traveling secret scan.

This extends, in letter, the floor membership ratified by
[D-253](0253-resolve-re-lock-control-plane-the-review-record-carries-the.md), which enumerated
exactly four pillars. The floor's laws are unchanged: every member is disclosed rather than
silently downgraded, and nothing advisory gates a merge.

## Why

The engine authors its own GitHub Actions workflows, and nothing else in the corpus validates
their grammar — the validator checks engine surfaces, not workflow YAML — so a malformed workflow
could ship unseen by an operator who cannot read it. The built workflow closes that gap in the
floor's own idiom (advisory, traveling, pinned) and had shipped upstream without an admitting
decision; adopting it is strictly protective, and deleting it to match the enumeration would
remove real protection in service of a count. The missing upstream record is tracked as
[engine-template issue 785](https://github.com/StarshipSuperjam/engine-template/issues/785).

## What we ruled out

**Delete the workflow to restore the four-pillar enumeration** (rejected — removes the only
validation of the engine's own authored CI grammar). **Describe it in the spec without a decision
record** (rejected — the four-pillar set was a ratified enumeration in a locked document; extending
it silently is the drift the append-only log exists to prevent). **Promote it to a required
check** (rejected — nobody asked for that, and an operator-unclearable red on workflow style
violates the floor's advisory law).
