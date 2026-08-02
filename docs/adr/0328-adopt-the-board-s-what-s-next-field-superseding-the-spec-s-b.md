---
status: accepted
engine_record: true
---

# Adopt the board's What's-next field, superseding the spec's ban

*Decided 2026-08-02 in this repository, by the operator, in the wave-7 ruling round under
[decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md). Reverses the
letter of the carried github-projects-sync design's deliberate ban on that board label.*

## The decision

**The "What's next" board field is design, as built.** The
[github-projects-sync](../spec/modules/github-projects-sync.md) module projects five engine-owned
fields, and one of them is labelled *What's next*, fed by the top line of the engine's own
attention ranking. The carried spec's explicit ban on that label — repeated, reasoned, and
resting on the false-belief guard — is superseded, and the document now records the field among
the projected set.

## Why

The ban's premise no longer holds. The carried text forbade the label because *"a 'what's next'
the engine never computes for them would read as a verdict"* — a label pretending to an answer
the engine did not have. At the pin the engine does compute it: the attention policy ranks the
open work, and the field projects that ranking's genuine top line — the top of the same ranking
the status verb's dashboard already surfaces in full (no board field carries the full ordering).
A projection of a real computation is not a false belief; it is the
board doing exactly what the module's honest-projection laws demand — engine-owned fields
carrying engine-derived signals, never authority. The remaining risk (an operator over-trusting
the top line as a plan) is the same risk the status dashboard's full ranking already carries, and
the same
answer applies: the board is a projection, the committed record is the truth, and the field's
content is traceable to the ranking that produced it.

## What we ruled out

**Keep the ban and file the field upstream as a defect** (rejected — it would grade down a
shipped, transparent projection to satisfy a premise the build has outgrown, and force either a
board-face rename or a removed field for no protective gain; the false-belief guard's real
demand — never project what was not computed — is satisfied). **Adopt silently as descriptive
drift** (rejected — the carried ban was deliberate and argued from principle, so its reversal is
a normative act that belongs on the record, not smuggled through as a mechanics update).
