---
status: draft
---

# Guardrails

## Summary

Guardrails is the engine's enforcement-and-review ladder: validation checks written work against its
declared shape per event, telemetry counts and trends the engine's own health signals in aggregate, audits
applies periodic judgment to what no rule can encode, and templates give prose surfaces a checkable shape.
The ladder never over-claims: every rule carries an honestly named strength (eADR-0006), local checks nudge
while the operator's merge stays the only unbypassable gate (eADR-0005), and detecting a problem is never
presented as fixing it (eADR-0015).

## Behavior

### Validation

**Every hard check is proven able to fail.** A standing, mandatory meta-check in the merge suite runs each
hard check against a committed deliberately-broken example and confirms the expected failure; a hard check
that lacks its broken example turns the meta-check red, and the meta-check carries its own so it is itself
falsifiable. A passing check is always presented as proof the gate works — that it was shown to catch a
deliberately broken example — never as proof the change is correct. (ADR-0026)

**What cannot be evaluated fails closed at the merge.** A bespoke check whose script is missing, exits
failing, or returns an unreadable result yields a hard finding, never a silent pass; a required rule that
cannot run blocks the merge rather than passing quietly, while locally it fails open so a broken check never
strands a working session. (ADR-0026, eADR-0005)

**A rule that does not bind a change says so.** When a required check evaluates a change from an automated
author its rule exempts, the operator sees a reported pass that names why the rule does not bind — never a
silent green that reads as verified, never a stuck pending check. Widening an exempt set is a
guardrail-weakening event under the engine's weakening gate (eADR-0011).
(ADR-0025)

**Cited follow-ups must be real.** Every follow-up issue a change's review record cites as a finding's
disposition must resolve to a real engine-labeled issue in the project's tracker; a citation resolving to
nothing fails the merge check, and an unreachable tracker is reported as could-not-verify, distinct from a
genuine failure. Green means the cited follow-ups exist — not that everything worth logging was logged.
(ADR-0027)

**The review record offers the operator runnable proof.** Every change's review record carries its
operator-runnable acceptance steps in plain language — things you can confirm yourself, distinct from things
the engine checked for you — or a no-op that states its reason; never a silent absence. An unrun recipe is
labeled a promise, not proof, and the steps are an offer, never a duty the operator must perform to merge.
(ADR-0028, eADR-0013)

**The operator is told where the teeth are.** Wherever the operator decides, the engine states plainly that
the merge-blocking check is the only gate that can stop a bad change, that local runs are advice, and — for
any rule that could not run — that the change was not verified for what that rule covers. (eADR-0005,
eADR-0006)

### Audits

**The self-audit arms itself.** A freshly deployed repo audits itself on a schedule with no operator setup,
and a stopped schedule is visible, not silent: the committed digest carries its run-date, and past a
staleness bound the next session opens with a plain notice naming the one re-arming action. The schedule's
substrate is swappable at the delivery layer without changing anything the operator sees.
(ADR-0022)

**Scheduled runs live on the operator's plan.** The scheduled run authenticates with a credential funded by
the operator's existing paid subscription, never a metered pay-per-use key; a lapsed credential stops the
run and surfaces through the same staleness notice, naming which credential lapsed and its recovery step.
(ADR-0022)

**The audit posture is canon.** The audit persona — cold-context, adversarial, retirement-default with no
quota, fresh-probe-based, read-only, report-never-heal, escalating machinery problems upstream — is fixed by
engine canon and not restated here. (eADR-0028)

**History corroborates, never decides.** The audit may read its own digest history to corroborate a finding
over time, but every call rests on a fresh probe this cycle; the digest keeps the fresh basis and the
history note visibly distinct, unreadable history degrades to a stated point-in-time review, and a
retire-candidate the operator declined returns as the same case, never a louder ask.
(ADR-0023)

**Saved-memory review without exposure.** The scheduled audit reads the operator's off-repo memory vault
through a least-privilege read-only credential provisioned behind a heavy-consent gate, and turn-on ends
with a successful engine-run test read. On a private repo the digest may name this project's stale saved
beliefs; on a public repo it structurally withholds specifics, reports the aggregate, says so plainly, and
points to levers the operator already controls — there is no opt-in flag that relaxes the withholding.
(ADR-0024)

