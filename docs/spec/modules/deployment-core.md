---
status: draft
---

# deployment-core

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 4, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 4's build begins, and — as a **security surface** — takes the engine's
full pre-settle design review then, per decision 0334. Revised in draft after four cold reviews; the
largest changes: effects gain a home and a target lease, drift gains its record and its boundary, health
gains its ceiling disclosure, and the marquee invariants gain merge-gated checks.*

## Summary

The **optional** deployment contract: putting an **identified immutable artifact** onto a **named,
resolved target**, verifying the product is actually healthy there, rolling back when it is not, and
recording drift between declared and actual. Its effect records live in **their own store under
delivery-core's state home** (recorded through [delivery-evidence](delivery-evidence.md) when installed;
the reconciliation vocabulary — `confirmed`\|`partial`\|`contradicted`\|`unknown` — is
**[delivery-core](delivery-core.md)'s shared base grammar**, referenced not redefined). External effects
are **runtime-serialized by a per-target lease** in the broker's runtime store — two worktrees cannot
double-apply what a git merge cannot undo; the merge-durability model covers records, the target lease
covers the world. An accepted request is not a deployment; a green endpoint is not a healthy product; a
rollback that did not verify is not a rollback.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `deployment-core` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`deploy-target.v1` — a named target with its **resolution proof** (`resolution: {method, at-revision}` — an alias-only target is unrepresentable), immutable provider identity, environment class (with the **class-vs-resolved-identity residual named**: the class attestation rides the resolved identity the operator sees, and a lying resolver is the stated residual admission probes), and its rollback anchor (with typed **anchor-absent** and **anchor-unretrievable** states — first deploys and pruned artifacts cannot pretend to a rollback they lack); `deploy-effect.v1` — artifact digest, target, provider operation identity, the **independently observed** post-state (an `observed` claim without a named source distinct from the operation's own response is **schema-invalid** — the plane's rule, carried as a hard check), and reconciliation in the shared vocabulary; `deploy-health.v1` — three lanes (provider-reported, endpoint-probed, behavior-verified), never merged, cross-module references opaque; `rollback-record.v1` — the rollback as its own verified effect, with **rollback-partial-failure** a named state; `drift-record.v1` — declared vs observed per target in the shared vocabulary — **this module owns effect-time reconciliation and the drift grammar; standing periodic drift observation is [operations-core](operations-core.md)'s ground**, per decision 0334's cut); the **[tool](../systems/surfaces/tools.md)** (`deploy.py` — plan/execute/verify/rollback through the installed adapter (which carries the broker path); **deterministic idempotency keys** derived from artifact digest + target identity + run — a retry re-derives the same key; the **per-target lease** taken in the broker-runtime store before any effect); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **unresolved-target check** — a `custom/script` check over the resolution proof; the **class-boundary check** — a deploy effect whose target class is outside the admitted set fails; the **unobserved-success check** — an effect claiming success with no observation reads `unknown`, and a staged success-without-observation fails; each negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core`, `authority-broker-contract` |
| `migrations` | none |

### The deployment model

- **Artifacts by digest; targets resolved before approval.** "Deploy latest" is unrepresentable; the
  grant's approval binds the resolved identity.
- **Effects reconcile independently; drift is a record.** Read-back uses a provider path distinct from
  the apply response; `contradicted` exists for "provider says done, observed state is wrong"; `partial`
  enumerates its delta **within the stated observation coverage** (the coverage bound rides the record).
  **Any drift repair is a new deployment under its own unexpired, operator-consented grant** — reconcile
  means record, never silently re-apply.
- **Health is three lanes with a stated ceiling.** Only behavior verification (a
  [browser-evidence](browser-evidence.md) scenario against the deployed surface, identified by the
  effect's deployed digest) may back a user-visible-health claim. **Without browser-evidence — or for
  any non-web product until other behavior lanes exist — no user-visible-health claim is representable**;
  health tops out at endpoint-probed, typed as such. Stated in the Summary-level promise, not buried.
- **Rollback verifies or types its failure.** Anchor captured before deploy where one exists;
  anchor-absent, anchor-unretrievable, and rollback-partial-failure are named states the operator sees —
  "I can always roll back" is deliberately not a promise this contract makes.
- **Duplicates and interruptions are safe by two named mechanisms.** The deterministic idempotency key
  dedupes retries; the per-target lease serializes concurrent invocations across worktrees and sessions;
  interruption resolves at reconciliation against recorded intent (the broker's ordering rule).

### Degraded behavior

No adapter → refuse plainly (the adapter carries the broker path, so "no broker" arrives as "no
usable adapter" — stated). Observation unavailable → `unknown`, with what could not be observed named.
Absent delivery-evidence → effects persist in this module's store; the recording seam degrades disclosed.
Both runtimes drive the same tool. Stub-adapter fixtures ride CI; live-provider conformance is
operator-local — the split stated.

### What stays out

- **No production-first.** The first exercised class is a disposable non-production target; production
  classes arrive by recorded decision — the class-boundary check is that decision's mechanical arm.
- **No provider mechanics, no credentials, no auto-deploy.**

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; the three marquee checks bite** — unresolved targets, out-of-class targets, and success-without-observation each fail their negative-fixtured checks. | Schema + the three custom checks ride CI (hard). | engine |
| **Transport is never deployment** — accepted-but-wrong-state reads `contradicted`; observation withheld reads `unknown`. | Fixture: staged against the stub adapter. | operator |
| **Partial stays partial, within coverage** — a staged partial application enumerates its delta and its coverage bound. | Fixture: staged partial. | operator |
| **Health lanes and the ceiling** — the false-green scenario reports lanes distinctly; without browser-evidence the user-visible claim is unrepresentable, typed. | Fixture: both staged. | operator |
| **Rollback honesty** — verified rollback, `unknown` rollback, anchor-absent, anchor-unretrievable, and partial-failure each read as their typed state. | Fixture: all staged. | operator |
| **Duplicates and races cannot double-apply** — same-key retry is the same effect; two staged concurrent invocations serialize on the target lease. | Fixture: staged retry + race. | operator |
| **Drift records, never re-applies** — a staged drift yields its record; no effect runs without a fresh grant. | Fixture: staged drift. | operator |
