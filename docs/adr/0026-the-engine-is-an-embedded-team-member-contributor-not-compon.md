---
status: accepted
engine_record: true
---

# The Engine is an embedded team member (contributor, not component); asymmetric awareness

*Decided 2026-05-23 in the design workspace.*

## The decision

Establish the headline relationship principle: **the Engine is a member of the engineering team building the product — a *contributor*, not a *component* of it.** It merely happens to live within the same substrate (the repo) as the product, where human contributors are external. Both human and engine contributions run **`knowledge → actions → output`**; the product is the culmination of **outputs (PRs)** plus the **system environments** (CI, the control plane) that frame them. Named corollaries: **(a) asymmetric awareness** — a contributor knows the product, the product does not know its contributors; the dependency arrow is **Engine → product, never product → Engine** (this generalizes the engine/product wall of [D-016](../spec/systems/infrastructure/repository-topology.md)/[D-020](../spec/systems/grammar/ontology.md) from *separation* to *dependency direction*). **(b) Clean removal** — a contributor can leave without unbuilding what shipped; removing the Engine degrades future AI-buildability but never the product itself (which must ship, e.g. to an iOS app, and remain operable). **(c) No imposed coupling** — the operator may *choose* to intertwine them; the design never forces it. **(d) The metaphor's one seam (a feature):** the Engine-contributor's mind and tools are externalized into committed in-repo files (Claude Code is stateless), so they travel and are instantiable — exactly [D-005](0005-distribution-model-is-use-this-template.md)'s "Use this template" model — yet the `.engine/` footprint is that contributor's workspace *inside* the shared repo, still never the product. Lands as a new [principles.md](../principles.md) principle (additive narration; it re-characterizes the wall conceptually but changes no locked-doc wall text) and corrects the [glossary](../reference/glossary.md) `Engine` definition.

## Why

The clarification resolves the otherwise-fanning ontological question of "what master does each capability serve" by collapsing it into one intuitive frame: the Engine relates to the product exactly as a contributor does. It supplies the cleanest rationale for the wall (a contributor's tools are not the product), for clean removal (a contributor leaving does not unbuild the product), and for product-agnosticism (the product cannot depend on its tooling and still ship standalone). It also exposes a latent error: the glossary's "apparatus *on top of which* a product is built" implies product→engine dependency ("built on top of X" = depends on X), the precise inference this principle forbids; the product is built *by* the Engine, not *on* it.

## What we ruled out

Model the Engine as a substrate/platform the product sits on (rejected — "on top of" asserts a product→engine dependency that breaks portability; shipping the product elsewhere would strand it). Adjudicate per-capability "masters" as a manifest field (rejected — it forces a classification, edges into the deferred cognitive-content scoping, and is unnecessary because asymmetry is enforced mechanically and wiring is master-agnostic). Forbid the operator from ever coupling them (rejected — the operator may intertwine by choice; the design only declines to *impose* coupling).
