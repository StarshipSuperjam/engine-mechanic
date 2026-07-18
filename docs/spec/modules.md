---
status: draft
---

# Modules

## Summary

Every engine capability ships as an installable module over one packaging grammar: a module declares what
it provides and what it wires, installs and removes mechanically, and binds into derived rosters by
presence (the packaging mechanics are engine canon — eADR-0009, eADR-0010, eADR-0023 — and are not
restated here). This capability is the catalog's shape: a required spine that is always present and never
an install choice, an operator-facing optional menu grouped under recognized discipline umbrellas, an
experimental layer behind a swappable seam, and named future slots held so later builds stay additive.

## Behavior

### The category model

Modules fall into four categories: required spine, operator-facing optional, experimental, and named
future stubs. The install walkthrough enumerates only the operator-facing optional packages — the things
an operator can opt out of; the required spine is never presented as a choice and is not disablable, but
it is disclosed in plain language in the project README and the self-map readout — hidden from the
installer is never undisclosed (ADR-0055).

Optional packages appear grouped under recognized software-discipline umbrellas — product management,
configuration management, verification and validation — each module with a one-line plain-language gloss.
The grouping is presentation data on the provisioning side, never a manifest field, so the locked
packaging grammar is untouched (ADR-0055).

An optional module earns its menu slot only if its use case is cross-cutting across project types and it
adds capability nothing already provides; kept optional modules default to off. Hiding required internals
is safe only while no operator-facing package depends on a hidden one — any such dependency must surface
at install confirmation (ADR-0055).

### The required spine

Core is the trusted root: the irreducible machinery that survives removing every module — the grammar,
the regenerable cognitive floors, the guardrail foundations including the validation engine and its
closed check kinds, the enforcement infrastructure, the lifecycle spine, the core policies, and the base
operator verbs. The root grounding file, the engine manifest, and the engine-owned control-plane files
are baseline infrastructure outside any module's provides (ADR-0056).

The validation mechanism and its content are split: the engine rides core; the engine's self-validation
rule corpus ships as one consolidated required package of check data only — no kinds, no detection logic,
wiring nothing, rules active by presence (ADR-0056).

A cognitive floor becomes its own required package only when it owns non-regenerable per-instance data
needing its own migration unit, or a seam another package binds to; otherwise it rides core. Memory
qualifies on both counts and is its own required package; knowledge rides core; the semantic-recall layer
is the lone optional, experimental package behind the swappable search interface
(ADR-0057).

The memory package owns the substrate, not the contract: the search interface declaration stays in core's
grammar while the module owns the fallback implementation, the recall substrate, and the
backup-and-restore mechanism and contract, which provisioning consumes but may not widen. Its capture
hooks ride the module under its own keys, and recall degradations are disclosed, never silent
(ADR-0057).

The routine-stance package ships only the operator's entry into the unattended stance — a thin command
delegating to one owned entry procedure — and wires nothing: the unattended permission posture is
operator-side platform configuration outside the committed seams and is never dressed as an engine wire
(ADR-0056).

### The design front door

The product-design module is the operator's one plain-language verb for saying what to build. It turns
intent into a committed, validated spec corpus in the product's own tree — one document per capability
moving stub to draft to locked — plus the product's design documentation, a living build plan, and work
Issues that are derived pointers, never the authority. Acceptance criteria are a criterion-by-how-verified
table typed by who can discharge each cell. Everything produced is product-owned and stands if the module
is removed (ADR-0058).

The engine validates the corpus's form read-only — presence, shape, coverage, coherence — and never
semantically gates product content. Locks are operator-governed: validation and any installed review
lenses inform, the operator's recorded acceptance gates, and re-acceptance keys on the immutable change
diff plus the operator's own acknowledgment gesture, never an AI-writable field. A mechanical coverage
check traces every locked criterion to committed work and removes itself with the engine; conformance is
judged as posture at the operator's merge, never a required gate on an agentic verdict. Lifecycle tokens
and methodology names never surface raw to the operator (ADR-0058).

### The review suites

Review ships as two optional agent-suite modules on the build workflow's two gates, installable per
stage: the plan-review suite (product-intent, architecture, feasibility, risk-governance lenses) and the
pre-submission suite (spec-conformance, usability, technical-integrity, security-governance, and the
divergence-hunter). The suites review all build work and are never gated behind the intake module; the
lens axis stays open, so a new lens is a file drop (ADR-0059).

Lenses are the judgment layer above mechanical validation and CI — complementing, never duplicating.
Spec-conformance derives each obligation from the locked spec and marks it met, diverged, or untested;
the divergence-hunter is its coupled adversarial twin, always run beside it as a second decorrelated
context, owning only narrow diff-introduced over-build surfaced as a grounded question. Both judge only
locked criteria, and on a spec-less change every referent-consuming lens is a disclosed no-op, never a
silent green. A lens may exercise code in an ephemeral, discarded copy: read-only means no mutation of
authoritative state, not no execution (ADR-0059).

