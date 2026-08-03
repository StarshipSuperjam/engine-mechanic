---
status: draft
---

# code-intelligence-core

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design, not yet built; enters in progress and settles only by the operator's
recorded acceptance before wave 1's build begins. Revised in draft after four cold design reviews; the
largest changes: excerpt quarantine, adapter integrity requirements, per-mode results with no cross-mode
rank, and file-digest freshness aligned with the plane's derived-on-read model.*

## Summary

The **optional** module that lets a deployed engine **understand the product's code before changing it**:
finding where a behavior lives (localization), what a symbol touches and what touches it (impact), every
claim bound to the content it was read from. It is a **contract over replaceable adapters** — one pinned
language-server adapter (Python first) plus lexical, syntax-tree, and history evidence — producing a
**localization dossier**: per-mode lists of falsifiable leads with the queries and exclusions that produced
them. **There is no cross-mode ranking and no verdict**: modes corroborate visibly, and adjudication belongs
to the consumer and ultimately the human. Everything the dossier quotes from the repository is **untrusted
data, quarantined as such** — provenance-tagged excerpts, never instructions to whatever reads them.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `code-intelligence-core` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`localization-dossier.v1` — per-mode lead lists with corroboration markers, queries run, exclusions, the per-mode attempt record (`ran`\|`timed-out`\|`unsupported`\|`degraded` — an absent lead is never silent), the quarantine framing for every quoted excerpt, and the content-digest bindings of files referenced and searched; `impact-set.v1` — **input: a plain seed set of files/symbols/spans** (never structured-change's candidate grammar — no dependency cycle; the consumer derives seeds and calls), output: affected symbols/files with per-item derivation lane (`lexical`\|`symbol`\|`structure`\|`history`); `orient` emits a dossier with no query — the repository-shape summary, same schema; and `structure-walk` — the **enumeration surface**: a whole-repository node/edge stream (files, symbols, references) within the adapter's declared capabilities, bounded and resumable, the bulk-extraction feed [product-knowledge-graph](product-knowledge-graph.md) later persists — per-symbol query fan-out is not a substitute and is disqualified as its build path); the **adapter contract [schema](../systems/surfaces/schemas.md)** (`code-intel-adapter.v1` — declared capabilities, all optional and disclosed; integrity requirements below); the **[tools](../systems/surfaces/tools.md)** (`code_intel.py` — orient/localize/impact/structure-walk; the adapter host); hard **[checks](../systems/surfaces/check.md)** (dossier **and impact-set** schema conformance — the boundary-crossing artifact is machine-gated); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (dossiers attach to runs) |
| `migrations` | none |

### The intelligence model

- **Bound to content, or refused.** Every dossier and impact set binds the content digests of the files its
  leads reference and the files searched — working-state content, uncommitted included, so a dirty tree is
  identified by what it actually held. Staleness is **per-binding**: a changed bound file stales the leads
  bound to it, not the whole dossier; freshness derives at read from the bindings, the plane's one model
  ([delivery-evidence](delivery-evidence.md) — where installed, a dossier is recorded in its grammar, kind
  `derived`, same bindings; absent it, the dossier carries the identical fields itself). The freshness key
  includes the per-mode attempt record, so an incomplete-index derivation can never masquerade as a
  complete one at the same content.
- **Modes stay separate; corroboration is visible; nobody sums.** Each evidence mode returns its own
  ordered list; corroboration markers show where modes agree. No cross-mode score exists. The seeded-
  misdirection fixture's success is *both* leads present with their modes and the corroboration visible —
  never "the right answer ranked first," which would smuggle in the adjudication this module refuses.
- **Excerpts are quarantined data.** Every quoted string — code, comments, commit messages, symbol names —
  is provenance-tagged and delimited as untrusted repository content. A consumer reads dossiers knowing
  excerpts are data; the acceptance fixtures stage hostile content (an instruction-shaped comment and
  commit message) and require it to arrive quarantined, never as bare prose a session could obey. On
  un-owned upstream checkouts (the external-contribution path) the posture tightens: quarantine plus no
  workspace-configuration execution, stated.
