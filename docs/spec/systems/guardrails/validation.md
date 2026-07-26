---
status: draft
---

# Validation

*Ratified in the design workspace on 2026-06-27 by [decision 0257](../../../adr/0257-resolve-re-lock-validation-the-negative-fixture-meta-check-l.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../../spec/index.md).*

## Summary

Answers **"does what got written match expectations?"** — the mechanical hard floor. It enforces JSON
Schemas on structured files, governed-shape rules on prose (allowed sections, length budgets, frontmatter
sync), the [ontology](../grammar/ontology.md) **catalog-coverage** gate (every catalogued
surface has its home; no orphan or uncatalogued surface), and the installed-module-set **coherence**
checks. It judges structure, never the semantic quality of prose — that is the [audits](audits.md)
layer's job ([principles §7](../../../principles.md)).

## Behavior

### The validator: a thin core over a kind registry

The prototype's validator grew into the repository's largest file because every new check meant new
validator code. This validator does not, because the check *inventory* and the check *logic* are split:

- **Rules are data.** Each [check](../surfaces/check.md) is a data file naming a `kind`, a
  `target`, parameters, a tier, its suites, and a message. Adding a check adds a file; the validator code
  is untouched.
- **Logic is a small registry of callables.** The core is a **thin dispatcher**: it loads the rules,
  routes each to its kind's callable, collects results, and reports them by enforcement tier. It carries
  no opinion of its own about how hard a rule bites — the rule's `tier` decides that. Each callable returns
  a fixed **result** — a pass/fail verdict plus zero or more findings on the canonical
  [`finding.v1`](../surfaces/schemas.md) base `{severity, message, location ref (file/line)}`
  ([D-113](../../../adr/0113-core-lock-closure-phase-0-the-build-spec-leaf-form-contract.md)); a check finding's `severity` is the rule's `tier` (`hard`|`soft`),
  the per-consumer severity the canonical base leaves open. The dispatcher collects these uniform results;
  the per-finding JSON Schema is a build-spec leaf, the result shape is not.
- **A closed core set of kinds** ships with this foundation: schema, shape, presence, coverage, coherence.
  A [module](../grammar/module-system.md) adds an additional kind by **providing a conforming
  callable, discovered by presence** — the [derived binding by presence principle](../../../principles.md),
  the same discovery axis as the agent roster and suite membership, **not** a wiring seam (the closed seam
  vocabulary has no check-kind directive) — and a `custom/script` escape-hatch kind covers one-offs. Adding
  a kind is an additive, reviewed callable — never an edit to a central validator file. The kinds are **diffable source
  modules**, not compiled artifacts, so they travel and review like every other committed file. The
  [control-plane](../infrastructure/control-plane.md)'s §15 guardrail-weakening guard is one such
  instance — a frozen-named `custom/script` check whose check wiring this foundation owns, while the
  control-plane owns its protection-off contract ([D-051](../../../adr/0051-guardrail-integrity-the-builder-cannot-silently-weaken-its-o.md)/[D-134](../../../adr/0134-resolve-q22-pin-the-15-weakening-merge-consent-as-a-distinct.md)).
- **`custom/script` fails closed, three ways.** The escape-hatch kind maps its committed script's outcome
  onto the same `finding.v1` result: a **missing script**, a **nonzero exit**, or **unreadable JSON output**
  each becomes a `hard` finding rather than a silent pass — the process→result contract that lets a bespoke
  check be trusted, and that the negative-fixture meta-check below exercises mode by mode.
- **Directly callable, not only trigger-driven.** The core is a library other systems invoke
  programmatically — the [module-system](../grammar/module-system.md) manager runs the coherence
  kind right after an install to confirm the set. A module install is a direct invocation, not a fifth
  suite trigger.
- **A dangling kind is a finding, not a silent pass.** A rule whose `kind` is unregistered is promoted to
  a tracked finding immediately, and in the CI suite it fails the required check (see tier-versus-context
  below), so a `hard` governance rule can never be quietly un-enforced.

