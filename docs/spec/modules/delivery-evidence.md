---
status: draft
---

# delivery-evidence

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design, not yet built; enters in progress and settles only by the operator's
recorded acceptance before wave 1's build begins. Revised in draft after four cold design reviews; the
largest change: freshness is **derived at read time**, never stored and swept.*

## Summary

The **required** module that makes a delivery claim **provable and perishable**: every "it works" produced
by delivery work becomes an **evidence record** with a source, a source lane, and a binding to the exact
surfaces it measured — and freshness is **computed whenever the record is read or gated**, by comparing
those bindings against the tree as it stands. There is no stored freshness flag, no sweep, and no hook to
fail open: a stale record cannot read `current` because `current` is never stored, only derived. Its second
job is **final-snapshot divergence recording**: a typed record binding the independently reviewed commit to
the submitted head, carrying the orchestrator's divergence classification and whether a re-review ran — the
record the build flow's Review prose renders from. This module records and derives; sufficiency stays with
the review gates and the operator's merge.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `delivery-evidence` |
| `distribution` | `required` |
| `applicability` | `detected` (a product producing behavioral evidence) |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`evidence-record.v1` — kind, source, **source lane** (`declared`\|`observed`\|`derived`\|`unavailable`, a schema field), an optional **producer lane** carried through from producers whose grammar distinguishes evidence tiers (engineering-quality's fast-loop vs clean-environment rides here, with its isolation receipt), and the **surface bindings**: the content digests of the files/artifacts measured, plus the deriving revision; `effect-receipt.v1` — an external effect's target, the observation source, observed result, and reconciliation state in [delivery-core](delivery-core.md)'s shared vocabulary (`confirmed`\|`partial`\|`contradicted`\|`unknown` — referenced, not redefined) — the base contract later effect-producing modules (deployment, operations) specialize; `snapshot-divergence.v1` — reviewed commit, submitted head, the orchestrator's classification, re-review disposition); the **[tools](../systems/surfaces/tools.md)** (`delivery_evidence.py` — record and freshness-read; freshness is derived on read from bindings, never written) with the **redaction pass** every record's source/result fields run through before commit (secret-shaped content is refused, not stored); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **stale-green check** — a `custom/script` CI check that re-derives freshness itself: any receipt citing an evidence record whose bound digests no longer match the tree fails, regardless of what any earlier read claimed; the **material-divergence check** — a snapshot-divergence record classified material with no recorded re-review fails; the **dangling-citation check** — a receipt citing a nonexistent evidence record fails; each carries its negative fixture per the hard-check-bite discipline); the **[operation](../systems/surfaces/operations.md)** runbook (`.engine/operations/delivery-evidence.md`); and the operator **[doc](../systems/surfaces/docs.md)** (`.engine/docs/delivery-evidence.md`) |
| `wires` | **none** — consistent with derived-on-read freshness: no mutation trigger exists to wire |
| `depends` | `core`, `delivery-core` (records attach to runs; run receipts cite evidence by opaque identity) |
| `migrations` | none |

### The evidence model

