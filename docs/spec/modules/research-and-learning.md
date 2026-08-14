---
status: draft
---

# research-and-learning

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 7 — deliberately the program's last module: it exists only after the
plane can deliver, deploy, and observe, because learning machinery ahead of delivery capability generates
backlog, not knowledge. Enters in progress, settles by the operator's recorded acceptance before wave 7's
build begins, and — as a **security surface** (the plane's one external-web intake) — takes the engine's
full pre-settle design review then, per decision 0334.*

## Summary

The **optional** module that closes the loop from **the world back to intent**. **What ships in this
cut, plainly**: a manual observation inbox (operator-entered signals; telemetry/feedback integrations
are later arrivals), repository-native research evidence, and **the plane's one reconciliation surface**
— `reconciliation.v1`, which also receives [product-knowledge-graph](product-knowledge-graph.md)'s
design-drift findings as a divergence class — where a divergence becomes an explicit operator decision
(change the product, change the intent, investigate, or accept — **`accepted` leaves a persisted
known-divergence record**, never a silent close). Its post-release value is contingent on deployed
products existing — installable earlier, vacuously, stated. Hard rules with mechanical homes: **no
observation becomes authority by existing** (promotion needs a decision reference *and* the promoted
content **keeps its untrusted-external provenance marker** into whatever it becomes — laundering by
approved promotion is the named risk); **no learning machinery edits governing surfaces** —
`research.py` **has no write path to any governing surface or behavior file**, and a negative fixture
proves a recorded correction pattern cannot reach one; and **research is evidence, not instruction** —
`research.py` **records only**: the *session* fetches web sources with its own tools under its normal
stances, and everything fetched is quarantined data. Quarantine-on-the-record protects later readers;
**the reading session's own exposure at synthesis time is the named residual** no record field can
close.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `research-and-learning` |
| `distribution` | `extension` |
| `applicability` | `detected` (research/feedback intake in use) |
| `activation` | `explicit` · `ungated` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`research-record.v1` — a question, the sources consulted (each dated, each cited, each carrying a **schema-borne quarantine/provenance field** — presence checked), the answer with its inference/observation lanes, named contradictions and gaps, and freshness bindings on repository content it cites — **web citations perish weaker**: date-only, no invalidation when a page later changes, the asymmetry stated; `observation-record.v1` — a signal with source, date, the same **quarantine/provenance field**, and triage state (`captured`\|`promoted:<target>`\|`expired`\|`rejected`) — expiry removes **authority**, not storage (the store accretes; the anti-hoard claim is about actionability, stated); `reconciliation.v1` — a divergence (observed-vs-settled, or a design-drift class from the graph), the evidence on each side, and the operator's typed resolution (`change-product`\|`change-intent`\|`investigate`\|`accepted` — persisted)); the **[tool](../systems/surfaces/tools.md)** (`research.py` — record/triage/reconcile **only**; it fetches nothing and writes no governing surface); hard **[checks](../systems/surfaces/check.md)** (schema conformance including provenance-field presence; the **uncited-claim check**; the **silent-promotion check** — promotion without a decision reference fails; the **no-write-path fixture** — a staged correction pattern reaching a behavior file fails; each negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` |
| `migrations` | none |

### The learning model

- **Research answers carry their own limits.** Sources dated and cited per claim; inference distinguished
  from observation; contradictions and gaps named in the record, not smoothed. A research record about
  the product binds the content it examined — it perishes like all plane evidence.
- **The inbox triages or expires.** Observations enter `captured` with an expiry; the paths out are
  promotion (a recorded decision routing it to memory, an issue, or a spec reconciliation), rejection, or
  expiry. Nothing captured is silently authoritative; the silent-promotion check makes the shortcut
  mechanical to catch.
- **Reconciliation is a decision surface.** A divergence record holds both sides' evidence and waits for
  the operator's typed resolution; `change-intent` routes into the settled-description change path (with
  its re-acceptance discipline), `change-product` into normal delivery work — the module routes, the
  operator decides, the existing gates govern.
- **No self-tuning, ever.** Correction patterns and recurrence measurements may be *recorded* and
  *proposed*; no observation, trend, or metric adjusts any governing surface, threshold, or behavior file
  except through the normal reviewed change flow.

### Degraded behavior

**Degraded** with no network → research records over repository content only, disclosed; web questions refuse plainly.
**Absent** telemetry/feedback integrations (not distributed in this cut) → the intake accepts operator-entered observations only, stated.
Both runtimes drive the same tool.

### What stays out

- **No automatic governance tuning, no promotion of memory into policy** — the program's standing rule,
  restated where the temptation would live.
- **No divergent ideation machinery** — generating candidate intent is not this module's ground; it
  reconciles what exists.
- **No unattended web research** in this cut — research runs are session work under the normal stances.

## Operator and automatic workflow routing

**Current disposition: `none` (design-stage).** This research-and-learning draft has no current operator
command or automatic route. Its breakout Build issue must choose and record its routing disposition under
decision 0336; no speculative route ships first.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Records validate; uncited claims and silent promotions fail** — the two negative fixtures bite. | Schema checks + negative fixtures ride CI (hard). | engine |
| **Research honesty** — a staged research record shows citations per claim, lanes, a named contradiction, and a named gap; a staged repository-content citation stales when the content moves. | Fixture: staged research scenarios. | operator |
| **The inbox cannot hoard** — a staged captured observation past expiry reads expired; promotion requires a decision reference. | Fixture: staged expiry and promotion. | operator |
| **Reconciliation routes, never rewrites** — a staged divergence yields the decision surface; `change-intent` lands in the settled-change path with its re-acceptance discipline intact. | Fixture: staged divergence walked through each resolution. | operator |
| **Fetched content stays data** — a staged hostile source arrives quarantined and cited, never obeyed. | Fixture: staged hostile source. | operator |
