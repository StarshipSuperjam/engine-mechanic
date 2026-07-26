---
status: draft
---

# State

*Ratified in the design workspace on 2026-07-16 by [decision 0317](../../../adr/0317-resolve-re-lock-state-the-taxonomy-kept-its-attachment-narro.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../../spec/index.md).*

## Summary

Answers **"where am I?"** — the temporal cursor every session reads first. State is small by design:
a set of committed pointers to the project's standing situation, not a store of depth. Because it is
committed, it is also the degradation floor — when every out-of-repo substrate is unavailable,
orientation still proceeds from State.

## Behavior

### What it is

One schema-validated, committed, git-native **machine-state file** — a *pointer* file, not a data
store, so it is the permitted committed pointer [repository-topology](../infrastructure/repository-topology.md)
law 5 carves out (configuration is not data). It lives in State's own subtree under `.engine/`, laid
per topology's Tier-2 placement law. It holds **pointers and counts only**:

- the project's **standing-situation** — where the work stands (the current phase + milestone). It is a
  read-only projection of native sources (the engine's build Issues for the phase; the project's **current**
  GitHub Milestone under the selection bound below, or `none set`, for the milestone) that
  [boot](../lifecycle/boot.md) assembles
  live; State's committed copy is a derived convenience for the offline/degraded read, never authoritative —
  the debt count's sibling, not a hand-advanced pointer;
- a **debt count + pointer** into the integration-debt register: the count, an *as-of* refresh marker,
  and where to look. The register itself is [telemetry](../guardrails/telemetry.md)'s view
  over open engine-labeled GitHub Issues; State's count is a derived convenience, never authoritative —
  its value is the offline/degraded read, refreshed by telemetry.

All committed, all diffable, all readable without any out-of-repo service.

What State deliberately does **not** hold:

- **a work inventory** — where the work lives is the native git/GitHub record (open branches and pull
  requests are in-flight work; open Issues are deferrals and backlog; Milestones are the plan), not a
  committed list. [attention](attention.md) *orders* the in-flight half and the engine-labeled
  debt register; the backlog and the plan carry the **plan's** ordering — decomposed by the engine from
  the spec the operator accepted and `locked`, and living as work lands — which attention never re-ranks
  ([D-314](../../../adr/0314-litigate-engine-template-394-attention-s-work-record-commiss.md));
- **session stance** — every session boots [Explore](../lifecycle/modes.md); stance is decided
  per-session and never persisted (a crashed Build session must not resurrect as Build);
- **narrative** — the open draft pull request is "what we're doing now"; merged PR bodies plus
  [memory](memory.md) are "what just happened"; State carries no prose log;
- **depth** — that is [memory](memory.md) and [knowledge](knowledge.md);
- **the debt register itself** — telemetry owns it.

### Why it is a foundation

A cold-booting session has no idea where the project stands. State is the minimum that makes the first
orientation correct, and because it is committed it is the [degradation](../../../principles.md) floor:
if the memory and knowledge servers — and even GitHub — are unreachable, [boot](../lifecycle/boot.md)
still orients from State alone.

### The malformed-file posture: fails loud, never misleads

A schema-invalid State file is **refused — never fed to the model as a misleading cursor**. The *file*
fails loud — the [schemas](../surfaces/schemas.md) / [validation](../guardrails/validation.md)
foundation's halt-on-malformed posture — while the *session* does not crash.
[Boot](../lifecycle/boot.md) surfaces the refusal in plain language (an injected orientation
notice plus a [telemetry](../guardrails/telemetry.md) finding, never a `SessionStart`
exit-code halt — that event has no block semantics) and falls through to the hook-independent root
`CLAUDE.md` floor. This is fail-loud within fail-open ([principles §5/§6](../../../principles.md)): a
non-engineer is told plainly that the cursor is unreadable and that project status is untrustworthy
until it is fixed, rather than being silently oriented from a corrupt file or hard-stranded.

### Honest degradation limits

State is the floor because it commits the cheap cursor offline-readable — but the floor is bounded, and
the design states the bound rather than overclaiming "orient from State alone":

