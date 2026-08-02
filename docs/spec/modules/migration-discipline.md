---
status: draft
---

# migration-discipline

*Reconciled with engine-template@`cdbbc33` as built (2026-08-02) — AI-compared and operator-ruled under [decision 0320](../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with the check's single-assertion scope adopted by [decision 0329](../../adr/0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md); ratified as intended design on 2026-05-30 by [decision 0142](../../adr/0142-lock-migration-discipline-product-migration-governance-the-s.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees. Until the [product spec index](../../spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

## Summary

The **optional** Software Configuration Management module that governs the **product's own data/schema
migrations** — the operator's application schema changes (Rails/ActiveRecord, Django/Alembic, Prisma,
Flyway, Liquibase, golang-migrate, raw SQL). It ships a standing discipline bar, recognition guidance that
routes a destructive or irreversible product migration into the engine's escalation channel, and one soft
hygiene check, kept (not cut) at [D-068](../../adr/0068-q1-resolved-the-v1-optional-module-roster-4-cut-2-kept.md) as "data/schema change governance; no
overlap." The *laws* it relies on live in the locked
[policies](../systems/surfaces/policies.md) (the always-present Escalation policy),
[check](../systems/surfaces/check.md), and [validation](../systems/guardrails/validation.md)
system docs; **this module is the content** — a policy instance plus its own soft domain check.

It `depends: core` on the **target axis**: this module's check inspects the operator's **product**
migration artifacts and presupposes **no** engine-self-validation corpus, so it needs only `core`'s check
engine — the kind dispatcher plus the read-only `custom/script` (or a presence-discovered conforming) kind
— never the self-validation rule corpus [validators-core](validators-core.md) consolidates. It is
a **standalone** optional capability that fills no [Slot](../../reference/glossary.md) ([D-069](../../adr/0069-core-module-seam-walk-the-demarcation-operationalized-glossa.md)).

## Behavior

### The product/engine migration boundary

The word "migration" is overloaded, so the boundary is stated plainly: the engine's own migration
machinery is **one mechanism** — the manifest `migrations` field, applied to the engine's own state on
upgrade — and **this module is none of it**. That mechanism surfaces as provisioning's engine-upgrade
migrations and backup-first reversal ([provisioning](../systems/infrastructure/provisioning.md)),
the [memory](../systems/cognitive/memory.md) ledger's owned migration unit, and the engine's
**own surface-schema** version-pinning ([schemas](../systems/surfaces/schemas.md)). All of it
operates on engine-owned config and gitignored stores.

This module governs the **product's** migrations instead. The collision is **terminological, not
mechanical**: the engine's `migrations` field and the product's own migration tooling share no code path,
no file, and no seam. The module **never runs a product migration** — that is the product's own
runtime/deploy pipeline; it performs **read-only inspection** of migration artifacts in pull requests and
routes a finding, never editing product source ("no seam edits product source"; the
[§13](../../principles.md) wall). The ecosystem names above are examples, not a closed set.

### Manifest shape

