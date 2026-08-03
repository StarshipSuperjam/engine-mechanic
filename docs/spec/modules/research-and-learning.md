---
status: draft
---

# research-and-learning

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 7 — deliberately the program's last module: it exists only after the
plane can deliver, deploy, and observe, because learning machinery ahead of delivery capability generates
backlog, not knowledge. Enters in progress and settles by the operator's recorded acceptance before wave
7's build begins.*

## Summary

The **optional** module that closes the loop from **the world back to intent**: repository-native research
evidence (sourced, dated, contradiction-honest answers to product questions), post-release observation
intake (feedback, support signals, telemetry observations arriving as typed records), and **intent–reality
reconciliation** — when observed reality and settled intent diverge, the divergence becomes an explicit
operator decision (change the product, change the intent, investigate, or accept), never a silent rewrite
of either side. Its hard rules are the oldest in the corpus: **no observation becomes authority by
existing** (capture is triage-bound, promotion is a recorded decision), **no learning machinery edits
governing surfaces** (proposals ride the normal change flow), and **research is evidence, not
instruction** (a sourced answer carries its sources, freshness, and gaps — it informs the operator's
choice, it never makes it).

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `research-and-learning` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`research-record.v1` — a question, the sources consulted (each dated, each cited), the answer with its inference/observation lanes, named contradictions and gaps, and freshness bindings on any repository content it cites; `observation-record.v1` — a post-release signal (feedback, support case, telemetry observation) with source, date, and triage state (`captured`\|`promoted:<target>`\|`expired`\|`rejected`) — capture carries an expiry, so the inbox cannot become a durable dumping ground; `reconciliation.v1` — an observed-vs-settled divergence, the evidence on each side, and the operator's typed resolution (`change-product`\|`change-intent`\|`investigate`\|`accepted`)); the **[tool](../systems/surfaces/tools.md)** (`research.py` — record/triage/reconcile; web-reaching research runs under the deployment's own network rules and every fetched source is quarantined data, cited never obeyed); a hard **[check](../systems/surfaces/check.md)** (schema conformance; the **uncited-claim check** — a research record's answer asserting a sourced fact with no citation fails, negative-fixtured; the **silent-promotion check** — an observation in `promoted` state without a recorded decision reference fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
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

No network → research records over repository content only, disclosed; web questions refuse plainly.
Absent telemetry/feedback integrations → the intake accepts operator-entered observations only, stated.
Both runtimes drive the same tool.

### What stays out

- **No automatic governance tuning, no promotion of memory into policy** — the program's standing rule,
  restated where the temptation would live.
- **No divergent ideation machinery** — generating candidate intent is not this module's ground; it
  reconciles what exists.
- **No unattended web research** in this cut — research runs are session work under the normal stances.

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