**Standing conformance to the operator's frozen spec.** Where the operator has locked a spec, the audit
sweeps for post-merge drift against it — report-only, prioritized with partial coverage disclosed,
deduplicated so recurring drift updates one reconcile draft — and its findings are labeled as engine
judgment for the operator to adjudicate at the reconcile merge. With no locked spec the sweep is silent,
never a nag to freeze one; it judges conformance to the operator's own spec, never product quality.
(ADR-0029, eADR-0007)

### Telemetry

**Self-surfacing, never self-healing.** Telemetry's loop — detect, triage into a tracked issue, surface at
the next session start, remediate as reviewed build work, confirm by validation — is engine canon and not
restated here; its one autonomous act is opening or updating a tracked issue. (eADR-0015)

**One signal, one issue, plain words.** A recurring signal collapses onto a single deduplicated
engine-labeled issue keyed to the signal's source, so tracked volume is bounded by the engine's own
inventory of sources, never by product size; when the signal goes absent the issue auto-closes — retiring
the flag, repairing nothing. Every engine-labeled issue identifies itself in plain language as the engine
noticing its own health, never a product problem, with backstage vocabulary kept out. (eADR-0015)

### Templates

**Scaffold and shape travel together.** A template is one artifact holding both the prose skeleton a
surface is authored from and the shape rules it is checked against, so authored-from and checked-against
cannot drift apart; changing a surface's shape is editing its template, never the validator. (eADR-0006)

**Structure gates, length nudges.** A missing required section on a governance-critical surface is a hard
failure at the merge; length is only ever a budget that warns and feeds telemetry, never a hard cap that
refuses a write. Each shape rule declares its enforcement tier honestly. (eADR-0005, eADR-0006)

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| A freshly deployed repo runs its first scheduled self-audit with no setup | Deploy, wait one cycle, find a dated committed digest in the repo | operator |
| A stopped audit schedule surfaces as staleness, not silence | Disable the schedule; past the bound, the next session opens with a plain notice naming the one re-arming action | operator |
| A lapsed scheduled-run credential is named, with its recovery | Revoke the credential; the staleness notice says which credential lapsed and the recovery step | operator |
| Vault-read turn-on ends in a demonstrated success | After provisioning, the engine runs a test read and reports the result | operator |
| A public repo's digest withholds belief specifics | Run the audit on a public repo with stale memory; the digest gives the aggregate, states the withholding, and offers the operator's own levers | operator |
| A private repo's digest names only this project's stale beliefs | Run the audit on a private repo; named beliefs appear, and nothing from any other vault namespace does | operator |
| Every hard check bites | The meta-check runs each hard unit against its broken example; a unit with no example turns the meta-check red | engine |
| Bespoke-check failure modes fail closed | Broken examples for missing script, failing exit, and unreadable result each produce a hard finding | engine |
| An exempt-author change shows a disclosed not-applicable | Open an automated dependency change; the check reports a pass naming why the rule does not bind — never pending, never silent | operator |
| Widening an exempt set trips the weakening gate | A change widening the set hard-blocks until the operator's deliberate acknowledgment | engine |
| A fabricated disposition citation fails the merge | A broken example citing a nonexistent issue yields a hard finding; an unreachable tracker yields the distinct could-not-verify finding | engine |
| The review record shows runnable steps or a stated no-op | Open any engine change; the things-you-can-confirm list is present, or the no-op states its cause — never silently absent | operator |
| No locked spec means a silent conformance sweep | Run the audit with no locked spec: no conformance output, no nag; lock a spec and drift a row: the digest names the divergence in plain language with one deduplicated reconcile draft | operator |
| Corroboration is visibly distinct from the fresh probe | A corroborated finding's digest entry shows the fresh basis and the history note separately; a history-less run states it is point-in-time | operator |
| A declined retire-candidate never escalates | Decline once; the next cycle re-presents the case with no added pressure | operator |
| The detect-remediate loop closes across sessions | Seed a persistent signal: one deduplicated engine-labeled issue opens, is surfaced first at the next session start, is fixed by a reviewed merge, and auto-closes once the signal stays absent; recurrence updates the one issue | engine |
| Engine-labeled issues read as engine health, in plain words | Open any engine-labeled issue; it identifies itself as the engine's self-monitoring and carries no backstage vocabulary | operator |
| Structure blocks, length only warns | A broken example missing a required governance-critical section fails the merge suite; an over-budget doc merges with a warning | engine |
