---
status: draft
---

# Operations

*Settled in the design workspace on 2026-05-25, ratified by [decision 0055](../../../adr/0055-collapse-command-into-the-skill-surface-invocation-is-a-gove.md).*

## Summary

A **multi-step engine procedure performed by reading-and-following** — the authoritative body of a
procedure that a [skill](skills.md) (whether operator-typed or model-auto-invoked) or an
[agent](agents.md) enters, or that a human follows where steps need human action. An operation is
prose-with-frontmatter: a runbook, not executable code and not a persona. It is the *content* a thin
invocation surface delegates to, so a procedure is written once and entered many ways — the boundary law's
**one procedure, one home** rule (see [One procedure, one home](#one-procedure-one-home) below).

## Behavior

### Meta-contract record

| Field | Value |
|---|---|
| name | `operation` |
| class | prose |
| location | `.engine/operations/` |
| purpose | the authoritative body of a multi-step procedure, referenced by its invokers |
| authority tier | 3 — mechanics/guidance (an operation *does* work; it does not govern) |
| lifecycle | `artifact` (active → deprecated → retired) |
| governing schema | JSON Schema over the frontmatter |
| template | the operation template (scaffold + shape spec) |

Instances are slug-named files under `.engine/operations/`, engine-namespaced per the
[ontology](../grammar/ontology.md) identifier law (an operation referenced by id never collides
with a product's own runbooks).

### What an operation is — and is not

An operation is the home for a procedure that is **shared** (entered by two or more invokers — skills,
operator-typed or model-auto, and agents) or that is a **human-in-the-loop runbook** (steps the operator must perform — e.g. authenticating
with an admin-scoped token — that no deterministic code can carry). It is deliberately *not*:

- **`tool` code** — a procedure that executes deterministically with no reading-and-following is
  [`tool`](tools.md) code, not an operation.
- **an `agent` persona** — a procedure carried out in an isolated context by a spawned reviewer/worker lives
  in the [agent](agents.md) file, not as an operation.
- **one skill's private depth** — a procedure entered only by a single [skill](skills.md), used
  nowhere else, belongs in that skill's own bundled resources (progressive disclosure), not as a standalone
  surface. Promoting it would regrow the prototype's surface zoo ([R6](../../../reference/risks.md)).
- **a `specification`** — "how to *perform* X" is an operation; "what system X *is*" is a design document,
  which the engine derives (self-map + knowledge graph), not a catalogued surface.

### One procedure, one home

A procedure has exactly **one authoritative body**. When a skill or agent needs it, that surface
**references** the operation — it never restates the steps. The reference is an ordinary link from the
invoking surface to the operation; there is no central index of "who uses this operation" to maintain (a
referencer points outward, so adding one mutates nothing here). This is what keeps an `/engine-upgrade`
skill's `SKILL.md` thin while the deep, reviewed procedure lives in one place.

### The anti-sprawl heuristic

The test for whether a procedure earns a standalone operation is **"is this only one skill's private
depth?"** — if yes, it folds into that skill; if it is a genuinely shared body (≥2 referencers) or a
human-in-loop runbook (which has no invoker count at all), it is legitimately an operation. This is a
**judgment bar an [audit](../guardrails/audits.md) applies**, never a hard mechanical gate: a
single-referrer operation is *a fold-or-retire candidate*, preserved only with an affirmative case — so a real
shared procedure anticipating a second referrer is never deleted out from under the design, and clutter does
not silently accrete. *How* the audits layer reaches that judgment is the
[audits](../guardrails/audits.md) surface's concern, deferred to it.

### Coverage and validation

The frontmatter is governed by a [schema](schemas.md) ([check](check.md) kind `schema`);
section structure is the operation [template](../guardrails/templates.md)'s control and length is
a `soft-warn` budget, never a hard cap. Semantic adequacy — does the runbook actually tell a cold operator
how to perform the procedure — is the [audits](../guardrails/audits.md) layer's job, not a
mechanical check (how the audits layer probes for it is that surface's concern).

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Shared body, entered many ways** — the operation holds the steps; skills and agents hold the entry. | Read this description against the built behavior and confirm they match. | operator |
| **Runbook, not code or persona** — reading-and-following content, distinct from `tool` and `agent`. | Read this description against the built behavior and confirm they match. | operator |
| **Anti-sprawl by judgment** — the ≥2-referencer / not-one-skill's-depth bar is an audit concern, so a genuinely shared procedure is never left homeless and clutter never accretes unexamined. | Read this description against the built behavior and confirm they match. | operator |
