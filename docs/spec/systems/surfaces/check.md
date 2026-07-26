---
status: draft
---

# Check

*Ratified in the design workspace on 2026-06-27 by [decision 0258](../../../adr/0258-resolve-re-lock-check-the-by-presence-negative-fixture-gramm.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../../spec/index.md).*

## Summary

The check-rule surface — the unit of mechanical validation, authored as **data, not code**. A check is
one rule: what to inspect, how, how hard it bites, and which suites run it. The
[validation](../guardrails/validation.md) foundation loads checks and dispatches each to a
check-kind callable; adding a check is adding a check file, never editing the validator. The
[ontology](../grammar/ontology.md) names `check` as a tier-3 (mechanics-and-guidance) surface;
this doc is its record.

## Behavior

### The rule record

A check is a `structured`-class instance, so it is schema-governed **whole** (no prose template — that
is for prose surfaces). Each rule carries seven fields, and may carry an optional eighth:

- **`id`** — engine-namespaced identifier (per the [ontology](../grammar/ontology.md) identifier
  law), stable so [telemetry](../guardrails/telemetry.md) can track its fire history and flag a
  rule that never fires as possibly inert.
- **`target`** — what the rule applies to: a surface category and/or a path glob.
- **`kind`** — which check-kind callable evaluates it (see below).
- **`params`** — the kind-specific parameters (a schema reference, an allowed-section list, a length
  budget, and so on).
- **`tier`** — the enforcement strength: `hard` or `soft` only.
- **`suites`** — the suites the rule self-declares into.
- **`message`** — the operator-and-AI explanation (see the standard below).
- **`ci_author_exempt`** *(optional; default absent)* — the pull-request author logins this rule **does not
  bind when evaluated in the `CI` suite** against a pull request authored by one of them; for such a PR the
  rule yields a **disclosed not-applicable result** (a stated pass naming why it does not bind this PR, never
  a silent skip), the [validation](../guardrails/validation.md) engine honoring the boundary itself
  so the closed kinds stay author-agnostic. It is **inert outside `CI`** — `pre-commit`/`pre-close` have no
  pull-request author — and is the rule's declaration of an *applicability* boundary, the PR-context sibling of
  `target`. Absent on every rule by default; the [control-plane](../infrastructure/control-plane.md)
  PR-body completeness check is its one v1 user, naming the recognized external-automation author
  `dependabot[bot]` ([D-207](../../../adr/0207-authorize-the-dependabot-pr-contract-exemption-a-ci-author-a.md)). The governing schema carries it as one optional field
  (its value a build-spec leaf), so a rule without it validates unchanged; **introducing or widening the set on
  a required rule is a guardrail-weakening change** ([§15](../../../principles.md)), hard-gated at the merge
  like any check-definition edit.

### Tier is `hard` or `soft` — never `posture`

A check is mechanical by definition, so its `tier` is `hard-fail` or `soft-warn`
([principles §7](../../../principles.md)). **Posture is not a check.** An expected-but-unmechanical
directive lives as prose in a [policy](policies.md) or [contract](contracts.md); its
observance is reached only *indirectly*, by a presence check that confirms the expected artifact exists —
and that presence check is itself `hard` or `soft`. Whether a `hard` tier actually blocks depends on the
suite's trigger context (only the CI suite gates the merge); the rule declares intrinsic strength, the
suite decides where teeth land. That context law is the [validation](../guardrails/validation.md)
suite grammar's.

### Self-declared membership

A rule names its suites in the `suites` field; the suite roster is **derived** from the rules that
declare into it, never a hand-edited central list. A [module](../grammar/module-system.md) thus
determines suite membership by *which check files it provides* — install drops the file and the rule
joins; uninstall removes it and the rule leaves. No central suite file is mutated, so there is no install
surgery to reverse. This is how the locked [control-plane](../infrastructure/control-plane.md)
seam keeps check-suite membership in the module system — the module governs *which* checks ship — while
the declaration itself lives here in the rule.

### The `message` standard — explain, never dumb down

`message` is one field serving the operator and the remediating AI alike. It is **clear and complete**:
it states what is wrong, why it matters, and the remediation, explaining any technical term rather than
assuming or omitting it. The standard is deliberate — the operator's merge click is *informed consent*
([control-plane](../infrastructure/control-plane.md)), and a person cannot consent to, or
choose a disposition for (fix in line / log an issue / escalate), an issue they were not given enough to
understand. A message is never simplified to the point of hiding substance, and never written only for an
engineer. The AI uses the same text plus `id`, `kind`, and `params` for mechanical detail. The schema makes
the field's *presence* a `hard` check; its *quality* against this standard is a semantic matter the
[audits](../guardrails/audits.md) layer reviews as posture — the validator cannot grade prose.

### Kinds: closed core, extensible by modules

