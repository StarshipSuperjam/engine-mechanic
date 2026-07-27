---
status: accepted
engine_record: true
---

# Resolve: re-lock `ontology` (the instance-identifier law gains the intra-engine layer — engine canon `eADR-####`, a deployment's per-instance stream `<project-slug>-eADR-####`, told apart for the overlay by path/`provides` and for the reader by id namespace) — a carrier of [D-298](0298-litigate-the-deployment-eadr-collision-the-operator-s-per-in.md)

*Decided 2026-07-12 in the design workspace.*

## The decision

Re-lock [ontology](../spec/systems/grammar/ontology.md), a carrier of [D-298](0298-litigate-the-deployment-eadr-collision-the-operator-s-per-in.md). The landed text — the "Instance identifiers" law now states the engine-vs-engine recursion (the canon keeps `eADR-####`; a deployment's per-instance records carry the per-project namespace `<project-slug>-eADR-####` on the same root; the id is a human-facing wall while path / engine-owned-set membership remains the overlay's classifier, so a prefix that disagreed with its folder defers to the folder) — passed the mandatory four-lens landed-text cold audit. `python3 lock.py --relock systems/grammar/ontology/README.md --decision D-299`; `validate.py` green for this fingerprint.

## Why

ontology holds the grammar law the whole change turns on, so it re-locks first (the [§10](../principles.md) amend-first / propagation-matrix ordering). The landed-text audit did its job — it caught a self-inconsistent numeral and two build-owe completeness gaps before the irreversible re-lock, none touching the design of the two locked docs.

## What we ruled out

**Re-lock before the landed-text cold audit** (rejected — the HARD gate before any irreversible re-lock; skipping it ranks with a silent locked-doc edit). **Edit [D-298](0298-litigate-the-deployment-eadr-collision-the-operator-s-per-in.md) to fix the "five" numeral** (rejected — the decision-log is append-only; the correction is recorded here, the [D-294](0294-resolve-re-lock-product-design-a-coupled-carrier-surfaced-by.md) resolve-stage-correction precedent).

## Further record

### Cold audit (four independent lenses, no shared context; the landed-text gate before the irreversible re-lock)

adversarial · technical-feasibility · non-engineer-operator · architect. **No BLOCKING; no SERIOUS against the design soundness of the two re-locked docs.** Dispositions of every serious/nit raised: **(adversarial)** SOUND for re-lock — it verified the collision-bound against shipped engine-template code (`Supersedes` intra-stream via `_supersedes_edges(..., canon_ids=)`; the KG key already path-qualified `contract:instance.<stem>` vs `contract:<stem>`), confirmed no stale bare-`eADR-####` deployment claim survives corpus-wide and no changelog-voice violation; its nits — the ontology general-then-recursion sentence mirrors eADR-0017's own structure (no action) and the `scenarios/product-design-intake.md` product-ADR contrast — resolved (the scenario mirrored as a **free unlocked propagation touch**). **(non-engineer-operator)** serves the operator's seat — `acme-eADR-0007` vs `eADR-0017` is holdable, zero typing friction, forward-only confirmed (`.engine/contracts/instance/` holds only `README.md`); its SERIOUS (the **narration-in-words** acceptance check sits in D-298's prose but not the actionable owe list) and nits (§12 is a relevance judgment not a word-filter; lead the README rewrite with the concrete paired example) are **carried into the filed engine-template build-owe issue as explicit acceptance criteria** — the correct home, not a planning re-lock gate. **(architect)** propagation complete, scope mechanically correct (validate.py trips exactly the two intended fingerprints); the verify-no-edit set independently re-confirmed truthful under the slug form; its SERIOUS on [product-design](../spec/modules/product-design.md):149 is dispositioned in [D-300](0300-resolve-re-lock-contracts-the-two-eadr-populations-named-can.md). **(technical-feasibility)** no infeasibility — the design is buildable against origin/main; every finding is build-owe *text* (the exact widened `id`/`supersedes` pattern, the `*eADR-*.md` globs, the test-logic re-scope, graph regeneration, the corrected issue-filing target) **carried into the filed issue**, not a re-lock gate. No blocking/serious finding was rejected-with-rationale.

### Correction to [D-298](0298-litigate-the-deployment-eadr-collision-the-operator-s-per-in.md)

its numeral "**five** locked docs" is a typo — exactly **four** distinct locked docs carry the descriptor "per-instance eADR stream" (the enumerated list D-298 itself gives: [provisioning](../spec/systems/infrastructure/provisioning.md), [module-system](../spec/systems/grammar/module-system.md), [modules/core](../spec/modules/core.md), [repository-topology](../spec/systems/infrastructure/repository-topology.md); [engine-architecture](../architecture.md) carries the *unlocked* variant "per-instance stream"). The governing scope is that enumerated list plus validate.py's two-fingerprint result — both correct; D-298's "2 + 4 = six" counterfactual arithmetic in the anti-choice is correct. Append-only history: the correction lands here, D-298 is not edited.
