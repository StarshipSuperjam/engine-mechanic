---
status: draft
---

# maintenance-ledger

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design for wave 5, not yet built; enters in progress and settles by the operator's
recorded acceptance before wave 5's build begins. Revised in draft after the trio's four cold reviews;
the largest changes: lease honesty under the pre-merge window, real append-only mechanics, and its own
forbidden-surface check.*

## Summary

The **required** durable schedule record for maintenance work: **slots** (a cadence over a durable
[operations-core](operations-core.md) concern — cadence says when to *look*; the concern's condition
standing says whether work is *warranted*; **eligibility is both**), **occurrences** with exact identity,
**leases**, **catch-up rules**, and **attempt history** — append-only in mechanism, not spirit:
attempt records are **content-chained**, and rewriting or deleting a past record is caught by the
ledger's transition check. Its lease honesty is the plane's: on committed state, a lease guards
**within one runner and across sequential succession** — two runners in unmerged worktrees cannot see
each other (the pre-merge window, named), and the double-work check catches the collision at merge,
*after* both ran. So for slots whose attempts carry **external side effects**, unattended execution is
recommended only where runtime serialization exists (the broker's runtime store is that future home);
observation-only slots are the safe unattended default — stated, not implied away. **A schedule is never
authority**: eligibility makes an attempt *possible* under the standing maintenance Issue's scope;
nothing here fires anything.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `maintenance-ledger` |
| `distribution` | `required` |
| `applicability` | `detected` (scheduled maintenance in use) |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`maintenance-slot.v1` — the concern reference (durable identity), cadence, catch-up rule (`skip`\|`latest-only`\|`all`\|`operator`) declared per slot, and the slot's side-effect class (observation-only \| effectful — the unattended-safety discriminator); `slot-lease.v1` — one attempt's hold on one occurrence, TTL ≥ the run lease's TTL, **succession gated on the prior run reading terminal or `unknown`** — never on slot-lease expiry alone, so a live first runner is not succeeded; `attempt-record.v1` — occurrence, run reference, outcome in delivery-core's vocabulary plus cause lineage, content-chained to its predecessor); the **[tool](../systems/surfaces/tools.md)** (`maintenance_ledger.py` — declare/read/occupy/record; the intended writer, the plane's honesty tier); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **double-work check** — two attempts on one occurrence without recorded, run-state-gated succession fail; the **chain-integrity check** — a rewritten or deleted past attempt record breaks the chain and fails; the **forbidden-surface check** — a maintenance run's diff touching the ledger's own checks, schemas, or the slots that scheduled it fails — the ledger's own guard, since the task envelope *declares* and never enforces; each negative-fixtured); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core`, `operations-core` |
| `migrations` | none |

### The ledger model

- **Occurrences are exact; catch-up is ruled.** A returning runner reads exactly which occurrences were
  missed and resolves them per the slot's rule — `operator`-ruled gaps surface as decisions and stay
  visible until resolved. **Volume is governed**: a per-window ceiling on new attempts (and on
  repair-task creation downstream) turns a flood — an `all`-ruled slot after a long gap — into an
  aggregate escalation ("too many pending"), never a queue that outruns the operator's attention.
- **Leases guard what they can, honestly.** Within a runner: exact. Sequential succession: gated on the
  predecessor run's terminal/`unknown` state, recorded — history reads "no longer live," never a guessed
  "died." Across concurrent unmerged worktrees: caught at merge, disclosed as after-the-fact — the
  stated reason effectful slots want runtime serialization before unattended use.
- **Lineage reads causes.** Attempts reference what they follow; alternating distinct causes and one
  recurring cause read differently and route differently.
- **Nothing fires.** Readers (an unattended session under the standing maintenance Issue, or an
  interactive session) act through the normal consent paths; the ledger answers reads.

### Degraded behavior

**Degraded** when ledger state is present but unreadable, it refuses occupy/record; **degraded** on partially corrupt history, it refuses the affected
occurrences and flags them. Both runtimes drive the same tool.

### What stays out

- **No trigger surface, no scheduler, no repair semantics.**
- **No self-modification** — the ledger's own forbidden-surface check enforces the mechanizable slice;
  the envelope's scope declaration remains a declaration, per the kernel's rule.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Schemas validate; the three guards bite** — double-work without run-state-gated succession, a broken attempt chain, and a self-modifying maintenance diff each fail their negative-fixtured checks. | Schema + the three custom checks ride CI (hard). | engine |
| **Missed occurrences resolve by rule, within the ceiling** — the staged gap resolves per each rule; the staged flood becomes an aggregate escalation at the ceiling. | Fixture: gap and flood scenarios. | operator |
| **Succession is run-state-gated** — a staged live first runner is not succeeded on slot-lease expiry; a staged `unknown` predecessor is, recorded. | Fixture: both staged. | operator |
| **Pre-merge collision is honest** — the staged two-worktree collision is caught by the double-work check at merge and reads as after-the-fact, per the disclosure. | Fixture: staged collision. | operator |
| **Lineage reads correctly; nothing fires** — staged histories read as intended; declaring slots executes nothing. | Fixture: staged histories + declare-and-observe. | operator |
