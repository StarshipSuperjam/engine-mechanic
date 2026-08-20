---
status: accepted
engine_record: true
---

# Preserve the product-system explorer design for late v1

*Decided 2026-08-19 by the operator after reviewing `codebase-to-course`, then
`Understand-Anything`, and correcting both an initially thin placeholder and an Engine-centered framing. This
decision accepts preserving and parking the complete design. It does not settle or schedule the capability,
authorize implementation, or deprecate `engine-parts`.*

## The decision

Keep the complete [product-system explorer](../spec/modules/product-system-explorer.md) design in the product
spec now, marked in progress and outside the build order. Revisit it near the end of the v1 build arc through
a mandatory operator decision before it can settle, enter a delivery phase, receive a route, or be built.

The explorer's primary subject is the **product system the Engine is building**. It gives the operator detailed
views of that system's architecture, behaviors, integrations, implementation, evidence, and candidate change
impacts. A required on-demand Engine lens connects a selected product element or change to the intent,
decisions, implementation activity, tests, reviews, uncertainty, and operator authority involved in producing
or checking it. Product and operating Engine subjects remain mechanically distinct even when the product is
the Engine itself.

The capability does not infer technical ability from the operator's role. The operator may understand or
write code, but does not have to reconstruct the system from code in order to govern it. The preserved design
uses operator-controlled resolution from landscape through evidence, with guided tours as one optional
navigation mode rather than the product identity.

Treat the explorer as the intended successor to `engine-parts`, but do not change that command now. Retirement
requires additive delivery, field-level parity, static and cold-session recovery, failure-mode proof, machine-
consumer migration, a compatibility period, rollback evidence, and a separate operator decision that
supersedes [decision 0336](0336-route-operator-and-model-workflows-through-generated-canonical-surfaces.md) and
changes the settled core catalog. If the explorer remains optional, the guaranteed minimal core inventory and
discovery function remains even if the old command name is retired.

## Why

The Engine is the operator's SDLC team. The operator therefore needs a technically serious window into the
system that team is building and the evidence behind it, not merely a tour of the Engine's own repository and
not a simplified explanation that withholds detail. Current product design, code intelligence, product graph,
evidence, cockpit, and Engine self-map capabilities each own important parts of that truth, but none is the
operator-facing composition that preserves their separate authority and makes product-to-Engine traceability
directly navigable.

The external references supplied useful interaction ideas, but not the Engine-native authority model. The
unlicensed `codebase-to-course` repository remains a clean-room influence only. The MIT-licensed
`Understand-Anything` repository makes later attributed reuse possible, not authorized; its graph-highlighted
guide, local search, bounded paths, and freshness states are useful patterns, while its audience personas,
runtime AI behavior, and generic codebase-scanning architecture are not the desired product.

The design is parked because the structured system/integration contracts, provider federation, delivery
bridges, access model, runtime budgets, and late-v1 module seams do not yet exist in a buildable form. Recording
the complete design avoids redoing this reasoning later without pretending those seams are ready now.

## Durable constraints preserved now

- Product-system understanding is primary; Engine implementation detail is available but not the default
  subject.
- The audience definition is ability-neutral and the detail is operator-controlled.
- Product and Engine records carry composite subject identities; cross-subject links are explicit, validated
  bridges, never an accidental graph merge.
- Structural reachability is not behavior, causality, completeness, safety, or approval.
- Declared, observed, computed, inferred, instructional, and unknown claims retain source, evidence, freshness,
  coverage, uncertainty, and visible contradictions.
- The explorer is a presentation and teaching consumer of product design, code intelligence, product graph,
  evidence, delivery, cockpit-adjacent, and Engine self-map contracts; it does not duplicate their authority.
- Static/no-JavaScript cold access, bounded degradation, independent product/Engine authorization, hostile-input
  confinement, purge, accessibility, and model-free ordinary generation are release obligations.
- Model-assisted narration is optional, explicitly invoked, tool-less, network-less, untrusted until reviewed,
  version-bound, and subordinate to the underlying claims.
- `engine-parts` stays governed by current core contracts until a separate, evidenced supersession decision.

## What we ruled out

- **A bare stub.** It would discard the research and make a future session rederive the capability.
- **An Engine-code tour as the primary product.** A deployed repository needs to explain the product system;
  the Engine lens explains the SDLC work behind it when wanted.
- **A view pitched below the operator's intelligence.** Avoiding mandatory code reading is not avoiding
  technical depth.
- **Two disconnected explorers.** The product/Engine boundary remains explicit, but validated bridge records
  make the operator's product-to-SDLC trace directly navigable.
- **Folding the capability into product graph, code intelligence, evidence explorer, or cockpit.** Those own
  structural facts, code binding, proof traversal, and global current state respectively.
- **Treating model narration or graph paths as authority.** They remain reviewed framing or bounded navigation.
- **Scheduling it now.** Detailed preservation is not late-v1 feasibility evidence.
- **Retiring `engine-parts` in this change.** The current command remains the guaranteed inventory until the
  replacement passes its explicit transition gate.
- **Unreviewed copying from either reference.** Unlicensed material remains clean-room only; MIT reuse would
  still need an explicit provenance, security, dependency, and maintenance decision.
