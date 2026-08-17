---
status: locked
---

# Policies

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with the reference to the discipline modules as optional corrected to their `required` distribution by [decision 0335](../../../adr/0335-separate-module-distribution-applicability-and-activation.md); ratified as intended design on 2026-06-04 by [decision 0168](../../../adr/0168-resolve-the-d-167-operator-policy-override-re-litigation-lan.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

The standing-rule surface — the engine's **what you must do**, ongoing. A policy is an active
directive that governs behavior across sessions, distinct from a [contract](contracts.md),
which records a one-time decision. Policies are the second authority tier: an accepted contract can
change a policy, a policy outranks the mechanics and guidance below it.

## Behavior

### Shape and storage

- **One file per policy**, slug-named, directory-as-index — the [ontology](../grammar/ontology.md) instance law.
- **Lifecycle** is the `decision` vocabulary: `proposed → accepted → superseded`.
- Each policy declares its **enforcement tier** ([principles §7](../../../principles.md)) — in prose,
  in a required Enforcement-tier body section rather than a frontmatter field, because one policy may
  bind a layered control no single fixed value could honestly represent; most are
  posture or soft-warn (behavioral), some bind to a hard check.
- A policy carries an **optional `established_by`** link to the contract that decided it — encouraged
  for auditability, not required, since some policies are foundational.
- The [template](../guardrails/templates.md) requires: Rule, Scope, Rationale,
  Enforcement-tier.

### The v1-core policies

The core module ships six prose policies plus one policy expressed as data (the model-bindings file),
all from layer one and non-removable — the four below, plus the
[attention](../cognitive/attention.md) policy (the tunable-values home the override section reads)
and the model-routing pair (the execution-posture rules and their data file). The four detailed here
are the trust-model three plus the **Triage-threshold policy**, which is foundational instead to
**telemetry's operation**: the legible home for the promotion thresholds telemetry reads, not a trust-model
peer. (Modules ship further policies alongside — the now-`required` dependency and migration discipline,
the `external-contribution` extension's upstream-contribution honesty, and the like — outside the core set.)

#### Contract-threshold

Keeps contracts exceptional and stops ADR over-production. A decision earns a
[contract](contracts.md) only when it is architecturally significant, constrains future
work, is hard to reverse, and has a genuine anti-choice; everything below the bar is recorded in the
structured pull-request body — the [control-plane](../infrastructure/control-plane.md) PR
contract — which the pull request carries as the durable record. Held by a layered
control: the bar as posture, a `hard-fail`
requiring the contract template carry a substantive anti-choice and significance statement (presence
is checkable; genuineness stays posture), and a `soft-warn` [telemetry](../guardrails/telemetry.md)
signal that surfaces an anomalous contract-creation rate at the next boot — the non-engineer's
safety net.

#### Finding-disposition

Governs what the AI does with anything it surfaces under a standing pushback habit, so no concern
dies in chat. Every finding takes exactly one durable disposition:

- **blocks current work** → escalate (see below);
- **minor and in scope** for the work at hand → fix in line;
- **real but out of scope** → log a tracked issue (a [control-plane](../infrastructure/control-plane.md) issue scaffold) and move on.

A "not urgent, later" aside with no artifact is a violation. The scope boundary guards against the
opposite failure: fix-in-line applies only when the fix is minor *and* related — a non-trivial or
unrelated fix becomes an issue, never silent scope expansion. Logged issues feed the remediation
loop and **re-surface to the operator in plain language at the next boot** (via
[attention](../cognitive/attention.md)), so a tracked finding is never a silent backlog the
operator must hunt down in GitHub. Enforcement is posture plus a **strong local block** at the
[close](../lifecycle/close.md) ritual: it pushes back until every finding raised has a
disposition (fixed / issue / escalated), producing a plain-language disposition summary the operator
reads instead of scouring the transcript. The durable, unbypassable backstop is human review at the
protected-branch merge, not the local block.

#### Escalation

The runtime rule for stopping autonomous action and surfacing a decision. Always-fire triggers (their
mechanical backstop is the lock fingerprint and the merge gate, not this policy): a change to a locked
or tier-1/tier-2 surface, and a hard-gate collision (the
[ontology](../grammar/ontology.md) collision rule). Judgment triggers — ambiguity,
irreversibility or external blast radius, scope breach — fire on a material threshold (when the
outcome the operator cares about would change, or the action is hard to reverse). Two modes:
**interactive** (exploration, build) stops and asks; **routine** cannot ask, so it halts and routes a
tracked finding via the "log it" disposition above, re-surfaced to the operator in plain language at the
next boot ([modes](../lifecycle/modes.md)).
The invariant across both: never silently proceed past a trigger. Escalations surface in plain
language naming the decision and the options, never a stack trace.

#### Triage-threshold

Holds [telemetry](../guardrails/telemetry.md)'s promotion thresholds, kept legible and tunable
rather than buried as constants: the **persistence threshold** (how long a persistent-but-benign signal must
persist before it promotes to a tracked issue), the **auto-resolve** observation count (how many absent
observations close a now-clear signal), and the **triage-pressure** threshold (the open-low-severity-issue
count above which the next boot renders the standing-backlog line). Telemetry *reads* these; the policy is
their governed, reviewable home — operational tuning, not a trust-model directive. Enforcement tier:
**posture** (the mechanical reading of these values is telemetry's; this policy's force is the legibility
expectation). The backstage vocabulary (streams, severity class, persistence threshold) stays in this policy
and telemetry's code and **never reaches the operator**; the policy's **Rationale** is written in plain terms
so an operator who opens the file is informed, not alarmed.

### Per-deployment value override

A policy's machine-read **tunable values** — the numeric knobs a consumer reads, never the policy's prose
rule — carry a **shipped default** a deployment may supersede for itself. The default lives in the committed
policy (template-owned machinery, overlaid wholesale on upgrade); a per-deployment
[**operator policy-override**](../../../reference/glossary.md) — a committed **operator config** file
(`.engine/operator-overrides.json`), preserved across overlays
the way the operator handle is — supersedes named keys, merged **per-key over the default at read time** (an
unset or stale key falls back to the default). A hard merge-gated check additionally surfaces a saved
override key that has gone stale — renamed, removed, structural, or non-numeric — so a dead setting is
raised to the operator rather than silently ignored forever. The policy and its shipped default stay present and
**non-removable**, and the authority tiers are unchanged: the override sets the *value* a consumer reads, it
does not re-rank policies against contracts or mechanics.

Two bounds keep this safe:

- **Tunable values only, never the laws.** Only genuine tuning knobs are override-eligible —
  [attention](../cognitive/attention.md)'s budget splits, intra-partition weights, and
  debt-blocking threshold, the triage-threshold persistence/auto-resolve/triage-pressure values, and
  the contract-threshold burst signal's rate limit.
  Tuning the triage-threshold values adjusts only the *latency and visibility of persistent-benign debt* (the
  operator's own backlog cadence) — a trust-critical signal promotes immediately regardless, so an override
  can never suppress a governance-critical alarm.
  A value that *encodes a structural law* is **not** override-eligible: attention's partition precedence and
  trim order stay fixed, so "blocking-debt-first" holds by construction, never by an operator's number. No
  enforcement/guardrail config is a tunable policy value, so the override never reaches the
  [§15](../../../principles.md)-monitored surface — it retunes *within* the laws, never weakens them.
- **Same validation as the default; determinism preserved.** The override is guarded at every stage — the
  authoring command refuses structural keys and non-finite numbers, the merge is per-key over the shipped
  default, the stale-key check bites at the merge gate, and each consumer applies to the merged values the
  same defensive normalization it already
  applies to the shipped ones — so an override can retune but cannot produce an out-of-law value. Because the
  merged value is a *static* input, a deterministic ranking function stays deterministic — the same inputs
  yield the same result.

Overrides are set through an **engine-mediated authoring command** ([core](../../modules/core.md)),
never a hand-edit, so a non-engineer tunes by a documented command rather than editing a config file. The
deferred [Q17](../../../reference/open-questions.md) auto-calibration, if ever built, would write learned values through
this same override lane. ([D-167](../../../adr/0167-take-up-q17-component-a-authorize-a-five-foundation-re-litig.md).)

## Operator and automatic workflow routing

**Current disposition: `none`.** This capability is internal engine machinery; no operator command or automatic natural-language route names it, and none is added speculatively under decision 0336.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| Escalation is posture-led but made safe by hard backstops it does not own: the lock fingerprint, the protected-branch merge gate ([control-plane](../infrastructure/control-plane.md)), and the close-ritual disposition gate. Even an un-escalated issue is caught at human review. | Operator observation across the named backstops, each with partial mechanical support: the protection and guarded-paths checks (hard, CI) bite on unauthorized protected-surface changes, the close ritual's turn-end block pushes back on an undisposed finding, and the disposition-resolution check (hard, CI) confirms cited issues are real while disclosing it cannot show every finding was logged. The terminal backstop — a human at the protected-branch merge — is repository governance no check can self-assert, so the row stays with the operator. | operator |
