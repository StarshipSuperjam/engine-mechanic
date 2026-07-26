---
status: draft
---

# qa-review

*Ratified in the design workspace on 2026-07-11 by [decision 0292](../../adr/0292-resolve-re-lock-qa-review-the-8-pair-split-across-two-lenses.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../spec/index.md).*

## Summary

The **pre-submission stage roster**: five cold-context reviewer [agent](../systems/surfaces/agents.md)
personas the [build orchestration](../systems/lifecycle/build-orchestration.md) invokes at its
**pre-submission-review** gate — the back half of the design → build → QA axis. Where the
[design-review](design-review.md) suite asks *is the design sound?*, this suite asks *what did we
actually produce — is it correct, usable, healthy, and safe?* It is the other half of the v1 lens roster
([D-066](../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md)) the [agents](../systems/surfaces/agents.md) surface defers to
the build orchestration.

These lenses are the **judgment** layer; they sit *above* the locked
[validation](../systems/guardrails/validation.md) suite and CI (the **mechanical** layer). A
persona judges, a check gates — they complement, never duplicate ([honest enforcement tiers](../../principles.md)).

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `qa-review` |
| `status` | `optional` |
| `provides` | five `role: pre-submission-review` agent personas (`.claude/agents/` files), one per lens below |
| `wires` | **none** (file-drop; roster derived from agent frontmatter) |
| `depends` | `core` |
| `migrations` | none (v1) |

### The five lenses

Each is **read-only with respect to authoritative state** (see the dry-run note), reports findings via the
uniform [`output-contract`](../systems/surfaces/agents.md) while the orchestrator decides and
writes, and declares `role: pre-submission-review` with the lens below. Build orchestration records that its
pre-submission gate consumes all five, so none dangles.

