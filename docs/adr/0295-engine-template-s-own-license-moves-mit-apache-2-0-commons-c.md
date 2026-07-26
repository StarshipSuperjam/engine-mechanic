---
status: accepted
engine_record: true
---

# engine-template's own license moves MIT → Apache-2.0 + Commons Clause; the design is confirmed license-agnostic (current-state docs name no license, the concrete choice lives here + in the engine-template artifact)

*Decided 2026-07-11 in the design workspace.*

## The decision

The engine-template repo's **own** license (the maintainer's copyright on the template, **not** a license imposed on adopters' products) moves from **MIT** to **Apache-2.0 + Commons Clause** — a deliberate commercial-protection choice that makes the template **source-available, not OSI open-source** (Commons Clause bars "Sell"ing software whose value derives substantially from the engine). **This supersedes the stock-MIT template-license seed named in [D-221](0221-authorize-the-first-run-license-clear-re-litigation-reconcil.md)/[D-222](0222-resolve-the-d-221-first-run-license-clear-re-litigation-land.md).** The design is confirmed **license-agnostic**: the current-state docs name no license, and the locked first-run clear machinery ([provisioning](../spec/systems/infrastructure/provisioning.md), [repository-topology](../spec/systems/infrastructure/repository-topology.md) law 2) already speaks only of "the engine's shipped **template-license seed**" and "the **template author's** copyright" — the recognizer is a body ∧ copyright-line conjunction that matches *whatever license body the template ships*, so it needs **no** locked-doc edit to accept the new seed. Only one current-state doc named "MIT" ([scenarios/first-run.md](../architecture.md#first-run-provisioning)); it is reworded to "its own `LICENSE`". The concrete license text (the new recognizer seed) is realized as an artifact in the engine-template repo, handled **outside this workspace** (no build issue is filed from here).

## Why

the corpus was authored license-agnostic from the start (the seed is a parameter, not a hardcoded name), so "allow this change" is a near-free reframe: rename the one hardcoded mention, record the concrete choice + its superseding of the MIT seed here, and surface the one genuinely-new Commons-Clause consequence as an open question rather than silently resolving a matter with legal dimensions. No lock is taken and no locked doc is touched, so the cold-session design audit gate does not apply; `validate.py` plus the propagation self-check are the gates.

## What we ruled out

**Hardcode "Apache-2.0 + Commons Clause" into the current-state design docs** (rejected — the docs stay license-agnostic; the concrete choice lives here and in the engine-template artifact, so a future license change is again a near-free reframe, not a doc sweep). **Resolve the `.engine/` downstream-binding question now** (rejected — logged as [Q41](../reference/open-questions.md) pending legal input; it would require re-litigating locked docs on a legal judgment not yet made). **Re-litigate the locked provisioning "stock text for GitHub/SPDX detection" line** (rejected — nuance noted above; the recognizer mechanism is unaffected, so a locked-doc re-lock for a one-clause rationale tweak is [R6](../reference/risks.md) over-reach). **File an engine-template build issue from here** (rejected — the concrete LICENSE + recognizer-seed swap is already handled outside this workspace). **Propagation:** [scenarios/first-run.md](../architecture.md#first-run-provisioning) (de-MIT edit) + [open-questions.md](../reference/open-questions.md) (Q41) + this entry. No edit owed to the locked [provisioning](../spec/systems/infrastructure/provisioning.md)/[repository-topology](../spec/systems/infrastructure/repository-topology.md)/[engine-architecture](../architecture.md) docs (already license-agnostic), [glossary.md](../reference/glossary.md) (no new/renamed term), [constraints.md](../reference/constraints.md) (a license *choice* is not a platform constraint), or [risks.md](../reference/risks.md) ([R29](../reference/risks.md)'s "template LICENSE leaks into the product" framing holds under any template license).

## Further record

### Nuance recorded (not fixed)

Apache-2.0 + Commons Clause is a **composite / non-SPDX-listed** license (Commons Clause is a rider on Apache-2.0), so GitHub's Licensee detector will likely label the template repo **"Other"** rather than a recognized SPDX id. The locked provisioning recognizer is **unaffected** — it body-matches the shipped seed, independent of GitHub's detector. The locked provisioning rationale that a `LICENSE` "must stay stock text for GitHub / SPDX license detection" is **left as-is** (operator-decided) with this nuance noted here — the underlying discipline (clean license text, no engine comment) holds, and a one-clause re-litigation of a locked doc is not warranted for a rationale that no longer maps cleanly to a composite license.

### Downstream-binding question opened as [Q41](../reference/open-questions.md), parked pending legal input — deliberately not resolved here

Under a *source-available* template license, the engine's own `.engine/` code travels into every adopter repo and stays, while the first-run root-`LICENSE` clear deletes the only in-repo license record and retains no Apache-2.0 §4 NOTICE/attribution — benign under permissive MIT, a real question under Commons Clause (does the restriction *bind* an adopter's use of `.engine/`?). Resolving it would touch the **locked** clear model (litigation alarm + re-lock); it needs legal input first, so it is logged, not decided.
