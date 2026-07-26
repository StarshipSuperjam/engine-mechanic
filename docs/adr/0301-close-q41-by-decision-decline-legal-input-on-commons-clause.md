---
status: accepted
engine_record: true
---

# Close Q41 by decision: decline legal input on Commons-Clause `.engine/` binding; accept the posture; the locked first-run clear model stays as-is (no locked-doc edit)

*Decided 2026-07-12 in the design workspace.*

## The decision

Close [Q41](../reference/open-questions.md) as **won't-pursue**. Q41 asked whether, under the source-available **Apache-2.0 + Commons Clause** template license ([D-295](0295-engine-template-s-own-license-moves-mit-apache-2-0-commons-c.md)), the engine's traveled `.engine/` code should carry its own in-repo license/`NOTICE` so the restriction **binds** an adopter's use of that code — and D-295 parked it "pending legal input." For an **experimental, no-revenue, sole-maintainer** template, the maintainer declines to commission counsel to settle Commons-Clause enforceability and **accepts the posture as-is**. The locked first-run clear model ([provisioning](../spec/systems/infrastructure/provisioning.md), [repository-topology](../spec/systems/infrastructure/repository-topology.md) law 2) is **unchanged** — **no `.engine/`-scoped LICENSE/`NOTICE` machinery is added** — so this close **touches no locked doc**. Recorded honestly: the close **declines** the enforceability question, it does not answer it — the maintainer accepts, eyes open, that without an in-repo `NOTICE` the source-available restriction **may not bind** an adopter's use of `.engine/`, a risk this repo tolerates. **Reopen trigger:** the repo commercializes, or a concrete enforcement need arises — then the `.engine/`-scoped `LICENSE`/`NOTICE` hedge is available as a scoped, lawyer-free re-litigation of the clear model + topology law 2.

## Why

the only instrument that settles Q41 is legal counsel the maintainer will not retain for this project, so leaving it parked is not neutral — it **falsely gates** downstream work (the [#471](https://github.com/StarshipSuperjam/engine-template/issues/471) standing-detector litigation next in this session, whose clear-model re-lock an open legal question against the clear's core action would make unsound). An honest won't-pursue close removes that phantom dependency; the concern is real but its blast radius (the restriction may not perfectly bind) is one the sole maintainer owns and accepts. Distinct from [R29](../reference/risks.md), which guards the **inverse** leak (the template author's copyright wrongly governing the *adopter's product*) and is untouched by this posture close.

## What we ruled out

**Add an `.engine/`-scoped LICENSE/`NOTICE` now** (rejected — the cheap belt-and-suspenders that would strengthen binding, but it re-litigates the locked clear model + topology law 2 for a protection an experimental no-revenue repo does not need; parked as the reopen trigger above, not built). **Keep Q41 parked "pending legal input"** (rejected — the input will never come; an eternally-parked question rots as a phantom dependency and falsely gates the #471 litigation). **Resolve Q41 by *asserting* the restriction binds** (rejected — that is the legal conclusion only counsel can draw; the honest close declines the question rather than answering it). **Treat the close as a licence to also drop or weaken the first-run clear** (rejected — Q41 concerns the *engine's own traveled code*, not the [R29](../reference/risks.md) adopter-product leak; the clear model is untouched and still correct).

## Further record

### Propagation

delete Q41 from [open-questions.md](../reference/open-questions.md); this entry. **No locked-doc edit** — the clear model is unchanged. Verify-no-edit (confirmed): [provisioning](../spec/systems/infrastructure/provisioning.md) / [repository-topology](../spec/systems/infrastructure/repository-topology.md) (clear model unchanged), [risks.md](../reference/risks.md) ([R29](../reference/risks.md) guards the inverse and is untouched), [D-295](0295-engine-template-s-own-license-moves-mit-apache-2-0-commons-c.md) (append-only; not edited). **Id allocation:** tail was D-300, no forward reservation above it; D-301 allocated monotonically (the #471 standing-detector litigation follows as **D-302**). `python3 validate.py` green.
