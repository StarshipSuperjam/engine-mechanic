---
status: draft
---

# external-contribution

*Settled in the design workspace on 2026-05-30, ratified by [decision 0143](../../adr/0143-lock-the-external-contribution-module-the-cross-repo-packagi.md).*

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
| `status` | `optional` |
| `provides` | the **upstream-clean nudge** ([check](../systems/surfaces/check.md) rule — predicate = the file-precise CODEOWNERS engine-owned set; `soft`, declaring the `pre-close` suite; blocks nothing, [§6](../../principles.md)); the **cross-fork submission tooling** (an [operation](../systems/surfaces/operations.md) — the two-base branch flow + the `upstream ← fork:feature` pull request); the **operator-narration** ([docs](../systems/surfaces/docs.md) / a posture [policy](../systems/surfaces/policies.md) — submitted-is-not-accepted, the ungoverned-upstream honesty line, the decision prompts). Concrete kind realizations, `message` / copy wording, and tooling form are build-spec leaves ([§2](../../principles.md)). |
| `wires` | **none** — the upstream-clean nudge self-declares its suite and the roster is derived ([§14](../../principles.md)); the cross-fork submission tooling is an [operation](../systems/surfaces/operations.md). The product branch is engine-clean by origin, so **no hook touches [knowledge](../systems/cognitive/knowledge.md)** — its regeneration runs in the Engine's fork-main context and produces nothing on a branch that holds no engine surfaces. Any `permission` for the cross-fork `gh` command is a build-spec leaf (a closed, keyed edit if needed). |
| `depends` | `core` |
| `migrations` | none (v1) — the module owns no engine store to migrate |

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
  **has not been exercised end-to-end at v1** ([R14](../../reference/risks.md), the [clean-code](clean-code.md)
  disclosure precedent), so opting in is informed consent.

### The contributor wall holds

The module is the [§13](../../principles.md) contributor relationship made installable: it is **optional**, so
opting in is **consent, not imposed coupling**; it is **outward read-and-propose** (it inspects the outgoing
diff and opens a pull request — it never seizes the upstream, never edits the upstream's settings, and the
upstream carries no dependency on the Engine); and the **removal test passes** — uninstalling it leaves the
operator's own product and fork intact, losing only the ability to contribute cross-repo with engine
discipline. The dependency arrow stays Engine→product, and the product upstream never knows its contributor.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The laws are the lifecycle-system and locked-systems'; the delivery is this module** — no restating laws. | Read this description against the built behavior and confirm they match. | operator |
| **Optional, not core** — [§12](../../principles.md); the cross-repo machinery is an extension an own-product deployment never needs. | Read this description against the built behavior and confirm they match. | operator |
| **`depends: core`, not `validators-core`** — the nudge inspects the outgoing diff and presupposes no self-validation corpus. | Read this description against the built behavior and confirm they match. | operator |
| **The Engine stays off the contribution by posture** — the product branch is engine-clean by origin, the §6 nudge catches an accidental engine path, and the upstream's own review backstops; honest posture, not a mechanical guarantee. | Read this description against the built behavior and confirm they match. | operator |
| **Honest tiers** — the nudge is `soft` / local, the discipline is posture, the hard gate is the upstream's; an ungoverned upstream is disclosed, not papered over ([§7](../../principles.md)). | Read this description against the built behavior and confirm they match. | operator |
| **The wall holds and the operator is never stranded** — optional consent, outward read-and-propose, a working fork on any failure, removal leaves the product intact. | Read this description against the built behavior and confirm they match. | operator |
