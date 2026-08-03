---
status: accepted
engine_record: true
---

# Ratify the platform-baseline dispositions — the migration set, the boundary as-is, and a settled corpus that changes only as each migration is built

*Decided 2026-08-02, completing the two-record sequence [decision 0332](0332-adopt-the-platform-capability-baseline-snapshot-and-comparis.md)
began: 0332 adopted the baseline snapshot and comparison rules as the platform-currency denominator and
deliberately deferred the dispositions' ratification to this record, so that no decision record would commit
to a boundary change ahead of the spec revision carrying it.*

## The decision

**The 247 dispositions in the baseline catalogs are ratified as standing decisions** — no longer
recommendations. That ratification decomposes into four commitments:

**1. The core-and-adapter boundary stands as drawn.** The audit reviewed the vendor-neutral core, the
provider adapter layer, and the host-configuration line against the full 247-record inventory and moved
nothing across them ([utility matrix](../reference/platform-baseline/utility-matrix.md)). The per-runtime
asymmetries the reconciliation surfaced are the deliberate eADR-0034 shape, not drift. No migration below
crosses the boundary.

**2. Five migrations are approved**, each a bounded engine-template build tracked as its own leaf issue
under the platform-currency release milestone:

- **M1 — audit-prep structured output.** Today the audit persona embeds a fenced machine-readable
  verdicts block inside its prose digest, and the promoting tool parses and schema-validates that block
  after the fact — a model-discipline contract. M1 moves the contract to the CLI's native structured
  output (`--json-schema`), so the shape is enforced at emission rather than relied on from the model.
  Workflow-internal.
- **M2 — SessionEnd: wire it or retract it.** The hook inventory declares `SessionEnd` hooks-owned while
  neither settings file registers a handler; the build either binds a real duty or retracts the claim.
- **M3 — routine terminology fix.** engine-template's routine docs say "Claude Desktop routine" while
  describing the *local* scheduled-task capability; the cloud product named "Routines" is a different
  thing. Docs-only, optionally naming the cloud host as an alternative substrate.
- **M4 — widen the effort vocabulary.** The model-bindings schema caps persona effort at
  `low | medium | high` while the platform ladder reaches higher tiers. **This schema is
  guardrail-floored, so its build pull request carries the weakening acknowledgment** — approved here as
  direction, consented to there as change.
- **M5 — host-hardening and dependency documentation.** Document the native OS sandbox and credential
  masking as *recommended host configuration* alongside the Engine's fail-open gate, and record the
  worktree-layout and shared-config-parity dependencies where engine-template's docs are silent. The
  engine-mechanic half of that recording lands with this record (risk R36 below).

**3. The settled spec corpus is not reopened now — an explicit no-change ruling per candidate site.**
Each migration's spec edit rides its build, where the change is real and reviewable; today every candidate
passage already describes the build truthfully:

- `systems/infrastructure/hooks.md` — the `SessionEnd` empty binding is already recorded as the sanctioned
  state (the decision-0320 wave-5 ruling), and the fail-open posture is fully specified with its
  test-pinned proceed-on-crash rows. M2's outcome updates the inventory row when it lands.
- `systems/guardrails/audits.md` — the doc *does* describe the as-built verdict mechanism (the persona
  appends a machine-readable verdicts block after its digest prose, which the promoting tool parses and
  strips), and M1 replaces exactly that mechanism — so this is the one candidate site with a known
  follow-on edit: the passage stays truthful today and is reconciled when M1's build lands.
- `systems/lifecycle/modes.md` and `build-orchestration.md` — the local-vs-cloud routine naming is already
  disambiguated ("explicitly *not* the cloud Routines product"); M3 targets engine-template's own docs.
- `systems/surfaces/agents.md` — persona `model`/`effort` are specified as platform-passthrough with no
  locked enum, so M4's schema widening needs no spec edit.

**4. The audit's no-change recommendations are ratified as-is**: the auto-memory fence (the engine's
committed memory substrate stays authoritative, the native notebook fenced), the two hand-maintained
instruction floors (no import/symlink dedup), the CLI-direct audit-prep design (the read-only persona
never writes), the rejection of auto-fix pull requests on principle (the engine never clears its own
gate), alias-only model binding, stdio-only MCP, and the three-way read-only redundancy as deliberate
defense stacking.

Alongside this record, the risk register gains **R36 — load-bearing dependence on unowned platform
behavior** (the durable engine-mechanic home for the audit's dependency findings), the architecture
overview gains its boundary-reviewed provenance note, and the baseline corpus's
"ratification rides the migration decision record" pointers resolve to this record.

## Why

Decision 0332 left the dispositions as recommendations precisely so this record could ratify them *with*
the spec revision they imply. The audit's central result is that the implied revision is nearly empty: the
settled corpus already tells the truth about the build, because the reconciliation wave measured every
record against the checkout before any disposition was assigned. Ratifying now — with the no-change
rulings recorded explicitly rather than left as silence — closes the loop 0332 opened without letting
"recommended" linger as a permanent hedge, and it gives the five migration leaf issues a decision to cite
that is stronger than a catalog stamp. The one boundary commitment this record makes is *no change*, so no
spec revision is outrun.

## What we ruled out

- **Editing the settled docs now to describe the migrated target state** (rejected — the corpus was
  settled days ago as *as-built* truth; describing unbuilt behavior would reintroduce the exact
  spec-versus-implementation conflation the audit's evidence rules exist to prevent. Each migration's edit
  lands with its build, consented to at that pull request).
- **One decision record per migration** (rejected — five records for five bounded, same-provenance changes
  would dilute the contract threshold; a single record carries each decision and its alternative, and the
  split rule stays reserved for a record that cannot).
- **Redrawing the boundary toward runtime symmetry** (rejected — the audit substantiated every
  Claude-vs-Codex asymmetry as deliberate under eADR-0034; forcing symmetry would trade recorded intent
  for cosmetic uniformity).
- **Leaving ratification to the platform-currency module build** (rejected — the module diffs against the
  baseline; if the baseline's judgments were still provisional at its first run, every finding would
  inherit that hedge. Ratification belongs with the migration spec, which is this record and its
  companions).
