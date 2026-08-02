# Product principles

*Reconciled with engine-template@`cdbbc33` as built (2026-08-02) — AI-compared and operator-ruled under [decision 0320](adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with the canon-evolution passages aligned by [decision 0330](adr/0330-adopt-the-built-semantic-recall-seat-and-the-canon-s-revised.md). Still **in progress** — reconciled is not settled, and this document describes the build as observed, not ratified guarantees. Until the [product spec index](spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

## What this product is for

A GitHub repository template that stands up a fully operative, AI-driven Engine capable of
cold-starting work on any project, directed and merged by a capable operator who builds through the
engine rather than by reading its code — not assumed to read code, so the burden of proof is on the
engine to build faithfully and show it on evidence the operator can weigh.

The people it serves:

- **Non-engineer operator** — primary consumer. Generates the repo, directs work, approves merges. A capable adult who builds *through* the engine rather than by reading its code; not assumed to debug code or GitHub internals. So the operator's trust cannot rest on code review — the burden of proof is on the engine to do faithful work and show it on evidence the operator can weigh, without their having to watch the mechanics.
- **The AI builder (Claude Code, or the Codex runtime)** — the engine's other consumer. Boots cold each session; needs externalized state, memory, knowledge, and attention plus unambiguous grammar.
- **Engine maintainer** — builds and evolves the template, and is the **sole non-engineer gate-holder of its construction** from the first commit, with no outside engineer ([constraints](reference/constraints.md)). Needs the design fully specified so changes are mechanical, not archaeological — and needs construction to be **approvable on evidence without reading code**, the same trust bar the deployed operator holds ([principles §17](principles.md)).

## Principles

The cross-cutting rules that resolve trade-offs across systems. When a system-level decision is
ambiguous, these break the tie. Each is here because it earned its place in the prototype review or
the original proposal.

### 1. Anything that can be a committed file should be

The distribution mechanism copies files, not settings. The more of the engine that lives in tracked
files, the more travels, diffs, and is reviewable. Reserve out-of-repo state for data that is
genuinely per-instance and high-volume (experiential memory), and for true platform settings that
cannot be files (branch protection).

### 2. Repo-authoritative truth; derived indexes are replaceable

Canonical state is committed and human-readable. Any index, cache, or vector store is a derivative
that can be regenerated from the canonical source. Never let a derivative become the only copy.

### 3. Derive, don't hand-author

Structural state (the knowledge graph, coverage maps) is generated from source and regenerates when
source changes. Hand-authored structural state rots silently. Derivation is fingerprint-gated so it
cannot drift unnoticed.

### 4. Ship the substrate, not the data

The template ships the *machinery* (schemas, capture code, MCP servers, validators) with empty data
stores. A generated repo accumulates its own memory and knowledge; the engine's own development data
never leaks into adopter projects.

### 5. Degrade to git-native

Every capability backed by an out-of-repo service has a committed fallback. If the service is down,
boot and orientation still succeed from tracked files. A non-engineer is never stranded.

### 6. Nudge locally, hard-gate at human review

Local hooks and checks *nudge* the working AI to self-correct; the hard, unbypassable gate sits at
the point a human reviews (the protected-branch merge). Local gates that hard-block create friction
without proportional trust; reserve mechanical refusal for governance-critical invariants.

### 7. Three enforcement tiers, named honestly

Hard-fail (command hooks, schema validators, required checks), soft-warn (advisory checks,
telemetry trends), and posture (expectations in rules and rituals) are distinct. Do not dress a
posture expectation as if it were machine-enforced, and do not pretend reporting is remediation.

### 8. Detect → triage → surface → remediate → validate

Telemetry does not heal autonomously. It detects drift, auto-triages persistent signals into tracked
debt, surfaces them at the next boot, where the AI remediates under guardrails, and validation
confirms the fix. The loop closes across sessions, performed by the AI — not by a daemon.

### 9. Modules declare files *and* wiring

A module is not a pile of files; it is files plus the wiring it requires (hook registration, MCP
registration, ontology entries, permissions, gitignore lines — and, on the Codex runtime, the
`codex-hook`/`codex-mcp` siblings of the first two). The manifest declares both,
declaratively and reversibly, so install and uninstall are mechanical and a coherence check can
confirm them. Check-suite membership is *not* wiring — a check rule self-declares the suites it joins,
so a suite's roster is derived from the rules present rather than mutated by a side-effect.

### 10. Amend the grammar before authoring

A new surface is named in the ontology before any instance of it is written. The grammar precedes
the content, so structure is never invented on the fly.

### 11. One history, living documents everywhere else

Change history lives in exactly one place per workspace (the decision-record corpus here, under
`adr/`; in the engine, the structured pull-request body — the control-plane PR contract — which the
pull request carries as the durable record). Decision records are the governed exception (the engine's
eADR-0014): a deployment's own engine decision records are **append-only** —
never edited, only superseded — while the engine's *shipped* founding canon, a cold copy with no
prior history to carry, is revised in place, each revision's why held by the pull-request body that
made it. Every other document is rewritten in place to its current truth and carries no inline
history.

### 12. Fault-containment is earned at the seams, not conferred by the shape

The engine is a small trusted core (the foundations) plus optional extensions (the modules). But the
containment that keeps one capability's failure from spreading is a property of the **wiring discipline
at the shared seams** — keyed, idempotent, reversible wiring; coherence validation; and not shipping
what is not selected — not a property the architecture's *shape* grants. So "modular" means "composed
of modules," never "fault-isolated"; the isolation claim is always attributed to the seam discipline,
never smuggled in by the adjective. Two consequences follow: the shared core stays minimal because it is
contagious by nature (a defect in a foundation reaches every project, so each candidate foundation must
justify why it cannot be an extension), and the shape may be called microkernel-*inspired* only as an
analogy with its limit stated — a true microkernel isolates via address spaces, whereas these extensions
share mutable files. This is planning/maintainer vocabulary; it does not leak into operator-facing surfaces — a **relevance judgment realized in writing and review** (keep internal machinery out of operator narration), **never a banned-word list or a mechanical word-substring filter** (which would grade prose mechanically against §7 and invite list-growth). The right word for the operator's need is the right word; whether prose leans on jargon is judged by the [audits](spec/systems/guardrails/audits.md) doc-probe and the per-PR build-conformance review, not a filter.

### 13. The Engine is a contributor, not a component

The Engine is a member of the engineering team building the product — it merely happens to live within
the same repo, where human contributors are external. Both run `knowledge → actions → output`; the
product is the culmination of outputs (PRs) plus the system environments that frame them. The Engine can
be no more part of the product than a human contributor is. The relationship is **asymmetric**: a
contributor knows the product, the product does not know its contributors — the dependency arrow runs
Engine → product and never the reverse. So the product is built *by* the Engine, never *on* it; removing
the Engine degrades future AI-buildability but never handicaps the product, which must ship and run
standalone. The operator may choose to intertwine them; the design never imposes coupling. This
generalizes the engine/product wall from separation of paths and identifiers to **direction of
dependency**.

### 14. Derived binding by presence

Where the engine must discover *which* providers, implementations, or members are present, it derives that
set from their **presence and self-declaration** — never from a central list an install must mutate. This is
the **discovery axis**, and it is distinct from the closed **wiring seam** (`hook`, `mcp`, `ontology-entry`,
`permission`, `gitignore`, and the Codex runtime's `codex-hook`/`codex-mcp` siblings — seven kinds,
closed), which stays the mechanism for keyed, reversible edits to shared state. Wiring is
not "by presence," and this principle does not claim it is: a module that must edit shared settings still
wires; a consumer that must find its providers derives them. The discovery axis already governs the agent
roster (derived from agent frontmatter), check-suite membership (derived from rules that self-declare their
suites), interface implementations (bound by the presence of a conforming file), and workflow activation (a
committed workflow runs by being present). The payoff is reversibility for discovery: adding a provider is a
file drop and removing it a file deletion, with the set re-derived rather than surgically mutated — the
discovery-side counterpart to the [module-system](spec/systems/grammar/module-system.md) wiring library's
guaranteed-reverser firewall, and one half of the R5 containment story.

### 15. Guardrail integrity — the builder cannot silently weaken its own enforcement

The builder runs inside the repo whose enforcement protects it, so it can reach its own guardrails: the
deny/permission blocks in `.claude/settings.json`, the CI workflows and check definitions, `CODEOWNERS`,
and the branch ruleset. It may *change* them — a module install legitimately strengthens them — but it may
never *weaken* them *silently*. A weakening change (removing, disabling, renaming, or loosening a guardrail,
or editing the ruleset-affecting files) is a governance-critical event: it is hard-gated at the human merge,
surfaced in plain language — *which* protection weakened and what the AI could then do unwatched, never a
bare "config changed" — and cannot pass on the builder's say-so alone. The guard that detects weakening must
not be falsifiable by the change it judges. This is reflexive §6/§7: a system's own gates are themselves a
governance-critical invariant, so mechanical refusal is warranted and the honest tier is named. Closure is
tiered honestly: **solo** reduces the threat to *cannot weaken silently* — blocked until the operator's
informed consent, which is §6's human gate; **team** makes it *cannot weaken at all* — a distinct identity
alone holds enforcement-admin. The design never dresses solo's consent gate as airtight prevention. This is
maintainer-layer framing of an operator-facing guarantee; the leak guard of §12 applies to the wording, not
the protection.

### 16. Deferral seams — the integrator relays; the owner detects and owns

Where two systems meet at a seam, **detection of the upstream condition and the upstream mechanism stay with
the owning substrate; the integrator binds to the seam's stable *channel contract*, not to the enumerated
*set* of upstream producers or items it relays.** An integrator surfaces, ranks, deduplicates, or gates over
a channel whose membership it does not own — it acts on whatever the owners hand it and stays silent on
*which* owners exist or *what* they detect.

This is the **ownership axis**, the sibling of the §14 **discovery axis**, and the two compose without
collapsing into each other. §14 answers *which providers are present* — derive the set from presence, never a
central list an install mutates. §16 answers *who owns what across a boundary* — detection and mechanism with
the owner, relay at the integrator. The cases separate cleanly: [boot](spec/systems/lifecycle/boot.md)'s
substrate surfacings are pure §16 with no §14 presence-binding; a check-suite roster is pure §14;
[telemetry](spec/systems/guardrails/telemetry.md)'s findings inbox is both — producers self-present (§14)
and emit-then-defer-acting (§16). Both ride the seam discipline §12 credits with fault-containment: a clean
seam is keyed, reversible, and owned on exactly one side.

**The integrator is not a dumb pipe.** It owns its own acting-mechanism *over* the channel — telemetry
deduplicates, promotes, and auto-resolves; [close](spec/systems/lifecycle/close.md) gates on the recorded
subset; [attention](spec/systems/cognitive/attention.md) ranks; boot orders and renders. What it does
**not** own is the upstream *detection* or the upstream *mechanism*: [memory](spec/systems/cognitive/memory.md)
owns reversible forgetting and boot shows only the readout; the [control-plane](spec/systems/infrastructure/control-plane.md)
defines the protection-off contract and [provisioning](spec/systems/infrastructure/provisioning.md) applies
the fix while boot only surfaces it and offers; a migration owns its version-mismatch check and boot only
nags. "Relay" names the ownership boundary, not an absence of work.

The payoff is a lighter web of interconnected requirements at no cost to operability. Because the integrator
binds to the channel and not the roster, **a new upstream producer or item attaches additively** — the
integrator's contract is unchanged by what fills it — and an owner's later evolution refines only its own side
and **cannot force the integrator's** (attention and boot make this explicit, each stating that a neighbour's
later settling cannot compel a change on its side). The many "this system changed, so its integrator must
change too" dependencies collapse to one channel contract per seam, and a reviewer reasons about a seam by
naming this principle rather than re-deriving the split each time. This is **planning/maintainer vocabulary**;
like §12 and §14 it never leaks into an operator-facing surface or runtime narration.

### 17. One trust gate — informed consent on evidence, never code review

The human gate that makes the engine trustworthy is **informed consent on evidence**, and it is the same
*kind* of gate at every layer — the deployed operator's merge and the maintainer's construction of the
template alike. The gate-holder is a non-engineer in both ([constraints](reference/constraints.md)), so **no layer's
safety may rest on a human reading code**. This generalizes §6 (the unbypassable gate is human review at the
protected-branch merge) and §15 (solo closure is "blocked until the operator's informed consent") from the
deployed world back to construction: the maintainer does not *review code*, they consent to a change on the
strength of an **evidence bundle dischargeable without reading code** — mechanical validation (deterministic,
binary), independent cold-context cross-checks (whose worth is independence and adversarial pressure, not the
gate-holder verifying them), **behavioral demonstration the non-engineer runs themselves** (the one class that
routes around AI judgment), and an honest self-report record that names its own tier. Confidence is **bounded
by how much of a change has a non-AI (mechanical or behavioral) correlate**, and the design states that bound
rather than dressing AI cross-checks as assurance the gate-holder can verify (§7) — the seed commit, with the
least behavioral correlate and no engineer, is the irreducible floor, named not hidden. What differs across
layers is **latitude, not the gate's kind**: the maintainer owns the whole repo and can spend freely on review
depth; the deployed operator wants to walk away. Like §12/§14/§16 the layer vocabulary is maintainer-framing;
the operator meets only plain language and the evidence they can run.

### 18. The Engine carries its own *why* — design rationale is a shipped, durable artifact

The engine self-describes its **what** by derivation (§3): the self-map and knowledge graph regenerate its
current structure from source forever. Its **why** cannot be derived — a rationale and the alternative it
rejected are authored judgments, not facts read off the surfaces — so it must be *carried*. A deployed Engine
is a standalone artifact whose builders (a future cold session, the
[engine-mechanic](spec/systems/lifecycle/external-contribution.md) building the next version in a separate
repo, another adopter) cannot reach the workspace where its structural laws were settled. So the rationale for
each structural law lives **inside the Engine** — a bounded canon of foundational
[contracts](spec/systems/surfaces/contracts.md) (eADRs) shipped with the template — not solely in the
session, the pull request, or the planning workspace that decided it. A builder reads *why* a law is the way
it is, and what was rejected, **before** retooling it blind.

This is the authored complement to §2/§3: canonical *structure* is committed and derived; canonical
*rationale* is committed and authored — both repo-authoritative, neither hostage to an external service or an
unreachable workspace. It does not loosen §3: the knowledge entities *about* eADRs stay derived and
fingerprint-gated; only the decision text is authored, exactly as every contract always has been. It honors
§11's one-history law the canon's own way (the engine's eADR-0014): a deployment's **own** engine decision
records are append-only — never edited, only superseded — while the shipped founding canon is a **living
cold-copy snapshot, revised in place and replaced wholesale by an engine release**, carrying no supersession
chain because a deployed copy has no prior history to preserve; and it is bounded by
the §13 wall and the contract-threshold, so it records *Engine* laws only and stays exceptional — never an
accumulation of routine decisions. Like §12/§14/§16/§17 this is maintainer-layer framing; the operator meets only the
plain fact that the engine ships records of why it is built as it is, while their project keeps its own.

### 19. Derived-committed artifacts are source-deterministic; conflicts on them are spurious

A **derived-committed artifact** is a committed file whose entire content is a *deterministic function of the
committed source tree* — the same tree in yields byte-identical output. The v1 members are the
[knowledge](spec/systems/cognitive/knowledge.md) graph (`graph.json`) and the
[ontology](spec/systems/grammar/ontology.md) self-map. An artifact with **any** authored content, or whose
output depends on anything beyond the committed sources (a run-date, an at-time judgment, per-instance state),
is **not** a member — which is why the surface catalog (authored governance fields, only its coverage derived)
and the [audits](spec/systems/guardrails/audits.md) digest (run-dated, judgment-bearing) are excluded though
both are committed and machine-touched. Two laws bind the class:

1. **Generation is source-deterministic** — canonical serialization (sorted keys, fixed indent, LF, a single
   trailing newline) makes one source tree yield byte-identical output. The CI fingerprint gate
   re-derives-and-compares and so *exercises* the property (a non-deterministic generator surfaces as a gate
   flap); the *enforcing* correlate is an explicit regenerate-twice round-trip test, and determinism is owned
   by [validation](spec/systems/guardrails/validation.md). This is the honest tier of §7 — the gate
   exercises, the test enforces; neither is dressed as the other.
2. **A merge or rebase conflict on a member is spurious** — given a clean source reconciliation, both sides are
   valid regenerations of one tree, so regeneration loses nothing. The sole sanctioned resolution is to clear
   the conflict and **regenerate from the reconciled tree** — never a hand-merge, never a side-pick. The
   operator never has to *resolve* it: an AI session does (the
   [build-orchestration](spec/systems/lifecycle/build-orchestration.md) orchestrator at `integrate` post-M1;
   an interim session before M1), and the operator meets a clean PR. The law makes the conflict
   spurious-and-recoverable; it does **not** make a transient `CONFLICTING` state impossible — a sibling PR can
   merge mid-flight — only operator-invisible to *resolve* (the [D-024](adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md) value: a non-engineer
   is never handed a merge conflict).

Membership is by **property, not a frozen list** — a future source-deterministic committed artifact joins
automatically, and the concrete path set (for any merge-driver wiring) is a build-spec leaf derived from the
property; the v1 roster and the instructive non-members live in the [glossary](reference/glossary.md). This is the
merge-time corollary of §2 (derived indexes are replaceable) and §3 (derive, fingerprint-gated), adding the
source-determinism requirement they leave implicit; that the integrator regenerates an artifact whose generator
it does not own is §16 (the owning system detects and generates, `integrate` relays). Like §12/§14/§16/§17/§18
this is maintainer-layer framing; the operator meets only a clean PR.

### 20. Spec-conformance is the standing target; no construction milestone licenses an under-build

The design workspace is the **complete final state**, not a floor to grow from — the standing
generalization of [D-003](adr/0003-specify-the-full-end-state-before-the-first-build-pr.md) (the whole end-state is settled before build; capability is
layered by *build order*, never by cutting from the end-state). So every build step drives the slice it
touches to **full spec capability** and is done only when nothing it covers is left partial. Incremental
delivery is expected: full conformance to a system lands across many pull requests, each a complete dose for
the slice it touches, parking nothing. What stages the work is **build order** — the dependency sort the
WBS fixes — never a deferral of capability.

**No construction milestone is ever a deferral license.** The engine's own build milestones — M1, the
engine's v1 — are not legitimate owners for any capability the spec defines. "Build it after M1 / after v1 /
once it's a real deployed repo" is an **under-build**, not a deferral. The dry-run's
"deferred to a later named owner" means a **concrete build step, the stage-0 seed, or the first-run
provisioning apply** on the drive to full conformance — never a milestone behind which in-spec work is
parked. A milestone marks *where construction has reached*, never *how much of a touched slice may be
skipped*; that the seed governance is *superseded* at M1 (stage-0) changes **which
governance file is active**, never how completely a slice is built. These are the *engine's* construction
milestones, distinct from any product milestone an operator may direct (the product clause below).

**The boundary is membership in the spec, and the spec — not the build session — decides it.** Two things
look unbuilt but are conformance, because the spec *itself* places them outside the artifact under
construction: (a) the construction-repo differences the spec sanctions under the **engine == product**
degeneracy (stage-0 §6, [D-111](adr/0111-resolve-q22-q23-the-construction-repo-carries-no-codeowners.md)) — the
[provisioning](spec/systems/infrastructure/provisioning.md) instantiator never runs in a repo that is
never generated from itself, so there is no rendered CODEOWNERS, the engine manifest is hand-seeded, and the
construction-governance `CLAUDE.md` is distinct from the deployed-floor one; and (b) a capability the spec
**scopes out of v1** — a future optional module, the post-v1
[engine-mechanic](spec/systems/lifecycle/external-contribution.md) as the *locus* of later evolution, a
tracked [open question](reference/open-questions.md). The decisive line is that **a capability is an in-spec member
unless a `locked` doc or a logged decision explicitly scopes it out** — a build session may not reclassify
an in-spec capability as out-of-scope to dodge building it. Excluding a non-member is conformance;
under-building a member and pointing at a later phase is the deviation this principle forbids.

**This binds the Engine to the Engine spec; it does not reach a product the Engine builds.** §20 is an
engine-integrity rule, enforced *while the engine is built* by the dry-run and
build-conformance instruments — maintainer build-apparatus (like `validate.py`
and this workspace itself), **not engine machinery**, so they retire when construction ends, not because
conformance stops mattering. The conformance *capability* ships and stays whole in every deployed repo as
[build-orchestration](spec/systems/lifecycle/build-orchestration.md)'s spec-conformance review, aimed at
the product's spec rather than engine-planning. A **product** a deployed Engine builds has, by default, no
frozen engine-planning-style spec: its scope is the operator's evolving intent, and the operator may direct
an intentionally staged or MVP product. But the operator may also install the optional
[product-design (SDD)](spec/modules/product-design.md) module and **`lock` rows of a
committed `docs/spec/`** — and a locked spec row *is* a frozen spec, the product analogue of a locked design
doc here. So the shipped review's **depth is conditional on what the operator has settled**: against a
`locked` `docs/spec/` it runs the full [conformance-enforcement floor](reference/glossary.md) — the
[spec-obligation matrix](reference/glossary.md) coverage denominator, the adversarial divergence-hunter lens, and the
deployed-environment demonstration harness, the same rigor that built the Engine — now pointed at the
*product's own* spec, never engine-planning; with nothing locked it stays the charitable disclosed-no-op.
The engine and the product are autonomous, each closing over its own spec (§13 — the dependency runs
Engine → product and never the reverse), so the engine's conformance discipline cannot reach into product
scope: **the engine will neither block an MVP product the operator scopes nor silently degrade its own
machinery to fit one.** The floor's conditionality is exactly what reconciles these: it bites only on rows
the operator *chose* to lock, so the **operator, not the engine, decides how much of their product is frozen
ground** — and "stays whole" becomes literal, the deployed engine shipping the *whole* floor rather than a
lightened one. The engine's machinery stays whole in every repo, template and deployed (§4/§5) — the
deployed operator never meets a degraded engine. Like §12/§14/§16/§17/§18 this is maintainer-layer framing; the operator meets
only a whole engine and their own product scope.

## What these rule out

These are the exclusions the principles above state for themselves, gathered in one place. Each is quoted or paraphrased from the principle that carries it, not added here.

- **A derivative as the only copy.** Canonical state is committed and human-readable; an index, cache or vector store is always regenerable from it.
- **Hand-authored structural state.** The knowledge graph and coverage maps are generated from source, because hand-authored structural state rots silently.
- **The engine's own data travelling to adopters.** The template ships machinery with empty stores; a generated repo accumulates its own.
- **Out-of-repo state as a default.** It is reserved for what is genuinely per-instance and high-volume, and for platform settings that cannot be files.
- **Advisory theatre in place of a real gate.** Enforcement is named at its honest tier, and the only unbypassable wall is the protected-branch merge.
- **Ceremony that buys no trust.** Friction is spent only where it earns something; routine work is not taxed.
- **Engine assumptions leaking into product code.** The product carries no dependency on the engine and ships standalone.
- **Additions that serve no quality attribute.** Measured against the rubric, an addition that serves none of them is scope creep.
