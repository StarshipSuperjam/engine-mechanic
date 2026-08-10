---
status: accepted
engine_record: true
---

# Separate module distribution, applicability, and activation into independent axes

*Decided 2026-08-10 in this repository, by the operator, through the plan-acceptance route
[decision 0327](0327-route-product-spec-authoring-through-plan-acceptance-into-b.md) establishes,
settling engine-mechanic issue #55. The exact axis tokens — in particular splitting activation into an
invocation dimension and an authorization dimension — were settled in the plan's cold review. Rides the
pull request that amends the module grammar and reclassifies the module corpus. This record **partially
supersedes** [decision 0334](0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md) and
[decision 0067](0067-operator-facing-module-packaging-industry-discipline-categor.md) /
[decision 0068](0068-q1-resolved-the-v1-optional-module-roster-4-cut-2-kept.md) as scoped below.*

## The decision

**The single module `status` field is retired in favour of independent axes.** Today one manifest field —
`required · default-on · optional · experimental · retired` — carries deployment inclusion, applicability,
operator consent, runtime activation, security authority, stack specialization, maturity, and lifecycle at
once. That overload is what lets governance machinery be described as "optional" when a universal Engine
claim depends on it, and what turns every conditional capability into install-time configuration that buys
little real isolation. It is replaced by three independent axes plus two orthogonal markers.

**The three axes.**

- **Distribution** — is this module physically part of this Engine installation? `required | profile |
  extension`.
  - *required*: ships and upgrades with every Engine. It may still be inapplicable, dormant, or
    unauthorized in a particular repository or run.
  - *profile*: physically present when its platform/stack/environment profile matches, that membership
    fixed at provisioning from objective facts — not offered as an arbitrary setup preference.
  - *extension*: genuinely expands Engine behaviour and may reasonably remain absent forever. It must pass
    the **strict extension test**: *removing the module leaves the truth of every core Engine governance,
    evidence, safety, and operator-legibility claim unchanged.*
- **Applicability** — does this module make sense for this repository/product/host/environment? `universal |
  detected | declared`. `detected` reads objective repository/host facts (re-evaluated per run); `declared`
  is used only where facts are insufficient. Applicability is **re-evaluated per run**, so a module present
  by profile can still report *inapplicable* on a given repository.
- **Activation** — given a module present and applicable, is its behaviour currently invoked and
  authorized? Activation carries **two independent dimensions**, because invocation mode and authorization
  are not the same question:
  - *invocation mode*: `always | on-trigger | explicit` — does behaviour run continuously, fire when its
    trigger occurs, or wait to be explicitly invoked.
  - *authorization gate*: `ungated | authority-gated` — whether an explicit grant/consent artifact (named
    by the module) must exist before any effect. A module may be `on-trigger` **and** `authority-gated` at
    once — `bounded-repair` and the deployment family are exactly this — which a single activation token
    could not express.

**Two orthogonal markers, kept out of the axes.** `experimental` is a **maturity** marker and `retired` is
a **lifecycle** state; neither is a distribution class. A module carries a distribution class plus, where
they apply, a maturity or lifecycle marker — never one standing in for the other.

**"Offered on at setup" is provisioning presentation data, not a manifest axis.** Whether an *extension* is
presented opt-out (on by default) or opt-in at first-run is selection-UX data keyed by module id — the same
kind of data as the SDLC-discipline grouping — never an activation or distribution token. This is where the
old `default-on` meaning goes; it never rides the manifest grammar.

**The load-bearing invariants**, made explicit rule text in the module-system grammar:

- **Implementation modularity is not deployment optionality.** Internal module boundaries — ownership,
  `depends`, `provides`, tests, manifests, fault containment — are preserved unchanged; only deployment
  semantics move. This is not a flattening of packages into `core`.
- **Required is not monolithic, universally-applicable, or always-active.** A required module may have no
  wires, no runtime cost until invoked, a no-op when its subject matter is absent, or refuse all action
  until an authority/consent artifact exists.
- **Applicable is not active**, and **presence/applicability confer no authority.** A security-sensitive
  required module ships its machinery and grants nothing by being present; effect waits on the
  authorization gate.

**The reclassification.** Every committed module receives a distribution class; every non-universal module
an applicability rule; every non-unconditional module an activation rule.

| Distribution | Modules |
| --- | --- |
| **required** (built) | `core`, `validators-core`, `audit-library`, `memory-substrate-sqlite-fts5`, `routine-mode` (conform; behaviour unchanged); `dependency-discipline`, `migration-discipline`, `product-design`, `design-review`, `qa-review` (**promoted** from optional; activation stays conditional — present, not always-on) |
| **required** (delivery, unbuilt) | `delivery-core`, `delivery-evidence`, `code-intelligence-core`, `structured-change`, `engineering-quality`, `execution-environment`, `authority-broker-contract`, `credential-broker`, `deployment-core`, `deployment-adapter`, `operations-core`, `maintenance-ledger`, `bounded-repair`, `large-change-coordination`, `profile-registry`, `operator-cockpit`, `evidence-explorer` |
| **profile** | `engineering-quality-python`, `runtime-backend-local-container`, `engineering-quality-typescript`, `platform-web`, `browser-evidence`, `debugger-diagnosis`, `platform-ios`; concrete credential/deployment provider realizations when chosen |
| **extension** | `memory-semantic-recall` (offered-on at setup), `external-contribution`, `github-projects-sync`, `product-knowledge-graph`, `research-and-learning`, `platform-currency` |

