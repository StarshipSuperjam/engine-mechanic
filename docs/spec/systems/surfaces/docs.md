---
status: locked
---

# Docs

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-06-18 by [decision 0216](../../../adr/0216-resolve-the-d-215-operator-prose-register-re-litigation-land.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

**Hand-authored, operator-facing explanation** — the plain-language documentation a non-engineer reads to
understand what the engine is and how to direct it. Docs are for the **operator**, not the AI: the AI's
understanding of engine internals comes from *derived* output (the [ontology](../grammar/ontology.md)
self-map and the [knowledge](../cognitive/knowledge.md) graph), which cannot drift, so docs carry
no design-of-the-engine burden and exist solely to serve a human.

This bounds `docs` against its neighbours: it is not a `specification` (the engine does not ship hand-authored
design docs — those are not a catalogued surface), not the self-map (derived, not hand-authored), and not the
[audit digest](../guardrails/audits.md) (a derived self-attestation). Docs are the irreducible
human-written remainder: "what is this, how do I use it."

## Behavior

### Meta-contract record

| Field | Value |
|---|---|
| name | `doc` |
| class | prose |
| location | `.engine/docs/` |
| purpose | hand-authored, operator-facing explanation of the engine |
| authority tier | 3 — mechanics/guidance |
| lifecycle | `artifact` (active → deprecated → retired) |
| governing schema | JSON Schema over the frontmatter |
| template | the doc template (scaffold + shape) |

Instances are slug-named files under `.engine/docs/`. They live in the **engine corner** and never claim the
product's own root `README` or doc tree — the engine documents *itself* for the operator; the product's
documentation is the product's ([engine/product wall](../infrastructure/repository-topology.md)).

### Operator-facing, plain language

Every doc is written to the **operator-communication law** — clear and complete, explaining rather than
assuming, never dumbed down and never engineer-shorthand — because a non-engineer's informed trust depends on
understanding. A doc that needs the reader to already know the internals has failed its only purpose.

The law has two **orthogonal** edges. The **substance** edge is above: never hide meaning, never
engineer-shorthand. The **register** edge governs *how the operator is addressed* — **address the operator as the
capable adult they are, never condescending, never a register pitched below them, never explaining at length what
they plainly already grasp as if they could not.** The edges are independent: a doc can satisfy the substance edge
in full and still fail the register edge by talking down — complete, accurate, and patronizing at once. Both
edges are the **rubric** the [audits](../guardrails/audits.md) cold-context random-artifact probe reads
operator-facing prose against (*Anti-drift* below): a doc that talks down is **surfaced for remediation rather than passing
unexamined** — the audit tier (a recommendation the operator adjudicates), which is what makes the standard bite
where silent posture did not, without dressing a recommendation as a hard gate.

### The v1 floor — a named orientation doc

The surface grammar is laws-not-leaves, but **operator-facing docs are the one place an empty slot would
strand a non-engineer**. So v1 ships **at least one operator orientation doc** as a *named, committed
deliverable* (not deferred membership), covering:

- what the engine is and how the operator directs it;
- how to **discover what commands exist** — the orientation doc itself is a self-sufficient
  command-discovery path, independent of whether any `/engine-help`-style index command also ships;
- that **default-on self-audit proposing retirements is normal hygiene** — so the first
  [audit](../guardrails/audits.md) Issue recommending the engine remove part of itself reads as
  routine upkeep, not the engine breaking or attacking itself.

This orientation doc is the natural target for the root `CLAUDE.md` grounding floor's "how to orient" pointer
([boot](../lifecycle/boot.md)) — boot owns that pointer's contract, but because the doc is a
committed v1 deliverable, such a pointer can always resolve.

### Anti-drift

Because docs are hand-authored, they can drift as the engine changes — the failure derived output is immune
to. Their defense is the [audits](../guardrails/audits.md) layer's **cold-context random-target
probe** — a sample, not a sweep: each audit run reads at least one randomly chosen **in-repo artifact**
cold (a doc is one case, alongside a tool's operator-facing strings or code), so any given doc may go
several cycles unread; drift defense accrues over time. When the pick is operator-facing prose, the probe
asks whether it still tells the truth,
still tells the operator how to *use* what it describes, and still meets **both edges** of the
operator-communication law — the register edge (never condescending or talked-down) *and* the substance
edge (clarity over jargon, no engineer-shorthand where a plainer word serves). Structure and
frontmatter are mechanically checked; truth, usefulness, register, and clarity are the audit's judgment, not a
check's — a doc that is accurate and usable but talks down is **flagged by the probe for remediation** (the audit
recommends; the operator adjudicates).

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **For the operator, not the AI** — the AI orients from derived output; docs serve the human. | Operator observation: the surface's catalogued purpose binds it to the human reader, and the operator's own read at merge confirms a doc serves them; no check asserts the semantic property. | operator |
| **Plain language, always** — the operator-communication law governs every doc. | Operator observation plus the sampled audit probe: the doc-shape check (hard, CI) asserts structure only and its own message disclaims judging whether content is clear or genuinely plain-language; the cold random-artifact probe reads register and clarity, one target a cycle, as a recommendation the operator adjudicates — advisory and sampled, never a merge gate. | operator |
| **Engine corner, never the product's** — docs document the engine; the product's docs are the product's. | Operator observation at review that no engine doc lands in the product's tree; the catalog-coverage check (hard, CI) supports only the engine-corner half (the catalogued home exists where declared, at directory granularity) and asserts nothing about the product side of the wall. | operator |
| **A floor, never empty** — at least one orientation doc ships in v1, named and committed. | Split: the committed-and-present half is held at the merge by the link-integrity check (hard, CI) — the root grounding floor's relative link to the orientation doc must resolve to a file that exists, so removing the doc blocks the merge. That the doc genuinely orients (its substance) is the operator's read — so the composite row stays with the operator, the check as named support for presence. | operator |
