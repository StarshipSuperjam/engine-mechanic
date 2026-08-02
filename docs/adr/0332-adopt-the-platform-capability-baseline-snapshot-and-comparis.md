---
status: accepted
engine_record: true
---

# Adopt the platform capability baseline — the snapshot and comparison rules become the platform-currency denominator

*Decided 2026-08-02, as the blocking prerequisite of
[engine-template #657](https://github.com/StarshipSuperjam/engine-template/issues/657), immediately after
[decision 0331](0331-settle-the-reconciled-corpus-as-the-build-baseline.md) settled the spec corpus the
audit reconciled against.*

## The decision

The one-time platform capability baseline audit of 2026-08-02 — 247 source-linked capability records across
Claude Code / Claude Desktop, Codex, and both model lineups, reconciled against engine-template at
`cdbbc335` — is adopted as the **denominator for all future platform-currency runs**. Its durable form is
the committed corpus under `docs/reference/platform-baseline/`: three catalogs, the utility matrix, the
coverage and conflict map, the comparison rules, and the snapshot (per-source URL, retrieval date, and
content fingerprint). The snapshot ages deliberately: it is never refreshed in place, and a re-baseline
happens only through a new recorded decision — the same discipline decision 0320 applies to the spec
corpus's own reconciliation pin. Until then, every platform-currency run reports as a diff against this
snapshot, under the committed comparison rules, and says so.

The catalogs' dispositions are adopted here as **recommendations**; their ratification — including the five
approved migrations and the no-changes recommended to stand — is the migration decision record that
accompanies the migration spec, so that no decision record commits to a boundary change ahead of the spec
revision that carries it. The audit's architecture conclusion is nonetheless stated now, in the utility
matrix, in plain words: the existing core-and-adapter boundary stands — reviewed against the full
inventory, not redrawn — and none of the approved migrations crosses it.

## Why

The recurring platform-currency module is only honest if its findings are true diffs against a known
denominator: without a baseline, every run re-audits from scratch against an implicit, incomplete picture —
the exact risk #657 names (duplicating native controls, missing stronger native mechanisms, depending on
bypassable behavior). The audit ran under committed evidence rules — live sources fetched the day of the
run, allowlisted origins only, every claim cited, every capability reconciled against the built repo before
disposition — and its coverage, including page-level gaps and two live source-map corrections, is disclosed
in the coverage map rather than implied complete. Content fingerprints make later diffs detect documentation
churn at an unchanged URL instead of misreading it as platform change.

## What we ruled out

- **A living baseline that refreshes in place** (rejected — a denominator that silently moves cannot anchor
  a diff; deliberate aging with recorded re-pins is the property the whole module rests on).
- **Adopting dispositions and migrations in this same record** (rejected — the boundary commitments belong
  with the spec revision that carries them; adopting them here would let a decision record run ahead of the
  reviewed change, the ordering the plan review flagged).
- **A machine-readable-only baseline (JSON/database)** (rejected — the corpus must be operator-readable at
  merge review and diffable in pull requests; markdown records with embedded YAML keep both properties, and
  a schema-backed form can be layered later by the module build if runs need it).
- **Deferring the baseline until the module build** (rejected — #657 makes the baseline the blocking
  prerequisite precisely so the module's first run has a denominator; building the module first would ship
  the incomplete-baseline risk permanently).
