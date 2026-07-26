---
status: accepted
engine_record: true
---

# Retire the `wbs/eadr-canon/` recommendation set: the eADR canon of record is engine-template's, and this workspace holds none

*Decided 2026-07-16 in the design workspace.*

## The decision

**Delete** `wbs/eadr-canon/` (the 33 per-law distillations + its README) and `wbs/eadr-canon-manifest.md`. They were a **one-time, PROPOSED recommendation** produced under [D-272](0272-finalize-the-foundational-eadr-canon-membership-33-laws-and.md) and **delivered**: engine-template adjudicated it, assigned the `eADR-####` ids, authored the shipped corpus, and dropped the recommendation banners. Their purpose is spent. The **eADR canon of record is engine-template's** — this workspace holds **no eADR record and authors none**; any question about what an eADR says is answered by reading the shipped artifact under `.engine/contracts/`, never a note here. The **transplant itself stands** as the real, completed work ([D-169](0169-add-the-foundational-eadr-canon-the-engine-ships-its-own-why.md)/[D-272](0272-finalize-the-foundational-eadr-canon-membership-33-laws-and.md), [principles §18](../principles.md)): the Engine carries its own *why*; only the delivery vehicle retires.

## Why

a delivered recommendation kept alongside the artifact it produced is worse than absent — it is a **second, drifting copy with no re-transplant path**, and it reads to a cold session as canon to maintain. This session proved the hazard concretely: it opened `S1-ontology-surfaces-catalogued-ranked.md`, treated its text as the eADR of record, and edited it to "fix" a false claim in the **shipped** `eADR-0016` — fixing nothing, while silently diverging the advisory from what was adjudicated. The file's own banner said *"This is not a shippable file."* Deleting the set removes the trap rather than posting a warning next to it, and forces every eADR question to the one place that can answer it. The standing rule this fixes in place: **the only canon revised in this workspace is the locked design corpus; everything already built is read from `engine-template`, never re-derived from a planning-layer note.**

## What we ruled out

**Keep the set as historical provenance** (rejected — the [D-272](0272-finalize-the-foundational-eadr-canon-membership-33-laws-and.md) log entry is the provenance; the files add a drifting duplicate whose only demonstrated effect was to mislead a session into fabricating eADR work). **Mark them stale / add a "delivered, do not edit" banner** (rejected — the deletion mandate forbids deprecation tags, and a banner is exactly what S1 already carried and this session read straight past; the trap survives the warning). **Keep them until the post-v1 mechanic might want them** (rejected — the mechanic reads the *shipped* canon by construction, which is the whole point of §18's transplant; it never had this workspace).

## Further record

### Propagation

**Deleted:** `wbs/eadr-canon/` (34 files), `wbs/eadr-canon-manifest.md`. **Non-locked carriers (edited under this entry):** wbs/module-order.md (the eADR-transplant step drops its pointers into the retired set; the seed is recorded as delivered-and-retired, the step and its gate unchanged), CLAUDE.md / [risks.md](../reference/risks.md) / [open-questions.md](../reference/open-questions.md) / [decision-log.md](README.md) (dead pointers into the retired set de-linked; **every claim's wording is preserved verbatim** — the foundational eADR canon is still real, still shipped, still the mechanic's `why`; only the pointers to the spent vehicle are dropped). **Verify-no-edit:** every locked doc — **no locked doc ever linked into the retired set** (mechanically confirmed), and every locked eADR *mention* ([contracts](../spec/systems/surfaces/contracts.md)'s `eADR-####` record type, [ontology](../spec/systems/grammar/ontology.md)'s identifier law, [core](../spec/modules/core.md)'s `provides`) refers to the **real shipped canon** and is untouched and correct. **Build-owe:** none — the shipped corpus is already the artifact of record. (The `eADR-0016` / `eADR-0024` text corrections remain build-owes under [D-309](0309-litigate-the-grammar-and-boot-cluster-ledger-grammar-core-u0.md), authored in engine-template.)
