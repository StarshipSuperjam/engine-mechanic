---
status: draft
---

# platform-web

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 3, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 3's build begins.*

## Summary

The **optional** web platform profile: what "run this web product locally and observe it" means as declared,
typed machinery — the development server as a managed environment service, the build artifact as an
identified output, and the page as an addressable surface [browser-evidence](browser-evidence.md) can act
on. It is deliberately thin: engineering-quality owns the toolchain, execution-environment owns the
substrate, browser-evidence owns the observation — this profile owns the **web-shaped glue**: server
lifecycle, readiness, base URLs, artifact identity, and the conventions that make a web product's rendered
surface reachable and identifiable for evidence.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `platform-web` |
| `status` | `optional` |
| `provides` | the **[schema](../systems/surfaces/schemas.md)** (`web-surface.v1` — the declared web product: how it builds (artifact identity by digest), how it serves locally (the dev-server command as an environment service declaration, its port, its readiness probe, its base URL), and the page-identity convention — route plus revision plus served-artifact digest — that browser evidence binds to); the **[tool](../systems/surfaces/tools.md)** (`web_surface.py` — start/await-ready/identify/stop through execution-environment's service machinery where installed, plain local process otherwise, disclosed); the **[operation](../systems/surfaces/operations.md)** runbook; a hard **[check](../systems/surfaces/check.md)** (schema conformance); and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` |
| `migrations` | none |

### Profile behavior

- **The dev server is a declared service.** Its command, port, environment, and readiness probe are
  `web-surface.v1` fields; under execution-environment it runs as a manifest service with the lease and
  teardown reconciliation that implies; without it, a plain local process whose looser containment is
  disclosed in every result that cites it.
- **Readiness is probed, never assumed.** "The server started" is process state; "the surface is ready" is
  the probe passing. Evidence taken before readiness is typed as such and does not count against
  postconditions.
- **Pages have identity.** A page observation binds route + source revision + served-artifact digest, so
  "the screenshot of the login page" is never ambiguous about which build of which revision served it —
  the binding browser-evidence requires to refuse stale-page claims.
- **Artifacts are identified outputs.** The production build's output is digest-identified; what deploys
  later (wave 4) is that identity, so build-to-deploy traceability starts here.

### Degraded behavior

Absent execution-environment: plain-process serving, disclosed. A server that fails readiness within its
declared budget reports the probe's observation, never a guessed "up". A port conflict is a named refusal.
Both runtimes drive the same tool.

### What stays out

- **No framework opinions, no scaffolding** — the product's stack is its own; this profile declares how to
  run and identify it, not how to write it.
- **No browser automation** — acting on the surface is browser-evidence's ground.
- **No deployment** — wave 4's.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Declarations validate** — a `web-surface.v1` instance conforms; artifact and page identities are digest-bound. | Schema check rides CI (hard). | engine |
| **Readiness gates evidence** — evidence cited against a pre-ready surface is typed pre-ready; the probe's pass is what flips it. | Fixture: slow-start server; evidence states inspected. | operator |
| **Page identity binds** — an observation of a staged page carries route + revision + served digest; serving a different build changes the identity. | Fixture: two builds served; identities compared. | operator |
| **Service lifecycle reconciles** — under execution-environment, server start/stop rides the lease and appears in the teardown receipt; without it, the disclosure is present. | Fixture: both configurations. | operator |
| **Port conflict refuses loudly** — an occupied declared port is a named refusal, never a silent alternate port. | Fixture: seeded conflict. | operator |
