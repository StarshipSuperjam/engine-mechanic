---
status: locked
---

# External contribution

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-06-06 by [decision 0184](../../../adr/0184-resolve-the-d-183-issue-authoring-grammar-correction-landed.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

The operating arrangement in which the Engine contributes to a **product repository the operator does not
own** — an open-source project, or the engine-mechanic building engine-template itself. It is the
[contributor-not-component principle (§13)](../../../principles.md) made operational: where greenfield and
brownfield ([provisioning](../infrastructure/provisioning.md)) co-locate the Engine with a product
the operator *owns*, external contribution carries the Engine's full substrate while the product lives in a
repo it can only contribute *to*. It is **fork-native**, reusing the locked delivery, topology, and lifecycle
machinery rather than adding new grammar; the genuinely new obligations are keeping the Engine out of the
upstream pull request and a trust model whose hard gate is the *upstream project's*, not the operator's.

## Behavior

### The fork-native arrangement

The operator forks the upstream project (and so **owns the fork**); the Engine is **brownfield-installed into
that fork** ([provisioning](../infrastructure/provisioning.md)). The fork is therefore an ordinary
same-repo deployment — product source at the root, the Engine in its `.engine/` corners
([repository-topology](../infrastructure/repository-topology.md)), the full cognitive substrate
committed exactly as designed. Product changes reach the un-owned upstream as a **cross-fork pull request
carrying only product-path changes** (`upstream ← fork:feature`). Nothing about the Engine, its substrate, or
its lifecycle changes shape; what changes is *where the merge gate lives* and *that the Engine must not ride
the contribution upstream*.

### "Upstream" has two senses — keep them apart

The locked distribution model calls a generated repo "**detached** (no upstream remote)"
([provisioning](../infrastructure/provisioning.md)), but that statement is scoped to the
**engine-update channel**: engine improvements arrive by tagged-release overlay, never by `git pull`, and
that is **unchanged here**. A fork-native deployment additionally carries a **product-project upstream** — the
repo it contributes to — used *only* for contribution, never for engine updates. The Engine still updates by
overlay; the product upstream is purely a contribution target. (The locked
[provisioning](../infrastructure/provisioning.md) doc carries this "detached" disambiguation as an
additive cross-reference, and [engine-architecture](../../../architecture.md) §3 reflects it.)

### Keeping the contribution clean

The Engine's committed files — `.engine/`, `.claude/`, engine-owned `.github/`, the root `CLAUDE.md`, and the
committed [state](../cognitive/state.md) and [knowledge](../cognitive/knowledge.md)
entities — live in the fork and **must never appear in the upstream pull request**. Two mechanisms keep the
contribution clean:

- **Engine-free product branch.** Product feature branches are cut from the upstream's default branch, which
  carries no engine files — so the branch is **engine-clean by origin**. The Engine runs from its own fork-main
  context (where its config and substrate live) and authors product-only commits onto that branch; its own
  substrate updates ([state](../cognitive/state.md), [knowledge](../cognitive/knowledge.md)
  entities) commit to fork-main, never the product branch. Because the product branch holds no engine surfaces,
  knowledge's commit-boundary regeneration — which runs in the Engine's fork-main context — produces nothing on
  it; **no change to knowledge's behavior is required**. The concrete worktree/branch mechanics are a
  build-spec leaf.
- **The upstream-clean nudge.** A local pre-submission [check](../surfaces/check.md) whose predicate
  is the file-precise CODEOWNERS engine-owned set the
  [topology](../infrastructure/repository-topology.md) already derives: if the outgoing diff touches
  any engine-owned path, it warns in plain language with the offending paths, *why it matters*, and the fix. It
  is a **[§6](../../../principles.md) local nudge, not a hard gate** — a leaked engine file is a hygiene
  failure, not a weakening of the fork's own guardrails, so [§15](../../../principles.md) does not apply.
  Cleanliness is therefore **posture, not a mechanical guarantee**: the branch is engine-clean by origin, the
  nudge catches an accidental engine path (a stray add, or a back-merge of the fork's engine branch) before
  submit, and the **backstop is the upstream's own review** — a maintainer would reject a pull request that
  adds `.engine/`. The nudge self-declares its suite ([§14](../../../principles.md)). As built, that suite is
  `pre-close` — collected on **every clean turn-close**, with no contribution-context gate — so the nudge can
  fire over ordinary work in the operator's own repository, where its cross-fork wording overstates the
  situation; the meaning stays fixed to an outgoing cross-fork contribution, and the context-blind message is
  tracked upstream as [engine-template#777](https://github.com/StarshipSuperjam/engine-template/issues/777).
  The [telemetry](../guardrails/telemetry.md) finding fires at **submission**, over a real outgoing diff —
  the submit tooling's duty, whichever way the operator decides — while the pre-close validator run
  deliberately emits none, keeping close's a-local-run-reaches-no-GitHub-event invariant.

### Following the host's conventions

A contributor adapts to the project it joins — it does not impose its own forms on a repo it does not own
([§13](../../../principles.md)). So the Engine authors its cross-fork pull request to the **upstream's own
pull-request template** (honoring its `CONTRIBUTING` and any DCO/CLA, already owned above), falling back to the
Engine's own PR shape **only when the upstream has none**. The upstream's templates are committed files
readable in the checkout, so this needs no new machinery. The Engine's *own* PR-body and engine-authored-issue
body contracts ([control-plane](../infrastructure/control-plane.md)) govern the **owner's own** repo,
never a contribution to someone else's. The upstream's **issue** templates govern when the Engine files an
*issue* upstream — a first-class second flow the module ships, with its own runbook and tooling that detect
and fill the target project's issue templates — though the contribution itself is a pull request, so the
upstream PR template is what governs a submission. Like the upstream-clean nudge, this is **posture, adding
no wiring or check**, backstopped by the upstream's own review.

### Trust — two gates, named honestly

The unbypassable human gate of every owned-repo deployment is the operator's own protected-branch merge
([§6](../../../principles.md)). Here the operator does not own the upstream, so the gates split:

- **Contributor-side (the operator's own, configurable).** The fork's branch protection plus the Engine's
  pre-submission checks — the validation suite and the upstream-clean nudge — run *before*
  the operator submits. This is the side the operator controls. (The Engine's own PR-body completeness gate
  binds the submission only when the upstream is the engine's own home; for any other upstream, the
  upstream's template governs, as above.)
- **Acceptance (the upstream's, not configurable).** For a **governed** upstream the real mechanical wall is
  the upstream project's **own required checks** (which run in the upstream's context for a fork pull request
  regardless of the fork's settings) **plus its maintainers' review** — a genuine [§6](../../../principles.md)
  human gate, where the reviewing human is simply not the operator. For an **ungoverned** upstream (no review,
  no checks) the acceptance gate is vacuous, and the honest line ([§7](../../../principles.md)) is that the
  operator's **fork-side checks are the only real quality gate** — never dressing an unreviewed merge as a
  trust gate.

The engine-mechanic sits at the well-governed end (engine-template carries the Engine's own stage-0 /
[control-plane](../infrastructure/control-plane.md) governance); an arbitrary open-source project
sits anywhere on the spectrum, surfaced honestly to the operator.

### The operator's view

Because the operator never merges their own work here, the mode owns plain-language narration so a
non-engineer is never misled ([§12](../../../principles.md) leak guard):

- **Submitted is not accepted** — narrated **at submission and on each status check** (not parked in a doc):
  "*I've opened the pull request; the maintainers decide whether it lands — that may take a while or be
  declined, and that's normal. Your fork already has the work — and if it's declined you keep it, and can
  revise or resubmit.*"
- The **ungoverned-upstream honesty** line, in plain words, when the upstream requires no review.
- The **upstream-clean nudge** explains what it caught, why it matters, and the next step — never a bare block.
- Every mechanical step a non-engineer cannot do by hand — the two-base branch flow, a rebase onto a moving
  upstream, a merge conflict, a DCO/CLA sign-off — is **owned by the Engine** and, when a genuine decision is
  needed, **degrades to a plain "I need a decision from you" prompt**, never a raw git conflict.

### Degradation

If the upstream is unreachable or unresponsive, the work is fully committed and merged on the operator's own
fork (git-native), so the operator **owns a working fork** regardless — stronger degradation than the
owned-repo case ([§5](../../../principles.md)). Surfacing an unfilable or stalled submission rides the
existing finding-disposition / [telemetry](../guardrails/telemetry.md) channel; the Engine drafts,
the operator files via their own `gh`.

### The cognitive substrate

The substrate's **home is unchanged**, because the fork *is* a same-repo deployment:
[memory](../cognitive/memory.md) (a local gitignored ledger) and
[attention](../cognitive/attention.md) (a committed policy plus a ranking function) live with the
Engine wherever it runs; [state](../cognitive/state.md) and
[knowledge](../cognitive/knowledge.md) keep their committed home in the fork's `.engine/` (knowledge
regeneration runs in the fork-main context and never lands on the engine-free product branch, as above). This
is the *purer* [§13](../../../principles.md) reading — the substrate is the contributor's, filed in the
contributor's own repo, never in the product the contributor does not own.

What the substrate **does not** gain cross-repo is *structural knowledge of the un-owned product's code*.
[Knowledge](../cognitive/knowledge.md) is the engine's derived **self-map of governed surfaces**
([D-042](../../../adr/0042-procedural-content-grounding-surface-cluster-designed-the-bo.md)), not a graph of product code — and you cannot externalize
product-describing surfaces into a repo you do not own. So the Engine reasons over an external product's
structure by **reading the upstream checkout live** (plus its [memory](../cognitive/memory.md) of the
work), not from a committed product graph. The post-v1
[product-knowledge-graph](../../modules/product-knowledge-graph.md) module
([D-105](../../../adr/0105-hold-a-post-v1-product-knowledge-graph-module-stub-product-s.md)) is the planned remedy — an engine-owned, gitignored structural graph
derived from the (un-owned) checkout. The **engine-mechanic is the exception** (below).

### The engine-mechanic

The self-hosting special case: a deployed Engine instance whose **product is the engine-template repo
itself**, which it builds and submits pull requests to. It is a **separate-workspace variant** — its product
is a checkout of engine-template it contributes to, *not* a fork it brownfields the Engine into (that would
install the Engine into a repo that already is the Engine). It is therefore **non-reflexive**: the dependency
arrow runs mechanic → template ([§13](../../../principles.md)), and the template ships and instantiates
standalone, unaware of the mechanic. Its trust base is engine-template's **own** merge gate plus maintainer
review (the well-governed end of the trust spectrum).

As built, the mechanic does **not** run this module's cross-fork runbook: because it *owns* its
engine-template product as a separate checkout, both external-contribution runbooks carve it out
explicitly, and it opens a **direct pull request into its own checkout** through
[build-orchestration](build-orchestration.md)'s owned-product arm. What it shares with an external
contribution is the trust base, not the submission path.
What keeps self-improvement honest is **not** a machine proof but an **independently-trusted human gate on the
product repo**: every change the mechanic proposes is reviewed and merged by the engine-template maintainer
*before* it is released, so the version any instance later upgrades to was human-ratified on engine-template,
not vouched for by the artifact that authored it. The operating rule that the mechanic **pulls only released,
ratified versions** (never its own un-ratified output) rides that human gate — it is human-review-grade
([§15](../../../principles.md)'s *cannot weaken silently* tier), honestly not a falsifiable guard. This mode
resolves the mechanic's design and home. The **defined point** at which construction hands off from the
stage-0 harness is **M1, the self-construction crossover**
([D-107](../../../adr/0107-author-the-wbs-module-build-order-the-builder-crossover-reso.md)): at M1 genesis hands off to the nascent engine building itself
**in-repo**, which carries the rest of v1; the separate mechanic stands up **post-v1** as the build locus.
The module build-order sets both timings.

**The mechanic is also the one product whose structure the substrate fully externalizes.** The cross-repo
knowledge gap above is real for a *code* product — code is not governed surfaces, so the engine's self-map
[knowledge](../cognitive/knowledge.md) cannot cover it. But engine-template **is** made of governed
surfaces, exactly what the knowledge graph speaks, so the product **self-describes**: the engine-template the
mechanic builds carries its **own** knowledge graph (a self-map of its own contracts, policies, and other
governed surfaces), which *is* a structural map of the product. Two graphs are in play — the engine version the mechanic *runs* maps its
own machinery, and the **engine-template checkout it builds** maps the product; the second supplies the
product-structure knowledge. Whether the mechanic's generator is pointed at the product checkout's surfaces is
a build-spec detail, but the point is structural: unlike any code product, that knowledge is **derivable,
because the product is an engine** — so for the mechanic the
[product-knowledge-graph](../../modules/product-knowledge-graph.md) gap largely closes without that
module.

### Packaging

External contribution is an **optional module**
([external-contribution](../../modules/external-contribution.md), `depends: core`), not a core
capability: a deployment building the operator's *own* product never contributes to a repo it does not own, so
the cross-repo machinery is a genuine extension and the contagious core stays minimal
([§12](../../../principles.md)). The module provides the upstream-clean nudge, the cross-fork submission
tooling, the upstream **issue-filing** flow (its own runbook and tooling, live-gated on the operator's
`gh`), and the operator-narration; the cross-fork pull request *is* the
[build-orchestration](build-orchestration.md) close in shape (a submitted PR), but the
**unbypassable merge wall moves from the operator's own merge to the upstream's** — a substantive change the
locked [build-orchestration](build-orchestration.md) close model carries
([D-104](../../../adr/0104-phase-c-cross-reference-the-external-contribution-mode-into.md)), not a mere cross-reference. The other three locked touches are minimal
additive cross-references that likewise live in their locked docs (provisioning's "upstream" disambiguation,
control-plane's upstream-acceptance note, topology's CODEOWNERS-predicate note).

### Build-spec leaves

- the **upstream-clean nudge** kind realization and `message` wording;
- the concrete **two-base branch / cross-fork submission** tooling form, and the `gh` permission it needs;
- the **operator-narration** copy (submitted-is-not-accepted, the ungoverned-upstream line, the decision
  prompts);
- the **worktree/branch mechanics** by which the Engine authors product-only commits onto the engine-free
  branch from its fork-main context;
- the **detection of the upstream's pull-request template / `CONTRIBUTING`** and the conformance of the
  authored PR body to it (fall back to the Engine's own shape when absent).

## Operator and automatic workflow routing

**Current disposition: automatic model routes.** Reached by intent through `engine-file-upstream-issue` (the target project's own Issue procedure) and `engine-submit-upstream-contribution` (the submission path); when the add-on is absent its setup is the generated `engine-setup-external-contribution` route — per decision 0336. These upstream routes follow the target project's templates and filing authorization and never use the Engine's own Issue helper.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Reuses the locked machinery** — brownfield install, namespaced confinement, file-precise CODEOWNERS, §13, degrade-to-git-native — adding no new grammar; the genuinely new pieces are the upstream-clean nudge and the split trust model, and build-orchestration's locked close model carries the one substantive change (the merge wall moves to the upstream, [D-104](../../../adr/0104-phase-c-cross-reference-the-external-contribution-mode-into.md)). | No merge-gated check asserts the reuse claim; your read that the module adds no new grammar carries it. Partial support: the `module-manifest` and `self-map-drift` checks (hard, CI) gate the module's declared shape and its `depends: core` structure. | operator |
| **The Engine stays off the contribution by posture, backstopped by the upstream** — the product branch is engine-clean by origin, the §6 nudge catches an accidental engine path, and the upstream's own review is the backstop; cleanliness is honest posture, not a mechanical guarantee. | Your observation carries it — the `upstream-clean` check is by design a soft pre-close nudge, never a merge gate (the criterion's own tier), and the upstream's review is the backstop no local check can replace. | operator |
| **Follows the host's conventions** — the cross-fork pull request adopts the upstream's PR template (and `CONTRIBUTING` / DCO-CLA), falling back to the Engine's own shape only when the upstream has none; the Engine's own [control-plane](../infrastructure/control-plane.md) PR/issue-body contracts govern only the owner's repo ([§13](../../../principles.md), posture, backstopped by the upstream's review). | Your read of an authored submission carries it; template detection and fill live in the submission and issue-filing tooling, ungated by any check, and the engine's PR-body gate binds the owner's repo only. | operator |
| **The hard gate is the upstream's** — for a governed upstream, its own checks plus review; for an ungoverned one, the honest line is that the fork-side checks are the only real gate ([§7](../../../principles.md)). | Not assertable from this repo — the gate is the upstream project's own required checks and maintainer review, outside the engine's control; your read of the upstream's governance carries it. | operator |
| **The operator is never misled or stranded** — submitted-is-not-accepted narration, plain-language nudges, decisions surfaced (never raw git), and a working fork on any upstream failure. | Your observation of the narration carries it; the external-contribution policy holds this at enforcement-tier posture, and no detector grades whether the narration was honest. | operator |
| **The engine-mechanic is non-reflexive; its trust base is engine-template's own human review** — as built it runs [build-orchestration](build-orchestration.md)'s owned-product arm (a direct pull request into its own checkout, not this module's cross-fork runbook), and the rule that it upgrades only to human-ratified releases rides that independently-trusted gate (human-review-grade, not a machine proof). | Your observation carries it — both external-contribution runbooks carve the mechanic out explicitly, and the trust base is engine-template's own protected-branch review, which no check in this repo can assert. | operator |
| **Maturity is disclosed at install** — per [R14](../../../reference/risks.md), the cross-repo path ships **un-exercised end-to-end at v1**; the install disclosure states this in plain operator language (the [clean-code](../../../reference/module-catalog.md) disclosure precedent), so opting in is informed consent, never trust in a maturity the path has not earned. | Your read of the install disclosure carries it — the module catalog's copy states the first contribution would be the live step's first run anywhere. Partial support: the `in-tool-demo-failure-path` check (hard, CI) keeps the nudge demo falsifiable and the `provisioning-catalog` check gates the catalog's well-formedness — neither asserts the disclosure's content. | operator |
| **Optional, not core** — [§12](../../../principles.md); opt-in is consent, and removal leaves the operator's own product unaffected. | Your observation that removal leaves your product untouched carries it. Partial support: the `module-manifest` check (hard, CI) and the self-map attest the module's optional, core-dependent structure. | operator |
