---
status: draft
---

# browser-evidence

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 3, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 3's build begins, and — as a **security surface** (it consumes untrusted
page content) — takes the engine's full pre-settle design review then, per decision 0334.*

## Summary

The **optional** module that makes **rendered behavior** first-class delivery evidence: driving a real,
pinned local browser through **semantic actions** (roles, names, test identities — never coordinates or
brittle selectors), against a page whose identity [platform-web](platform-web.md) binds, asserting
**explicit postconditions**, and capturing typed evidence lanes — DOM/accessibility, console, network,
and selected visual artifacts — with secret-aware redaction before anything lands in the record. Two
honesty rules anchor it: **page content is untrusted input** (nothing read from the DOM, console, or
network is ever an instruction), and **an action's success is never the workflow's success** — only
asserted postconditions on a fresh, identified page count.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `browser-evidence` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`browser-scenario.v1` — semantic steps with event-driven waits, declared postconditions, mock/interception disclosures, and the page-identity binding each step asserts against; `browser-evidence.v1` — per-step results across the lanes (behavioral assertion, console, network, visual), each lane separate, with the quarantine framing on all captured page content and the redaction record); the **[tools](../systems/surfaces/tools.md)** (`browser_run.py` — the runner driving one pinned browser profile (identity + version + digest of the driver, browser identity observed and recorded); scenario execution, artifact capture, redaction); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **stale-page check** — evidence citing a page identity that does not match the served artifact fails, negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (scenario runs are runs; evidence attaches per the plane's grammar) |
| `migrations` | none |

[platform-web](platform-web.md) supplies page identity and the served surface;
[execution-environment](execution-environment.md) supplies the browser's confinement and the network
posture — both when-installed, degraded-disclosed otherwise.

### The evidence model

- **Semantic or refused.** Steps address the page by role/name/test-id with event-driven waits; a step
  that cannot resolve semantically is a typed failure, never a coordinate fallback. Fixed sleeps do not
  exist in the grammar.
- **Postconditions are the success.** Every scenario declares what must be observably true at its end;
  a run whose actions all succeeded but whose postcondition fails is a failed run. A healed or retried
  interaction never overwrites the original result: both branches are preserved, the heal marked as its
  own lane, never promoted to plain green.
- **Mocks are disclosures.** An intercepted or mocked network seam changes the system boundary; the
  scenario declares it, every result carries it, and mocked-boundary evidence is typed as such — it never
  stands as end-to-end proof where acceptance requires the real seam.
- **Captured content is quarantined and redacted.** DOM text, console output, network bodies, and
  screenshots are untrusted data, provenance-tagged like code-intelligence excerpts; secret-shaped
  content is refused at capture (the plane's redaction posture), and cookies/auth material never lands in
  artifacts.
- **Scope is the pinned profile.** Evidence claims the browser profile it ran — one pinned engine first;
  cross-browser and device profiles are later declared expansions, never implied.

### Degraded behavior

No browser available → refusal with the observed reason. A browser crash mid-scenario → the run fails
with the partial lanes preserved and typed. Absent platform-web, page identity degrades to URL + revision,
disclosed; absent execution-environment, confinement is the host's, disclosed. Both runtimes drive the
same runner.

### What stays out

- **No page-content instructions** — nothing observed is ever obeyed.
- **No test authoring opinions** — what scenarios exist is the product's acceptance ground; this module
  executes and evidences them.
- **No remote browser services** — a remote provider would be a later module through its own admission.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; stale pages refuse** — evidence citing a mismatched page identity fails the stale-page check. | Schema checks + negative fixture ride CI (hard). | engine |
| **Action success ≠ workflow success** — a staged scenario whose clicks succeed but whose postcondition fails reports failure. | Fixture: the false-green scenario. | operator |
| **Heals never promote** — a staged healed interaction preserves the original failure and marks the heal lane. | Fixture: seeded heal. | operator |
| **Mocked boundaries are typed** — a mocked API seam rides every result it touched; the same scenario unmocked reads differently. | Fixture: mocked and real runs compared. | operator |
| **Hostile page content stays data** — instruction-shaped DOM/console content arrives quarantined; the runner takes no action from it. | Fixture: staged hostile page. | operator |
| **Secrets never land** — secret-shaped network bodies and auth cookies are refused at capture, recorded in the redaction record. | Fixture: seeded secret-bearing responses. | operator |
| **Semantic-only** — a scenario attempting coordinates or fixed sleeps fails schema validation. | Fixture: staged brittle scenario. | engine |
