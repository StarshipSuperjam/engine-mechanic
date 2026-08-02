---
status: draft
---

# Conduct

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-06-14 by [decision 0195](../../../adr/0195-ratify-lock-the-conduct-surface-fresh-five-lens-cold-session.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees.*

## Summary

The operator-stance surface — the engine's **how it works with you**. A *code of conduct* is a standing,
plain-language behavioral expectation the operator holds for how the AI engages: the dialog stance, when to
push back, provenance-before-decisions, plain-language-to-the-operator, not fragmenting trivial fixes, and
the like. It is the deployed-Engine analogue of this workspace's own collaboration stance — the thing a
non-engineer would otherwise have to re-teach in every repo.

Conduct is **tier-3 (mechanics & guidance)** in the [ontology](../grammar/ontology.md) authority
order — specifically the *guidance* half — and **posture** in enforcement. It *shapes* the AI's behavior;
it never enforces, blocks, or gates. It is subordinate to every contract, policy, and mechanical guardrail:
whispers, not walls. (Contrast the [policies](policies.md) standing-rule surface, the second
authority tier, which can bind to a hard check; conduct never does.)

## Behavior

### What it is and is not

- **It is** the operator's standing *behavioral stance* — how the AI should conduct itself across all work
  in this repo, present from the first session.
- **It is not** project narrative (that is [memory](../cognitive/memory.md)'s job — the
  transcript-first record and the operator's pins, which accumulate per-project and ship empty), structural fact (that is
  [knowledge](../cognitive/knowledge.md)), design rationale (that is the
  [contracts](contracts.md) eADR canon), or an enforcement gate (that is
  [policies](policies.md) / [checks](check.md) / [hooks](../infrastructure/hooks.md)).
  Keeping the boundary sharp is what lets each home do exactly one job.

### Shape and storage

- **Class `prose`**, location `.engine/conduct/`, lifecycle `artifact` (`active → deprecated → retired`).
- **Two layers, both committed:**
  - **Defaults** — `.engine/conduct/defaults.md`: universal-good codes of conduct shipped in
    [core](../../modules/core.md)'s `provides` — **template-owned machinery, overlaid wholesale on
    upgrade**, so the Engine can improve the universal stance.
  - **Operator override** — `.engine/conduct/operator.md`: the deployment's own codes of conduct —
    **operator config**, in no `provides`, **preserved across an engine overlay**. The
    [audits](../guardrails/audits.md) three-way split tells it from machinery by `provides`
    membership, exactly as a per-deployment override is told from a shipped [policy](policies.md).
- **Each code of conduct carries a stable `id`** (frontmatter), a one-line title, and the prose rule. The
  `governing_schema` requires the `id`, the `title`, and the lifecycle `status` of each entry; the
  [template](../guardrails/templates.md) scaffolds each code as a Rule section (the
  plain-language stance) plus an optional Rationale — the id and title ride the frontmatter, and the
  scaffold's shape is held by the conduct shape check rather than a fixed-section spec. In the
  committed layer file the two meet: each code lands as one prose section headed by its title,
  matched one-to-one against its frontmatter entry by that same shape check. (File granularity — the two layer files above
  vs. one file per code of conduct plus a derived, fingerprint-gated aggregate — is a build-spec leaf; either way
  the floor-load `@import` below targets a fixed pair of paths, one per layer, so granularity does not move the
  floor law.)
- **Bounded.** Because the set is paid on every session (below), it is a small, capped stance — each code of
  conduct earns its place; it is never a dumping ground. The bound is **posture** (the attention cost), with no
  hard numeric cap. The backstop is the [audits](../guardrails/audits.md) sweep, which treats each
  layer by its `provides` class: `operator.md` is the audits **third case** — affirmatively-owned operator config,
  **never retirement-default**, so the sweep may surface one that has gone **stale** (it disables a default `id`
  the shipped `defaults.md` no longer carries, or its stance is now equal to a default) for the operator to
  **re-tune or clear**, but it **never nominates a deliberate stance for deletion**; `defaults.md` is template
  machinery, so a seemingly-dead default is an **escalate-upstream** signal, never a local retirement.

### Composition — per-rule by id

The active stance is the **union** of the two layers, composed deterministically **by `id`**, never by prose
merge:

- an operator code of conduct whose `id` matches a default **supersedes** that default;
- an operator **disable-list** drops a named default `id` — realized as a frontmatter field on the operator layer (e.g. a `disables: [id, …]` list), the exact schema shape a build-spec leaf;
- otherwise the two layers union.

This is the prose counterpart of the policy override's per-key merge ([policies](policies.md));
because prose does not merge per-key, supersession is whole-rule, keyed on `id`. The result a session reads
is a single, deterministic stance.

### Loaded at the floor, hook-independent

Conduct is part of the **grounding floor**, not the hook-dependent boot pack. The root `CLAUDE.md` — the
topology-governed floor ([boot](../lifecycle/boot.md), [repository-topology](../infrastructure/repository-topology.md))
— **`@import`s** the two layer files, so they are expanded into the session's context at launch alongside
`CLAUDE.md` itself and re-injected after a compaction — **present even when the `SessionStart` boot hook does
not run**. This is the same floor guarantee `CLAUDE.md` carries, held with the same honest posture
(platform-loaded, substantially reliable, not airtight). The two layer files are **in-repo relative imports**,
not external `~/` imports, so they are not subject to the platform's first-time external-import approval prompt
(the live Claude Code docs scope that prompt to external imports) — to be re-confirmed against the live platform at build-spec. It is deliberately **not** pushed into the boot
pack (which vanishes on a hook failure) and **not** surfaced as a governance alarm — it is the AI's
behavioral floor. The active stance is **committed and always readable**, and is surfaced on demand
by the authoring verb itself, whose first step reads the current stance back before any change. Because the
floor is paid every session, the *bounded* rule above is load-bearing.

### Travel across repos — seeded, then operator-owned

The operator's stance must ride **every** repo without re-teaching. The `operator.md` layer is **seeded at
provisioning from a seed the maintainer's template carries**: the maintainer authors their codes of conduct
once in their template, and every repo generated from it starts with them. Thereafter `operator.md` is
**operator-owned and preserved** across upgrades. The **public** template's `defaults.md` stays universal —
a third party who generates from it without the maintainer's seed gets the universal defaults plus an empty
override they fill themselves. An optional final step of the authoring verb **promotes** a
code of conduct learned in one repo back into the maintainer's template seed — a step of the one verb,
not a separate command. The seed-and-preserve
mechanism is [provisioning](../infrastructure/provisioning.md)'s, and the first-run seed is
**disclosed** to the operator in plain language — the stance is present and theirs to tune (the copy is a
build-spec leaf) — never silently installed.

### Tuning — a non-engineer authors prose, never hand-edits blind

Codes of conduct are added, revised, and retired through an **engine-mediated authoring verb**
([core](../../modules/core.md)) — the policy-tuning-verb precedent adapted for prose: the AI
drafts or revises the code of conduct with the operator, writes the instance, and commits it. Direct prose
edit is allowed (the file is legible), backstopped by the §15 guard below and the protected-branch merge
review, so a non-engineer never has to hand-edit a config file blind.

### It cannot weaken a guardrail

Conduct is posture. The first two protections below are **load-bearing and airtight from day one**; the third
is **defense-in-depth**:

- **Mechanical guardrails do not depend on it.** `PreToolUse` denies, required checks, branch protection, and
  the protected-branch merge wall hold regardless of any prose the model reads, so no code of conduct can
  disable them. This is the primary protection — it needs nothing built.
- **Every change is committed and reviewed.** Conduct is committed config, so adding or revising a code of
  conduct rides a reviewable pull request — a weakening stance is **merge-visible, never silent**, exactly as
  [§15](../../../principles.md) requires.
- **A validation guard (defense-in-depth).** A [check](check.md) flags a code of conduct that
  purports to instruct weakening a guardrail (skip a gate, auto-approve, treat built-in auto-memory as
  authoritative, force-push, merge without review) — a `soft-warn` surfaced for the human merge, the reflexive [§15](../../../principles.md) guard
  applied to this surface. It is a `validators-core` rule — and because `validators-core` is itself a
  required module, the guard is always present with the surface; the same required module carries the
  two hard structural checks (frontmatter and shape, the latter also holding the disable-list to the
  operator layer only). The guard checks conduct *content* and never makes conduct itself enforce.

### Relation to memory

Conduct is the **cold-boot stance floor**; [memory](../cognitive/memory.md)'s record — the captured
transcript and the operator's pins — is the **per-project enrichment** that accumulates through use (and ships empty). They compose: the
floor is present from session one, and memory deepens it as the project teaches the Engine. A preference
learned in a project may be **promoted** to a standing code of conduct on the operator's explicit, governed
call (the authoring verb) — never automatically.

### Placement

Conduct rides **[core](../../modules/core.md)** rather than an optional module: it must be present
in every repo from cold boot (it cannot be deselected) and it is loaded by the core/topology-owned floor, so
coupling it to a separable package would make the floor depend on a non-core path. The §12 minimal-core
justification — the addition is a defaults file, two `@import` lines, and a small authoring verb, not a
subsystem — lives in [core](../../modules/core.md).

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Pure posture, subordinate to every law.** Conduct shapes behavior and never enforces; it is tier-3 and never collides with a contract, policy, or mechanical gate. | Operator observation that conduct appears in no hard gate: its only behavioral guard is soft-tier (a warning, never a block), its two hard checks assert file form only, and no conduct file wires a deny or a hook — the absence from every enforcement path is the observable proof it never enforces. | operator |
| **Present from cold boot, in every repo.** It rides `core` and the topology-governed floor (it cannot be optional), seeded so the operator's stance travels without re-teaching. | Operator observation: both layer files are floor-imported by the root `CLAUDE.md`, conduct rides the non-deselectable core module, and first-run seeds the operator layer from the template's seed with a plain-language disclosure. No check asserts the floor import. | operator |
| **Tunable but never silently weakening.** Operator-owned, preserved across overlay, authored by a verb; any change is merge-visible and guarded against weakening a guardrail. | Operator observation with named partial support: the conduct-weakening guard (soft, CI) warns on weakening-shaped content but never blocks, so it cannot fully assert the criterion; merge-visibility is the protected-branch flow, preservation is the operator layer's absence from every module's provides, and the authoring verb exists as the committed skill and operation. | operator |
| **One job.** It carries behavioral stance only — not project narrative, structural fact, design rationale, or enforcement. | Operator observation at review: the semantic boundary is human judgment. The two hard structural checks (frontmatter and shape) mechanically confine the file's form — each code one titled prose section, the disable-list on the operator layer only — but neither asserts what the prose is about. | operator |
