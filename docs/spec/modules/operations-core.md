---
status: draft
---

# operations-core

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 5, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 5's build begins. Revised in draft after the trio's four cold reviews;
the largest changes: the unattended entry authority is specified, lateness splits into two named facts,
and the honest wording — never authority to land a change.*

## Summary

The **optional** module that owns the delivery plane's **operational states**: what is deployed
(consuming [deployment-core](deployment-core.md)'s drift grammar for **standing, periodic observation** —
its side of decision 0334's cut), whether it is healthy, what maintenance **conditions** stand (the
concern/condition model), what is broken (incident state), and where a qualifying problem routes. The
trio's honest authority statement: the schedule→route→repair chain confers **no authority to land a
change** — the merge gate and every consent path stand — but it *does* set unattended work in motion and
consume budget, and the operator consents to exactly that when they author the **standing maintenance
Issue**: the scope-locked, operator-authored entry authority through which unattended sessions may create
repair tasks from qualifying routes. (That entry is a small named generalization of the engine's existing
routine machinery — routine today enters builds; the maintenance Issue is its maintenance-shaped sibling,
carried as engine-template work by this wave's build. Until it exists, unattended operation is
aspiration; interactive paths work now — stated.)

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `operations-core` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`maintenance-concern.v1` — the **durable subject**: kind (dependency freshness, certificate expiry, health observation — **backup verification is deferred until deployment adapters give it a subject**, stated), its due condition, and its stable identity the ledger references; `condition-standing.v1` — the volatile read-time standing (`due`\|`current`\|`overdue`\|`unknown`) derived from the concern's own condition — **distinct from the ledger's schedule facts**: `overdue` here means the observed condition passed its threshold (a cert inside its expiry window); a *missed occurrence* is the ledger's schedule fact — two lateness facts, named apart; `incident.v1` — observation, reproduction state (referencing [delivery-core](delivery-core.md)'s owned reproduction grammar), hypothesis references, typed resolution (`repaired`\|`mitigated`\|`accepted`\|`open`); `repair-route.v1` — deterministic playbook \| bounded-repair \| operator, with the routing reason, the qualifying class, and the route's identity that [bounded-repair](bounded-repair.md)'s provenance check resolves); the **[tool](../systems/surfaces/tools.md)** (`operations.py` — observe/derive/route; read-and-derive only); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **stale-deployed-state check** — unresolvable deploy-effect references fail; the **observation-only check** — a `custom/script` negative-fixtured check proving the observe/derive fixture paths perform no mutation, the mechanizable slice of the no-execution promise); the **[operation](../systems/surfaces/operations.md)** runbook (including authoring the standing maintenance Issue); and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` |
| `migrations` | none |

### The operations model

- **Observation-only, with real observers gated honestly.** The first exercised kinds are the two with
  reachable subjects on this substrate: **dependency freshness** (manifest/index reads) and **certificate
  expiry** (a TLS read) — each with an acceptance row against a *real* source, not only staged fixtures.
  Deployed-product observation arrives with deployment adapters; kinds without a subject ship as typed
  deferred, never as permanently-`unknown` observers.
- **Two lateness facts, composed at the ledger.** Condition standing (this module's) says whether work is
  *warranted*; the ledger's cadence says when to *look*. Slot eligibility composes them there — this
  module never claims the schedule.
- **Incidents are typed observations; `accepted` is honest and durable.** Acceptance leaves a standing
  known-state record, never a silent close.
- **Routing is recorded reasoning with a resolvable identity.** Deterministic playbook first;
  bounded-repair only for repair-eligible classes with the module installed; operator otherwise. The
  route's qualification is consumed at routing, not re-validated at attempt — stated.
- **Standing drift consumes, never re-owns.** Periodic drift observation reads deployment-core's
  drift-record grammar against declared state; effect-time reconciliation stays deployment-core's.

### Degraded behavior

Without deployment-core: no deployed-state or standing-drift derivation; **repo-local kinds only**
(dependency freshness of the repository's own manifests) — the narrow honest slice, named, not implied
general. Without maintenance-ledger: standings derive on read, nothing schedules. Unreadable state
refuses derivation. Both runtimes drive the same tool.

### What stays out

- **No execution** — the observation-only check carries the mechanizable slice; the remainder is the
  stated posture with the merge gate behind it.
- **No scheduler** — the ledger records; the maintenance Issue and the operator's own unattended setup
  are the entry.
- **No auto-escalating authority.**

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; dangling deploy references fail; the observe paths cannot mutate** — the observation-only check's negative fixture bites. | Schema + both custom checks ride CI (hard). | engine |
| **Real observers observe** — dependency freshness against a real index and certificate expiry against a real endpoint each yield correct standings. | Fixture: the two real-source rows. | operator |
| **Standings are honest** — staged conditions yield `due`/`current`/`overdue`; unobservable yields `unknown`, never `current`; deferred kinds read deferred, not `unknown`. | Fixture: the staged condition set. | operator |
| **Routing is recorded, deterministic-first, and resolvable** — the three staged classes route correctly with reasons; the route record's identity resolves for the provenance check downstream. | Fixture: the three staged classes. | operator |
| **`accepted` persists** — an accepted incident leaves its standing record. | Fixture: staged acceptance. | operator |