1. **`lens: spec-conformance`** — *Did we build what we said?* Requirements coverage, acceptance-criteria
   pass, regression, edge cases, data correctness. A **primary consumer of the
   [product-design](product-design.md) referent — the committed `locked` spec**
   ([D-244](../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)), judged built-vs-spec as the **systematic conformance reviewer**
   (build-conformance §8): it derives each obligation and marks it met,
   diverged, or untested, resolving no doubt charitably — **re-deriving each obligation from the `docs/spec/`
   span itself, never from the matrix rows** (the matrix is the denominator, not the lens's checklist —
   [R16](../../reference/risks.md)) — the deployed product build against a `locked` spec earning the same rigor that
   built the Engine ([conformance-enforcement floor](../../reference/glossary.md), [§20](../../principles.md)); its
   summary **restates, in the operator's words, which criteria it verified and which it could not** — the
   guard against a green "QA passed" resting on a thin spec. It is one **judgment** leg of that floor —
   **paired with the adversarial `divergence-hunter` lens below**, which runs against the same `locked` rows
   as a second, decorrelated cold context — and complements the **mechanical**
   [spec-obligation matrix](../../reference/glossary.md) (every `locked` criterion, criterion-granular and
   fingerprint-pinned to its `docs/spec/` span, product-design-provided): a persona judges conformance, a
   check gates traceability, never duplicating. It may run the **deployed-environment demonstration
   harness** (the spec's operator-runnable how-verified rows) as a disclosed dry-run (below), the
   [§17](../../principles.md) behavioral correlate carried beside the judgment. It judges **only criteria
   whose row is `locked`**; absent a `locked` spec (or for an adjacent `draft`/`stub` capability) it is
   the disclosed no-op (below), never a block on unspecced scope. *Catches:* the build diverged from the
   spec.
2. **`lens: usability`** — *Does it work well for the people using it?* Usability, real utility, workflow
   friction, accessibility, error recovery, learnability. *Catches:* a result that meets spec yet is
   confusing or unpleasant to use.
3. **`lens: technical-integrity`** — *Is the built software internally healthy?* Code quality, adherence
   to the intended architecture, performance, observability, reliability under failure, testability,
   dependency health, and **whole-repo dead code** — orphaned or never-called surfaces, judged as a
   *maintainability* concern, referent-free (the *spec-divergent* over-build a diff introduces is
   `divergence-hunter`'s, judged against the spec; the two judge different properties, never duplicating a
   finding). *Catches:* a result that
   passes tests but is fragile, opaque, dead-weight, or costly to maintain.
4. **`lens: security-governance`** — *Is it safe to release?* Authn/authz, injection, secrets and
   exposure, privacy, compliance controls, audit/change-control, abuse testing, release risk. *Catches:* a
   functional result that should not ship. (Its plan-review counterpart — *what could go wrong?* — is the
   design-review `risk-governance` lens; same concern, different role.)
5. **`lens: divergence-hunter`** — *Does anything here diverge from the spec — built wrong, or built at
   all without warrant?* The adversarial counterpart to `spec-conformance`
   (build-conformance §8 adversarial-divergence-hunter brief): a
   **distinct cold context that assumes a divergence exists and hunts for it** — default-to-divergent, a
   suspected divergence reported with its location and plain-language consequence rather than explained
   away (a false alarm the orchestrator rejects is cheap; a semantic misbuild merged into the foundation is
   not). It hunts two faces of one question — *where do the build and the `locked` spec fail to
   correspond?*: **(forward)** a semantic misbuild that passes its own tests, a test whose assertion does
   not match its name, a guardrail that no-ops on some path, a requirement silently dropped; and **(the
   narrow backward arm)** an **over-build** — a surface *this PR's diff introduces* that no obligation asks
   for — surfaced as a **ground-truthed suspicion** (the orchestrator confirms it, build-conformance
   §4) and phrased to the operator as a question, **never** a whole-repo
   dead-code verdict and **never** "any code not tracing to a `locked` row" (whole-repo reachability and
   dead-code health are `technical-integrity`'s referent-free concern, lens 3 above). Like
   `spec-conformance` it **re-derives from the `docs/spec/` span, never the matrix rows**, judges **only
   criteria whose row is `locked`**, and is the disclosed no-op absent a `locked` spec; it **runs together
   with `spec-conformance`** so the systematic and adversarial reads never separate — the independence
   guards the **semantic-misbuild class** that a self-consistent build hides from the mechanical
   [spec-obligation matrix](../../reference/glossary.md) and can slip past the demonstration harness
   ([R16](../../reference/risks.md)). *Catches:* a build that passes its own tests but implements the spec wrongly,
   or ships a surface the spec never asked for.

### Dry-run capability — read-only means no mutation, not no execution

A lens may need to **run the code to judge it**. "Read-only reviewer" is the rule that a reviewer never
mutates the work under review or repo-authoritative state — **not** a ban on execution. A lens may execute
the suite in an **ephemeral, discarded worktree** and report the results: that is *reporting findings*, not
*writing the artifact*. Build orchestration already isolates work in throwaway worktrees on short-lived
branches, and the orchestrator remains the single writer of final commits, so the
[agents](../systems/surfaces/agents.md) surface needs no change to permit this — a lens that
dry-runs simply carries a `permissions` grant that includes execution in a scratch worktree while excluding
writes to the PR branch. Because executing the operator's code can have side effects a non-engineer would
not anticipate, a dry-run is **disclosed to the operator in plain language** — that the engine ran their
code in a throwaway copy to judge it — through the gate's operator-facing rendering
([build orchestration](../systems/lifecycle/build-orchestration.md)), never run silently.

### Depth is proportionate

How many lenses run is risk-proportionate and operator-gated at the plan-gate risk assessment; a trivial
change runs none. A change with no `locked` spec to check against — none exists, or the pointer reaches only
a `draft` — makes both `spec-conformance` and its paired `divergence-hunter` a **disclosed no-op** ("no spec
is locked to check against"), never a silent green pass ([D-244](../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)).

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Judgment above mechanics** — the lenses judge; the validation suite and CI gate; no duplication. | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
| **The conformance guard** — `spec-conformance` (the systematic reviewer) and `divergence-hunter` (its adversarial, run-together counterpart) judge built-vs-the-`locked`-spec from two decorrelated cold contexts and restate verified-versus-unverified criteria so a thin spec cannot manufacture false confidence; together they are the **judgment** legs of the [conformance-enforcement floor](../../reference/glossary.md), whose mechanical legs are the criterion-granular [spec-obligation matrix](../../reference/glossary.md) and the deployed-environment demonstration harness ([D-244](../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)) — full rigor against a `locked` spec, a disclosed no-op without one. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Dry-run is allowed** — read-only is no-mutation, so a lens may execute in a discarded worktree. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **File-drop, derived roster; reviewers report, the orchestrator decides.** | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