### Configuration-management governance

The dependency-discipline module assigns each concern its honest tier: the security review gate is hard
at CI, relaying the platform's native review data through the existing required check with no new
binding, no operator-privileged step, and no third-party component; pinning is a soft ecosystem-detected
nudge, a disclosed no-op without a manifest; cadence is posture by construction. A firing hard gate gives
a plain-language next step, a remediation offer, and a recorded accepted-exception path, and its power to
block merges is disclosed at install (ADR-0060).

The migration-discipline module never runs a product migration and never hard-gates one: destructiveness
is not mechanically decidable, so a destructive product migration routes to human escalation through the
always-present escalation policy with recognition guidance and a recommended safer path. Its one soft
presence check resolves three ways — present, missing, or framework-has-no-concept — always disclosed
(ADR-0060).

### The board projection

The board-sync module projects the repo-authoritative work signal onto the platform's project board
strictly one-way: the board is a replaceable derivative, never authoritative. The engine writes only its
own fields on its own items — never status, column, or position — so a human's board gesture is never
overwritten; its trigger is a non-blocking, fail-open hook, and every failure degrades to git-native
truth with a staleness marker. Setup of the non-traveling board is module-owned with informed consent and
no standing credential; every projected label names only a verdict the engine actually computed — its
ordering field reads as ranked work (ADR-0061).

### Dependency edges

A module's declared dependency is a presence assertion derived from what its checks inspect: modules
inspecting the operator's product artifacts depend only on core's check engine; only capability genuinely
resting on the engine's own self-validation floor takes the corpus edge. Every future module's edge is
re-derived from its inspection target, never inherited from a sibling (ADR-0062).

### Named future capability

Two future optional modules are held as named stubs off the operator menu, each with an engine-observable
commissioning trigger and no shipped detector or threshold: the product-side structural graph — derived
from any committed canonical structural artifact, never hand-authored, structure not belief — commissioned
when structural live-reads strain the boot context budget; and the code-style governance family,
commissioned when posture and learned preference stop holding consistency. No expression-contracts
surface exists, and while no automated code-style floor ships, the generated project's plain-language
disclosure states that absence and names the planned remedy (ADR-0063).

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| The install walkthrough lists only opt-out-able optional packages, grouped under the discipline umbrellas with a plain gloss; the required spine never appears as a choice | Run an install; compare the menu against the catalog's category assignments | operator |
| The required spine is disclosed in the project README and the self-map readout | Read the generated README and ask for the self-map readout | operator |
| Adding a module resolves its dependency closure, copies files, applies wiring, and ends in a coherence check that is green or fails loudly | Add an optional module to a live repo and observe the confirmation and check result | engine |
| Removing a module refuses in plain language while another present module depends on it | Attempt removal of a depended-on module | operator |
| The self-validation corpus package contains check data only; the kinds and dispatcher live in core | Inspect the package's contents against its manifest | engine |
| The search contract is declared in core; the memory module supplies the implementation; recall degradations surface a notice instead of failing silently | Disable the recall service and the derived index in turn; observe boot and search behavior | engine |
| Intake is one plain verb; no framework or lifecycle token surfaces raw on the operator path | Run an intake session; scan every operator-facing message | operator |
| A spec locks only on the operator's recorded acceptance; the engine never locks or vetoes on its own | Attempt a lock without acceptance; review the recorded gesture on a real lock | operator |
| Every locked criterion traces to committed work via the coverage check, which disappears with the engine | Break a trace and watch the check fire; remove the engine and confirm the check is gone | engine |
| On a spec-less change, every referent-consuming lens reports a disclosed no-op, never a silent green | Run the review suites against a change with no locked spec | engine |
| A firing hard dependency gate presents a next step, a remediation offer, and an accepted-exception path | Introduce a flagged dependency change and read the gate output | operator |
| A destructive product migration produces an escalation, never a mechanical block, and the module never executes a migration | Stage a destructive migration in a test product; observe the routing | engine |
| A board outage never blocks work: truth stays git-native and the board carries a staleness marker; human-owned board fields are never overwritten | Sever the board connection mid-flow; move a card by hand and confirm it stays | operator |
| Board labels name only computed verdicts — the engine ordering field reads as ranked work everywhere it appears | Inspect every projected field label across board surfaces | engine |
| Each optional module's dependency edge matches its inspection target | Re-derive each edge from what the module's checks read and compare with its manifest | engine |
| The post-v1 stubs ship no detector, meter, or threshold; their commissioning triggers are stated in the catalog | Inspect the shipped set and the catalog entries | engine |
| The generated project's disclosure states the absent code-style floor and names the planned remedy | Read the generated project's plain-language disclosure | operator |