| Field | Value |
|---|---|
| `id` | `migration-discipline` |
| `status` | `optional` |
| `provides` | a **migration-discipline [policy](../systems/surfaces/policies.md)** (the standing bar — review-before-apply, reversibility / expand-contract, backup-before-destructive; the policy's own enforcement tier is **posture**) whose stop-and-ask commitment realizes the locked, always-present Escalation policy's standing irreversibility trigger for product-schema migrations (the built policy states that posture in its own plain words rather than naming the Escalation record); a **`soft` ecosystem-detected presence [check](../systems/surfaces/check.md) rule** with **one assertion** — *a migration carries a rollback where the framework has the concept* — declaring the `CI`/`pre-commit`/`pre-close` suites; and the **read-only detection logic** it invokes (a `custom/script` tool reading only file and directory names). The check **deliberately does not** assert that a schema-changing PR carries a migration at all — its own message and the policy both disclaim that half, leaving it to pull-request review and the standing posture (the single-assertion scope adopted by [decision 0329](../../adr/0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md), resolving this document's earlier internal contradiction in its own Enforcement section's favor). Remaining `params` and `message` text are build-spec leaves ([§2](../../principles.md)). |
| `wires` | **none** |
| `depends` | `core` |
| `migrations` | none — the manifest field is the engine's own-state upgrade mechanism, and this module owns no engine store to migrate; this is distinct from the *product* migrations it governs |

### Wiring nothing — active by presence

`wires: none`. The policy is read as the already-catalogued [policies](../systems/surfaces/policies.md)
surface (no `ontology-entry` wire); the presence check self-declares its `suites` and the roster is
**derived** ([§14](../../principles.md)), so it **joins the `CI` suite by self-declaration — riding the
single ruleset-bound PR-validation check with no new ruleset binding**. The **escalation routing is not
wiring either**: the Escalation policy is locked and **always present** (one of the v1-core policies),
so this module **relays into** it ([§16](../../principles.md)) and registers or edits nothing. The
read-only detection needs no `permission`. Nothing touches `hook`/`mcp`/`permission`/`gitignore`. Install
is a file drop, uninstall a file removal — the discovery-side half of the [R5](../../reference/risks.md) containment
story.

### Enforcement — honest tiers

A check is `hard` or `soft`, and CI is the only gate ([validation](../systems/guardrails/validation.md),
[§6](../../principles.md)/[§7](../../principles.md)). What this module can honestly enforce is bounded by a
hard fact: **migration *safety* — reversible? destructive? lock-heavy? backward-compatible? — is not
mechanically decidable across ecosystems.** There is no "migration-safety database" to relay the way
dependency-discipline relays GitHub's vulnerability data. So the tiers are named honestly:

- **The discipline bar — posture.** The policy states the standing expectations (review-before-apply,
  reversibility / expand-contract, backup-before-destructive) as guidance the builder follows; it is
  backstopped by human review, not mechanically enforced.
- **Destructive / irreversible product migration → escalation — the primary mechanism, posture-grade, not
  mechanical teeth.** The locked Escalation policy **already** escalates "irreversibility or external blast
  radius" with or without this module; this module's policy is **domain recognition guidance** that helps
  the builder catch a destructive product migration as an instance of that standing trigger. When it fires,
  it follows the policy: **interactive stops and asks; routine halts and routes a tracked finding
  re-surfaced at the next boot.** It is **judgment-triggered — there is no mechanical destructiveness
  detector** — so its hard backstops are the locked policy's own: the lock fingerprint, the protected-branch
  merge gate, and the close-ritual disposition gate. It is the module's primary mechanism, but it is honest
  posture backed by the human gate, not a mechanical wall.
- **The presence check — `soft`.** A hygiene nudge (CI + local), never blocking; **presence-only — it does
  not detect destructiveness, and it never checks whether a schema change has a migration at all** (the
  adopted single-assertion scope above). It is ecosystem-detected (by directory convention and file names
  — it never reads SQL) and resolves the rollback nudge along the built branches: separate up/down
  conventions get the present-or-soft-warn pair; Flyway gets per-version undo pairing; a **forward-only
  framework** (Supabase, Prisma, Flyway/Liquibase without the undo tier) is a **disclosed not-applicable**
  — with hand-written rollback files winning over the framework name where both appear; an **in-file
  rollback framework** (Rails, Django, Alembic — the rollback lives inside the migration file) is likewise
  a disclosed not-applicable that never warns; a migrations directory it detects but cannot classify gets
  its own honest disclosure; and when no migration framework is present at all it is a **disclosed no-op**,
  framed *not yet applicable — it activates when the project adds migrations*, never a silent pass.

### Operator trust — a non-engineer cannot judge migration safety

The operator is a non-engineer who cannot evaluate whether a migration is safe, so escalation must hand
them enough to decide, not a bare menu (wording deferred to build, each relayed to an existing seam):

- A destructive-migration escalation surfaces, in plain language, **what the migration does, the concrete
  data-loss / irreversibility risk, the options, a recommendation, and at least one concrete reversible or
  safer path the engine offers to take** (expand-contract, backup-first, additive-then-cutover where the
  framework supports it). Handing a non-engineer only "here are the options" abandons them on the decision
  this module exists to protect.
- The decision is the operator's, surfaced once the change is **described well enough to judge** (not a
  blank "I am about to do something destructive — proceed?"), and the operator **can approve it** — it is a
  stop-and-ask, never a veto, so a destructive change they genuinely want is never permanently walled off.
- In **routine** mode the halt emits a plain-language finding stating it stopped *because* a destructive
  migration needs a human, what the migration would do, and the recommended safe path — surfaced at the
  next boot via the finding-disposition / attention channel, never buried as an issue to hunt for. The
  routine path gives the operator no less than the interactive one.
