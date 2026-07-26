---
status: draft
---

# Docs

*Ratified in the design workspace on 2026-06-18 by [decision 0216](../../../adr/0216-resolve-the-d-215-operator-prose-register-re-litigation-land.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../../spec/index.md).*

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
in full and still fail the register edge by talking down — complete, accurate, and patronizing at once. This
register standard is the **rubric** the [audits](../guardrails/audits.md) cold-context doc-probe reads
each doc against (*Anti-drift* below): a doc that talks down is **surfaced for remediation rather than passing
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
probe**: an audit reads a randomly chosen doc as a cold consumer and asks whether it still tells the truth,
still tells the operator how to *use* what it describes, **and still addresses the operator in the right
register** — the operator-communication law's register edge, never condescending or talked-down. Structure and
frontmatter are mechanically checked; truth, usefulness, **and register** are the audit's judgment, not a
check's — a doc that is accurate and usable but talks down is **flagged by the probe for remediation** (the audit
recommends; the operator adjudicates).

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **For the operator, not the AI** — the AI orients from derived output; docs serve the human. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Plain language, always** — the operator-communication law governs every doc. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Engine corner, never the product's** — docs document the engine; the product's docs are the product's. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **A floor, never empty** — at least one orientation doc ships in v1, named and committed. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