`engine-knowledge-graph` remains an unscheduled stub; its distribution class is **not settled here**. Its
design session must rerun the strict extension test rather than inherit a class by default.

**State reporting.** Operator/status surfaces must distinguish, and never conflate: absent because an
extension/profile is not distributed here (naming which, so the remedy is legible) · present but
inapplicable · present and applicable but inactive · present and applicable but authority-disabled · active
· degraded/faulted.

**Upgrade convergence.** A release that makes modules newly `required` converges deployed repositories to
the new required set at ordinary upgrade — the target set derived from the release manifest, no
per-previous-selection migration branches, no rewrite of product-owned content (the promoted modules touch
only engine-namespaced files and wiring). The settled "never resurrect a module the operator deselected"
rule is preserved for `extension`/`profile` modules and reconciled with convergence by one rule:
**deselection is only ever a valid state for an `extension`; a `required` (or newly-matching `profile`)
module is installed-if-absent at upgrade regardless of prior absence, because declining a required module
was never a valid state.** That an operator who once declined a now-required governance module gains it at
upgrade is a deliberate consequence, disclosed in the upgrade's pull request.

**Security surfaces stay open to their pre-settle review.** `authority-broker-contract`, `credential-broker`,
`deployment-core`, `deployment-adapter`, and `bounded-repair` are unbuilt drafts that decision 0334 holds to
a full pre-settle security review before their wave builds. This record adopts their **required-distribution
contract intent**; it does **not** foreclose that review, which retains full authority to revisit the
classification when each module settles. Their spec documents stay `draft`. As a required-contract invariant,
`credential-broker`'s custody substrate and cipher dependency do not materialize or load absent an installed
provider adapter, and its deliberately-vulnerable reference adapter can never be wired as a live adapter —
presence ships the contract, never a live custody path.

**Scope of supersession.** Decision 0334's ruling that "every [delivery] module is `optional`" and its
rejection of "making the delivery substrate `required`" are superseded **only** in light of the new grammar:
required now means *present*, not *forced on*, so the plane still never activates on a project that never
asked for it — 0334's actual intent — while its contracts are universally present so deleting one is not a
route to a weaker external-effect path. Decision 0334's wave order, boundary cuts, program rules, and
settle-at-the-gate discipline stand unchanged. Decision 0068's *cut* roster and decision 0067's
*category-presentation model* stand; only the optional-roster **classification** of the five promoted
governance modules is superseded.

## Why

An operator builds through the Engine rather than by reading its code, so the deployment story has to be
honest at a glance: what ships, what applies here, what is running, and what is merely present-and-waiting.
One field carrying all of those at once forced two bad outcomes — governance and evidence machinery the
Engine's universal claims depend on could be described as optional and declined, and every conditional
capability became an install-time choice that multiplied configuration and upgrade paths without buying real
isolation. Separating the axes lets the Engine ship its safety and governance spine to every deployment while
keeping it dormant, inapplicable, or unauthorized until it genuinely applies — the thing the old grammar
could not say. Splitting activation into invocation and authorization is what makes "present, on-trigger, and
still authority-blocked" expressible, which is the true state of every external-effect and unattended-repair
capability; collapsing them would re-create the overload one level down. The reclassification then follows
directly: what a universal claim rests on is `required`, what a platform fact selects is `profile`, and what
survives the strict extension test is `extension`.

## What we ruled out

**Keeping the single overloaded `status` field** (rejected — it is the defect itself: it lets a universal
dependency read as optional and turns every conditional capability into install-time configuration). **Two
axes only, folding applicability into an `activation: detected` token** (the shape the build-side issue
sketched; rejected — applicability is *relevance to this repository* and activation is *is behaviour
running*; a web repo makes `browser-evidence` applicable while it stays inactive until a review path requests
it, so the two must move independently). **A single-value activation enum with combined tokens**
(`always|on-trigger|explicit|default-on|authority-gated`; rejected — `bounded-repair` and the deployment
family are `on-trigger` **and** `authority-gated` at once, which one token cannot carry, and `default-on`
smuggles the setup-inclusion meaning back into the manifest, reviving the overload the whole change exists to
kill). **Keeping `default-on` as a manifest token** (rejected — offered-on-at-setup is provisioning
selection-UX data keyed by module id, not a runtime property of the module). **Flattening the promoted
governance modules into `core`** (rejected — the package seams remain useful for ownership, tests, and fault
diagnosis; this is deployment semantics, not package structure). **Making the delivery substrate `required`
under the old grammar** (the objection decision 0334 correctly raised — it would have forced the plane on
projects that never asked; rejected *there*, and here it does not recur, because required distribution no
longer implies active behaviour). **Reclassifying the five draft security surfaces as a foreclosed, settled
decision** (rejected — an accepted append-only record fixing their class would pre-empt the pre-settle
security review decision 0334 mandates; the classification is adopted as contract intent and held open to
that review instead).
