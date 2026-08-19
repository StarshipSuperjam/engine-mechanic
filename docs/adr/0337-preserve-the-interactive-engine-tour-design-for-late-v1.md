---
status: accepted
engine_record: true
---

# Preserve the interactive Engine tour design for late v1

*Decided 2026-08-19 by the operator after reviewing `codebase-to-course` as a reference and correcting an
initially too-thin placeholder. This decision accepts the act of preserving and parking the design; it does
not accept the capability as settled, schedule it, or authorize implementation.*

## The decision

Keep the complete [interactive Engine tour](../spec/modules/interactive-engine-tour.md) design in the product
spec now, marked in progress and outside the build order. Revisit it near the end of the v1 build arc through
a mandatory operator decision before it can settle, enter a delivery phase, receive a route, or be built.

The durable constraints retained now are the operator-centered purpose; local/private/static posture; a
clean-room boundary from the unlicensed reference; evidence lineage with primary-source authority; a
default-deny private-data wall; accessible, no-JavaScript-complete teaching; no telemetry or runtime AI
improvisation; optional activation; and measurable non-engineer comprehension as the release outcome.

## Why

The Engine's getting-started guide is approachable and its generated self-map is accurate, but neither gives a
non-engineer guided practice in how their actions travel through the Engine, where the evidence lives, or which
decisions remain theirs. The reference repository supplied enough concrete interaction ideas and failure
classes to formulate a much fuller Engine-native design. Reducing that work to a name-only stub would force a
future session to repeat the research and reasoning.

The design is parked because its eventual packaging, adapters, curriculum order, validation resources, and
relationship to late delivery-plane views depend on the Engine that exists near the end of v1. An accepted
parking decision plus a detailed draft preserves knowledge without pretending those provisional choices are
ready to build. The late-v1 revalidation is therefore part of the decision, not an optional cleanup step.

## What we ruled out

- **A bare stub.** It would discard the useful design already developed and make the operator rederive it
  later.
- **Settling or scheduling the capability now.** A detailed document is not evidence that its late-v1 seams,
  costs, validation resources, or packaging choices are ready.
- **Adding it to delivery wave 7 now.** The build order records agreed delivery commitments; this capability is
  deliberately outside that program until the operator revisits it.
- **Waiting to record anything until implementation.** That loses the curriculum, source, privacy, security,
  accessibility, and degradation conclusions already reached.
- **Copying or forking the reference implementation.** No compatible license was visible when reviewed, and
  its unresolved correctness and security work makes direct reuse both legally and technically unsuitable.
- **Folding the tour into the operator cockpit, evidence explorer, product knowledge graph, or getting-started
  guide.** Those surfaces answer current-state, evidence-navigation, product-structure, or concise-orientation
  questions; guided comprehension is a distinct outcome.
- **Generating explanations with a model at runtime.** It would make the same Engine appear to teach different
  rules, weaken provenance, and introduce unnecessary privacy and availability risk.

