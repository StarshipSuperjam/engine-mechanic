# Risks and technical debt

Known risks to the design and their mitigations. A risk graduates to a decision (and leaves this
register) once its mitigation is settled and recorded in `decision-log.md`.

## R1 — Control-plane bootstrap is skipped

**Risk.** Branch protection does not travel with the template; if the operator never applies it, the
protected branch is unprotected and the AI can merge unverified work — defeating every guardrail
beneath it. The non-engineer is the least likely to run a `gh` command unprompted.
**Severity.** High — it undermines the trust proposition wholesale.
**Mitigation direction.** The [control-plane](../spec/systems/infrastructure/control-plane.md) locks the
bootstrap contract: the branch ruleset is applied by an operator-privileged actor (the default Actions
token cannot; it needs repository-administration capability — the `repo` scope or fine-grained
Administration:write, which the operator's `gh` carries by default), a committed CI guard on the
evaluated-rules endpoint fails loud until protection is detected, and the unprotected state is surfaced to
the operator in plain language continuously. [Provisioning](../spec/systems/infrastructure/provisioning.md)
settles the *mechanism*: the operator's own `gh`, engine-orchestrated, applies the ruleset — usually with
the `repo` it already holds, falling back to an operator-approved scope grant only when the capability is
absent (the engine cannot self-grant) — with attempt-now-but-defer-is-common backed by the guard + boot
nag, and a degrade-and-disclose path where the capability is ungettable. One consequence to track
elsewhere: in solo mode the engine inherits the operator's standing `repo` (full repository control, of
which ruleset-admin is one part) — a settings-tampering surface now governed by the guardrail-integrity law
([principles §15](../principles.md), [D-051](../adr/0051-guardrail-integrity-the-builder-cannot-silently-weaken-its-o.md)): a weakening change to enforcement config or the
ruleset hard-blocks the merge until the operator's informed consent, and team mode closes the sub-vector
structurally. The same §15 class covers a **check-coverage narrowing** — e.g. the Dependabot PR-contract
exemption ([D-207](../adr/0207-authorize-the-dependabot-pr-contract-exemption-a-ci-author-a.md)): introducing or widening a required check's exempt-author set is a
weakening change gated by the acknowledgment, and because the exempt check stays a **disclosed not-applicable
result** the operator is never trained that a green check is uniformly *verified*.
[Provisioning](../spec/systems/infrastructure/provisioning.md) is now **locked**
([D-077](../adr/0077-lock-the-provisioning-system-terminal-foundation-lock-the-bo.md)), fixing the bootstrap mechanism, the degrade-by-cause banner, and the
instantiator/boot surfacing split; this risk stays open until the first-run UX lands.

## R2 — Memory loss / portability for a non-engineer

**Risk.** Experiential memory is local and gitignored (correctly — it should not travel or be
review-gated). But a disk failure or machine switch loses "how did I get here", and the operator has
no backup discipline.
**Severity.** Medium — degrades continuity, does not strand boot (state is committed).
**Mitigation direction.** Make memory's canonical form an append-only **NDJSON ledger** (the SQLite
index is a derived, rebuildable cache), so backup/restore is "copy the ledger / rebuild the index" and
portability across machines is the same move — keeping the data out of git. **Settled** by
[D-061](../adr/0061-lock-the-memory-system-wave-2-the-episodic-ledger-store-q3-b.md): the mechanism is decided — automatic, per-project-namespaced export of the
ledger to an operator-configured off-repo private destination (v1 default a **shared cross-project vault**, or a per-project private repo, via the
operator's own `gh`), restore = replace the ledger + rebuild the index, reused as
[Provisioning](../spec/systems/infrastructure/provisioning.md)'s [D-048](../adr/0048-provisioning-delivery-designed-end-state-brownfield-capable.md) migration
reversal, with operator-facing floors fixed in [memory](../spec/systems/cognitive/memory.md).
[D-081](../adr/0081-re-litigate-memory-ledger-write-integrity-law-reframe-usage.md) firms this further: a **ledger write-integrity law** (serialized atomic appends;
line-resilient reads) protects the canonical store from torn or concurrent writes, and the restore floor
states its bound honestly — automatic restore-offer needs the project repo present (its committed
destination pointer), so a bare machine with nothing cloned first requires the repo. R2 now
**closes when the export path is built** (a build / provisioning bootstrap-UX matter), no longer an open design
gap. Tracked in [memory](../spec/systems/cognitive/memory.md) and
[provisioning](../spec/systems/infrastructure/provisioning.md). [D-264](../adr/0264-authorize-git-native-retention-for-the-pre-migration-memory.md) hardens the
migration-reversal half: the pre-migration snapshot is a **distinct retained tag the routine backup never
overwrites**, so a routine backup landing between an engine update and the operator's undo can no longer
clobber the restore point. Its one **owned residual** — because a migration *reshapes* the ledger,
successive retained snapshots largely do not dedup, so the shared vault grows ~linearly in
(migrations × ledger size) — is bounded by memory's pruning policy (retain at least until no
code-older-than-data mismatch can still cite the snapshot; the numeric cap a build-spec leaf).

## R3 — "Self-healing" over-promise

**Risk.** Describing telemetry as self-healing misleads the operator into thinking they can walk away
from problems the engine only *reports*. Trust built on a false claim breaks loudly.
**Severity.** Medium — expectation risk, not a mechanism failure.
**Mitigation direction.** Name and build the honest loop (detect → triage → surface → AI-remediate →
validate); never claim autonomous correction. **Firmed** by [D-075](../adr/0075-lock-the-telemetry-system-guardrails-arc-head-the-triage-vol.md): telemetry is locked
with the honest loop, and the triage-volume resolution explicitly rejects both autonomous state-alteration
("self-healing") and any volume cap that would have telemetry *judge* which signals matter — its only
autonomous write stays open/update/auto-resolve of a deduped issue. Closes when the loop is built. Tracked
in [telemetry](../spec/systems/guardrails/telemetry.md).

## R4 — Attention left as hardcoded constants

**Risk.** If prioritization stays buried as static budget constants, the weakest cognitive leg never
matures, and the AI rabbit-holes or surfaces the wrong things first.
**Severity.** Medium.
**Mitigation direction.** Make attention an explicit **policy plus function** — a committed,
governed allocation/ranking policy (budgets, weights, trim order, debt-blocking rule) read by a
deterministic ranking function — rather than constants buried in boot code; this is the engine's
instance of the *context engineering* discipline ([D-033](../adr/0033-ground-the-cognitive-substrate-in-established-standards-line.md)). **Firmed** by
[D-029](../adr/0029-cognitive-substrate-is-one-workflow-a-2-store-1-register-1-c.md)/[D-030](../adr/0030-memory-ledger-canonical-observe-don-t-predict-capture-lexica.md); closes when the policy and function are built **and calibrated against the build-session fixture that establishes the ordering is correct** ([D-083](../adr/0083-re-litigate-attention-honesty-clarification-reference-time-a.md)) — an explicit, deterministic policy is necessary but not sufficient; until the fixture exists, "surfaces the right things first" stays unproven.
Tracked in [attention](../spec/systems/cognitive/attention.md).

## R5 — Module install as surgery, not mechanism

**Risk.** If modules model only files and dependencies (not wiring), every install/uninstall requires
hand-editing settings, MCP registration, check-suites, and the ontology — reintroducing the
"every feature is a refactor" failure that sank the prototype's breadth.
**Severity.** High — it is the structural failure mode we are restarting to avoid.
**Mitigation direction.** Manifests declare wiring declaratively + reversibly; a permanent shared
wiring library applies/reverses it with keyed, idempotent edits to shared files; a coherence validator
confirms the installed set. The sharpest reversibility win is that **check-suite membership needs no
wiring at all** — a [check](../spec/systems/surfaces/check.md) rule self-declares its suites, so install
is a file drop and uninstall a file removal, with the roster derived rather than mutated. This no-wiring
win is generalized by the [derived binding by presence principle](../principles.md): the agent roster and
[interface](../spec/systems/surfaces/interfaces.md) implementations bind the same way — by presence, not
wiring — so the *discovery* side of install carries no surgical risk at all (the closed seam handles only
genuine shared-state edits). The
[module-system](../spec/systems/grammar/module-system.md) design **firms** this mitigation — a closed seam
vocabulary, engine-namespaced-identity keying, manifest-derived reversal, and a directly-callable coherence
check, and the now-locked [provisioning](../spec/systems/infrastructure/provisioning.md)
([D-077](../adr/0077-lock-the-provisioning-system-terminal-foundation-lock-the-bo.md)) specifies the appliers/reversers that apply and reverse it — but it does **not**
close until they are built. Tracked in
[module-system](../spec/systems/grammar/module-system.md), [hooks](../spec/systems/infrastructure/hooks.md),
and [provisioning](../spec/systems/infrastructure/provisioning.md).

## R6 — Scope re-creep

**Risk.** The prototype grew too broad to control. The same forces (every capability feels worth
building) apply here.
**Severity.** High — it is the original failure.
**Mitigation direction.** Every system and module must serve a quality attribute in
`goals-and-quality.md`; the WBS module build-order layers strictly on the
dependency graph; additions that serve no attribute are rejected at the decision log. Defer is a build-order word, not a scope cut — the
end-state stays fully specified, but capability layering keeps each step controllable. The authoring
grammar adds three running controls: the contract-threshold policy keeps decision records exceptional,
the finding-disposition scope boundary stops a session's claim from expanding silently as it
fixes what it finds, and the [operations](../spec/systems/surfaces/operations.md) anti-sprawl heuristic
(an audit concern) keeps the procedural-body surface from accreting single-referrer runbooks that are
really one skill's private depth. (See [contracts](../spec/systems/surfaces/contracts.md), [policies](../spec/systems/surfaces/policies.md), [operations](../spec/systems/surfaces/operations.md).) The stage-0 build harness operationalizes the WBS-layering control for the template's *own* construction: building proceeds PR-gated, one step at a time, under a hand-built governance harness the real modules supersede in graph order, so construction cannot sprawl ahead of the dependency graph.
**Firmed at the audit layer** by [D-076](../adr/0076-lock-the-audits-system-re-founded-for-the-deployed-repo-hygi.md): the [audits](../spec/systems/guardrails/audits.md)
concern-list's own growth is bounded by deliberate reviewed authorship plus reflexive function-probe
retirement (the contract-threshold mechanism applied to concerns), and the riskier deployed-Engine
**auto-calibration** ambition — re-weighting from a project's own observed usage, which would over-fit a
single project and over-weight the contagious core ([§12](../principles.md)) — is deliberately held **out of
required core**, deferred to a future optional module ([Q17](open-questions.md)) rather than built
speculatively in v1. Its determinism-safe *substrate* — the per-project [operator policy-override](glossary.md)
of tuning values — over-fits nothing (a static input, not a learned one), so it rides core
([D-167](../adr/0167-take-up-q17-component-a-authorize-a-five-foundation-re-litig.md)); only the learning half is held out. The audit further counters preserve-drift by
weighing **its own prior digests** as over-time corroboration of a retire case — strengthening the
retirement-default read without crossing into that held-out learning loop: persistence of an observed condition
corroborates, a fresh function-probe still decides, and nothing is re-weighted or persisted
([D-233](../adr/0233-authorize-the-audit-over-audit-re-litigation-feed-the-period.md)).

