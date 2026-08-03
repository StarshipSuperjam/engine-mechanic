---
status: draft
---

# deployment-core

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 4, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 4's build begins, and — as a **security surface** — takes the engine's
full pre-settle design review then, per decision 0334.*

## Summary

The **optional** deployment contract: what it means, provider-neutrally, to put an **identified immutable
artifact** onto a **named target**, verify the product is actually healthy there, roll back when it is not,
and reconcile drift between what was declared and what the provider actually runs. It specializes the
plane's effect-receipt grammar for deployment effects and owns the typed states no transport result may
skip: an accepted request is not a deployment; a green health endpoint is not a healthy product; a rollback
that did not verify is not a rollback. Provider mechanics live in
[deployment-adapter](deployment-adapter.md) implementations; credentials live behind the
[credential-broker](credential-broker.md) — this module owns the contract and the honesty rules.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `deployment-core` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`deploy-target.v1` — a named target resolved to immutable provider identity (account/region/resource — never an alias left unresolved), its environment class (non-production first), and its rollback anchor; `deploy-effect.v1` — the deployment effect specializing the plane's effect-receipt base: artifact digest, target, the provider operation's identity, the **independently observed** post-state, and reconciliation (`confirmed`\|`partial`\|`contradicted`\|`unknown`); `deploy-health.v1` — typed health: provider-reported, endpoint-probed, and behavior-verified are three separate lanes, never merged; `rollback-record.v1` — the rollback as its own effect with its own verification, never assumed from the deploy's undo); the **[tool](../systems/surfaces/tools.md)** (`deploy.py` — plan/execute/verify/rollback through the installed adapter and the broker; idempotency keys on every effect so duplicate invocation cannot double-apply); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **unresolved-target check** — a deploy effect whose target carries an unresolved alias fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core`, `authority-broker-contract` (every deployment effect exercises a task grant) |
| `migrations` | none |

[delivery-evidence](delivery-evidence.md) records the effects (when installed — its effect-receipt base is
what `deploy-effect.v1` specializes, stated); [platform-web](platform-web.md)'s artifact identity is the
first artifact source.

### The deployment model

- **Artifacts are immutable and named by digest.** What deploys is a digest; "deploy latest" is
  unrepresentable. The artifact-to-revision link rides the effect so deploy-to-source traceability holds.
- **Targets resolve before approval.** A target alias resolves to immutable provider identity *before* the
  grant is approved — the approval binds what will actually be touched, and the unresolved-target check
  makes the shortcut mechanical to catch.
- **Effects reconcile independently.** After the provider accepts, the actual state is observed through a
  read-back distinct from the operation's own response; `contradicted` exists for "the provider says done
  and the observed state is wrong." Partial failure yields `partial` with the delta enumerated — never
  rounded to success or silently retried.
- **Health is three lanes.** Provider-reported health, endpoint probes, and behavior verification (a
  browser-evidence scenario against the deployed surface, where installed) report separately; a claim of
  "healthy" names its lane. Only behavior verification may back a user-visible-health claim.
- **Rollback is an effect, verified like one.** The rollback anchor is captured before the deploy; rolling
  back executes and *verifies* — a rollback whose post-state was not observed is `unknown`, loudly. A
  failed rollback is a named, un-rounded state the operator sees.
- **Duplicate and interrupted invocations are safe.** Idempotency keys make re-invocation observable as
  the same effect; an interruption mid-deploy resolves at reconciliation to the observed actual state,
  never to an assumption.

### Degraded behavior

No adapter → deployment operations refuse plainly. No broker → refuse (deployment without brokered
authority is not a degraded mode — it is out of contract). Observation unavailable → effects stay
`unknown` and the tool says what could not be observed. Both runtimes drive the same tool.

### What stays out

- **No production-first.** The contract's first exercised class is a disposable non-production target;
  production classes arrive by recorded decision after the contract has been exercised.
- **No provider mechanics, no credentials** — adapters and the broker respectively.
- **No auto-deploy.** Every deployment traces to a run under an operator-consented grant; no schedule or
  event deploys on its own.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Adapter-dependent rows are disclosed not-applicable until the first adapter
exists.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; unresolved targets fail** — deploy effects conform; an aliased target fails the check. | Schema checks + negative fixture ride CI (hard). | engine |
| **Transport is never deployment** — a staged accepted-request-then-wrong-state scenario reads `contradicted`; observation withheld reads `unknown`. | Fixture: both staged against a stub adapter. | operator |
| **Partial stays partial** — a staged partial application enumerates its delta and never rounds to success. | Fixture: staged partial. | operator |
| **Health lanes stay separate** — a staged green-endpoint/broken-behavior scenario reports the lanes distinctly; the health claim names its lane. | Fixture: the false-green health scenario. | operator |
| **Rollback verifies or reads `unknown`** — staged rollback with observation withheld is `unknown`; a failed rollback is named, never rounded. | Fixture: both staged. | operator |
| **Duplicates cannot double-apply** — re-invoking a completed effect with the same idempotency key is observably the same effect. | Fixture: staged duplicate invocation. | operator |
