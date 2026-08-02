---
status: draft
---

# dependency-discipline

*Reconciled with engine-template@`cdbbc33` as built (2026-08-02) — AI-compared and operator-ruled under [decision 0320](../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with the workflow-Actions license carve-out adopted by [decision 0329](../../adr/0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md); ratified as intended design on 2026-05-30 by [decision 0150](../../adr/0150-lock-dependency-discipline-the-dependency-governance-discipl.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees. Until the [product spec index](../../spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

## Summary

The **optional** Software Configuration Management module that ships **domain dependency governance** —
version **pinning**, a dependency-change **review gate**, and update-**cadence** posture — *beyond* the
control-plane Dependabot floor ([D-067](../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md), [D-068](../../adr/0068-q1-resolved-the-v1-optional-module-roster-4-cut-2-kept.md)). The
*laws* it relies on live in the locked [check](../systems/surfaces/check.md),
[validation](../systems/guardrails/validation.md), and [policies](../systems/surfaces/policies.md)
system docs; **this module is the content** — a policy instance plus its own domain check rules, exactly
as [validators-core](validators-core.md) is "the corpus" over `core`'s validation engine. It
`depends: core` — like its sibling [migration-discipline](migration-discipline.md) — on the
**target axis**: its checks inspect the operator's **product** dependency manifests and presuppose **no**
engine-self-validation corpus, so they need only `core`'s check engine (the kind dispatcher plus the
read-only `custom/script` or a presence-discovered conforming kind), never the engine-self-validation rule
corpus [validators-core](validators-core.md) consolidates. It is a **standalone** optional capability
that fills no [Slot](../../reference/glossary.md) ([D-069](../../adr/0069-core-module-seam-walk-the-demarcation-operationalized-glossa.md)).

## Behavior

### Scope boundary and the no-overlap axis

- **The security floor is not this module's.** The committed secret-scan workflow + `dependabot.yml`
  that protect any repo regardless of plan are the [control-plane](../systems/infrastructure/control-plane.md)'s
  floor. This module owns dependency *discipline* on top of it.
- **Cadence is posture, by construction.** Update cadence as a *mechanism* is `dependabot.yml`'s
  schedule — a control-plane infrastructure artifact outside the [ontology](../systems/grammar/ontology.md),
  and the closed seam vocabulary has **no directive that can edit it**
  ([module-system](../systems/grammar/module-system.md)). So this module **neither owns nor
  edits `dependabot.yml`**: cadence lives only as posture in its policy, while its checkable teeth are
  pinning and the review gate. The control-plane owns the file; this module relays ([§16](../../principles.md)).
- **No overlap with the review lenses.** Three layers govern dependency safety without duplicating one
  another ([D-068](../../adr/0068-q1-resolved-the-v1-optional-module-roster-4-cut-2-kept.md)'s no-overlap bar): the **control-plane floor** is the always-on
  mechanical baseline; **this module** is the mechanical *discipline* — a PR-time gate on dependency
  *changes* plus pinning hygiene; the [design-review](design-review.md) `risk-governance` and
  [qa-review](qa-review.md) `security-governance` / `technical-integrity` lenses are
  cold-context *judgment* at the plan and pre-submission gates. Floor, mechanism, judgment — different
  layers.

### Manifest shape

| Field | Value |
|---|---|
| `id` | `dependency-discipline` |
| `status` | `optional` |
| `provides` | a **dependency-discipline [policy](../systems/surfaces/policies.md)** (the standing pinning/cadence/review-gate bar; the policy's own enforcement tier is **posture**); the **review-gate [check](../systems/surfaces/check.md) rule** (`tier: hard`, declaring the `CI`/`pre-commit`/`pre-close` suites), which relays GitHub's native dependency-review comparison; the **pinning check rule** (`tier: soft`, ecosystem-detected, a disclosed no-op when no pinnable manifest is present); and the **read-only detection logic** those checks invoke. Named by what it governs — the concrete files, the kind realization (a presence-discovered conforming check-kind or the `custom/script` read-only escape-hatch), `params`, and `message` text are build-spec leaves ([§2](../../principles.md)). |
| `wires` | **none** |
| `depends` | `core` |
| `migrations` | none |

### Wiring nothing — active by presence

`dependency-discipline` `wires` **none**, the same clean seam discipline as its peers. The policy is read
as the policy surface (already catalogued by the [ontology](../systems/grammar/ontology.md), so
no `ontology-entry` wire); each check rule's `suites` field self-declares its membership and the suite
roster is **derived** ([§14](../../principles.md)), so the review-gate and pinning checks **join the `CI`
suite by self-declaration — riding the single ruleset-bound PR-validation check with no new ruleset
binding and no wiring**. Nothing needs a `hook`, `mcp`, `permission`, or `gitignore` entry. Install is a
file drop, uninstall a file removal — the discovery-side half of the [R5](../../reference/risks.md) containment story.

### Enforcement — honest tiers

A check is `hard` or `soft`; whether a `hard` tier *blocks* is the suite's context, and **CI is the only
gate** ([validation](../systems/guardrails/validation.md), [§6](../../principles.md)). The
local `pre-commit`/`pre-close` runs are nudges, never a local wall.

- **Review gate — `hard` at CI.** A pull request that introduces a vulnerable or license-incompatible
  dependency fails the required check and blocks the merge. The license leg's built rule structure: an
  **unidentifiable license blocks on any repo** (the gate cannot vouch for what it cannot read); a
  **copyleft license blocks only on a private/internal repo**, where linking obligations bite — on a
  **public** repo the same finding is a **non-blocking heads-up**, since the code is already public. One
  deliberate ecosystem carve-out, adopted by
  [decision 0329](../../adr/0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md):
  **workflow-declared GitHub Actions skip the license leg entirely** — GitHub reports no license data for
  the Actions ecosystem, so blocking on an unidentifiable Actions license would block every action; the
  **vulnerability leg still applies to actions in full**. Its teeth are **conditional on the platform
  exposing the dependency-review data**: full teeth where it is available — **public repos (free)** and
  **private repos only with the paid GitHub Code Security add-on** (part of GitHub Advanced Security,
  billed per active committer — a real recurring cost on the order of $30/committer per month, included
  on Enterprise; **not** a free settings toggle); where it is **not** available (a private repo without
  that paid add-on — the same disclosed branch also absorbs any comparison the API refuses, a fork's
  denied compare included) the rule is a **disclosed no-op** — it states, in plain language, that the gate
  is unavailable on this tier, what is and is not protected, and that unlocking it means **purchasing** the
  paid add-on (a cost/benefit choice, the exact current price named in the operator disclosure), and
  proceeds. It is **never a silent
  green**, and it never fails closed in a way that strands the operator off their own repo. Unlike the
  control-plane secret-scan floor, dependency review has **no git-native fallback** — there is no "floor
  that travels," only full teeth or a disclosed absence.
- **Pinning — `soft`-warn.** A hygiene nudge in CI and locally; never blocks. It is **ecosystem-detected
  by manifest presence**, and when no pinnable manifest exists (a fresh repo) it is a **disclosed no-op**
  framed as *not yet applicable — it activates when the project adds dependencies*, distinct from "could
  not run," and never a silent pass.
- **Cadence — posture only.** Stated in the policy; the update mechanism stays the control-plane floor.
- **The policy itself is posture** — a standing directive whose prose states the three per-directive
  expectations; the teeth are the checks above, not the policy ([§7](../../principles.md): posture is not
  dressed as enforced).

### Operator trust — the gate must never strand a non-engineer

The operator is a non-engineer who cannot themselves judge whether a dependency is vulnerable, so a
firing hard gate carries binding obligations (the wording and mechanism are build-spec leaves; each
relays to an existing seam rather than re-owning it):

- A hard-gate failure surfaces a **plain-language next step plus the AI-remediation offer** — through the
  [check](../systems/surfaces/check.md) `message` standard ("explain, never dumb down") and the
  finding-disposition / remediation loop — never a bare red mark.
- A **per-finding, operator-informed accepted-exception path** (accept a specific advisory or license so
  the check passes legitimately) so a genuinely unfixable finding never strands the operator
  ([Degradability](../../reference/goals-and-quality.md)). Accepting an exception is enacted as an entry in the
  dependency-review check's **own committed allow-list** (the `allow-ghsas`/`allow-licenses` set), **homed
  in the module's `check` provides** — coherence-clean as part of the check definition, never a
  free-floating file. Adding an entry **durably loosens the gate's coverage for every future pull
  request**, so it is a guardrail-**weakening** change, not a one-off pass. Because that allow-list **is
  part of a check definition** — the [§15](../../principles.md)-monitored class (principles §15 names "the
  CI workflows and **check definitions**") — and an *added* allow-entry is the §15 verb *loosening a
  guardrail* (a weakening-direction diff, not a strengthening addition), the existing locked
  [control-plane](../systems/infrastructure/control-plane.md) **§15 weakening-detection guard**
  classifies it and **hard-blocks the merge until the operator's distinct weakening-acknowledgment**
  — the single deliberate affordance (a pull-request checkbox or operator-applied label, never a typed
  phrase) naming, in plain language, the specific advisory/license now un-gated and what it exposes. The
  module **relays into that existing gate — it neither re-implements nor owns the acknowledgment
  mechanism** ([§16](../../principles.md)). The disposition is recorded in the pull request's **Review**
  section (the finding's disposition) and the residual exposure in its separate **Risk** section (the
  locked [control-plane](../systems/infrastructure/control-plane.md) PR-contract sections). The
  consent is thus **the operator's, deliberate, and visible — distinct from the AI silently passing**
  ([§6](../../principles.md)/[§15](../../principles.md)).
- **Setup-time disclosure** that this package can block merges — a [provisioning](../systems/infrastructure/provisioning.md)
  selection-UX requirement — so opting in is informed consent, not a later surprise.
- All operator-facing text explains domain terms (pinning, dependency, license) plainly; the
  unavailable-tier disclosure is a cost/benefit choice in plain language, never platform SKU jargon.

### Ships its own domain detection

Unlike [validators-core](validators-core.md) (which ships check **data only, zero detection**),
this **feature** module legitimately ships **read-only domain detection** — the dependency-review-relaying
check and the pinning inspector — sanctioned by the locked check/validation docs (a module-provided
conforming check-kind discovered by presence, or the `custom/script` read-only escape-hatch kind; the
disclosed-no-op requirement biases the choice toward a kind that can emit a *not-applicable* finding). The
detection is strictly **read-only**: it inspects manifests and the dependency-review comparison and emits
findings, and **never rewrites a lockfile** (that would breach the read-only kind contract and the
[R5](../../reference/risks.md) mutation firewall). Because the review gate relays GitHub's **native, first-party**
dependency-review data (the dependency-review REST API, or GitHub's own published dependency-review
Action — never a **third-party** scanner or Action injected into every repo's CI; the one companion read
is a first-party repo-metadata call for visibility, consulted only to pick the copyleft rule's
private-versus-public branch and failing open when unreachable) and the allow-list is
the engine's **own committed check configuration** (not a third-party-dictated file), the module
introduces **no third-party supply-chain surface**. The API traffic itself rides the engine's one shared
authenticated GitHub client ([tools](../systems/surfaces/tools.md)), inheriting its off-host
fail-closed guard.

### The contributor wall holds

The module inspects and gates the **product's own** dependency manifests, which respects the
[engine/product wall](../systems/infrastructure/repository-topology.md) and the
[contributor-not-component](../../principles.md) principle: it is **optional**, so opting in is **consent,
not imposed coupling** (§13); and every check is **read-only**, never editing product source ("no seam
edits product source"). A CI gate on the product's dependencies is the engine acting as a **contributor**
reviewing a contribution — the same shape as the control-plane PR-completeness gate — not the engine
becoming part of the product. The removal test passes: the `dependabot.yml` floor is the control-plane's,
so removing this module leaves the product's dependencies and its floor intact.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.* *(No row in this table earns `engine` — every criterion here rests at least partly on your observation.)*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The laws are the check/validation/policies systems'; the delivery is this module** — no restating the laws here. | Operator observation: read this document and the module's policy against the linked system documents and confirm they deliver without re-legislating. No merge-gated check asserts the non-duplication. | operator |
| **Owns discipline, not the floor** — pinning + the review gate + cadence-as-posture; the secret-scan workflow + `dependabot.yml` floor stays the control-plane's, and this module never edits `dependabot.yml`. | Operator observation: the manifest provides only a policy, two checks, and their read-only tooling — `dependabot.yml` appears in no provides. Partial support: module-manifest (hard, CI) proves the provides set is what's declared, and the guardrail-weakening guard (hard, ruleset-bound) watches the floor file itself, so a module edit to it would demand your acknowledgment — neither asserts the ownership boundary as such. | operator |
| **Honest tiers** — review gate `hard` at CI, pinning `soft`, cadence and the policy itself posture; no posture dressed as enforced ([§7](../../principles.md)). | Operator observation: the review check declares `tier: hard` with the CI suite, the pinning check `tier: soft`, and the policy's own enforcement-tier section names cadence and itself as posture. The review gate carries a **disclosed not-applicable to the bite meta-check** — its aimed verdict comes from GitHub's live dependency-review data, so no seedable fixture can force it in CI; the gate's blocking behavior is exercised instead by its own demo and unit tests riding the CI unit-test step, never merge-gated on their own. | operator |
| **Wires nothing** — policy, checks, and detection logic all bind by presence; the review gate rides the existing required CI check with no new ruleset binding; `depends` ≠ wiring. | Operator observation: the manifest carries `wires: []` and both checks self-declare their suites, so they ride the one ruleset-bound validation run. Partial support: module-manifest (hard, CI) validates the manifest's grammar without asserting the wires list is empty. | operator |
| **Ecosystem-agnostic with disclosed no-ops** — the review gate relays GitHub's cross-ecosystem dependency-review data; the pinning check detects the ecosystem and discloses its inapplicability rather than passing silently. | Operator observation: the review tool relays the platform's cross-ecosystem comparison and discloses on every no-PR/unavailable/degraded branch, and the pinning inspector detects by root-manifest presence with a disclosed not-yet-applicable when none exists. The disclosed-no-op behavior is proven by the tools' own demo self-checks riding the CI unit-test step — never merge-gated on their own. | operator |
| **Optional means consent, and the operator is never stranded** — opt-in is informed, every hard finding is actionable or carries an accepted-exception path **gated by the §15 weakening-acknowledgment** (a durable allow-list entry is a guardrail weakening, never a silent pass), and read-only inspection keeps the §13 wall intact. | Operator observation: the provisioning catalog's entry discloses the can-block-merges consequence at opt-in, and the allow-lists live inside the review check's own definition. Partial support: the guardrail-weakening guard (hard, ruleset-bound) covers the check-definition prefix, so adding an allow-entry triggers the §15 acknowledgment gate — the consent and never-stranded legs remain your observation. | operator |
