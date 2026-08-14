---
status: draft
---

# debugger-diagnosis

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 3, not yet built; enters in progress, settles by the operator's
recorded acceptance before wave 3's build begins, and — as a **security surface** (the debuggee executes
product code, and captured variables can carry live secrets) — takes the engine's full pre-settle design
review then, per decision 0334. Revised in draft after four cold reviews; the largest changes: the
capture posture is a stated deliberate deviation from the plane's refuse rule, capture is disabled by
default when unconfined, and the verdict is marked as recorded judgment.*

## Summary

The **debug-adapter profile** that makes runtime inspection a **hypothesis instrument, never a wandering
ground**: a debug-adapter session (Python first — the first profile of a family; other languages are
deferred, stated) opens only against a **stable reproduction** and a **falsifiable hypothesis**, captures
only the planned frames and variables within declared bounds, and closes with a verdict — `supported`,
`refuted`, or `inconclusive` — that is **recorded session judgment over mechanical facts**: the rerun
anchors the reproduction, the captures are the facts, and the causal step from facts to verdict is the
session's authored inference, marked as such, never a machine-proven state. Its capture posture is a
**deliberate, stated deviation** from the plane's refuse-secrets rule: a debugger must record the values
a hypothesis names, so it **masks and records** (with a redaction record and an `unclassifiable`
fail-closed state) instead of refusing — and because shape-heuristics under-cover arbitrary object
graphs, **capture is disabled by default when unconfined**: enabling unconfined capture is an explicit
per-deployment declaration, visible in every session record — presence of the module confers no
unconfined-capture authority; the machinery ships, the grant does not, until that declaration exists.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `debugger-diagnosis` |
| `distribution` | `profile` |
| `applicability` | `detected` (a debug adapter for the stack) |
| `activation` | `explicit` · `authority-gated` (unconfined capture needs an explicit per-deployment declaration) |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`diagnosis-session.v1` — the reproduction (the plane's owned reproduction grammar: command + expected failing observation + content bindings, scoped per the command-sourced binding convention), the hypothesis (statement + the named observations that would support or refute it — the schema checks presence and shape; **semantic falsifiability is the operator's read**, stated), the **bounded capture plan** (named frames/variables, depth limit, child-count limit, byte ceiling — `evaluate`-style expression execution is **unrepresentable in the plan**; passive variable reads only), and the split **session observation**: reproduced?, outcome type, cleanup state; `debug-adapter.v1` — the adapter profile/pin home: identity + version + artifact digest, the **pure-package offline-after-sync obligation** (a runtime-downloading adapter is disqualified), declared DAP capabilities — a second-language profile conforms to this contract); the **[tool](../systems/surfaces/tools.md)** (`debug_session.py` — the module's dominant build item, named honestly: a framed DAP protocol client with event dispatch and child-process lifecycle, new to this substrate; it enforces the budget — **wall-clock + capture count + byte ceiling**, wall-clock guarding hangs with external termination — and runs the module's **own capture-time masking pass**, reusing the engine's existing secret-scan machinery, writing the redaction record (that/where, never the value)); a hard **[check](../systems/surfaces/check.md)** (schema conformance — including hypothesis-shape presence, verdict-requires-rerun (`if/then`), and plan-bounds presence; negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (sessions are runs; session count is bounded by the task's attempt budget — the anti-wandering ceiling that holds even unattended) |
| `migrations` | none |

[execution-environment](execution-environment.md) confines the debuggee when installed (teardown then
defers to its receipt and residue check); [delivery-evidence](delivery-evidence.md) records verdicts in
its grammar when installed (kind `derived`, same bindings — the verdict perishes when the bound code
moves); absences degrade as stated below.

### The diagnosis model

- **Reproduction first, or no session.** A non-reproducing scenario closes typed, honestly — recorded,
  not debugged around. Repo-resident launch/debug configuration is **never honored as an execution
  source** (workspace-configuration execution disabled, the code-intelligence rule).
- **Hypothesis-scoped, bounded capture.** The plan names roots; the bounds (depth, children, bytes) cap
  reach — a captured `self` cannot become the heap. Value rendering executes product `repr` code: that is
  product-code execution, disclosed, and confined where the environment is. An `uninspectable` value that
  is hypothesis-critical forces `inconclusive` naming the gap.
- **Masked capture, honest ceiling.** Secret-shaped values mask; `unclassifiable` values mask entirely
  (fail closed); the redaction record names that and where. The heuristic's under-coverage of arbitrary
  object graphs is a named residual — one reason this module settles thorough and captures nothing
  unconfined by default.
- **Verdicts anchor and admit their nature.** `supported`/`refuted` require the exact reproduction rerun;
  the verdict field carries its recorded-judgment marking. Budget exhaustion closes `inconclusive` with
  captures preserved — those captures carry the same redaction and a no-verdict marker, so the honest
  third state cannot become a capture harvest with less scrutiny.
- **Session hygiene, honestly scoped.** Confined: teardown rides the environment's receipt. Unconfined:
  the tool confirms debuggee-process liveness by PID and reports everything else (ports, temp state, forked
  children) as **unconfirmable**, plainly.

### Degraded behavior

**Faulted** — missing/broken adapter → refusal with observed reason. **Degraded** — capability gaps →
typed `uninspectable`. **Degraded** — budget exhaustion → `inconclusive`, captures preserved under the
rules above. **Authority-disabled** — unconfined → capture disabled unless the deployment's explicit
declaration enables it, visible per session. A session's debuggee attachment is pinned to one runtime's
process; both runtimes use the same tool, never the same live session.

### What stays out

- **No hypothesis-free sessions, no expression evaluation, no production attachment, no auto-repair.**
- **No unbounded capture** — bounds are schema-required.
- **No second-language adapters in this cut** — the `debug-adapter.v1` contract is their door, later.

## Operator and automatic workflow routing

**Current disposition: `none` (design-stage).** This diagnosis draft has no current operator command or
automatic route. Its breakout Build issue must choose and record its routing disposition under decision
0336; no speculative route ships first.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Sessions validate** — reproduction and hypothesis-shape present; plan bounds present; a `supported`/`refuted` verdict without its rerun is schema-invalid; an `evaluate`-bearing plan is unrepresentable. | Schema checks with negative fixtures ride CI (hard). Semantic falsifiability stays the operator's read — stated. | engine |
| **Reproduction gates attach** — a staged non-reproducing scenario closes typed, no session. | Fixture. | operator |
| **Bounds cap reach** — a staged deep object graph captures to the declared depth/children/bytes and no further. | Fixture: staged deep graph. | operator |
| **Masking holds, unclassifiable fails closed** — seeded secret-shaped and unclassifiable values mask; the redaction record names that/where, never values. | Fixture: seeded values. | operator |
| **Unconfined default is off** — without the explicit declaration, an unconfined session refuses capture; with it, the declaration is visible in the record. | Fixture: both postures. | operator |
| **Verdict is judgment over anchored facts** — the staged known-defect hypothesis resolves with its rerun; the verdict carries the recorded-judgment marking; the budget-exhausted path yields `inconclusive` with marked captures. | Fixture: staged defect + exhaustion (determinism of the injected-failure fixture confirmed at build). | operator |
| **Cleanup honesty by posture** — confined teardown rides the environment receipt; unconfined reports PID-liveness plus unconfirmable remainder. | Fixture: both postures. | operator |
