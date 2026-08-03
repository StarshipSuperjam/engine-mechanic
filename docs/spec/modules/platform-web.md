---
status: draft
---

# platform-web

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 3, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 3's build begins. Revised in draft after four cold reviews with its seam
partner [browser-evidence](browser-evidence.md); the largest changes: page identity becomes an owned
schema, the dev server binds loopback-only by default, and the composition with the environment plane is
stated as mechanics, not verbs.*

## Summary

The **optional** web platform profile: the dev server as a declared service, the build artifact as an
identified output, and — its load-bearing export — **`page-identity.v1`**, the owned schema binding
route + source revision + served-artifact identity, which [browser-evidence](browser-evidence.md)
references opaquely and asserts staleness against. It is deliberately thin glue: engineering-quality owns
the toolchain (this profile **consumes** [engineering-quality-typescript](engineering-quality-typescript.md)'s
build output and assigns identity to it — it never runs a second build), execution-environment owns the
substrate (the service declaration is **injected as an environment-manifest service**; `web_surface.py`
is a caller of the environment controller, never a lease holder), browser-evidence owns observation. The
artifact-identity digest is computed over **declared inputs** — source revision plus toolchain identity —
not raw output bytes, because web build output is not byte-stable across platforms; the residual (two
hosts can produce differing bytes under one identity) is stated, not hidden.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `platform-web` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`web-surface.v1` — the declared web product: its build-artifact identity source (the engineering-quality `build` kind's output it consumes), its dev-server service declaration (command, port, **loopback-only bind by default** — a non-loopback bind is a disclosed, explicit opt-in — environment fields that **refuse secret-shaped values** by the tool's redaction pass, and a **readiness probe** defined as an HTTP check: URL, expected status/body match, and a probe budget); **`page-identity.v1`** — the owned identity schema: route + source revision + served-artifact identity, with the digest field's absence (degraded topologies) a typed state consumers must handle); the **[tool](../systems/surfaces/tools.md)** (`web_surface.py` — start/await-ready/identify/stop; under execution-environment it *injects* the service into the run's environment manifest and calls the controller — one environment holds server and browser for a scenario run, leased to that run; without it, a plain local process, loopback-bound, disclosed); the **[operation](../systems/surfaces/operations.md)** runbook; a hard **[check](../systems/surfaces/check.md)** (schema conformance); and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` |
| `migrations` | none |

### Profile behavior

- **The dev server is a declared service, composed not improvised.** Under execution-environment the
  declaration becomes a manifest service (lease, teardown reconciliation, the works); the plain-process
  fallback is loopback-bound and disclosed in every result citing it. An occupied declared port is a
  named refusal, never a silent alternate.
- **Readiness is probed, never assumed — and consumed downstream.** "Ready" is the probe passing within
  its budget; a server failing its budget reports the probe observation, refusing a guessed "up".
  Browser-evidence consumes this readiness state: evidence taken pre-ready is typed pre-ready **on both
  sides of the seam**, and postconditions are never asserted against a pre-ready page.
- **Pages have owned identity.** `page-identity.v1` is this module's export; a page observation binds
  route + revision + served-artifact identity, so "the screenshot of the login page" is never ambiguous
  about which build served it. Where this module is absent, consumers degrade to route + revision with
  the digest field typed absent — the same schema, the reduced strength visible.
- **Artifacts are consumed, identified, and traceable.** The production artifact's identity (declared-
  inputs digest) is recorded and reproducible from the same inputs; what deploys later (wave 4) is that
  identity — one artifact identity from build to deploy, never two competing ones.

### Degraded behavior

Absent execution-environment: plain-process serving, loopback-bound, disclosed. Absent
engineering-quality-typescript: the artifact-identity source degrades to a declared local build command,
its identity carrying that provenance, disclosed. Readiness-budget failure reports the probe observation.
Both runtimes drive the same tool.

### What stays out

- **No second build, no framework opinions, no browser automation, no deployment** — consumed,
  declared, delegated, and deferred respectively.
- **No secret material in service environments** — refused by the redaction pass; the product's real
  secrets are the wave-4 broker's ground.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Declarations validate** — `web-surface.v1` and `page-identity.v1` instances conform; a secret-shaped environment value is refused; a non-loopback bind without the explicit opt-in fails validation. | Schema checks + negative fixtures ride CI (hard). | engine |
| **Readiness gates evidence, both directions** — pre-ready evidence is typed pre-ready and excluded from postconditions; a budget-exceeded server reports the probe observation, never "up". | Fixture: slow-start and never-ready servers. | operator |
| **Page identity binds and degrades honestly** — two builds served yield distinct identities; absent this module the degraded identity types its missing digest. | Fixture: two-build and degraded scenarios. | operator |
| **Artifact identity is consumed and reproducible** — the identity derives from the eq-ts build output's declared inputs, recomputably; no second build runs. | Fixture: staged build + identity recomputation. | operator |
| **Service lifecycle composes** — under execution-environment the server rides the manifest/lease/teardown; the plain-process fallback is loopback-bound and disclosed. | Fixture: both topologies. | operator |