- **Typed, source-bound, lane-honest records.** A record names its kind (check result, test run,
  demonstration, observed external effect, review finding), its exact source (command, fixture, artifact
  digest), and its lane as a schema field. Lane honesty — that `observed` was genuinely observed — is not
  mechanically provable; the record therefore also names *what makes the observation independent* (the
  read-back source, distinct from the effect's actor) or takes the `declared` lane. A claimed observation
  with no named independent source is schema-invalid as `observed`.
- **Surface bindings, not builder trust.** A record binds the content digests of what it measured. For
  file-sourced evidence the binding is the file set itself. For command/test-sourced evidence the binding
  is the declared file set where an impact analysis supplies one, else **the whole deriving revision** —
  conservative, honestly noisy, and disclosed in the record. A too-narrow self-declared binding is the
  known residual risk: bindings are review-visible precisely so a reviewer can judge them, and the
  conservative default exists so narrowing is always a visible, deliberate act.
- **Freshness is derived, never stored.** `delivery_evidence.py` computes freshness at read: bindings
  matching the tree → `current`; any bound digest changed → `stale`; bindings unreadable → `unknown`. The
  stale-green CI check runs the same derivation itself at the merge gate — it trusts no prior read, no
  flag, and no session-side state. There is no sweep; there is nothing to fail open.
- **Effect receipts reconcile claims with the world.** The receipt records intended effect, observation
  source, observed state, and a reconciliation outcome; `contradicted` exists so "we observed it and it is
  wrong" is never softened into `partial` or `unknown`. Transport success with no observation is
  `unknown`, always. In wave 1 no module produces external effects, so `confirmed`/`partial`/
  `contradicted` ship as grammar with fixtures only; their first real producers arrive with deployment
  (wave 4) — stated here so the untested-in-wave-1 status is explicit.
- **Snapshot divergence is a record of a judgment, not a grader.** The orchestrator (the build flow's
  single writer) authors the record: reviewed commit, submitted head, its divergence classification, and
  whether a proportionate re-review ran. The classification is recorded judgment, never a mechanical
  semantic diff. What *is* mechanical: the material-divergence check fails a record classified material
  with no recorded re-review — so the one dangerous combination cannot ride silently. The build flow's
  Review prose renders from this record; the record is the typed source, the prose the human surface.
  This module's records serve the delivery plane's runs; the engine's own required build flow keeps its
  existing practice and may adopt the record without depending on this optional module.

### Retention and privacy

Records live in the committed evidence store under delivery-core's state home. The redaction pass refuses
secret-shaped source/result content at record time (the leak-guard posture, applied before anything is
committed). Records accrete as history; pruning or archival is a recorded maintenance decision (the
maintenance wave's ground), and erasure follows the engine's erasure grammar — named here so neither is an
afterthought. No prompts or transcripts are ever captured.

### Degraded behavior

**Faulted** — an unreadable store or unreadable bindings answer `unknown`, never `current`. Because
freshness derives at read, there is no degraded sweep state to disclose — the failure surface is the read itself, and it fails
closed. Both runtimes read the same committed store through the same tool.

### What stays out

- **No sufficiency judgment, no scoring.** Records and derivation only; gates and the operator decide.
- **No stored freshness.** A cached freshness answer is never authoritative; the check re-derives.
- **Present, not absent-by-default.** delivery-evidence ships in every Engine; it stays inactive until
  delivery work produces evidence — no burden on a project that produces none.

## Operator and automatic workflow routing

**Current disposition: `none` (design-stage).** This delivery-plane evidence draft creates no current
operator command or automatic route. Its breakout Build issue must record its chosen routing disposition
under decision 0336; no speculative route ships first.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Records validate; lanes and bindings are schema-borne** — every record conforms; `observed` without a named independent source is schema-invalid. | Schema check rides CI (hard). | engine |
| **Freshness derives correctly** — mutate a bound surface, read: `stale`; unrelated mutation with narrow bindings: `current`; unreadable bindings: `unknown`. | Fixture: all three staged; reads inspected. | operator |
| **Stale green is refused at the gate by re-derivation** — a receipt citing evidence whose bound digests no longer match fails CI even when a session-side read claimed `current`. | Fixture: the staged stale-as-current receipt; the check must catch it (negative fixture per hard-check-bite). | engine |
| **Material divergence cannot ride silently** — a snapshot-divergence record classified material with no recorded re-review fails CI. | Fixture: the staged material-no-re-review record. | engine |
| **Dangling citations fail** — a receipt citing a nonexistent evidence record fails CI. | Fixture: staged dangling citation. | engine |
| **Transport is not an outcome** — an effect receipt with no observation reads `unknown`; a contradicting observation reads `contradicted`, never `partial`. | Fixture: observation withheld; contradicting observation staged; receipts inspected. | operator |
| **Secrets never land** — a secret-shaped value in a staged record's source/result is refused at record time. | Fixture: seeded secret-shaped content; refusal inspected. | operator |
| **Conservative binding is disclosed** — a command-sourced record with no impact set binds the whole revision and says so. | Fixture: staged command record; binding inspected. | operator |