- **Offline-answerable from State + local git:** the standing-situation cache (best-effort, rendered
  stale-labelled), the last-known debt count, and local branches and pull requests.
- **Degrades with GitHub:** the live standing-situation projection (`phase` and `milestone`) and
  [telemetry](../guardrails/telemetry.md)'s engine-labeled debt register are GitHub-derived;
  any read failure — outage *or* expired auth — falls back to the committed values above, and
  [boot](../lifecycle/boot.md) says so loudly; substantive work then proceeds degraded only past
  [build orchestration](../lifecycle/build-orchestration.md)'s plan-gate consent step.
- **Beyond State's reach:** when even `SessionStart` fails, State cannot announce its own corruption (the
  emitter did not run). That legibility is the hook-independent floor's job — the root `CLAUDE.md` carries
  the standing expectation-setter (*if you see only this and no boot orientation, the engine did not fully
  ground; treat project status as unknown*), whose exact wording is [boot](../lifecycle/boot.md)'s.
- **Known-unbounded — faults the floor does not catch:** two failure modes pass through. A hand-edit that
  leaves the cursor **schema-valid but factually wrong** clears the malformed-file refusal (which catches
  only schema-*invalid* files), so the surfaced situation can be confidently wrong; the catch for it is the
  operator's review of the committed cursor diff, not State. And a GitHub auth/scope failure **errors**
  (401/403/404) rather than returning empty — so the degrade-with-GitHub fallback above is correct only if
  the reading guard treats that error as a *read failure*, never **swallowing it as "empty / unprotected"**
  (the failure mode is the swallow, not a literal empty read). State names these bounds rather than
  implying the partition is exhaustive.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **One cursor, schema-validated.** A single machine-state file governed by the [schemas](../surfaces/schemas.md) surface; the malformed file fails loud (above), so a corrupt cursor never misleads. | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