A rule's `kind` resolves to a callable in the validator's kind registry, and every callable conforms to the
kind-callable **result contract** the [validation](../guardrails/validation.md) foundation fixes —
a pass/fail verdict plus zero or more findings on the canonical [`finding.v1`](schemas.md) base, a
check finding's `severity` being the rule's `tier` ([D-113](../../../adr/0113-core-lock-closure-phase-0-the-build-spec-leaf-form-contract.md)). That foundation ships
a closed **core** set (schema, shape, presence, coverage, coherence); a
[module](../grammar/module-system.md) adds an additional kind by **providing a conforming callable,
discovered by presence** (the [derived binding by presence principle](../../../principles.md)), not a wiring
seam; and a `custom/script` escape-hatch kind covers one-offs. A rule
naming a kind that is not registered does not silently pass — the validator promotes it to a finding, so
a `hard` governance rule can never be quietly un-enforced.

### The negative fixture — every hard check is proven to bite

A `hard` check is a gate, and a gate that cannot be shown to fire is posture dressed as enforcement
([§7](../../../principles.md)). So each **check-logic unit** carries a **negative fixture** — a committed
seeded bad input the check is meant to catch — and the [validation](../guardrails/validation.md)
meta-check proves the unit **bites** by running it against that fixture and asserting the expected `hard`
finding. The logic unit is where bespoke logic lives: each **kind callable** (the closed core five plus any
module-added kind) carries at least one negative fixture, and each **`custom/script` instance** carries its
own; a data rule of a proven kind inherits the kind's proof.

- **Bound by presence, not a rule field.** A negative fixture is tied to its logic unit by a
  naming/location convention (the [derived binding by presence principle](../../../principles.md)), so the
  rule record above is unchanged — no fixture field, no schema change. The fixture co-locates with its unit
  (a kind callable's with the callable, a `custom/script` instance's with the rule), so the binding is a
  file drop and its removal a file removal — a module that adds a kind ships the kind's fixture with it, and
  uninstall takes both ([§14](../../../principles.md)/[R5](../../../reference/risks.md) reversibility); a fixture left
  behind after its unit is gone is inert (glob-excluded, coverage-exempt test data), so it can never strand
  a gate.
- **The fixtures namespace is reserved, glob-excluded, and coverage-exempt.** Fixtures are **test data, not
  a surface**: they live in a reserved namespace that real check `target` globs do not match and that the
  `coverage` gate does not read, so a committed bad input neither turns the real suite red nor registers as
  an orphan or uncatalogued surface. Whether the namespace also needs a
  [repository-topology](../infrastructure/repository-topology.md) placement clause is settled with
  topology. The fixture unit follows the kind: a single bad file for schema/shape/presence, a malformed
  mini-tree for the repo-global coverage/coherence kinds.
- **Distinct from the `id` inert signal.** [Telemetry](../guardrails/telemetry.md)'s flag of a
  rule that *never fires* (the `id` bullet above) is the **after-the-fact, rule-aim** signal — it watches
  whether a deployed rule ever bites in production; the negative fixture is the **up-front, per-kind** proof
  that the logic *can* bite at all. They complement, never duplicate. The fixture proves a *witnessed*
  negative, never correctness against every input or stability under drift — the
  [validation](../guardrails/validation.md) meta-check carries that honest ceiling and the only
  admissible carve-out: a logic unit with **no statically-decidable failure path in the CI environment**
  (the bounded property validation fixes, never an author's self-classification) resolves to a disclosed
  not-applicable.

### Shape and storage

- Instances are slug-named files, indexed by directory listing, living where
  [repository-topology](../infrastructure/repository-topology.md) places the surface
  (`.engine/check/`).
- The governing schema is **JSON Schema 2020-12**, resolved through the catalog `governing_schema` field
  like every other structured surface ([schemas](schemas.md)).
- Lifecycle is the `artifact` vocabulary: a check is born `active` on merge, `deprecated` for managed
  phase-out (tied to module migrations), then `retired`.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| A check is data the validator consumes; the validator carries no rule of its own, and no rule carries its own logic — the closed kind set is the only place check logic lives. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| Coverage is gated: a catalogued check surface with no `.engine/check/` home, or an uncatalogued check in use, is a finding the [knowledge graph](../cognitive/knowledge.md) surfaces. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| A `hard` check-logic unit is **proven to bite**: a discovered negative fixture exists and the [validation](../guardrails/validation.md) meta-check confirms it yields the expected `hard` finding (or a disclosed not-applicable where no statically-decidable failure path exists in the CI environment). The meta-check demands a fixture against a roster — kind callables from the validator's kind registry, `custom/script` instances from the check-rule directory listing — so an in-scope unit (one with a statically-decidable CI failure path) present in its roster but missing its co-located fixture is itself a `hard` finding, the absence read against the unit's presence, never as "no unit here". A gate cannot be silently un-proven. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