## R7 — Engine upgrade supply chain and template drift

**Risk.** A generated repo is detached from the template (no upstream remote). Without an upgrade path it
**drifts** — never receiving fixes to the foundations or modules as the template evolves. With one, the
updater pulls **executable engine code** (validators, hooks) from the template's releases, which is a
supply-chain surface, and a botched overlay could clobber operator config or product paths.
**Severity.** Medium — drift erodes trust slowly; a bad overlay is contained by review and reversibility.
**Mitigation direction.** The whole engine is versioned packages with `migrations`; the
[provisioning](../spec/systems/infrastructure/provisioning.md) updater pins to a **tagged release**,
overlays **only engine-namespaced paths** (preserving operator config and gitignored data), runs the
**coherence validator**, and lands a **reviewed PR** through the [control-plane](../spec/systems/infrastructure/control-plane.md)
gate; it **degrades** to the current version when the release source is unreachable. **Which** repository
the source resolves from is the engine's **home repository** recorded in the manifest (never the deployed
repo's own `origin`); because that coordinate selects where executable engine code is fetched, it is itself
a [§15](../principles.md) guardrail-integrity file — a repoint is a weakening-class change gated by the
operator's weakening acknowledgment — so the home is a reviewed committed control, not an implicit remote.
The versioned-package
model, the engine-manifest lockfile (per-package versions), and the **overlay-filtered-by-installed-set**
rule (no resurrection of deselected modules) **firm** this mitigation, as does the **backup-first migration
reversal** (a data migration snapshots the affected store before mutating, to a **distinct retained copy
the routine backup never overwrites** ([D-264](../adr/0264-authorize-git-native-retention-for-the-pre-migration-memory.md)), and a migration-owned
version-stamp check — surfaced by [boot](../spec/systems/lifecycle/boot.md) — flags a
code-reverted-but-data-not-restored mismatch with the restore command, since PR-revert restores
code but not gitignored data); the now-locked [provisioning](../spec/systems/infrastructure/provisioning.md)
([D-077](../adr/0077-lock-the-provisioning-system-terminal-foundation-lock-the-bo.md)) fully specifies the updater, but it stays open until it is built. The
preserved-config set now includes the **[operator policy-override](glossary.md)** ([D-167](../adr/0167-take-up-q17-component-a-authorize-a-five-foundation-re-litig.md)):
the overlay preserves it like any operator config, and because it is a *committed* file (reverting with the
PR) it needs no backup-first migration — a value-schema change that strands an override key falls back to the
shipped default and is surfaced at boot, per-key, no reshaping. Tracked in
[provisioning](../spec/systems/infrastructure/provisioning.md) and
[module-system](../spec/systems/grammar/module-system.md).

## R8 — Knowledge-graph hub-explosion at scale (conditional)

**Risk.** A *dense-graph* representation of the knowledge graph can degrade retrieval as it grows: a few
highly-connected "hub" nodes come to dominate traversal and drown relevance — the pathology the
spreading-activation research line names "hub explosion."
**Severity.** Low and conditional — v1's knowledge graph is plain per-surface JSON at one-project scale
with derived mechanical edges, **not** a dense semantic graph, so the pathology does not bite unless a
dense-graph representation is later adopted.
**Mitigation direction.** Keep the knowledge **representation/retrieval leaf swappable** — the same seam
that lets a richer engine slot in also lets it be bounded (sparsity, capped traversal, activation with
inhibition are candidate swap-ins, tracked in [open-questions](open-questions.md)). The
foundational eADR canon does **not** instantiate this condition — it derives
no forward `ratifies` edge (linkage is reverse-citation only), so it adds entities without hub fan-out
([D-169](../adr/0169-add-the-foundational-eadr-canon-the-engine-ships-its-own-why.md)). The [D-203](../adr/0203-enrich-the-derived-knowledge-graph-schema-a-build-spec-leaf.md) schema enrichment likewise does **not**
instantiate this condition: it stays sparse and declared-only, adding **forward edges** (`supersedes`
among non-canon contracts) and **node attributes** (`status`, check `tier`, type discriminators,
identity `title`) — not a dense semantic web — so it adds no hub fan-out, and its new edge types stay
off the cold-start adjacency walk. [D-224](../adr/0224-direct-the-structural-neighbors-orientation-render-to-traver.md)'s reverse-adjacency render likewise adds no
hub fan-out — it traverses today's edges in *reverse direction* (no new edges, no new edge types) within
attention's fixed structural-neighbors slice, so it neither densifies the graph nor enlarges the
cold-start walk. Tracked in
[knowledge](../spec/systems/cognitive/knowledge.md); opened by [D-033](../adr/0033-ground-the-cognitive-substrate-in-established-standards-line.md).

## R9 — Product design-artifact drift is unmonitored by design