| **A cursor, not a register / store / inventory / narrative.** State stays tiny so the first thing read every session is cheap; everything that grows lives with its owner — debt in [telemetry](../guardrails/telemetry.md), depth in [memory](memory.md) / [knowledge](knowledge.md), work in git/GitHub, narrative in pull requests. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Pointers and counts only.** The debt count carries an as-of marker so it renders with provenance ("*N open problems as of <when>, source: GitHub Issues*"). When it can only be read from State's offline copy it renders so the operator cannot mistake it for current — "*N open problems as of <when> — I couldn't refresh this, so it may be wrong; re-ground before you rely on it*" — and substantive work on a degraded count waits on [build orchestration](../lifecycle/build-orchestration.md)'s plan-gate consent step (boot surfaces the degraded readout; the gate is build-orchestration's). It is never the authoritative register. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **The standing-situation is assembled, not advanced.** Where the project stands is a read-only projection of native sources — `phase` from the engine's own build Issues + git (the most-recently-merged tracked build Issue), `milestone` from the project's **current** GitHub Milestone under the selection bound below when one exists and `none set` when it does not — assembled live by [boot](../lifecycle/boot.md) the way it assembles recently-shipped work. **No session advances it, and [build-orchestration](../lifecycle/build-orchestration.md) owns none of it**: build-orchestration merely produces the GitHub artifacts (build Issues; the Milestones it emits, grouped per the [product-design](../../modules/product-design.md) build-plan when one drives the build; and Milestone progress) the projection reads. The committed copy is only the offline cache (above), refreshed best-effort from the same source as the debt count and rendered with the same staleness provenance, never the authority — so online a cold boot reads the live projection, not a stored marker that could rot. The honest bound is named, not hidden: `phase` is engine-derivable (strong, like the debt count) — a *max* over an attribute always present on its candidates, so it carries no ambiguity, only a zero case; `milestone` names Milestones that are **engine-planned when a [product-design](../../modules/product-design.md) build-plan drives the build** (build-orchestration emits the ones the build-plan groups) and operator-kept otherwise ([principles §2/§3](../../../principles.md)) — but its **provenance** is not its **derive**, and the derive is where GitHub supplies nothing. **The selection bound is State's to fix, because the platform has no answer to select:** GitHub names no *active* Milestone — a Milestone is only `open` or `closed`, several may be open at once, and a due date is optional, so there is no field to elect one by. So the bound **reads rather than infers**: the field carries the **open Milestone set as found** — the one, where exactly one is open; **all of them, named**, where several are; `none set` where none are open (which is *not* the same as the project keeping none). Where a build-plan drives, its phases **are** those Milestones, so the open set already is the open phase — no join key to invent, no ordering rule, nothing to guess. **The engine never elects one of several by a heuristic of its own:** nothing consumes this field but the operator's display, so inferring a single "current" would buy nothing and would be the confident-looking partial picture the degradation law forbids — and a due-date heuristic would buy worse than nothing, since a stalled Milestone stays open with its date in the past and would be pinned as "current" indefinitely ([§5](../../../principles.md), [D-315](../../../adr/0315-amend-d-314-correct-its-operator-authorship-premise-the-buil.md)). Rendering is [boot](../lifecycle/boot.md)'s under its card laws; this bound fixes only what the field carries. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Operator-facing "now and next" is surfaced, not stored** — on two channels, not one. Locking State tiny does not orphan the operator's "where are we": [boot](../lifecycle/boot.md) **pushes** the *now* — the in-flight work and open debt [attention](attention.md) orders, the recently-shipped digest, and the standing `phase`/`milestone` — while the *next* is **pulled** on demand through the [status verb](../../../reference/glossary.md), under boot's push/pull split. **"Next" is read, not ranked:** where a build Issue carries a checklist it is that checklist's next unchecked item (the record is [build orchestration](../lifecycle/build-orchestration.md)'s, written proportionately), under the phase order of the build-plan where one drives the build; where no build is in flight, **nothing is next until the operator names one** — said plainly, never rendered as an empty ranking ([D-314](../../../adr/0314-litigate-engine-template-394-attention-s-work-record-commiss.md)). State holds the cursor; the view is assembled. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Seams are deferrals.** [attention](attention.md) orders; [telemetry](../guardrails/telemetry.md) owns and refreshes the debt register; [boot](../lifecycle/boot.md) **assembles and surfaces the standing-situation** read-only from native sources (and reads the committed cache offline); [memory](memory.md) / [knowledge](knowledge.md) hold depth; [modes](../lifecycle/modes.md) decides stance. State **owns** the cursor file (its offline-cache fields), its schema, and its laws; it is never *advanced* by a session — its values are derived projections, the debt count's sibling. | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
| **The offline cache is refreshed by one shared pass and committed as freight.** The two offline-cache fields — the standing-situation and the debt count, **both together, never split** — are refreshed by a single GitHub-derived-cache pass (composing [telemetry](../guardrails/telemetry.md)'s debt-count derive and [boot](../lifecycle/boot.md)'s standing-situation derive) and **committed by the [audits](../guardrails/audits.md) digest pass as freight** on its periodic, operator-reviewed self-attestation pull request (the concrete refresh-and-commit wiring lands with the [audit-library](../../modules/audit-library.md) build). Two bounds are named, not hidden. The cache rides that pull request as a **separate committed file gated by its own schema check, not folded into the digest's fingerprint gate**: it is **schema-gated, not drift-gated**, because a cache derived from continuously-changing *external* GitHub state has no committed referent to fingerprint against (unlike the [knowledge](knowledge.md) graph and the self-map, which derive from committed source) — a drift gate here would be incoherent, not merely omitted ([principles §3](../../../principles.md)). And **a missed audit cron is not a silent no-op**: it only *ages* the labelled offline copy, never the live online read ([boot](../lifecycle/boot.md) derives that live each session), so an un-refreshed cache cannot silently mislead the way an advanced-and-unrefreshed stored cursor once did (#100). | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
| **The field set is a build-spec detail.** The exact fields and JSON Schema of the machine-state file are fixed in State's build-spec pass; this document fixes the laws, not the leaves. | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