### Proven to bite: the negative-fixture meta-check

A `hard` check that cannot be shown to *fail* is posture dressed as enforcement — the one thing
[§7](../../../principles.md) forbids — at the surface the operator most directly relies on (the CI
green). So the foundation proves each hard check **bites**: a standing `hard` **CI-suite** meta-check runs
every in-scope hard check (every hard logic-unit with a statically-decidable CI failure path) against a
committed **negative fixture** (a seeded bad input) and asserts the
expected `hard` finding by **set-membership** — the finding's `id`/`severity` is present, never an
order/count assert, since the finding stream is not a [§19](../../../principles.md) source-deterministic
member. This is a **system-local invariant**, not a numbered principle: it *instances*
[§7](../../../principles.md) (name the tier honestly) and is reflexively kin to
[§15](../../../principles.md) (the guard must not be falsifiable by what it judges). Validation fixes the
**law and execution model**; the meta-check rule-data instance — a `custom/script` rule riding a
**run-one-rule-against-a-substituted-target** entry point on the directly-callable dispatcher
([core](../../modules/core.md)'s to provide) — is
[validators-core](../../modules/validators-core.md)'s.

- **Scope is the logic-unit.** Each check-**kind callable** (the closed core five plus any module-added
  kind) carries at least one negative fixture proving the *kind* bites, and each **`custom/script`
  instance** carries its own (each script is its own logic). A data rule of a proven kind **inherits the
  kind's proof**. The invariant proves *kind/logic bite*, **not rule aim**: a mis-aimed rule of a proven
  kind (a `schema` rule naming the wrong schema, a `presence` rule whose glob matches nothing) is not caught
  here, and `coverage`/`coherence` do not backstop it — rule-aim stays the
  [check](../surfaces/check.md) telemetry posture (a rule that never fires is flagged
  possibly-inert), the after-the-fact signal this up-front gate complements.
- **Distinct from the dangling-/unresolvable-kind law.** That law (above) proves a kind is *registered and
  runnable* and fails closed when it cannot evaluate; this proves a kind *bites on a seeded negative*. A
  check can be perfectly runnable and still be a green no-op — this is the gate that catches it.
- **Fixtures are discovered by presence** — the discovery law and the reserved fixture namespace are the
  [check](../surfaces/check.md) surface's (not a rule field), and whether that namespace needs a
  [repository-topology](../infrastructure/repository-topology.md) clause is settled there.
  Validation's only stake is the execution-model consequence: a committed negative must reach the meta-check
  **without turning the real suite red or reading as an orphan surface** — the isolation that namespace must
  deliver.
- **The only admissible carve-out is a check with no statically-decidable failure path in the CI
  environment** — every check that *can* be made to fail in CI carries a fixture; the carve-out is bounded
  by that property, never an open category. Such a check resolves to a **disclosed not-applicable**, reusing
  the `ci_author_exempt` disclosed-no-op grammar rather than a silent skip: the first-run reference-closure
  check's *computed-path* leg (best-effort by its own definition, below) and its no-op-after-retirement
  state, and a `ci_author_exempt` rule's exempt-author verdict, are proven at construction where their
  failure path exists, never by a synthetic bad asset shipped into a generated repo
  ([§4](../../../principles.md)).
- **A module-added kind ships its negative fixture co-located with the callable**, so the meta-check **fails
  closed** on a present in-scope kind with no fixture, and uninstall is a pure file removal — the
  [§14](../../../principles.md) derived-by-presence reversibility, never a centralized fixture stranded as an
  orphan when its kind leaves.
- **The meta-check carries its own negative fixture** — a seeded hard logic-unit whose fixture is missing or
  non-biting must turn it red — so the checker-of-checkers is itself falsifiable
  ([§15](../../../principles.md)); this terminates the regress without a meta-meta-check.

The honest ceiling is [§7](../../../principles.md)'s: a fixture proves a *witnessed* negative trips the
check **today** — not completeness against every negative, nor stability under later drift. The CI run
*exercises* the gate; the fixture *enforces* the bite ([§19](../../../principles.md)'s
exercise-versus-enforce distinction), and neither is dressed as the other.

### Check suites: thin declarations, derived rosters

A **suite** is a thin authored declaration — a name, a trigger, and an execution context. It does **not**
enumerate its rules. Membership runs the other way: each rule self-declares which suites it joins, so a
suite's roster is **derived** from the rules present. A [module](../grammar/module-system.md)
therefore sets membership by *which check files it provides* — drop a file and its rule joins; remove the
file and it leaves. There is no central suite file to edit on install and un-edit on uninstall, which is
what keeps install mechanical rather than surgical. This keeps the locked
[control-plane](../infrastructure/control-plane.md) seam honest: the CI harness owns neither
check content nor membership — membership is declared in each check's `suites` field and governed by what
the module system provides, exactly downstream of the harness.

### Triggers: the law is fixed, the set grows additively

The **law** — suites bind to triggers, and adding a new trigger is a reviewed addition, not a casual one —
is fixed. The trigger **set** is additive data, not frozen prose; the v1 triggers span two substrates,
local Claude Code [hooks](../infrastructure/hooks.md) and
[control-plane](../infrastructure/control-plane.md) GitHub workflows:

- **`pre-commit`** — the commit boundary, run as a `PreToolUse` hook intercept on the `git commit` Bash
  call (no separate pre-commit framework).
- **`pre-close`** — the [close](../lifecycle/close.md) ritual's `Stop` hook.
- **`CI`** — the pull-request workflow the control-plane binds as a required check.
- **`audit-prep`** — a scheduled (cron) workflow that reports into [telemetry](telemetry.md); its
  concrete runner lands with the [audits](audits.md) system, so the trigger is named now and
  populated when audits is designed.

Multiple named suites may share a trigger; a genuinely new trigger means a new execution context, added by
review rather than frozen here.

### Tier versus context: where teeth actually land

A rule's `tier` is its intrinsic strength; whether a `hard` tier *blocks* depends on the suite's context:

- **CI is the only unbypassable gate.** A `hard` rule in the CI suite fails the required check and blocks
  the merge, bound via the [control-plane](../infrastructure/control-plane.md) ruleset.
- **Local triggers nudge.** The same `hard` rule under `pre-commit` or `pre-close` surfaces as a strong
  nudge, not an absolute wall ([principles §6](../../../principles.md)) — except the governance-critical
  local blocks the [hooks](../infrastructure/hooks.md) budget enumerates.
- **An unresolvable `hard` rule fails closed at CI.** A rule whose kind cannot run is promoted to a finding
  everywhere; in the **CI** suite it additionally **fails the required check**, so a governance rule that
  cannot evaluate blocks the merge rather than passing silently — while locally it still fails open, so a
  broken kind never strands the working session.
- **`audit-prep` reports** into telemetry rather than gating.
- **A CI-author applicability boundary resolves to a disclosed no-op.** A rule may declare a
  `ci_author_exempt` author set ([check](../surfaces/check.md)); when the CI suite evaluates it
  against a pull request whose author is in that set, the engine produces a **disclosed not-applicable result**
  — a pass carrying a finding that names why the rule does not bind this PR — rather than running it to a fail.
  It **never silently skips** (a silent green would read as "verified"), and it is **CI-only** (no pull-request
  author exists at `pre-commit`/`pre-close`), so the rule is still loaded and dispatched everywhere and only its
  CI verdict against an exempt author resolves to the no-op — the "runs identically as a library locally and in
  CI" commitment below is preserved. The boundary lives in the rule's **data** and the engine honors it,
  keeping the five closed kinds **author-agnostic** (the realization — a pre-dispatch resolution versus a
  kind-emitted finding — is a build-spec leaf, the law being a disclosed not-applicable result with the kinds
  unaware of the author). The [control-plane](../infrastructure/control-plane.md) owns the
  domain boundary this realizes (which authors a required check binds); introducing or widening the set on a
  required rule is a guardrail-weakening change ([§15](../../../principles.md), [D-207](../../../adr/0207-authorize-the-dependabot-pr-contract-exemption-a-ci-author-a.md)),
  hard-gated at the merge like the [dependency-discipline](../../modules/dependency-discipline.md)
  accepted-exception allow-list.

### Execution mapping

The local run escalates with the work: `PostToolUse` runs only the **touched-file subset** of the
`pre-commit` suite incrementally after each edit; the **`pre-close` run is the authoritative local
full-suite pass**, because the `Stop` hook always fires before work leaves the session, where the
`pre-commit` intercept can be missed on a manual commit. But both local runs are **best-effort and can be
skipped entirely** — a manual commit, or a released `Stop` block — so they only rehearse. The **sole
guarantee** is the protected-branch CI run, which has teeth once the
[control-plane](../infrastructure/control-plane.md) bootstrap is applied (Risk R1).

### What the operator is told

A check exists to inform a non-engineer's merge decision, so results are surfaced in plain language, not
engineer shorthand. Where the operator decides — the pull request and the [boot](../lifecycle/boot.md)
orientation — three things are stated plainly: that **the CI check is the only gate that can stop a bad
merge, and the local runs are advice**; that **a passing check means the engine proved that gate catches a
deliberately broken example — proof the gate works, not proof the change is correct**; and, for any rule that could not
run, a named line that the change was *not* verified for what that rule covers. Each rule's `message` is written to the operator-communication
standard the [check](../surfaces/check.md) surface fixes — clear and complete, explaining rather
than assuming — because the operator must understand an issue to choose its disposition.

### What it covers

- **Catalog coverage and module coherence are first-class:** the installed module set, settings, MCP
  registration, suites, and ontology must agree, and validation fails loud on drift
  ([module-system](../grammar/module-system.md)).
- **PR-body completeness** is a check that the [control-plane](../infrastructure/control-plane.md)
  PR contract's sections are present and non-empty; structure and presence are `hard`, truthfulness is
  posture.
- **The contract anti-choice and the close findings-disposition summary are presence checks** — the
  [contracts](../surfaces/contracts.md) template requires a substantive anti-choice, and the
  [close](../lifecycle/close.md) ritual requires a disposition for every finding raised. Presence
  is `hard-fail`; genuineness stays posture, per the [policies](../surfaces/policies.md).
- **First-run reference-closure** is a `custom/script` check that no file *surviving* first-run retirement
  statically references a retired first-run asset — the
  [provisioning](../infrastructure/provisioning.md) *travel-safety* invariant, its
  definition-of-record. It is `hard` in the **CI** suite, so a violation blocks the merge before a
  broken first-run can ship; its finding follows *What the operator is told* above — the consequence (an
  adopter's first check would fail with an error they cannot read), the concrete file and reference, and the
  disposition (stop referencing the retired machinery, or retire the file in the same pass) — never
  retire-set / closure shorthand on the surface. The check is honest to what static analysis can decide
  ([§7](../../../principles.md)): the `import` and `importlib` legs — and subprocess- or path-references
  given as literals — are caught completely, while a *computed* path reference is a behavioral residual the
  invariant still forbids but a static check catches only best-effort, never a guarantee dressed as one.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| Runs identically as a library locally and in CI — in both it executes inside the engine [tool-runtime](../infrastructure/repository-topology.md); the CI job materializes that runtime first (`astral-sh/setup-uv` pinned to a commit SHA, then group-scoped `uv sync`, per the [control-plane](../infrastructure/control-plane.md) CI harness) before invoking the dispatcher. Only the trigger context changes whether a `hard` result nudges or blocks ([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)). | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
| A malformed structured file fails loud rather than misleading the AI, consistent with the state foundation's halt-on-malformed posture. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| The validator owns no rule and no suite roster; both are data it reads, so the foundation stays small as the rule set grows. | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