**Risk.** [product-design](../spec/modules/product-design.md) authors product-owned artifacts (the committed
`docs/spec/` corpus, the arc42 doc, C4 diagrams, the ADR stream, the Diátaxis tree). The engine
**mechanically validates the spec corpus's FORM** ([D-244](../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)) but runs **no**
[audits](../spec/systems/guardrails/audits.md) cold-context **quality** probe on any of them — so an arc42 doc
or ADR the engine wrote, or a locked spec whose form still passes, can silently **drift from the product's
current reality** as the product changes.
**Severity.** Low — it degrades a product-side convenience, never the engine or the build path; product-doc
freshness is the product's own responsibility under [asymmetric awareness](../principles.md).
**Mitigation direction.** Stated honestly rather than papered over ([principles §7](../principles.md)), on a
clean line — the engine validates product-artifact **form**, never **freshness or correctness**.
**Mechanical form-validation of the spec corpus is in scope**: read-only,
[migration-discipline](../spec/modules/migration-discipline.md)-shaped checks that the spec is well-shaped
([D-244](../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)), wall-safe because they inspect a product-owned artifact and own nothing
([D-142](../adr/0142-lock-migration-discipline-product-migration-governance-the-s.md): the removal test is *strengthened*). **Semantic freshness is unmonitored by the
Engine by design** — extending engine **quality-audit** machinery (the cold-context "is this still right /
has it gone stale" probe) onto product artifacts would breach the
[engine/product wall](../spec/systems/infrastructure/repository-topology.md) and [§12](../principles.md). The
Engine *contributes* an update when it next touches that area, as a contributor would, but does not own it. A
related durability choice: product C4 defaults to stable mermaid `flowchart` form, not the experimental
`C4Context` DSL, so a non-engineer's diagrams do not break on a renderer bump. Tracked in
[product-design](../spec/modules/product-design.md); opened by [D-065](../adr/0065-product-design-front-door-design-the-q14-intake-module-as-a.md), scope clarified by
[D-244](../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md).

## R10 — Review-roster proportionality for a solo non-engineer

**Risk.** The v1 roster is eight cold-context reviewer lenses across two gates
([design-review](../spec/modules/design-review.md) / [qa-review](../spec/modules/qa-review.md)). Run
indiscriminately, that is slow, costly, and intimidating for a solo non-engineer building something small —
review theatre rather than trust.
**Severity.** Low-to-medium — an untuned default burns the operator's time and budget and erodes the very
trust the lenses exist to build.
**Mitigation direction.** Depth is risk-proportionate and operator-gated in two beats at the plan gate
([build-orchestration](../spec/systems/lifecycle/build-orchestration.md), [D-073](../adr/0073-lock-build-orchestration-wave-3-terminal-and-re-litigate-con.md)): the
orchestrator proposes a **consequence-named depth** (a trivial change runs zero lenses; the "medium default"
is the assessment's proposal over the derived lens set, not a standing list) and the operator approves the
spend **before** it happens, against a plain-language headline and a cost estimate honest about per-gate
batching; **after** the audit the orchestrator synthesizes the findings into one recommended call plus the
trade (never eight raw verdicts), re-engaging the operator only on material findings and always on an
unresolved blocking finding, with every disposition surfaced in the PR **Review record**. Closes when the
roster and the risk-assessment depth proposal are built and tuned. Tracked in
[build-orchestration](../spec/systems/lifecycle/build-orchestration.md); opened by [D-066](../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md).

## R11 — Build-entry verb may be dropped by the model (platform reliability)

**Risk.** A v1 Build-entry vehicle is an operator-typed (operator-only-invocable)
[skill](../spec/systems/surfaces/skills.md) — a mechanism that stops the model from self-electing into
Build. Claude Code has a known quirk where the model sometimes does not honor a user-typed
`disable-model-invocation` skill, so an operator's entry attempt can be dropped.
**Severity.** Low — it degrades the *entry* convenience, never the guardrail: a dropped entry leaves the
session in Explore (the safe default), so the failure is fail-safe, not fail-open.
**Mitigation direction.** Stance defaults to Explore on every ambiguous or failed signal
([modes](../spec/systems/lifecycle/modes.md)), so a missed entry costs a retry, never an unguarded write;
the operator-legible stance readout keeps the still-in-Explore state visible ("*I won't change files
yet*"), and the durable wall is the protected-branch merge regardless of stance. **The verb is not
the sole interactive entry: plan-acceptance ([D-179](../adr/0179-augment-interactive-build-entry-with-plan-acceptance-correct.md)) is the honor-rate-free primary path
(a deterministic plan-exit completion event, not a model-honored flag), so this quirk affects only the
non-plan-mode verb fallback.** Closes when the build-entry verb is built and its honor-rate confirmed
against the shipped platform. Tracked in [modes](../spec/systems/lifecycle/modes.md); opened by
[D-070](../adr/0070-lock-the-modes-system-wave-3-head-three-stances-on-two-axes.md), de-risked by [D-179](../adr/0179-augment-interactive-build-entry-with-plan-acceptance-correct.md).

## R12 — Dependency on research-preview Dynamic Workflows for the eventual parallel substrate

**Risk.** Anthropic's **Dynamic Workflows** is a research preview that could become the natural
coordination substrate for the [build-orchestration](../spec/systems/lifecycle/build-orchestration.md)
parallel-workers strategy (many subagents, intermediate results kept out of the orchestrator's context
window). A preview feature can change shape, gate behind a tier, or not reach GA; designing *toward* it
risks a substrate that never lands. Its context-window-isolation mechanism *is* documented in primary
Anthropic docs; only the deterministic-workflow-file **filename** is secondary-source and
uncorroborated — to confirm against GA documentation before any adoption.
**Severity.** Low — it is an *optimization* of an already-working mechanism, not a load-bearing
dependency. The design names no preview feature in any locked doc; the worker mechanism is described
substrate-agnostically (isolated worktree, Agent-spawned workers).
**Mitigation direction.** Design-for, guard-as-preview: the GA fallback is the **current Agent-tool +
`isolation: worktree`** worker mechanism, which is native and sufficient; never hard-depend on the
preview. Confirm the mechanism against GA documentation before any adoption. The adoption thread is
parked in [Q21](open-questions.md); closes when Dynamic Workflows reaches GA and an adopt/decline call
is made (or when the question is otherwise resolved). Opened by [D-100](../adr/0100-decouple-the-locked-agent-grammar-from-the-model-landscape-m.md).

## R13 — External contribution: engine leak and un-owned upstream trust

**Risk.** In the cross-repo [external-contribution](../spec/systems/lifecycle/external-contribution.md) mode
the Engine works in the operator's fork of a repo it does not own and submits a product-only pull request
upstream. Two surfaces: (a) **engine-file leak** — the fork carries the Engine's committed files (`.engine/`,
`.claude/`, the committed [state](../spec/systems/cognitive/state.md) / [knowledge](../spec/systems/cognitive/knowledge.md)
entities), which must never ride the upstream PR; the product branch is engine-clean by origin (cut from the
upstream's engine-free default), but a **stray add or a back-merge of the fork's engine branch** could carry
engine paths into the contribution; (b) **un-owned upstream trust** — the operator does not control the
upstream's review/CI, so a non-engineer could read "submitted" as "accepted", contribute to an *ungoverned*
upstream whose merge is no real gate, or be blocked late by a per-upstream DCO/CLA that rejects AI-authored
commits.
**Severity.** Low-to-medium — it degrades a *contribution* convenience and an honesty surface, never the
operator's own product or the engine's own guardrails (the fork is a working same-repo deployment regardless).
**Mitigation direction.** (a) The leak is held off by **engine-clean branch origin** (product branches cut from
the upstream's engine-free default; the Engine authors product-only commits onto them from its fork-main
context, so knowledge's regeneration — running in that context — never lands on the product branch, and no
change to the locked knowledge foundation is needed) plus the **[§6](../principles.md) upstream-clean nudge** as a
posture catch (predicate = the [topology](../spec/systems/infrastructure/repository-topology.md) file-precise
CODEOWNERS engine-owned set), **backstopped by the upstream's own review** — honest posture, not a mechanical
guarantee. (b) The trust split is **named honestly** ([§7](../principles.md)): the upstream's
own review/CI is the real wall for a governed upstream (its required checks run upstream-side regardless of
fork settings); for an ungoverned upstream the honest line is that the fork-side checks are the only real gate;
the operator-facing narration states **submitted ≠ accepted** and that acceptance may take weeks or be
declined, surfaces DCO/CLA in plain language, and degrades any conflict/rebase to a plain "I need a decision"
prompt — never raw git. The contribution also **follows the upstream's own PR template / `CONTRIBUTING`** (the [§13](../principles.md) follow-the-host rule — a contributor adapts to the project it joins, falling back to the Engine's own shape only when the upstream has none), posture-level and backstopped by the upstream's review, adding no new surface or check ([D-183](../adr/0183-authorize-the-issue-authoring-grammar-correction-build-issue.md)). Designed in [external-contribution](../spec/systems/lifecycle/external-contribution.md),
the system design is **locked** ([D-121](../adr/0121-lock-the-external-contribution-system-doc-reconcile-the-stal.md)) and the module stays `designed`. **Open until** the module is built and the platform facts are
validated against live GitHub (fork Actions enablement; the three-dot-diff no-back-merge caveat; per-upstream
DCO/CLA acceptance). Tracked in [external-contribution](../spec/systems/lifecycle/external-contribution.md);
opened by [D-102](../adr/0102-cross-repo-external-contribution-as-a-first-class-v1-operati.md).

## R14 — External-contribution / engine-mechanic path ships un-exercised at v1

**Risk.** The build-order model ([D-107](../adr/0107-author-the-wbs-module-build-order-the-builder-crossover-reso.md)) keeps the v1 builder **in-repo**: the nascent
engine builds the rest of v1 under the maintainer merge gate, and the **separate engine-mechanic** build
locus stands up only post-v1. A consequence is that the cross-repo path ships **un-exercised end-to-end at
v1 release**, on two surfaces. (a) **Maintainer-side** — the engine-mechanic's version-separation workflow
(run a released, ratified version N to build N+1 in a separate repo) is *never run during v1 construction*,
so it is un-dogfooded the first time it is relied upon, exactly when it governs the riskiest (foundational)
self-modification. (b) **Operator-side** — `external-contribution` is a shippable v1 optional
(built in v1) an operator can install, yet its cross-repo fork→upstream path shipped
without an end-to-end exercise, so a non-engineer could adopt it trusting a maturity it has not earned.
**Severity.** Low-to-medium — a *confidence* gap on an optional capability and a maintenance terminus, not a
defect in the v1 spine; both surfaces are reversible and gated by human review (the maintainer's, the
upstream's).
**Mitigation direction.** (a) **Post-v1 dogfooding** before the engine-mechanic is trusted for foundational
revision — stand it up and exercise the released-version-N → build-N+1 loop on a non-foundational change
first; the acceptance benchmark ([D-152](../adr/0152-resolve-q15-author-the-pre-release-acceptance-benchmark-the.md)) is the natural home for an end-to-end
mechanic exercise (its self-hosting observation, §3). (b) **Operator-facing maturity disclosure** at install (the [clean-code](../spec/modules/clean-code.md)
disclosure precedent — the project README states what the module has and has not been exercised against),
phrased in plain operator language with **no maintainer vocabulary leaking** ([§12](../principles.md)). Relates
to R13 (the same cross-repo path's leak/trust surfaces) and to the
foundational eADR canon ([D-169](../adr/0169-add-the-foundational-eadr-canon-the-engine-ships-its-own-why.md)) the mechanic reads to
build N+1 — built and stress-tested in v1, but first *relied upon* post-v1 like the rest of this path;
opened by [D-107](../adr/0107-author-the-wbs-module-build-order-the-builder-crossover-reso.md).

## R15 — The seed trust-root is unverifiable by a non-engineer (no engineer available)

**Risk.** The bootstrap's sole human gate is a non-engineer who cannot read code, and no outside engineer is
available ([constraints](constraints.md), [D-136](../adr/0136-re-base-the-bootstrap-trust-model-on-a-sole-non-engineer-gat.md)). The seed (stage 0.0) is the
irreducibly-ungated first commit — the trust root no later rail can recover (stage-0 §2).
A behavioral proof shows a gate *fires on the input tried*; it cannot show the gate is **bound by its frozen
name, evaluated from a trusted source, and unbypassable on every path** — properties that need reading
ruleset/workflow config. So a CI job that *looks* like it gates but no-ops, or a ruleset binding a check name
that never reports, is undetectable by the very person trusting it. This is the one place the
non-engineer-maintainer premise bites with no fallback.
**Severity.** Medium-to-high, and possibly project-defining — it is the trust root and a silent seed defect is
unrecoverable by later rails; blast radius is bounded only by the seed being minimal and the build reversible
behind the merge.
**Mitigation direction.** Shrink, do not pretend to close: (1) **seed-minimization via GitHub-native
protections** the maintainer sees toggled in the UI and trusts through GitHub's documented behavior, over
bespoke CI guards (stage-0 §2/§5); (2) an **exhaustive operator-runnable checklist** —
one fail-then-pass recipe per seed guarantee, first-exercise proofs not assertions, nothing left as "trust the
cold agents"; (3) **maximal independent + adversarial cold review** of seed contents (build-conformance
lenses). The residual after all three is **named and accepted knowingly**, never dressed as closed (the
honest-tier discipline, [principles §7/§17](../principles.md)). Relates to R1 (the protected-branch bootstrap,
now applied by a non-engineer) and R10 (solo non-engineer review proportionality); opened by [D-136](../adr/0136-re-base-the-bootstrap-trust-model-on-a-sole-non-engineer-gat.md).

## R16 — Build-conformance is AI-on-AI: a shared blind spot or a wrong spec reproduces faithfully

**Risk.** Through the whole bootstrap and all v1 self-construction, spec-conformance of built code is judged
by cold AI lenses and adjudicated by the orchestrator — all AI the non-engineer cannot verify
(build-conformance). The residual splits along two independent axes. On the
**correctness** axis two failure modes are irreducible: (a) a **self-consistent semantic
divergence** — code that builds, passes its own (AI-written) tests, and reads plausibly but implements the spec
wrongly — that *both* the conformance lenses and the behavioral demonstration miss (a shared AI blind spot);
and (b) **spec-error reproduction** — if a design doc is itself wrong, the code and every lens reproduce the
error faithfully, because conformance checks code-against-spec, never spec-against-intent. On the **coverage**
axis is a *distinct* mode (c) **silent under-build**: an obligation built only *partially* — the partial
build passing its own tests — accumulates unnoticed because per-PR conformance is re-derived from prose with
no durable denominator and no reverse sweep, so nothing carries the not-yet-built remainder across sessions.
Mode (c) is a coverage gap, not a correctness one, and — unlike (a)/(b) — it is **mechanically closable**.
The **reverse** coverage direction — a built surface tracing to *no* obligation (an **over-build**) — has no
mechanical denominator (nothing enumerates every built surface), so it is **not** mechanically closable; its
narrow, diff-introduced form is judgment-closed by the [qa-review](../spec/modules/qa-review.md)
`divergence-hunter` lens as a ground-truthed suspicion (carrying the same shared-blind-spot residual as (a)),
while whole-repo dead-code is `technical-integrity`'s referent-free health concern, outside conformance scope.
**Severity.** Medium — bounded by independence + adversarial framing of the lenses, by the fraction of each
change with a non-AI (mechanical or behavioral) correlate, and by small reversible PRs; the coverage mode (c)
is closed by the obligation-matrix denominator below (over the obligations it enumerates); the correctness
modes (a)/(b) stay irreducible for a finding with no behavioral correlate.
**Mitigation direction.** (a) For divergence: independent, adversarial, default-to-divergent lenses; the
orchestrator's HARD ground-truth + re-adjudicate disciplines (build-conformance §4);
and **maximizing the share of each change with a behavioral correlate** the maintainer runs themselves — the
only evidence that routes around AI. The no-correlate residual is named, not closed. (b) For a wrong spec:
that is the upstream job of the dry-run and the cold-session **design** audit, never
build-conformance — keeping those rigorous is the mitigation. (c) For under-build: the **spec-obligation
matrix** — a durable record *derived from and fingerprint-pinned to* each design-doc span
(build-conformance §4, the [§3](../principles.md)/[§19](../principles.md) derive-don't-
hand-author mechanic) — supplies the missing denominator, a continuous reverse sweep of not-yet-built rows,
and cross-session memory. It closes the coverage residual **without** touching (a)/(b): it is a *derived
index*, never a trusted second referent — the human-readable design span it points to stays ground truth, so
it adds no new AI-legible surface the non-engineer must take on trust. The same matrix travels to a deployed
product build (against its `locked` `docs/spec/`) as the SDD module's enforcement layer. Relates to R3 (never
over-claim closure) and R14; opened by [D-136](../adr/0136-re-base-the-bootstrap-trust-model-on-a-sole-non-engineer-gat.md).

## R17 — Optional Cloud-Routine audit substrate rides a research preview

**Risk.** [audit-library](../spec/modules/audit-library.md) offers an **optional** Anthropic **Cloud Routine**
as an alternative substrate for the recurring self-audit (subscription-based, unattended, laptop-closed).
Cloud Routines are a **research preview** — "behavior, limits, and the API surface may change" — so a feature
an operator opted into could shift, gate behind a tier, or not reach GA.
**Severity.** Low — it is an *optional* alternative, never the default. The **default substrate is the
committed GitHub Actions `audit-prep` cron**, which depends on no preview, so **no core mechanism rides the
preview**; and audits *report, never gate*, so a substrate that changes or stops loses a cycle of signal,
never blocks work.
**Mitigation direction.** Design-for, never depend-on (the R12 posture): the default GitHub-Actions substrate
is present-by-default and preview-free; the committed digest and the **digest-staleness boot signal** are
runner-independent, so a stopped Cloud Routine surfaces on the operator's return exactly as a stopped cron
would; the Cloud-Routine walkthrough discloses the preview status, the paid-plan + Claude-Code-on-web
precondition, and the daily-run cap in plain operator language. Promoting Cloud Routines to the default is
revisited only when the feature reaches GA (the R12 "adopt at GA" pattern). Tracked in
[audit-library](../spec/modules/audit-library.md); opened by [D-146](../adr/0146-resolve-q33-github-actions-stays-the-default-audit-substrate.md).

## R18 — The uv tool-runtime: first-run availability, network, and supply chain

**Risk.** The engine's **tool-runtime** is a uv-managed Python environment auto-bootstrapped on first
run: uv is downloaded and installed, then `uv sync` fetches the locked dependency closure. Three
surfaces. (a) **First-run availability** — on an offline machine, behind a download-blocking proxy, or
on an unsupported platform, uv cannot install or `uv sync` cannot fetch, and the engine's Python tools
(the [validation](../spec/systems/guardrails/validation.md) dispatcher, the
[boot](../spec/systems/lifecycle/boot.md)/[memory](../spec/systems/cognitive/memory.md) hooks,
[provisioning](../spec/systems/infrastructure/provisioning.md), the MCP servers) cannot run — and the
design deliberately refuses to degrade to the operator's system Python. (b) **Supply chain** —
auto-installing a binary and fetching packages on first run is a code-execution and dependency surface;
a compromised installer or package would run in the operator's environment.
**Severity.** Medium — first-run availability degrades **loud** (boot's `CLAUDE.md` floor still orients,
interpreter-independent) and is recoverable by retry for the common transient causes; the supply chain
is bounded by pinning and lockfile hashes. Not low: where the runtime genuinely cannot materialize, the
deployed engine is **inoperable** until it can (named and accepted, [D-156](../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)).
**Mitigation direction.** Engine-managed, not an operator chore, and degrade-loud-never-fake
([principles §5/§7](../principles.md), [D-156](../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)): uv is installed PATH-independently
(`UV_NO_MODIFY_PATH`, an engine location, absolute-path invocation) with its source and version pinned;
`uv.lock` pins per-distribution sha256 hashes for reproducible, verifiable installs (hash *verification*
depends on index-provided hashes, so it is strong, not absolute); a first-run failure surfaces in plain
language with an engine-offered **retry** (most causes are transient — offline, or a network blocking the
download) and, when persistent, the likely cause plus finish-automatically-once-reachable — never a
dead-end, never a silent or system-Python fallback; once provisioned, the managed interpreter and cache
let the runtime operate offline. The lifecycle partition keeps the surfaces clean: **R18** owns first-run
/ offline / installer; **R7** owns upgrade-time re-materialization from a new release's `uv.lock`; **R15**
owns the maintainer's seed-time local install (CI uses `astral-sh/setup-uv` pinned to a commit SHA; the
single documented local step at the ungated seed rides R15's named, accepted residual). Closes when the
tool-runtime bootstrap is built and validated against live uv on the supported platforms. Tracked in
[provisioning](../spec/systems/infrastructure/provisioning.md),
[repository-topology](../spec/systems/infrastructure/repository-topology.md), and
wbs/stage-0-harness.md; opened by [D-156](../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md).

## R19 — Operator-presentation is relay-posture: the AI is the sole pipe to the operator

**Risk.** No Claude Code hook channel reaches the operator's screen ([constraints](constraints.md),
live-verified), so every operator-facing engine emission — the boot status, governance alarms, degraded
notices, the build risk-assessment, blocked-action notices, the close-gate prompt — is delivered **only if
the AI relays it** in its own reply (the [operator-presentation relay](glossary.md)). Relay is **posture**,
not a mechanical guarantee: a session under context pressure or poor grounding can skip a relay, and for
non-governance content the operator has no separate signal that it was skipped.
**Severity.** Medium. Three structural bounds keep it from high: (a) the **present-marker** — the AI must
open every session with a named orientation block (an alarm, or a one-line all-clear carrying the token), so
a skipped *governance* relay shows as a missing marker the floor tells the operator to distrust; (b) the
**merge wall** — governance is backstopped at the protected-branch merge regardless of any relay; (c)
**imperative relay markers** reserved for the must-push set make the high-impact relay as strong as the
platform allows. The residual is a silently-skipped *non-critical* relay (routine status), which is the
**pull** half (the [status verb](glossary.md)) the operator fetches on demand — not pushed, so not
skip-prone — and as an `operator-typed` verb it is typeable from a cold session start
([D-200](../adr/0200-authorize-the-status-verb-cold-start-re-litigation-model-aut.md)), a self-served unfiltered view independent of any AI relay. Not low: the relay floor is honest posture and the platform offers nothing stronger
([§6/§7/§17](../principles.md)).
**Mitigation direction.** AI-facing reframe of injected content + imperative markers (strengthen the
posture); push the safety-critical subset, pull routine via the status verb (bound the firehose), and
**collapse an unchanged standing alarm to a terse, consequence-keeping reminder** so repetition does not
breed habituation ([boot](../spec/systems/lifecycle/boot.md)'s [standing-alarm presentation ledger](glossary.md),
[D-269](../adr/0269-litigate-q18-engine-template-313-resolve-cross-session-anti.md)) — **fail-toward-full** on any ledger loss or fingerprint ambiguity, with the named
residual that a worsening which does not move the structured-condition fingerprint could collapse when it
should escalate (bounded by fingerprinting the *structured condition* — the evaluated-rules signal / the
weakened guardrail's identity — not the rendered prose, and by the offer-to-fix that clears an actionable
condition); operator-facing copy foregrounds the merge wall as the real governance guarantee, never "the AI
might forget." **Version-contingent:** the whole relay convention is the
design's response to a platform quirk and is revisited if a future Claude Code ships a reliable
operator-visible channel — the UX shape (push-critical / pull-routine) survives such a change; only
AI-as-pipe retires. Build-spec re-verify leaves: that `additionalContext` reaches the model on the current
version, and that `systemMessage`/`permissionDecisionReason`/stderr remain non-delivering (so no
defense-in-depth secondary is silently relied on). Opened by [D-187](../adr/0187-authorize-the-operator-presentation-relay-re-litigation-the.md).

## R20 — Operator-checkout strand: an engine session can leave the operator's checkout broken

**Risk.** A session that runs *in* the operator's top-level checkout (rather than an isolated worktree) can
mutate its git state — detach `HEAD`, commit, reset — leaving it **stranded** (the 2026-06-03 incident: a
session detached `HEAD` and committed in the operator checkout, leaving it 62 behind and predating
`.claude/settings.json`, so no hooks/boot ran and the operator saw no status card for ~5 days). The
protected-branch merge protects *shipped history*, not the *local checkout's integrity*, so this harm sits
**outside the merge wall**.
**Severity.** Low-to-Medium — a named, bounded residual ([R6](risks.md)). Structurally mitigated: Claude
Desktop auto-isolates each interactive session in its own worktree ([constraints](constraints.md)), so the
common case never runs in the operator checkout and the incident's worst symptom (a broken main silently
disabling boot) largely cannot recur — a session grounds in its worktree regardless of main's state. The
residual is the entry points native isolation does not cover: a Local-Desktop routine without its per-task
worktree toggle, a CLI or resumed session, or a worktree session reaching back into main by absolute path.
**Mitigation direction.** *Prevention:* native worktree isolation (primary) + the `core` deployed-floor
**never-strand-main** posture + Routine's worktree-toggle guidance and every-commit scope-lock
([build-orchestration](../spec/systems/lifecycle/build-orchestration.md)). *Detection:* the boot-invoked
**stranded-checkout detector** — branch-agnostic — catches the broken states, a checkout **parked off the main
line** on a non-default branch (the gentle day-one signal), and one **missing merged work** whether on the
default branch or a side branch (closing the gap where a checkout parked on a long-merged feature branch read
*healthy* while far behind), with an **offer-to-fix that is lossless-or-it-does-not-run**
([provisioning](../spec/systems/infrastructure/provisioning.md), [boot](../spec/systems/lifecycle/boot.md)). The
broken-states arm also receives the **first-run verdict's broken/partial-checkout state** — instantiator *and*
engine manifest both absent (a botched copy or a manually-deleted instantiator that never completed setup) — so
the provisioned verdict routes it here rather than silently reading it as "set up"
([D-277](../adr/0277-litigate-engine-template-353-first-run-dead-on-arrival-in-a.md)). Honest tiers: native isolation is a default not a wall; posture is a [§6](../principles.md) nudge; the detector
is hook+runtime-dependent and cannot fire in the double-fault / pre-`settings.json` case — there the
present-marker floor ([R19](risks.md)) is the backstop and prevention is the only remedy. Relates
[R1](risks.md) (the merge wall protects shipped history, not local-checkout integrity), [R18](risks.md)
(shares the open-findings-tier boot surfacing), [R19](risks.md) (the relay / present-marker posture). Opened
by [D-189](../adr/0189-authorize-the-operator-checkout-boundary-re-litigation-confi.md).

