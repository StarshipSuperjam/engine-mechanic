---
status: accepted
engine_record: true
---

# Allow concise CoALA lineage in pre-adoption marketing

*Decided 2026-08-21 by the operator while settling the Engine landing-page refresh. This decision narrows the
operator-surface leak guard in [decision 0033](0033-ground-the-cognitive-substrate-in-established-standards-line.md);
it does not revise the Engine's cognitive architecture or make CoALA an implementation specification.*

## The decision

The template's pre-adoption marketing README and banner may name **CoALA** as direct inspiration for the
Engine's cognitive functions and value proposition. The reference stays concise and factual: it may connect
CoALA's cognitive framing to the Engine's repository-based state, memory, knowledge, attention, and
decision-support functions, and from there to the value of an engineering coworker that keeps continuity
across sessions.

The existing runtime boundary remains. A deployed Engine does not narrate ordinary work in CoALA terminology,
does not expose maintainer taxonomy to the operator as operating vocabulary, and does not claim that the
Engine implements CoALA as a specification. Detailed research mappings remain maintainer material rather than
landing-page content.

## Why

Pre-adoption marketing has a different job from runtime narration. A short, attributed lineage statement
helps prospective operators understand that the Engine's continuity model is grounded in a credible cognitive
architecture rather than an arbitrary collection of prompts. Suppressing that fact from the landing page
discarded a legitimate differentiator without improving the clarity of normal Engine operation.

The original leak guard still solves a real problem after adoption: operators should direct engineering work
in product and delivery terms, not learn research vocabulary merely to use the Engine. Narrowing the guard by
surface preserves that usability boundary while allowing honest product lineage where it is useful.

## What we ruled out

- **A feature-by-feature CoALA audit in the README.** It would turn a marketing page into a volatile capability
  matrix and invite claims broader than the settled architecture warrants.
- **Presenting CoALA as the Engine's governing specification.** It is direct inspiration for the cognitive
  framing, not the implementation contract for the repository, delivery, trust, or authority model.
- **Carrying CoALA vocabulary into normal runtime narration.** The deployed Engine continues to speak in the
  operator's product and engineering language.
- **Removing lineage entirely from operator-facing material.** The template landing page is the deliberate,
  bounded exception because it explains the product before adoption.
