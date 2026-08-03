---
status: draft
---

# debugger-diagnosis

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 3, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 3's build begins.*

## Summary

The **optional** module that makes runtime inspection a **hypothesis instrument, never a wandering
ground**: a debug-adapter session (Python first, through the standard debug adapter protocol) opens only
against a **stable reproduction** and a **falsifiable hypothesis**, captures only the stack and variable
facts the hypothesis names, and closes with a typed verdict — `supported`, `refuted`, or `inconclusive` —
plus the exact reproduction rerun that anchors it. Runtime observation is evidence *about a named
question*; the module refuses to be a general runtime-poking surface, because unbounded debugger access
is expensive, privacy-heavy, and produces narrative rather than proof.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `debugger-diagnosis` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`diagnosis-session.v1` — the reproduction (command + expected failing observation + content bindings), the hypothesis (a falsifiable statement naming the observations that would support or refute it), the capture plan (which frames/variables, bounded), and the verdict with its evidence; captured values ride the plane's quarantine and redaction posture); the **[tool](../systems/surfaces/tools.md)** (`debug_session.py` — drives one pinned debug adapter per profile (identity + version + digest), executes the capture plan, enforces the session budget, cleans up the debuggee); a hard **[check](../systems/surfaces/check.md)** (schema conformance — a session record without a reproduction or a falsifiable hypothesis is invalid); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` |
| `migrations` | none |

Confinement rides [execution-environment](execution-environment.md) where installed (the debuggee runs
product code — the same execution-boundary reality as engineering-quality's executing kinds, disclosed the
same way); absent it, unconfined-disclosed.

### The diagnosis model

- **Reproduction first, or no session.** The failing behavior must reproduce (command, expected
  observation, bound content digests) before a debugger attaches; a non-reproducing scenario is itself a
  typed, honest outcome — recorded, not debugged around.
- **Hypothesis-scoped capture.** The capture plan names the frames and variables the hypothesis needs;
  the tool captures those, bounded, and nothing else — no full-heap dumps, no ambient watch-everything.
  Captured values are quarantined data, redacted at capture.
- **Verdicts are anchored by reruns.** `supported`/`refuted` require the exact reproduction rerun under
  the stated conditions; `inconclusive` is the honest third state, with what was missing named. A verdict
  is evidence for the repair workflow — never itself a fix approval.
- **Session hygiene is part of the record.** The debuggee's teardown (process, ports, temp state) rides
  the session record; a session that cannot confirm cleanup says so.

### Degraded behavior

Missing/broken adapter → refusal with observed reason. Adapter capability gaps (a value it cannot
inspect) → typed `uninspectable`, never a guess. Budget exhaustion → the session closes `inconclusive`
with captures preserved. Both runtimes drive the same tool.

### What stays out

- **No hypothesis-free sessions** — schema-invalid by construction.
- **No production attachment** — this is local, reproduction-bound diagnosis; live-system observation is
  operations' later ground.
- **No auto-repair** — verdicts feed the normal change workflow.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Sessions validate** — a record without reproduction or falsifiable hypothesis is schema-invalid. | Schema check rides CI (hard; negative fixture stages the hypothesis-free session). | engine |
| **Reproduction gates attach** — a staged non-reproducing scenario yields the typed non-reproduction outcome, no debug session. | Fixture: non-reproducing scenario. | operator |
| **Capture stays in plan** — the staged session's captures contain exactly the planned frames/variables; secret-shaped values are redacted. | Fixture: seeded out-of-plan and secret values. | operator |
| **Verdicts anchor to reruns** — a `supported` verdict without its reproduction rerun is schema-invalid; the staged hypothesis resolves correctly on a known defect. | Fixture: the known-defect scenario. | operator |
| **Cleanup is honest** — a debuggee left running by an injected failure is reported as unconfirmed cleanup, never silence. | Fixture: injected cleanup failure. | operator |