**Boundary — harness-exhaust accumulation is not this risk and is not engine-owned.** R20 is the *strand*
residual: a session leaving the operator checkout in a **broken** state (detached `HEAD`, missing/stale
engine files). It is distinct from the *accumulation* a healthy deployment accrues — a pile of stale local
session branches and per-session worktree backings (a real checkout showed **177 local `claude/*` branches
vs 1 on the remote, 41 worktrees**). That accumulation is **exhaust of Claude Code's per-session worktree
machinery**, which auto-cleans only clean, gracefully-exited sessions and leaves crashed / interrupted /
named / non-interactive ones behind — a known upstream gap ([anthropics/claude-code#26725](https://github.com/anthropics/claude-code/issues/26725)).
It is **local-only** (no Engine surface, no committed file, nothing on the remote), so it is addressed at the
**local / Claude layer** — a rescue-aware local sweep (worktrees first, then merged/stale branches, never a
blanket `git branch -D`) and an operator-owned scheduled routine, with the upstream gap tracked — **not** by
Engine machinery. An engine-owned auto-reconciler was considered and rejected ([D-239](../adr/0239-reject-an-engine-owned-git-hygiene-reconciler-accumulated-lo.md)):
squash-merged branches defeat an offline prune, "accumulated local cruft" is the locked
[audits](../spec/systems/guardrails/audits.md) charter (recommend-only, never an autonomous daemon —
[§8](../principles.md)), and mopping up version-contingent platform exhaust is a layer violation. The
never-strand-main posture and native worktree isolation ([D-189](../adr/0189-authorize-the-operator-checkout-boundary-re-litigation-confi.md)) stand unchanged.

## R21 — Codes of conduct: an operator stance that misleads the AI, or drifts toward bloat

**Risk.** The [conduct](../spec/systems/surfaces/conduct.md) surface injects operator-authored prose into every
session at the grounding floor. Two failure modes: **(a) a guardrail-weakening stance** — a code of conduct that
tells the AI to skip a gate, auto-approve, or treat built-in auto-memory as authoritative; and **(b) bloat** — an
unbounded stance set inflating the every-session floor (the attention cost the thin `CLAUDE.md` exists to bound).
**Severity.** Low — a named, bounded residual ([R6](risks.md)). Conduct is **pure posture**, so it cannot
mechanically weaken a guardrail (PreToolUse denies, required checks, branch protection, and the merge wall do not
depend on model compliance); it is **committed**, so any change rides a reviewable pull request — a weakening
stance is merge-visible, never silent ([§15](../principles.md)). The harm is bounded to the posture space the AI
already operates in, not the mechanical guardrails.
**Mitigation direction.** *(a)* the [validation](../spec/systems/guardrails/validation.md) weakening guard (a
`soft-warn` flagging a code of conduct that purports to weaken a guardrail, surfaced for the human merge) + the
committed-PR review + the floor's own "subordinate to every law" framing. *(b)* the surface is **bounded/capped**
(codes of conduct earn their place; attention-budgeted like the rest of the floor), and the
[audits](../spec/systems/guardrails/audits.md) sweep can surface a **stale** operator code of conduct (the audits
**third case** — affirmatively-owned operator config, **never retirement-default**) for the operator to re-tune
or clear, never nominating a deliberate stance for deletion. Honest tier: posture is a [§6](../principles.md) nudge, never a wall; the merge
review is the backstop. Relates [R19](risks.md) (the relay/floor posture) and [§15](../principles.md) (guardrail
integrity). Opened by [D-192](../adr/0192-authorize-the-conduct-surface-codes-of-conduct-a-tier-3-pros.md).

## R22 — Release-cut: a contract-silent breaking change ships under-bumped, or release automation silently no-ops

**Risk.** Two failure modes in the release process. **(a) A contract-silent breaking
change** — module-internal behavior altered with no new `migrations` entry, no module add/remove, and no edit to a
declared contract — fires none of the bump rule's mechanical signals, so the floor reads it as a patch and an
instance auto-upgrades across a break that was never gated. **(b) Release-automation silent no-op** — a
`GITHUB_TOKEN`-opened release PR's required checks never run (the recursion guard), or a `GITHUB_TOKEN`-created
tag/Release fails to trigger any downstream `on: release` automation, so a cut appears to succeed while a step
silently did not fire.
**Severity.** Low–moderate; a named, bounded residual ([R6](risks.md)). (a) is the honest [§7](../principles.md)
ceiling — the bump *floor* is mechanical, the *ceiling* is the maintainer's judgment; (b) is a documented platform
trap pinned as a build-spec constraint, so it is a build-conformance/verification item, not a standing unknown.
**Mitigation direction.** *(a)* the **unconditional** maintainer confirmation against a plain-language change
inventory (a human who knows what they shipped can raise an under-call a diff cannot see) + the every-cut
acceptance-benchmark gate + the breaking call demonstrated behaviorally where a
correlate exists ([§17](../principles.md)); the residual neither catches is stated, never dressed as coverage. *(b)*
the named build-spec constraints (a PAT / GitHub App / operator-`gh` actor for the release PR and any post-tag
automation; `fetch-depth: 0`; `cancel-in-progress: false`) + the silent-failure invariants (tagged commit = the
reviewed merge commit; atomic-or-loudly-incomplete; a legible gate path; plain-language failure + recovery).
**Relates [R14](risks.md)** — the release-cut is the bridge R14's "run a *released, ratified* version N" mitigation
depends on; this opens that dependency, it does not close R14. Honest tier: the floor is mechanical, the ceiling is
[§6](../principles.md)/[§17](../principles.md) human-gated posture; the protected-branch merge is the wall. Opened by
[D-194](../adr/0194-resolve-q36-the-engine-release-cut-version-production-proces.md).

## R23 — Standing-situation: the offline cache can be stale

**Risk.** The standing-situation ("where we are": `phase` + `milestone`) is **assembled read-only by
[boot](../spec/systems/lifecycle/boot.md) from native GitHub sources** when online — so the live card **cannot
silently rot** — and [state](../spec/systems/cognitive/state.md)'s committed copy is a **best-effort offline cache**.
The residual: when GitHub is unreachable the card falls back to that cache, which can be **stale** (nothing rewrites it
on the hot path — it refreshes via the same GitHub-derived-cache pass as the debt count, committed by the
[audits](../spec/systems/guardrails/audits.md) digest pass as freight, with the concrete wiring deferred to the
[audit-library](../spec/modules/audit-library.md) build). A secondary bound: `milestone` is read as found — GitHub elects no *active* Milestone, so the field carries the open set (one, several, or none) under [state](../spec/systems/cognitive/state.md)'s selection bound ([D-315](../adr/0315-amend-d-314-correct-its-operator-authorship-premise-the-buil.md)); it reads `none set` only when none are open, else
`none set`.
**Severity.** Low; a named, bounded residual ([R6](risks.md)) — and **strictly smaller than the
[D-196](../adr/0196-authorize-the-standing-situation-pointer-advance-re-litigati.md) design it supersedes**, which made the *online* card depend on a posture advance step that
could silently no-op (the #100 failure itself). A stale offline cache is **not governance-critical** (it cannot breach
the protected branch) and is the **same degradation [state](../spec/systems/cognitive/state.md) already accepts for the
debt count**.
**Mitigation direction.** Online the card is **derived live** (no stored marker trusted), removing #100's symptom for
the common case; offline the cache renders with the debt count's `as-of`/"may be stale, re-ground" provenance, never as
current; `milestone: none set` is rendered as honest (no Milestone is open — not a claim the project keeps none), not an error, and a several-open `milestone` renders as the several it is. The offline-cache
refresh rides the same GitHub-derived-cache pass as the debt count and is **committed by the audit-digest pass as
freight** (the committer pinned at [D-205](../adr/0205-authorize-pinning-the-offline-cache-committer-the-audit-dige.md); the concrete wiring lands with the
[audit-library](../spec/modules/audit-library.md) build). Honest tier: the live derivation is the authority, the
committed cache a labelled convenience, the protected-branch merge unaffected. Opened by [D-198](../adr/0198-authorize-correcting-100-where-we-are-is-assembled-read-only.md),
superseding the [D-196](../adr/0196-authorize-the-standing-situation-pointer-advance-re-litigati.md) R23 framing; the offline-cache committer pinned at [D-205](../adr/0205-authorize-pinning-the-offline-cache-committer-the-audit-dige.md).

## R24 — Memory compaction: an interrupted rebuild-and-swap, or a restore that resurrects an erased record

**Risk.** [Memory](../spec/systems/cognitive/memory.md)'s **ledger compaction** rewrites the one canonical
append-only store (to bound growth and enact audit-adjudicated erasure). Two new failure modes follow: (a) a
**crash mid-rebuild-and-swap** could corrupt or lose the single source of truth; (b) a **restore or
migration-revert** could land an older ledger generation over a newer one, **resurrecting a record a later
compaction erased**. Compaction also *closes* the prior long-standing gap that the append-only ledger had **no
growth bound** and "hard-delete on evidence" had no mechanism.
**Severity.** Low–medium; new failure modes confined to a deferred maintenance pass, both mechanically
mitigated and **never governance-critical** (compaction touches only the local gitignored ledger; the
protected-branch merge is unaffected).
**Mitigation direction.** (a) The **crash-safe-swap law** (same-directory temp → fsync → atomic rename over
the original → directory fsync → generation-stamped **full** index rebuild, never an incremental patch) makes
the swap atomic-or-loud: a crash at any point leaves exactly one intact ledger, and a stale index is always
fully rebuilt — so an erased record can never resurface from a stale index, and because **recall-membership is
re-derived from record type on every full rebuild** ([D-273](../adr/0273-litigate-engine-template-332-ambient-turn-deltas-dominate-me.md): ambient turn-deltas are excluded
from recall, the curated layer is not), an interrupted compaction can never silently re-admit raw deltas to
recall either. (b) The **ledger-generation stamp**
carried in [memory](../spec/systems/cognitive/memory.md)'s backup snapshot manifest lets a restore/revert that
would resurrect an erased record be **surfaced** through [boot](../spec/systems/lifecycle/boot.md)'s
open-findings path (the [D-048](../adr/0048-provisioning-delivery-designed-end-state-brownfield-capable.md) code-older-than-data channel), never silent; and compaction
does not run within a [provisioning](../spec/systems/infrastructure/provisioning.md) migration window (ordering,
not just the shared lock). A **disabled audit cron strands permanent erasure only** — Layer-1 folding +
index-pruning continue autonomously, so the failure direction is "nothing lost." Opened by
[D-209](../adr/0209-authorize-the-ledger-compaction-re-litigation-bound-the-appe.md).

## R25 — Security floor's code-scanning / disclosure pillars: a deliberate free-private gap, or a toggle that fails silently-on

**Risk.** The [security floor](glossary.md)'s native code-scanning (CodeQL) and private-vulnerability-reporting
(PVR) pillars are **native-only where the tier supports them** ([control-plane](../spec/systems/infrastructure/control-plane.md)).
Two surfaces. **(a) A deliberate free-private coverage gap** — on a free private repo CodeQL is unavailable
(it 403s without GitHub Code Security) and PVR does not exist at all (it is public-repos-only,
[constraints](constraints.md)), and the design ships **no bespoke third-party fallback** for them (the operator's
native-over-bespoke choice — another scanner is "another layer to inject bugs"). So the most common non-engineer
deployment gets neither. **(b) A toggle that fails silently-on** — provisioning enables both by an
operator-privileged `gh` call (`PATCH .../code-scanning/default-setup`, `PUT .../private-vulnerability-reporting`);
a fire-and-forget that ignored the call's status could leave a feature **off while the operator believes it on** —
a false-protection signal worse than a disclosed gap.
**Severity.** Low — a named, bounded residual ([R6](risks.md)). Code scanning and PVR are **enhancements over**
the core floor (the committed secret-scan workflow + `dependabot.yml` + the protected-branch review gate stand on
every tier), so their absence degrades a layer, never strands the operator; and native code-scanning alerts are
**advisory, not a merge gate**, so a finding never blocks a non-engineer at a button they cannot clear.
**Mitigation direction.** *(a)* the **disclose-never-downgrade** invariant the floor already locks: the
free-private gap is surfaced in plain language as a **known drawback** with what would unlock it (make the repo
public, or add Code Security), the operator's visibility is **never auto-switched**, and the gap is stated
honestly rather than papered over (the [§7](../principles.md)/[R9](risks.md) honest-tier discipline). *(b)* the
toggle **branches on the call's HTTP status** (2xx = enabled; 403 = unsupported → skip + disclose; 422/409/503 =
transient → retry-or-disclose), **never fire-and-forget** — the same degrade-loud-never-fake posture as the
control-plane bootstrap ([R1](risks.md)); the disclosure rides the [provisioning](../spec/systems/infrastructure/provisioning.md)
security-scanning-tier build-spec leaf. Relates [R1](risks.md) (the shared operator-privileged toggle path) and
[R7](risks.md) (native code scanning, unlike a committed scanner, adds **no third-party CI supply-chain surface**).

## R26 — Marketing landing front leaks into a generated repo's product README

**Risk.** The root `README.md` is engine-marketing **at rest** in the template and product-owned in a generated
repo ([topology](../spec/systems/infrastructure/repository-topology.md) law 2, [provisioning](../spec/systems/infrastructure/provisioning.md),
[D-213](../adr/0213-authorize-the-human-facing-front-door-re-litigation-the-root.md)). Because "Use this template" copies every committed file, the marketing front **travels**
to the generated repo's root; provisioning's apply phase replaces it with a product-owned starter, but **only iff
the slot still holds the engine's recognizable marketing seed**. Two surfaces. **(a) A sequencing regression** — if
a maintainer authors the template's marketing landing README *before* the provisioning replace step ships, every
repo generated in that window keeps the Engine's marketing copy as **its own product README**, a foreign artifact
at the product's root. **(b) A recognizer miss** — if the replace predicate fails to identify the engine's own
seed, it leaves the marketing front in place (the same leak); an *unqualified* replace would instead risk clobbering
an operator's edited README, which the predicate exists to prevent.
**Severity.** Low — a named, bounded residual ([R6](risks.md)). The leak is cosmetic and operator-correctable (they
own the root README and can overwrite it), never a governance or data hazard; and the replace fires **only** on the
recognizable engine seed, so operator-owned content is structurally never touched.
**Mitigation direction.** The **sequencing gate** is recorded as a build-owes ([D-213](../adr/0213-authorize-the-human-facing-front-door-re-litigation-the-root.md)): the
provisioning replace step ships before the marketing landing README lands. The recognizer (how apply identifies the
engine's own marketing seed) is a [provisioning](../spec/systems/infrastructure/provisioning.md) build-spec leaf,
build-verified so the predicate matches the shipped seed and only that; the **first-run disclosure** surfaces the
seed/replace in plain language so a leak that did slip through is visible to the operator, never silent. Relates
[R7](risks.md) (template drift / what travels) and the [D-067](../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md) project-README disclosure the
starter now writes.
Closes when the toggles + disclosures are built and verified against live GitHub. Opened by [D-212](../adr/0212-resolve-the-d-211-security-floor-re-litigation-landed-text-c.md).

## R27 — Derived-committed artifact: non-deterministic generation, or a mis-classified member

**Risk.** [§19](../principles.md) names a class of committed files (the
[knowledge](../spec/systems/cognitive/knowledge.md) graph, the [ontology](../spec/systems/grammar/ontology.md)
self-map) whose conflicts are resolved by **regeneration from the reconciled tree** — safe only because
generation is *source-deterministic* and the file is *fully* derived. Two failure modes break that. **(a)
Determinism drift** — a generator change introduces non-determinism (an unsorted glob / `os.walk`, set
iteration, a locale / timestamp / float), so the same source tree yields differing bytes; the CI fingerprint
gate then flaps red with no source change, reintroducing the very CI-red → `CONFLICTING` escalation §19 exists
to remove. (One latent case exists today — `module_coherence.provides_claims()` does not sort its glob — though
it does not currently reach committed bytes; tracked as a defense-in-depth build-owe.) **(b) Mis-classification**
— a future artifact that is *partly authored* (a catalog's governance fields, a run-dated audit digest) is
wrongly treated as a class member, so regenerate-to-resolve **destroys authored content** on a real conflict.
**Severity.** Low–moderate — bounded ([R6](risks.md)). (a) fails *loud* (a red gate, never a silent bad merge),
so the operator is protected from merging garbage; its cost is friction, not a data hazard. (b) is the sharper
mode (silent content loss), but is structurally guarded: §19 defines membership by the *source-deterministic,
fully-derived* property, and the [glossary](glossary.md) + [ontology](../spec/systems/grammar/ontology.md) name
the catalog and the audit digest as instructive non-members.
**Mitigation direction.** A **required** regenerate-twice round-trip determinism test
([validation](../spec/systems/guardrails/validation.md) owns it) is the enforcing correlate of §19.1 — the
build-owe that turns determinism from *exercised* (the fingerprint gate flaps) into *enforced*. The unsorted
glob is sorted as defense-in-depth. Mis-classification is guarded by the property-based membership and the named
non-members; adding a member is a reviewed, audited authoring act, never an implicit add. The operator-facing
**degradation** (a failed or flapping regeneration surfaced in plain language — "could not regenerate an
internal index; not safe to merge") keeps a determinism break from stranding the operator behind an opaque red
check.
Closes when the round-trip test + the glob sort ship and the operator degradation message is built. Opened by
[D-218](../adr/0218-resolve-the-d-217-derived-committed-artifact-reconcile-re-li.md).

## R28 — First-run retirement leaves a surviving file dangling on a retired module, reddening an adopter's first CI

**Risk.** First-run `retire()` deletes the instantiator and its first-run assets
([provisioning](../spec/systems/infrastructure/provisioning.md)). A file that **survives** retirement but
still statically references a **retired** module — by `import`, `importlib`, a subprocess invocation of its
path, or a hard-coded read of a retired file's path — breaks a generated repo's `unittest discover` at
**collection time**, so the adopter's required `engine-ci` goes red. Per [constraints](constraints.md) a
generated repo's workflows first run on the next real push/PR, so the operator meets this as a Python
`ImportError` on their **first real PR** — the trust-critical ask-and-walk-away moment — an error a
non-engineer cannot read, surfaced through no channel but the AI's reply. Distinct from [R18](risks.md) (the
tool-runtime cannot *materialize*) and [R5](risks.md) (install *wiring* surgery): here the runtime is fine
and nothing was wired — a *surviving file references something that was deleted*. The **reference-survival**
failure mode.
**Severity.** Low-to-moderate — bounded ([R6](risks.md)). It fails **loud** (a red required check, never a
silent bad merge), and the template-side hard closure check is go-forward **prevention** — once built, a
non-closed survivor can never ship. Not lower: absent the check it lands at the first-PR moment as an
unreadable error, the [§17](../principles.md) non-engineer-hostile case the design exists to prevent.
**Mitigation direction.** The first-run *reference-closure* invariant
([provisioning](../spec/systems/infrastructure/provisioning.md), its definition-of-record) + a **hard CI
closure check** ([validation](../spec/systems/guardrails/validation.md) coverage,
[validators-core](../spec/modules/validators-core.md) rule-data) that fails the template's required check
before a non-closed survivor ships; the check reads the retired set **without itself importing retired
machinery** and **no-ops once retirement has happened** (the adopter's post-first-run tree). An adopter who
generated before the fix — or a slip-through — remediates via the **engine-upgrade overlay** (engine code
replaced wholesale → the corrected retire-set + the new check) plus boot's plain-language open-findings
relay; the operator is never asked to debug the import. Closes when the closure check ships and the surviving
danglers are brought into closure (engine-template build-owe). Opened by [D-220](../adr/0220-resolve-the-d-219-first-run-travel-safety-re-litigation-land.md).

## R29 — Template LICENSE (the author's copyright) leaks into a generated repo's product

**Risk.** The root `LICENSE` is the engine's own at rest in the **template** (so the public repo is legally usable) and
product-owned in a generated repo ([topology](../spec/systems/infrastructure/repository-topology.md) law 2,
[provisioning](../spec/systems/infrastructure/provisioning.md), [D-221](../adr/0221-authorize-the-first-run-license-clear-re-litigation-reconcil.md)). Because "Use this template"
copies every committed file, that LICENSE — carrying the **template author's** copyright — **travels** to the generated
repo's root and would **govern the adopter's own product** until replaced by hand; provisioning's apply phase **clears**
it at first run, but only iff the slot still holds the engine's recognizable template-license seed. This is R26's
**legal** sibling — one model, two instances (the README-marketing leak is cosmetic; this one mis-states who owns the
adopter's product), the shared spine: a conservative positive-match recognizer, first-run disclosure,
brownfield-safe-by-construction. Two surfaces. **(a) A sequencing regression** — if the template ships its LICENSE
*before* the clear step ships, every repo generated in that window keeps the template author's copyright as its product's
license. **(b) A recognizer miss** — if the clear predicate fails to identify the engine's own seed it leaves the foreign
copyright in place (the same leak); an *unqualified* clear would instead risk deleting a product's own LICENSE — which is
why the predicate is a **conjunction** (body-match ∧ distinctive template-author anchor — the copyright-holder line, or
the Commons Clause licensor/product field under the current Apache seed whose body is holder-less boilerplate —
preserve-on-doubt), never a body-only match.
**Severity.** Low-to-moderate — bounded ([R6](risks.md)) and operator-correctable (they own the root LICENSE), but a
*legal*-correctness leak, not the cosmetic kind [R26](risks.md) names: a foreign copyright governing the adopter's
product is a real defect, so it ranks above R26 while staying below a data/governance hazard. The clear fires **only** on
the recognizable engine seed, so a product's own LICENSE is structurally never touched.
**Mitigation direction.** Recognize-and-clear at first run ([provisioning](../spec/systems/infrastructure/provisioning.md),
definition-of-record) + a **sequencing gate** (build-owe — the clear ships with/before any committed template LICENSE,
closing surface (a)) + the **first-run disclosure** (surfaces the removal in plain language so a leak that slipped through
is visible, never silent). The recognizer (a build-spec leaf) is the conjunction above, conservative and preserve-on-doubt,
closing surface (b)'s clobber risk. **Residual — a repo generated before the clear shipped, or drifted back to the seed** still carries the foreign copyright
(the clear fires only at first run): the remedy is **designed** — the **foreign-`LICENSE`-seed detector**
([provisioning](../spec/systems/infrastructure/provisioning.md), [D-302](../adr/0302-litigate-engine-template-471-design-the-standing-foreign-lic.md)), a standing boot-invoked
**self-seed** detect-and-offer that fires on the engine's **own** historically-shipped seed (never on a guess about the
operator's legal identity, which the engine does not hold) and, on consent, removes it through a **reviewed pull request
the operator merges** (the durable, protection-compatible path — a live repo's *committed* license governs the product) —
the [R20](risks.md) stranded-checkout pattern at detection/surfacing, its fix a reviewed PR, not a boot-time write. The
detector reads the committed `HEAD:LICENSE` and dedupes against an already-open removal PR; a **bounded local-`HEAD`
staleness** window remains — after merge the local checkout's `HEAD` lags `origin` until it next syncs (the never-strand
floor does not auto-update it), so the offer can persist a boot or two against an already-removed file, clearing on sync,
a re-consent in that window an empty-diff no-op. A plain decline collapses to a terse standing line (never fully silent) while a
**kept-on-purpose** acknowledgment retires it ([boot](../spec/systems/lifecycle/boot.md) intent-exit); a maintainer who
*intends* adopters to inherit terms ships them as an explicit authored choice, never the silent default. Relates
[R26](risks.md) (the cosmetic README sibling — no standing detector, [D-302](../adr/0302-litigate-engine-template-471-design-the-standing-foreign-lic.md) scoped this to LICENSE-only)
and [R7](risks.md) (template drift / what travels). Closes when the first-run clear + the standing detector + the
per-era/historical-seed recognizer + disclosure are built and the sequencing gate holds. Opened by
[D-222](../adr/0222-resolve-the-d-221-first-run-license-clear-re-litigation-land.md); standing detector + Apache-anchor recognizer correction designed by [D-302](../adr/0302-litigate-engine-template-471-design-the-standing-foreign-lic.md).

## R30 — Operator-facing jargon/identifier leak in tool output is judgment-tier, not mechanically gated

**Risk.** Ending the banned-word-list anti-pattern ([D-225](../adr/0225-recenter-the-spec-on-the-ai-is-the-thing-made-trustworthy-re.md)) removes the per-string mechanical checks
that asserted operator-facing tool renderers carried no maintainer vocabulary or raw code identifiers. Detection of a
jargon or internal-identifier leak in operator output now lives entirely at the **judgment tier** — the per-PR
build-conformance review during construction, and the
[audits](../spec/systems/guardrails/audits.md) cold-context doc-probe (extended to operator-facing tool strings,
[D-227](../adr/0227-resolve-the-d-226-audits-re-litigation-landed-text-cold-audi.md)) post-v1. Both are recommend-not-block and the doc-probe samples randomly, so a leak — an
unexplained internal term, or a raw symbol/file token (`gather_signals`, `pyproject`) — can slip into an operator
screen if both miss it on the introducing change.
**Severity.** Low, and concentrated post-v1. This is the honest [§7](../principles.md) tiering, not a regression dressed as
none: prose quality was never mechanically gradable ([check](../spec/systems/surfaces/check.md): the validator cannot grade
prose), so the prior substring tests were posture-dressed-as-enforcement that also over-reached onto ordinary words
([D-225](../adr/0225-recenter-the-spec-on-the-ai-is-the-thing-made-trustworthy-re.md)). Through v1 the per-PR build-conformance review covers tool output at the introducing PR (the
riskier window), so the real residual is the **post-v1 standing case**: there only the sampling audit doc-probe stands,
and a non-engineer cannot themselves recognize a leaked identifier — so the bound is named honestly, not dressed as
"operator-correctable." It stays Low because identifier leaks are rare, none is a governance or data hazard, and the
optional symbols-not-words behavioral floor (below) remains available if the residual proves real.
**Mitigation direction.** The judgment tier is the definition-of-record: build-conformance per-PR (construction) + the
extended audit doc-probe (post-v1). An optional behavioral floor — a single *correctness* assertion that operator output
carries no raw code identifiers (symbols / file-tokens / exception fragments), which guards *symbols, not words* and is
therefore not a banned-word list — remains available if the residual proves real in practice. Relates
[Q31](open-questions.md) (the post-v1 self-conformance instrument that would own this standing check). Opened by
[D-225](../adr/0225-recenter-the-spec-on-the-ai-is-the-thing-made-trustworthy-re.md).

## R31 — Standing CI-resident vault-read credential whose shared-vault grant spans every co-located namespace

**Risk.** To let the scheduled self-audit read the off-repo memory backup, a deployed repo stores a
least-privilege read-only credential (a fine-grained PAT, `contents:read`, scoped to the vault repo) as a
repository secret ([D-241](../adr/0241-authorize-completing-the-audit-s-off-repo-memory-read-enable.md)). It is the minimum-surface mechanism the platform allows for a
**non-interactive cross-repo read** (the own-repo workflow token cannot reach a separate private repo), but it
is a **standing credential** in CI: under the **shared-vault default** that one secret can read **every
co-located project's memory namespace**, not only this project's, so a compromise or misconfiguration of one
repo's Actions secrets exposes the shared vault's read surface across projects. It also carries the
non-engineer pitfalls of any secret — an expiring or mis-named one stops the read.
**Severity.** Low–Medium. The credential is **read-only and single-repo-scoped** (no write, no admin, no other
repo), the project repos are the operator's own private repos, and the vault read **projects only this
project's namespace** into the digest — so the realistic exposure is "one repo's secret store is breached → the
operator's own co-located memory is readable," not a data-integrity or governance hazard. It rises toward
Medium only under the shared-vault default at scale (more namespaces behind one secret).
**Mitigation direction.** **Least privilege + disclosure + a structural escape, not a guarantee.** The
credential is read-only, scoped to the single vault repo, and distinct from the own-repo token and the
`CLAUDE_CODE_OAUTH_TOKEN`. The **shared-vault blast radius is disclosed where the secret is set**, with the
**per-project repo the actionable way to keep a sensitive project out of the shared grant**
([memory](../spec/systems/cognitive/memory.md)/[D-238](../adr/0238-resolve-the-d-237-memory-backup-shared-vault-flip-the-four-l.md)). The turn-on is a **heavy-consent
gate** in plain language owned by [provisioning](../spec/systems/infrastructure/provisioning.md) — which **ends
it with an engine-run test read** confirming the grant actually works — steered to a **no-expiry** token where
the operator's personal account allows it (an org-hosted vault re-caps and relies on the re-arm); an expired or
mis-set secret stops the read, surfaced by the audit's **staleness backstop naming which credential lapsed**,
with the **credential-specific re-arm** the provisioning turn-on owns
([audit-library](../spec/modules/audit-library.md)).
The scheduled cross-repo read is **un-exercised end-to-end at v1** ([R17](risks.md)), disclosed as such. Opened
by [D-241](../adr/0241-authorize-completing-the-audit-s-off-repo-memory-read-enable.md).

## R32 — No cross-project contributor memory: an operator "remember everywhere" must be disclosed, never silently filed project-local

**Risk.** The engine's experiential [memory](../spec/systems/cognitive/memory.md) is **per-project by
construction** ([D-058](../adr/0058-discharge-the-wave-0-gate-q10-substrate-content-world-taggin.md)) and **deliberately supersedes** Claude Code's built-in per-project
auto-memory ([D-251](../adr/0251-reject-engine-template-255-s-explore-gate-memory-carve-out-t.md)) — but it does **not** replace the contributor's genuinely
**cross-project** notebook (recall an operator wants to follow them across every project). So a literal
operator "remember X across all my projects" has **no engine home**: the substrate can capture it only
project-locally, and a silent project-local file would let the operator mistake it for a global preference.
**Severity.** Low. In a project-bound instance nearly all "remember this" is project recall, which the
substrate's automatic capture serves fully; the cross-project case is the rare one, and the failure mode is a
missed preference, not a data-integrity or governance hazard.
**Mitigation direction.** **Disclose-and-defer, not build.** The interim contract is **honest-on-contact** —
"I can remember this for this project now; across all your projects is something I can't do yet" — never a
silent project-local file (the build-owe (ii) path, [D-251](../adr/0251-reject-engine-template-255-s-explore-gate-memory-carve-out-t.md)). Building a cross-project
capability would re-open the locked per-project scope ([D-058](../adr/0058-discharge-the-wave-0-gate-q10-substrate-content-world-taggin.md)) for a realistically rare need,
so it is **deferred, revisited only on a demonstrated gap** (the [D-243](../adr/0243-decline-engine-template-238-s-public-repo-saved-memory-opt-i.md) shape). Opened by
[D-251](../adr/0251-reject-engine-template-255-s-explore-gate-memory-carve-out-t.md).

## R33 — A hard check passes without biting: a false-green gate the operator reads as verified

**Risk.** A `hard` check can be present, registered, and green-on-everything while its logic is a no-op or
its negative path is never exercised — a **false-green gate**. Because a green required check reads to the
operator as *verified* (their one independently-corroborable signal,
[control-plane](../spec/systems/infrastructure/control-plane.md)/[§17](../principles.md)), a gate that never bites
silently converts "verified" into "nobody looked" — the **checker-of-checkers** hole, sharpest as more checks
become committed `custom/script` logic.
**Severity.** Was Medium-high (it undermines the trust model's load-bearing signal); reduced to Low-medium by
the meta-check below, bounded to the named residuals.
**Mitigation direction.** The standing, CI-enforced **negative-fixture meta-check**
([D-256](../adr/0256-authorize-the-every-hard-check-is-proven-to-bite-re-litigati.md)…[D-260](../adr/0260-resolve-re-lock-core-the-dispatcher-run-one-rule-entry-point.md);
[validation](../spec/systems/guardrails/validation.md)/[check](../spec/systems/surfaces/check.md)/[validators-core](../spec/modules/validators-core.md)/[core](../spec/modules/core.md))
proves every in-scope hard logic-unit *bites* against a committed [negative fixture](glossary.md) — the
up-front enforcing correlate to the after-the-fact "possibly inert" telemetry flag, and a deterministic
mechanical gate (so it sits on the realizable side of [D-244](../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)'s agentic-verdict line). **Two
residuals, named not closed:** **(a)** a fixture proves a *witnessed* negative trips the check today — **not**
completeness against every input or stability under drift (the [§7](../principles.md) ceiling), and rule-*aim*
(a mis-aimed rule of a proven kind) stays the "possibly inert" telemetry posture, not this gate; **(b)** the
gate imposes a **permanent authoring tax** — every future hard logic-unit must ship its negative fixture or
the meta-check reds (the deliberate posture→mechanical trade). Opened-and-mitigated by
[D-256](../adr/0256-authorize-the-every-hard-check-is-proven-to-bite-re-litigati.md). Distinct from R16 (build-conformance AI-on-AI semantic divergence; this is a
mechanical gate not firing).

## R34 — Generated artifacts read as authoritative before their warrant is surfaced at consumption

**Risk.** A generated artifact (self-map, knowledge graph, coherence/coverage verdict, digest) reads
as authoritative the moment it is green or committed-and-gated, yet its derivation logic can be wrong.
Its home decision ([D-261](../adr/0261-establish-the-artifact-warrant-discipline-a-7-17-application.md)) lands the [§7](../principles.md)/[§17](../principles.md)
**artifact warrant** as **design-side canon only** (the glossary term + matrix rule; the two genuine
design-doc gaps closed in [module-system](../spec/systems/grammar/module-system.md) +
[ontology](../spec/systems/grammar/ontology.md)). The **consumption-side surfacing** — the plain-language
line riding the surfaces where the operator actually meets a result: the **boot** orientation, the
**pull-request** body, and the **coherence- and coverage-check renderings** — is a build-owe. Until it
lands, the operator meets green outputs without the bound at the moment of consent, so the over-trust
this discipline guards against persists.
**Severity.** Medium. The mechanical checks are sound and the gap is disclosure, not correctness — but
informed consent ([§17](../principles.md)) requires the bound be *visible where consent happens*, and the
design-side text alone does not reach a walk-away operator. It falls to Low as the build-owes land and
rises if they drift.
**Mitigation direction.** The discipline is canon (the glossary *Artifact warrant* term + the
change-propagation-matrix rule force it on every new generated artifact); the two design-doc gaps are
closed. The named consumption surfaces (boot, PR, coherence/coverage check renderings) are
**must-land** build-owes filed in `../engine-template`; warrant **accuracy** rides the per-PR
build-conformance review and register/jargon drift the
[audits](../spec/systems/guardrails/audits.md) prose-probe — no new check kind. Opened by
[D-261](../adr/0261-establish-the-artifact-warrant-discipline-a-7-17-application.md).

## R35 — A locked doc's prose outruns its mechanism: the lock gate reviews design, it does not measure construction

**Risk.** A design doc can be ratified — passing `validate.py`, a per-system cold audit, and whole-corpus
cross-doc re-runs — while one of its sentences promises behavior no mechanism in the corpus can deliver.
Every gate this workspace owns is a **reading** gate: agents read the prose and judge it against other
prose. None executes anything. So an over-claim that is internally plausible and cross-doc consistent
survives indefinitely, and **a lock certifies that a design was reviewed, not that its prose was measured
against a mechanism**. This is the sibling of [R33](#r33--a-hard-check-passes-without-biting-a-false-green-gate-the-operator-reads-as-verified)'s
false-green gate one layer up: R33 is a check that never bites; this is a claim nothing ever tested. It
bears directly on [§17](../principles.md) — the operator weighs this corpus on the gates' word, and the gates
cannot see this class.
**Severity.** Medium. Bounded by the fact that construction *does* measure it (below), so the exposure is
the window between ratification and the build step that touches the claim — but that window has run to
months, and the corpus is ratified far ahead of the build.
**Evidence it is live, not theoretical.** [attention](../spec/systems/cognitive/attention.md)'s claim that
it *ordered* the operator's backlog Issues and Milestones as candidate work shipped **locked**; it survived
its per-system audit, the [D-151](../adr/0151-whole-corpus-design-audit-re-litigate-state-af-1-to-fix-the.md) whole-corpus audit, and **[D-154](../adr/0154-build-ready-capstone-re-run-re-litigate-attention-s4-to-fix.md) — a
re-litigation of that exact doc pair for that exact defect class**. It was caught only when a build session
**measured** the built path and found it byte-identical to ranking nothing ([D-314](../adr/0314-litigate-engine-template-394-attention-s-work-record-commiss.md)). Two
plan-stage lenses and a landed-text lens in that same pass each reproduced the defect *inside the fix*,
which is the shape of the hazard: prose is cheap to make plausible and expensive to falsify by reading.
**Mitigation direction.** No new workspace gate is proposed — a reading gate cannot fix a reading gate's
blind spot, and inventing one would repeat the error. The real instruments are **already load-bearing and
stay so**: the dry-run build simulation (cold agents simulating construction, which is
the cheapest thing here that approximates measurement), the **build sessions themselves** — whose
conformance findings are the only signal that has actually caught this class, and whose litigation requests
are therefore treated as first-class design input, not build noise — and, per-pass, an **over-claim hunter
lens** charged to ask of each affirmative claim whether a named mechanism backs it and whether its tier is
named honestly ([§7](../principles.md)). **Closes** only if a mechanical means of measuring a prose claim
against a mechanism exists here, which is not currently foreseen; until then it is a **standing, accepted
residual** and the honest bound on what a `locked` status asserts. Opened by [D-314](../adr/0314-litigate-engine-template-394-attention-s-work-record-commiss.md).
