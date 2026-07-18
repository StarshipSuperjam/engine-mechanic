# Principles

The cross-cutting laws of the engine; when a decision is ambiguous, these break the tie. Each entry
states its law only — reasoning lives in the decision records, cited never restated — and where one
of the Engine's own shipped contracts carries a law in full, the entry here relays and the contract
governs.

## 1. Laws, not leaves

Design documents state invariants, walls, contracts, and operator-observable behavior — never build
leaves. A file path, a count, a tool name, a model name, a numeric cap: those belong to the build and
its pull requests, where they change without a design edit. Rationale lives in the decision records;
a spec cites a decision, never restates. A pinned leaf goes stale the day the build moves; a stated law stays true.

## 2. One law, one home

Every law is stated in exactly one place. Downstream documents relay — they name the law and add
only what is new at their own altitude, never restating. A restated law forks when its home amends.

## 3. The design record stays small

The design record must stay an order of magnitude smaller than the thing it governs, and must never
again become a prose copy of the code. Growth pressure is resolved by distilling upward into laws,
not by transcribing the build.

## 4. Anything that can be a committed file should be

The engine travels by copying files: what is tracked ships, diffs, and is reviewable. The template
ships the substrate, not the data — machinery with empty stores; a deployment accumulates its own
memory and knowledge, and the engine's development data never leaks into an adopter's project.

## 5. Repo-authoritative truth; derive, don't hand-author

Canonical state is committed and human-readable; every index or store over it is a replaceable
derivative, and structural state is generated from source, gated so drift cannot pass unnoticed.
A committed derived artifact is source-deterministic — same tree, byte-identical output — so a
merge conflict on one is spurious, resolved only by regenerating from the reconciled tree, never
by hand and never by the operator (ADR-0004).

## 6. Degrade to git-native

Every capability backed by an out-of-repo service has a committed fallback. When the service is
down, boot and orientation still succeed from tracked files; a non-engineer is never stranded.

## 7. Nudge locally, hard-gate at human review — tiers named honestly

Local hooks and checks nudge the working AI to self-correct; the one unbypassable gate is human
review at the protected-branch merge. Enforcement tiers — hard-fail, soft-warn, posture — are
distinct and honestly named: posture is never dressed as machinery, reporting never as remediation.

## 8. One trust gate: informed consent on evidence, never code review

At every layer the human gate is the same kind: consent to a change on the strength of evidence a
non-engineer can weigh — mechanical validation, independent cold-context cross-checks, behavioral
demonstration, an honest self-report. No layer's safety may rest on a human reading code, and
confidence is bounded by how much of a change has a non-AI correlate — a bound stated, never hidden.

## 9. The AI is the thing made trustworthy

The operator is a capable adult who builds through the engine rather than by reading its code;
non-code-literacy constrains exactly one thing — trust cannot route through code review. Grounding
documents carry this role framing, never a deficiency framing. No word is forbidden and no
forbidden-word list may exist: clarity is a judgment exercised in writing and review, never a
mechanical filter; maintainer-layer vocabulary — analogies, lineage, layer framing — stays out of
operator surfaces, lineage cited honestly as vocabulary only (ADR-0007, ADR-0002).

## 10. Evidence must be able to fail

A behavioral demonstration is a falsification over the real shipped surface; a recipe that can only
succeed is not evidence, and a parallel reimplementation is the alarm. Demonstrations retire when a
regression test covers them or are promoted by logged decision (ADR-0008).

## 11. Every generated artifact carries its warrant

Each generated artifact states what a green result shows, what it does not show, and what review
still covers, proportionate to how non-obvious the bound is. The engine never lets a passing check
imply assurance it cannot give (ADR-0009).

## 12. A small core, containment earned at the seams

Core is what survives when every module is removed; everything else installs and uninstalls
mechanically, and because a defect in core reaches every project, each candidate must justify why
it cannot be a module (ADR-0003). Fault containment is a property of
the wiring discipline at the shared seams, never of the modular shape itself.

## 13. The Engine is a contributor, not a component

The dependency arrow runs engine → product and never the reverse. The product ships and runs
standalone; removing the engine degrades future buildability, never the product.

## 14. Discovery by presence; owners detect, integrators relay

Which providers exist is derived from their presence and self-declaration, never from a central
list an install must mutate. Across a seam, detection and mechanism stay with the owning system;
the integrator binds to the channel contract, not to the roster of what fills it.

## 15. Amend the grammar before authoring; one history everywhere else

A new surface is named in the ontology before any instance is written — structure is never invented
on the fly. Change history lives in exactly one place per workspace; every other document is
rewritten in place to its current truth.

## 16. The builder cannot silently weaken its own enforcement

The engine may strengthen its guardrails, but a weakening change is governance-critical: hard-gated
at human review and surfaced in plain language — which protection weakened, and what could then
happen unwatched. Solo closure is honestly "cannot weaken silently," never dressed as prevention.

## 17. The Engine carries its own why

Structure is derived; rationale cannot be. The reasoning behind each structural law — and the
alternative it rejected — ships inside the engine as an authored, bounded canon of decision
records, readable before anyone retools a law blind.

## 18. The spec is the standing target; no milestone licenses an under-build

Every build step drives the slice it touches to full spec capability; build order stages the work,
never a deferral of capability. A capability is in-spec unless a locked document or a logged
decision scopes it out — a build session may not reclassify to dodge building. This binds the
engine to the engine's spec; the operator alone decides how much of their product is frozen ground
(ADR-0064).
