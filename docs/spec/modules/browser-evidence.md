---
status: draft
---

# browser-evidence

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 3, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 3's build begins, and — as a **security surface** — takes the engine's
full pre-settle design review then, per decision 0334. Revised in draft after four cold reviews; the
largest changes: evidence rides the plane's one grammar, safety gates are mechanized where
schema-expressible, the browser materializes through the environment plane, and the visual lane's
redaction ceiling is stated instead of promised away.*

## Summary

The **rendered-web profile** that makes **rendered behavior** first-class delivery evidence: driving a real,
pinned browser through **semantic actions** against pages whose identity
[platform-web](platform-web.md)'s `page-identity.v1` binds, asserting **explicit postconditions**, and
capturing evidence **channels** — DOM/accessibility, console, network, visual — recorded through
[delivery-evidence](delivery-evidence.md)'s grammar where installed (kind `observed`, the channels riding
the producer lane; one evidence system, not two). Its trust boundary is explicit: **the authored scenario
is trusted input, reviewed like code; page content is untrusted runtime data** — nothing observed is ever
an instruction, and **scenario control flow is fixed by the authored scenario alone**: no step, wait, or
postcondition may be parameterized by observed content, a structural rule of the scenario grammar. An
action's success is never the workflow's success — only postconditions on a fresh, identified page count.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `browser-evidence` |
| `distribution` | `profile` |
| `applicability` | `detected` (a rendered web product) |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`browser-scenario.v1` — semantic steps (roles/names/test-ids) with event-driven waits, declared postconditions, mock/interception declarations, the referenced `page-identity.v1`, and structural rules the schema itself enforces: no coordinates, no fixed sleeps, no observed-content parameters, **no secret-shaped values** (authenticated scenarios are **out of scope until the wave-4 broker exists** — stated, not smuggled); `browser-evidence.v1` — per-step results across the channels, each channel separate, the **heal channel structurally unable to read as plain green** (a healed step's original failure is a required field), quarantine framing on all captured content, and the redaction record — naming that and where redaction occurred, never the value); the **[tool](../systems/surfaces/tools.md)** (`browser_run.py` — drives one pinned browser profile; the browser **materializes through [execution-environment](execution-environment.md)'s digest-pinned image** (a runtime-downloading driver distribution is disqualified by the substrate contract; a bare-host operator-supplied browser is the disclosed host-runtime mode, its observed identity recorded); scenario execution, capture, and **capture-time redaction — this module's own named security-critical pass**: structural field-stripping for auth material (cookies, authorization headers — always, not heuristically) plus the heuristic secret-shape pass for bodies, its ceiling stated); hard **[checks](../systems/surfaces/check.md)** (schema conformance — which carries the structural rules, the heal-channel invariant, quarantine-framing presence, and mock-declaration presence; the **stale-page check** — at CI it verifies record-internal identity consistency and that the cited revision is tree-derivable; **served-digest verification requires the artifact, a stated residual** — and absent platform-web the check's reduced strength (no digest to bind) is disclosed at the gate; negative-fixtured throughout); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` |
| `migrations` | none |

### The evidence model

- **Semantic or refused; postconditions are the success.** Steps resolve by role/name/test-id with
  event-driven waits; a step that cannot resolve semantically fails typed. A run whose actions succeeded
  but whose postcondition failed is a failed run. Readiness is consumed from platform-web: postconditions
  are never asserted against a pre-ready page.
- **Heals are represented, never generated, never promoted.** The runner performs no heals; external
  retry logic may write the heal channel, and the schema makes a heal without its preserved original
  failure invalid — the promotion path is unrepresentable.
- **Mocks are declared and reconciled.** The scenario declares interceptions; the runner records what was
  *actually* intercepted, and a mismatch is a typed finding. A closed-egress environment severing a real
  seam is a **disclosed non-real boundary** in the result — the product's error page satisfying a
  postcondition never reads as end-to-end proof.
- **The visual lane has a stated ceiling.** Screenshot redaction of rendered secrets is unsolved; the
  rule is therefore structural: **no screenshots where authenticated or secret-bearing state is on the
  page** unless the scenario declares the capture with explicit per-scenario opt-in — and artifacts land
  in the committed record, so the ceiling is a rule about what is captured, not a promise about what can
  be scrubbed.
- **Unconfined mode has a floor.** Absent execution-environment, the browser runs with its own sandbox
  flags always on, and scenarios declared as exercising untrusted origins refuse to run unconfined — a
  stated minimum, not a disclosure shrug.
- **Scope is the pinned profile.** Evidence claims the browser profile it ran; cross-browser and device
  profiles are later declared expansions.

### Degraded behavior

**Faulted** — no browser available → refusal with the observed reason. **Faulted** — browser crash
mid-scenario → failed run with partial channels preserved and typed. **Degraded** absent platform-web →
page identity degrades per its schema (digest absent, typed), and the stale-page check's reduced strength
is disclosed. **Degraded** absent delivery-evidence → results carry their own bindings, the plane's
pattern. Both runtimes drive the same runner.

### What stays out

- **No page-content instructions, no observed-content control flow** — schema-structural.
- **No heal generation, no test authoring opinions, no remote browser services.**
- **No authenticated scenarios in this cut** — the broker's arrival is the gate, stated.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Browser-running rows are disclosed not-applicable until the environment
substrate materializes the browser.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; the structural rules bite** — coordinates, fixed sleeps, observed-content parameters, secret-shaped values, receipt-less heals, and undeclared mocks are each schema-invalid. | Schema checks with negative fixtures ride CI (hard). | engine |
| **Stale pages refuse, honestly scoped** — a mismatched record-internal identity fails at CI; the served-digest residual and the absent-platform-web reduction are disclosed at the gate. | Negative fixture + disclosure inspection. | engine |
| **Action success ≠ workflow success** — the staged false-green scenario reports failure. | Fixture: staged false-green. | operator |
| **Seam staleness end-to-end** — serve build A, capture real evidence, serve build B: the old evidence reads stale against the new page identity. | Fixture: the integrated two-build walk (owned here). | operator |
| **Mock reconciliation and severed seams** — declared-vs-actual interception mismatch is a typed finding; a closed-egress severed external call reads non-real, never end-to-end. | Fixture: both staged. | operator |
| **Hostile content stays data** — instruction-shaped DOM/console content arrives quarantined; the runner takes no action from it. | Fixture: staged hostile page. | operator |
| **Auth material is stripped structurally** — staged auth cookies/headers never land in artifacts; a staged secret-bearing body is caught by the heuristic pass or disclosed within its stated ceiling. | Fixture: staged secret-bearing responses. | operator |
| **Visual ceiling holds** — a staged authenticated page yields no screenshot without the declared opt-in. | Fixture: staged auth-state page. | operator |
| **Unconfined floor holds** — an untrusted-origin scenario refuses to run unconfined; sandbox flags are observed on in the fallback. | Fixture: staged unconfined run. | operator |
