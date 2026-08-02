---
status: accepted
engine_record: true
---

# Admit engine-recall as the single `model-auto` skill

*Decided 2026-08-01 in this repository, by the operator, in the wave-6 ruling round under
[decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md).*

## The decision

The built **engine-recall** skill — the memory-consultation command, declared
`invocation: model-auto` so the assistant may start it on a relevance match — is admitted as
**v1's single `model-auto` skill**. The [skills](../spec/systems/surfaces/skills.md) document's
"v1 ships no `model-auto` skill" roster claims are corrected to record the one member.

This extends, through its own carve-out, the roster claim of
[D-200](0200-authorize-the-status-verb-cold-start-re-litigation-model-aut.md)/[D-201](0201-resolve-the-d-200-status-verb-cold-start-re-litigation-lande.md):
that pair's operative decision — flipping the *status verb* to `operator-typed` because a
`model-auto` skill is absent from the operator's `/` menu at a cold session start — stands
untouched, and its conclusion that v1 then shipped zero `model-auto` skills explicitly kept the
value in the taxonomy "so a future need is additive." engine-recall is that anticipated additive
arrival, and the cold-start premise does not bite here: recall is a mid-session push-to-consult
(the same metacognition gap the memory scent addresses), not a verb the operator must reach at a
cold start, so menu invisibility at the first message costs nothing. The build's own grammar
agrees — the codex-skill-coherence check carves out "a command deliberately declared
model-reachable" as an allowed reachable render.

The upstream admitting record is tracked as
[engine-template issue 796](https://github.com/StarshipSuperjam/engine-template/issues/796).

## Why

The skill meets the document's own earns-a-skill bar for a model-invocable command: the need
recurs, it benefits from auto-invocation exactly where the assistant would otherwise not think
to consult memory, and it is engine-owned. Reverting the build to `operator-typed` would discard
the push-to-consult capability the skills document's own scent-complement passage describes,
in service of a roster count whose governing record already anticipated additive growth. What
remains owed is bookkeeping — the arrival shipped upstream with no admitting record, so the
roster claim and the shipped set disagreed silently; this record and the upstream issue close
that gap.

## What we ruled out

**Keep the intent and revert the build** (rejected — discards a real capability that the
governing decision's own carve-out anticipated; nothing in D-200's verified cold-start premise
is contradicted by a skill that is not a cold-start verb). **Correct the roster without a
decision record** (rejected — "v1 ships no `model-auto` skill" is a ratified claim in the
document; extending it silently is the drift the append-only log exists to prevent, the same
rule applied to actionlint in [decision 0324](0324-admit-actionlint-as-an-advisory-member-of-the-security-floor.md)).
**Make it operator-typed as well** (rejected — D-200 verified menu-visibility and
model-invocability are mutually exclusive for one skill on the platform, and the operator's
typed path to the same capability is unaffected: the assistant runs the recall operation
directly when asked).