- **Adapters are integrity-bound executables.** The pinned adapter must be a pure-package distribution
  installable offline after sync into the engine's runtime (a runtime-downloading distribution is
  disqualified by the engine's substrate contract); pinned by identity, version, **and artifact digest**;
  routed through dependency review like any executable dependency; run as a subprocess with
  workspace-configuration execution disabled. The exact tool is a build-entry recorded decision inside
  these constraints. The product's installed dependency closure is not visible from the engine's runtime —
  cross-library resolution is typed `partial`, disclosed; pointing the adapter at the product's own
  environment is a per-deployment option, recorded when taken.
- **Contract and first adapter ship together, deliberately.** Unlike the engineering-quality split, the
  adapter contract stays in this module for wave 1: its second consumer
  ([product-knowledge-graph](product-knowledge-graph.md)) is waves away, and the contract gets its first
  cross-language stress at wave 3 — a **recorded revisit trigger**: when the TypeScript-stack work arrives,
  the fused shape is re-judged and split then if the contract needs an independent home.
- **Cost has a boundary.** Derivation is per-run over a disposable, gitignored, digest-keyed cache —
  rebuildable, never authoritative, never committed ("no persistent index" means no authoritative store; a
  disposable cache is how per-run derivation stays affordable). Each subcommand carries a declared budget;
  exceeding it degrades to lexical/history modes, typed as such. The acceptance fixture pins a budget
  against a repository of the engine's own size.

### Adjacent surfaces it must not absorb

code-notes remain review-owned prose — a comment is never authority here. The engine's knowledge graph maps
engine surfaces. The derived *product* structural map is product-knowledge-graph's later ground, fed by
these adapters, not duplicated here.

### Degraded behavior

No adapter → lexical/history-only, disclosed. Crash, timeout, or unsupported language → typed per-mode
attempt states, disclosed, never silent absence. **The local-only posture is stated honestly**: no network
egress by design (local subprocess, offline-installable adapter, no upload of source anywhere); the egress
fixture demonstrates it on staged runs — an existence demonstration, with the enforced boundary being the
adapter constraints above, not the fixture.

### What stays out

- **No authoritative index or graph store**; the cache is disposable and gitignored.
- **No correctness verdicts, no cross-mode rank** — locating, never certifying.
- **No repository content leaves the machine** by design, as bounded above.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Dossiers and impact sets validate** — schema conformance including per-mode attempt records, quarantine framing, bindings, and derivation lanes. | Schema checks ride CI (hard). | engine |
| **Per-binding staleness** — a changed bound file stales its leads; an unrelated change leaves narrow-bound leads current; incomplete-index derivations never read complete. | Fixture: all three staged; reads inspected. | operator |
| **Misdirection is exposed, not adjudicated** — the seeded wrong-file lexical lead and the right-file symbol lead both appear, mode-tagged, corroboration visible. | Fixture: seeded misdirection; dossier inspected. | operator |
| **Hostile content arrives quarantined** — instruction-shaped comment and commit-message content appears only as delimited, provenance-tagged excerpts. | Fixture: staged hostile content; dossier inspected. | operator |
| **Impact fidelity** — on a staged change with a known touch-set, the impact set includes the direct callers; a gross omission fails the fixture. | Fixture: known-touch-set scenario. | operator |
| **Adapter integrity holds** — a digest-mismatched adapter is refused; the Python adapter provides the definition/reference/symbol capabilities the localization fixtures rely on. | Fixture: mismatched digest; capability probe. | operator |
| **Budget degrades honestly** — an over-budget derivation on the sized fixture repo degrades to lexical/history, typed. | Fixture: budget exceeded; dossier inspected. | operator |
| **No egress on staged runs** — orient/localize/impact under egress observation make no outbound call. (Existence demonstration; the boundary is the adapter constraints.) | Fixture: egress-observed runs. | operator |
