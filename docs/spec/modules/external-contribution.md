---
status: locked
---

# external-contribution

*Reconciled with engine-template@`cdbbc33` as built (2026-08-02) — AI-compared and operator-ruled under [decision 0320](../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with the manifest's `status` field separated into the distribution, applicability, and activation axes by [decision 0335](../../adr/0335-separate-module-distribution-applicability-and-activation.md); ratified as intended design on 2026-05-30 by [decision 0143](../../adr/0143-lock-the-external-contribution-module-the-cross-repo-packagi.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

The **optional** module that realizes the
[external-contribution](../systems/lifecycle/external-contribution.md) operating arrangement — the
Engine contributing to a product repository the operator does **not** own (an open-source project, or the
engine-mechanic building engine-template). The *laws and design depth* live in that lifecycle system doc and
the locked [check](../systems/surfaces/check.md) /
[build-orchestration](../systems/lifecycle/build-orchestration.md) /
[control-plane](../systems/infrastructure/control-plane.md) systems; **this module is the
packaging** — the artifacts that activate the mode plus the manifest that installs them.

It is **optional, not core**: a deployment building the operator's *own* product never contributes to a repo
it does not own, so the cross-repo machinery is a genuine extension and the contagious core stays minimal
([§12](../../principles.md)). It `depends: core` — **not** [validators-core](validators-core.md):
its nudge inspects the *outgoing contribution diff* and presupposes **no** engine-self-validation corpus, so
it needs only `core`'s check engine (the kind dispatcher + the read-only path-set predicate the
[topology](../systems/infrastructure/repository-topology.md) already derives), never the
self-validation rule corpus. It is **standalone** and fills no [Slot](../../reference/glossary.md)
([D-069](../../adr/0069-core-module-seam-walk-the-demarcation-operationalized-glossa.md)).

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `external-contribution` |
| `distribution` | `extension` |
| `applicability` | `detected` (a fork-native contribution arrangement to an un-owned upstream) |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **upstream-clean nudge** ([check](../systems/surfaces/check.md) rule — predicate = the file-precise CODEOWNERS engine-owned set; `soft`, declaring the `pre-close` suite; blocks nothing, [§6](../../principles.md)). One built firing fact disclosed plainly: the pre-close suite is collected on **every clean turn-close** and dispatches by suite membership — the rule's declared outgoing-contribution context is not enforced at that entry — so its no-argument run reads the *local branch diff* and, over ordinary owner-repo engine work, speaks its cross-fork wording outside any submission flow; the message-scope mismatch is the build's to fix, tracked as [engine-template issue 777](https://github.com/StarshipSuperjam/engine-template/issues/777). **Two** [operations](../systems/surfaces/operations.md): the **cross-fork submission flow** (the two-base branch flow + the `upstream ← fork:feature` pull request) and the **issue-filing flow** (opening an issue on a contributed-to project, following that project's own templates), each backed by its tool in the module's `tool` group — read-and-propose, not read-only: each tool inspects freely but performs its one outward write (opening the pull request; filing the issue) only on an explicit affirmative decision, its own header calling the act irreversible and outward-facing (the check tool alone is fully read-only); and the **operator-narration**, delivered as a posture [policy](../systems/surfaces/policies.md) plus the two runbooks' own notes (submitted-is-not-accepted, the ungoverned-upstream honesty line, the decision prompts) — no separate docs surface materialized. Remaining copy wording and tooling form are build-spec leaves ([§2](../../principles.md)). |
| `wires` | **none** — the upstream-clean nudge self-declares its suite and the roster is derived ([§14](../../principles.md)); the cross-fork submission tooling is an [operation](../systems/surfaces/operations.md). The product branch is engine-clean by origin, so **no hook touches [knowledge](../systems/cognitive/knowledge.md)** — its regeneration runs in the Engine's fork-main context and produces nothing on a branch that holds no engine surfaces. Any `permission` for the cross-fork `gh` command is a build-spec leaf (a closed, keyed edit if needed). |
| `depends` | `core` |
| `migrations` | none — the module owns no engine store to migrate |

### Trust — two gates, honest tiers

The mode's hard gate is the **upstream's**, not the operator's, so enforcement is named honestly
([§6](../../principles.md)/[§7](../../principles.md)):

- **Contributor-side (configurable).** The fork's branch protection + the Engine's pre-submission checks
  (PR-body completeness, the validation suite, the upstream-clean nudge) run before the operator submits.
- **Acceptance (not the operator's).** A **governed** upstream's own required checks (which run in its context
  for a fork pull request) + maintainer review are the real wall — a [§6](../../principles.md) human gate whose
  human is not the operator. An **ungoverned** upstream's merge is vacuous as a gate, and the honest line is
  that the fork-side checks are the only real one — never dressed as review it is not.

### Operator trust — never misled, never stranded

The operator never merges their own work in this mode, so the module owns the narration that keeps a
non-engineer oriented (wording deferred to build, [§12](../../principles.md) leak guard):

- **Submitted is not accepted** — narrated at submission and on status checks: the maintainers decide; it may
  take a while or be declined; either way the working fork already has the work, and a decline still leaves a
  fork the operator can use, revise, or resubmit.
- Mechanical steps a non-engineer cannot do by hand (two-base branch flow, rebase on a moving upstream, merge
  conflict, DCO/CLA sign-off) are **Engine-owned** and degrade to a plain "I need a decision" prompt, never a
  raw git conflict.
- **Degradation** ([§5](../../principles.md)): an unreachable / unresponsive upstream leaves a **working fork**;
  the stalled submission rides the finding-disposition / [telemetry](../systems/guardrails/telemetry.md)
  channel (Engine drafts, operator files).
- **Setup-time disclosure:** the provisioning selection-UX states plainly that this package contributes to
  repos the operator does not control, that acceptance is the upstream's call, and that the cross-repo path
  **has not been exercised end-to-end at v1** ([R14](../../reference/risks.md), the [clean-code](../../reference/module-catalog.md)
  disclosure precedent), so opting in is informed consent.

### The contributor wall holds

The module is the [§13](../../principles.md) contributor relationship made installable: it is **optional**, so
opting in is **consent, not imposed coupling**; it is **outward read-and-propose** (it inspects the outgoing
diff and opens a pull request — it never seizes the upstream, never edits the upstream's settings, and the
upstream carries no dependency on the Engine); and the **removal test passes** — uninstalling it leaves the
operator's own product and fork intact, losing only the ability to contribute cross-repo with engine
discipline. The dependency arrow stays Engine→product, and the product upstream never knows its contributor.

## Operator and automatic workflow routing

**Current disposition: automatic model routes.** When installed, this add-on's setup is reached by the
generated `model-only` route `engine-setup-external-contribution`; its work is reached by intent through
`engine-file-upstream-issue` (the target project's own Issue procedure) and
`engine-submit-upstream-contribution` (the external-contribution submission) — per decision 0336. Those
upstream routes follow the target project's templates and filing authorization and never use the Engine's
own Issue helper; none installs the add-on or grants authority because a trigger matched.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.* *(No row in this table earns `engine` — every criterion here rests at least partly on your observation.)*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The laws are the lifecycle-system and locked-systems'; the delivery is this module** — no restating laws. | Operator observation: the manifest provides one check, two operations, one policy, and the tool group, and each packages delivery against the lifecycle-system laws rather than restating them. No merge-gated check asserts the non-duplication. | operator |
| **Optional, not core** — [§12](../../principles.md); the cross-repo machinery is an extension an own-product deployment never needs. | Operator observation: the manifest declares `distribution: extension` and no other module depends on it. Partial support: module-manifest (hard, CI) holds the distribution field schema-valid, and self-map-drift (hard, CI) keeps the rendered extension marking true — the never-needed-by-own-product judgment is yours. | operator |
| **`depends: core`, not `validators-core`** — the nudge inspects the outgoing diff and presupposes no self-validation corpus. | Operator observation: the manifest's depends carries `core` alone. Partial support: self-map-drift (hard, CI) regenerates the dependency edge and catches a map that disagrees with the manifest — it validates consistency with whatever is declared, not that the dependency must exclude validators-core. | operator |
| **The Engine stays off the contribution by posture** — the product branch is engine-clean by origin, the §6 nudge catches an accidental engine path, and the upstream's own review backstops; honest posture, not a mechanical guarantee. | Operator observation: the submission runbook builds the branch engine-clean by origin and the soft nudge inspects for engine-owned paths. The nudge rides pre-close only — a local nudge, never merge-gated — so the criterion's own "posture, not guarantee" framing is exactly what you verify by reading. | operator |
| **Honest tiers** — the nudge is `soft` / local, the discipline is posture, the hard gate is the upstream's; an ungoverned upstream is disclosed, not papered over ([§7](../../principles.md)). | Operator observation: the check declares `tier: soft` with the pre-close suite (a local-nudge context), the policy's own enforcement section says no detector grades the narration, and the ungoverned-upstream disclosure rides the policy and runbook notes. No merge-gated check covers any leg. | operator |
| **The wall holds and the operator is never stranded** — optional consent, outward read-and-propose, a working fork on any failure, removal leaves the product intact. | Operator observation: opt-in status, the runbook's degradation paths (an unreachable upstream leaves the working fork), and the policy's your-fork-keeps-the-work commitment. No merge-gated check exercises the removal or degradation paths. | operator |