- **Setup-time disclosure:** because this package pauses an in-progress build to ask and halts an
  unattended routine before destructive schema changes, the provisioning selection-UX states that plainly,
  so opting in is informed consent.
- All operator-facing text explains domain terms (migration, schema, rollback, expand-contract) per the
  check `message` standard — "explain, never dumb down" — including the not-applicable / no-op disclosures.

### No overlap with the review lenses

Dependency on migrations is also touched at the review gates, but the layers are distinct (the
[D-068](../../adr/0068-q1-resolved-the-v1-optional-module-roster-4-cut-2-kept.md) no-overlap bar): the [design-review](design-review.md)
`feasibility` lens names "migration" explicitly, and [qa-review](qa-review.md)'s
`spec-conformance` / `technical-integrity` lenses judge migration *outcomes* (data correctness) without a
migration-named lens. Those are **cold-context judgment at the plan and pre-submission gates** —
point-in-time, risk-proportionate, operator-gated. **This module is the standing discipline** — the
always-on policy bar, the continuous destructive-migration recognition and escalation shaping, and the
per-PR presence nudge — applying continuously, independent of whether a review lens is installed or runs.
Standing discipline versus gate-judgment: different layers, no duplication.

### The contributor wall holds

The module inspects and routes on the **product's own** migration artifacts, which respects the
[engine/product wall](../systems/infrastructure/repository-topology.md) and the
[contributor-not-component](../../principles.md) principle: it is **optional**, so opting in is **consent,
not imposed coupling** (§13); it is **read-only** (it inspects migration code in pull requests and
escalates — it never runs a product migration or edits product source); and the **removal test passes and
is in fact strengthened** — because the core Escalation policy already escalates irreversibility, removing
this module leaves destructive product migrations *still escalating*, losing only the standing bar, the
recognition guidance, the recommendation/safe-path shaping, and the hygiene check. The dependency arrow
stays Engine→product.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The laws are the policies/check/validation systems'; the delivery is this module** — no restating laws. | Operator observation: the manifest provides only a policy instance, one check rule, and its read-only script — each citing the system laws rather than restating tier/gate/escalation text. No check asserts this. | operator |
| **Governs the product's migrations, not the engine's** — the engine's own `migrations` mechanism stays the engine's; the boundary is terminological, not mechanical; the module never runs a product migration. | Operator observation: the check targets the product-migrations context, its script prunes the engine's own corner and reads only names — the module's demo proves an engine-side migrations file is walled out. Partial support: the migration-rollback check itself proves the wall and read-only floor when it runs; the never-runs-a-migration claim is the script's read-only construction, your read. | operator |
| **Escalation is posture-grade, not mechanical teeth** — migration safety is not decidable across ecosystems, so a destructive product migration is routed to a human decision (the core policy already escalates irreversibility); this module shapes that escalation to carry a recommendation and a safe path. | Operator observation: the policy's own enforcement-tier section says there is no mechanical detector, and the check's message explicitly does not judge destructiveness. No check covers this — which is the criterion's own point. | operator |
| **Honest tiers** — the bar and the escalation are posture (human-gated), the presence check is `soft`; nothing is dressed as enforced ([§7](../../principles.md)). | Operator observation: the check declares `tier: soft` and its script asserts no finding is ever hard, so it never blocks even in CI's blocking context; the posture legs are the policy's own words. Partial support: the check's declared tier carries the soft sub-claim; the full multi-leg claim is your read. | operator |
| **Wires nothing** — policy and check bind by presence; the escalation relays into an always-present locked policy; `depends` ≠ wiring. | Operator observation: the manifest carries `wires: []`, and the policy and check are file-drop artifacts discovered by presence. Partial support: module-manifest (hard, CI) validates the manifest grammar without asserting the wires list is empty. | operator |
| **`depends: core`, deliberately** — the check inspects product artifacts and presupposes no engine-self-validation corpus, so `core`'s engine suffices. | Operator observation: the manifest's depends carries `core` alone and the check's kind is the read-only script core's dispatcher owns. No check asserts the dependency's rationale. | operator |
| **Optional means consent, and the operator is never stranded** — opt-in is disclosed, escalations carry a recommendation and a safe path, and read-only inspection keeps the §13 wall intact. | Operator observation: the manifest declares `status: optional`, the script reads names only, and the policy's rationale commits every escalation to a plain-language account plus a safer path. No mechanical check; verify by reading the policy and manifest. | operator |
