---
status: draft
---

# audit-library

*Ratified in the design workspace on 2026-06-23 by [decision 0242](../../adr/0242-resolve-the-d-241-audit-memory-read-enablement-the-landed-fo.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../spec/index.md).*

## Summary

The module that **ships the engine's self-audit** — the judgment rung described by the
[audits](../systems/guardrails/audits.md) system. The audits *laws* (the three posture laws, the
function-probe, the hybrid concern model, the digest) live in that system doc; **this module is how they
ship**: the audit persona, the seed concern-list, the audit-digest machinery, and the scheduled run that
fires them. Audits is **not** one of the eleven foundations, but it is **`required`** core
([D-067](../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md)): deployed-repo self-audit hygiene is part of the trust proposition a
non-engineer relies on, so it is **never an install choice** — present in every generated repo, not opt-in
and not removable. ([§12](../../principles.md) keeps the *eleven foundations* minimal; a required *module*
sits on top of them as core that travels and runs by default.)

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `audit-library` |
| `status` | `required` |
| `provides` | the audit persona ([agent](../systems/surfaces/agents.md) file in `.claude/agents/`); the seed **concern-list** + its **concern-entry schema** (audits-owned declarative data); the **audit-digest generator** (the dated, fingerprint-gated digest); the **digest-staleness check** (emits a finding past the staleness bound); the `audit-prep` cron workflow (a `.github/workflows/` file — the default scheduled substrate) |
| `wires` | **none** |
| `depends` | `validators-core` — the semantic self-audit assumes the mechanical self-validation floor holds (the [validators-core](validators-core.md) corpus), a real presence assertion, not merely a catalog edge; rests on the always-present [telemetry](../systems/guardrails/telemetry.md) and [agents](../systems/surfaces/agents.md) foundations |
| `migrations` | none (v1) |

### Wiring nothing — every artifact is active by presence

audit-library is the clean demonstration of the seam discipline: it `wires` **nothing**. Every artifact it
provides is active by **presence** (the [derived binding by presence principle](../../principles.md)):

- the **audit persona** is discovered by Claude Code in `.claude/agents/` and recognized by its `audit`
  role — a file drop, no wiring ([agents](../systems/surfaces/agents.md));
- the **`audit-prep` cron workflow** runs by being a committed `.github/workflows/` file;
- the **concern-list** is read as audits-system-owned data, not a catalogued surface.

So install is a file drop and uninstall a file removal, with nothing to reverse in shared state — the
discovery-side half of the [R5](../../reference/risks.md) containment story.

### The scheduled run — substrate, invocation, and auth

The audit fires on a recurring schedule. Its **default substrate is the committed `.github/workflows/`
`audit-prep` cron**, present in every generated repo. Because that workflow ships committed, the engine holds
a **staleness baseline from day one**: a run that is missing, failing, or not yet authenticated leaves no
fresh digest, and the digest-staleness boot signal surfaces that on the operator's return — the safety net a
never-created cloud routine cannot offer. The workflow file is present automatically; the audit *runs* only
once the operator completes the one-time auth setup below, and the staleness signal is the backstop whenever
that setup is missing or later lapses.

A committed workflow runs the read-only [audit persona](../systems/surfaces/agents.md)
**non-interactively** as the **top-level session** (the locked agents `--agent` top-level-session semantic) —
e.g. `claude -p --agent audit --model <judgment-tier>`. The load-bearing grammar any realization must satisfy:

- the run is **non-interactive** (`-p`/`--print`) — without it a `claude` invocation waits for a TTY the
  runner has not got — and it must **not** be `--bare` (that would skip the `.claude/agents/` persona
  discovery and the token auth the run depends on);
- the persona is the **top-level `--agent` session**, scoped to that run, so it never changes the operator's
  interactive sessions;
- the **`judgment` model-tier the [audits](../systems/guardrails/audits.md) laws fix is pinned at
  the invocation** (`--model`), never left to the persona's frontmatter `model:` — which the platform does
  not reliably apply to a top-level `--agent` session — so the engine's most judgment-heavy run cannot
  silently drop to a default model.
- the run must be able to read the **committed digest's own prior history** — it reads the dated digest sequence as
  the audit-over-audit corroboration input the [audits](../systems/guardrails/audits.md) laws fix. This is
  a **same-repo** read (the digest lives in the repo the run already operates in), so it needs **no auth beyond the
  own-repo workflow token** the run already carries — distinct from the cross-repo memory-backup read below. *How*
  the run obtains the history — the token-free local-`git` read from a **full-history checkout** (the default
  checkout is shallow and carries none), or a `gh`-API read of prior versions — is a build-spec leaf; on a substrate
  whose clone carries no history (the optional Cloud-Routine fresh clone, whose depth the engine does not control)
  the input is simply absent and the audit degrades to a point-in-time review and says so, per the audits digest
  contract.

The concrete vehicle — the official `anthropics/claude-code-action` (passing `--agent`/`--model` through its
CLI args) versus a direct `claude` install — is a **build-spec leaf**; the grammar above is the contract.

**Auth — subscription-funded, no metered key.** The workflow authenticates with a
**`CLAUDE_CODE_OAUTH_TOKEN`** repository secret — a **one-year** token the operator generates once with
`claude setup-token` (a browser sign-in), tied to their Claude subscription, **not** a metered
`ANTHROPIC_API_KEY` (which stays the console-billed alternative). The token **requires a paid plan — Pro,
Max, Team, or Enterprise** — and draws on that subscription's usage like interactive Claude Code, with no
separate metered key and no account toggle to enable. So the setup is two short steps the
walkthrough names **exactly** and in plain language: run `claude setup-token`, then add the result as a
repository secret named *exactly* `CLAUDE_CODE_OAUTH_TOKEN` (GitHub → Settings → Secrets and variables →
Actions) — a name typo fails the run silently. Two honest recurring-cost notes the walkthrough carries: a
**too-frequent** cadence consumes the plan's usage like any other Claude Code work (a run that hits the
usage limit produces no digest until it resets), and the **one-year token expires**. In both cases the
audit simply stops producing digests, so the **staleness notice on the operator's next boot** surfaces the
gap — for the **Claude-run** token (`CLAUDE_CODE_OAUTH_TOKEN`), re-run `claude setup-token` and re-set the
secret when it has expired, or ease the cadence when usage limits are the cause. The **vault read credential**
(below) is a **distinct second credential with its own re-arm** (the provisioning-owned turn-on copy) —
re-issue the read token and re-set *its* named secret, **never** `claude setup-token` — so the staleness notice
**names which of the two lapsed** and routes to the matching one-step recovery. No silent stop goes unsurfaced.

**The substrate is swappable.** The committed audit digest and the digest-staleness boot signal key on the
digest's committed run-date, **not** on any particular runner — so they surface a stopped audit on the
operator's return *whatever ran it*. The engine's grammar names only "the scheduled audit run"; the default
runner is the cron workflow above, and an operator may instead move the run to a **Cloud Routine** (below)
without any redesign.

#### Optional — run the audit as a Cloud Routine

An **Anthropic Cloud Routine** runs the audit on Anthropic-managed cloud, so it fires with the operator's
machine off, drawing on their subscription with no repository secret. It suits the **read-only** audit
precisely where it does **not** suit a [Routine build](../systems/lifecycle/build-orchestration.md):
the audit tolerates a fresh clone and a proposed-changes pull request, where a build needs the operator's
working tree and a scope-lock. (This is the Anthropic **Cloud Routines product** — distinct from the
engine's Local Desktop **Routine build stance**, which deliberately does not use it.)

The walkthrough **eliminates the wrong choices**: create a **Remote** routine (not *Local* — a Local task
runs only while the machine is awake), on a **recurring** schedule (not a one-off), against **this
repository**, pasting the **provided audit prompt verbatim** (it instructs the run to load and follow the
committed audit persona), then **"Run now" once and confirm a fresh digest appears**. Disclosed plainly: a
Cloud Routine needs a **paid plan with Claude Code on the web enabled**, is a **research-preview** feature
that may change — the engine never depends on it; if it stops, the staleness signal says so and the default
workflow remains — and counts against the account's daily routine allowance.

#### Coverage of local memory

The audit's first concern — **stale saved-memory beliefs** — needs the project's experiential memory, which
is **gitignored** and so absent from any committed-files-only run (a GitHub Actions checkout *and* a Cloud
Routine fresh clone both see only committed files). The audit reaches it by reading the operator's **memory
backup** — the off-repo private destination memory already exports to (a **shared vault by default**, or a
per-project repo; [memory](../systems/cognitive/memory.md)) — a **pure read of an existing artifact
that requires and makes no change to the memory system**, seeing only what memory has *committed* there. This
is a real **two-part** precondition, not a free read, and a complete turn-on names **both** parts as one gated
outcome: the **backup must exist** *and* the **scheduled run must be granted access to it** — completing only
the first leaves the read dark.

**The access credential and the pointer.** On the default GitHub-Actions substrate the own-repo workflow token
(`GITHUB_TOKEN`) is repo-scoped and **cannot reach the separate private vault**, so the scheduled run reads it
with a **distinct least-privilege, read-only credential** — a **fine-grained PAT scoped to the single vault
repo, `contents:read` only**, stored as the audit's repository secret (distinct from the own-repo token and
from the `CLAUDE_CODE_OAUTH_TOKEN` that authenticates the Claude run, not the vault read). The run also needs
the **committed destination pointer** to locate the vault — a CI checkout sees only committed files, so
[provisioning](../systems/infrastructure/provisioning.md)'s first-run setup writes *and commits* it
(memory's committed destination pointer, topology law 5). **Provisioning owns the whole turn-on** — scoping the
read credential, storing the secret, committing the pointer — as a **heavy-consent trust gate** in the
operator's own language, never an in-digest toggle; the engine relays the grant rather than leaving a
non-engineer to invent it. Under the **shared-vault default that one read credential spans every co-located
project's namespace** (the co-location [memory](../systems/cognitive/memory.md) discloses at the
backup choice, surfaced again where the secret is set), with the **per-project repo the actionable way to keep
a project out of that grant**.

**Belief content is surfaced only on a private project repo.** The audit digest is **committed to the project
repo**, so naming a stale saved decision would commit a reference to experiential memory into the tree. The
gate is therefore **structural, keyed on repo visibility**: on a **private** repo the digest may reference this
project's saved beliefs (this namespace only — the read reaches no other); on a **public** repo the engine
**omits the belief specifics and says so**, reviewing staleness only in the aggregate it can safely commit. It
stops *future* digests from carrying belief specifics but cannot unpublish a *past* one already committed
(whether the repo was public then or was private and later flipped) ([§7](../../principles.md)) — the delivery
of the digest-contract privacy bound [audits](../systems/guardrails/audits.md) fixes.

When the backup is absent — **or set up but not yet reachable by the run** (the access credential lapsed,
mis-scoped, or mis-named) — the audit **says so in the digest, in plain language**, naming *which* part is
missing and the one step that finishes it: set up the backup, or — when the access half is the gap —
**re-issue the read token and re-set its named secret** (the provisioning-owned turn-on copy, **never**
`claude setup-token`, which is the unrelated Claude-run token). It never silently skips its headline check or
pretends memory is empty — an **actionable** notice the operator clears by completing the turn-on, not a
standing alarm they learn to scroll past.

#### Un-exercised at v1

The scheduled run across substrates — its **cross-repo saved-memory read turn-on** and especially the
Cloud-Routine path — is **not exercised end-to-end during v1 construction**; the walkthrough discloses this at setup in plain
operator language, the same maturity honesty the project applies to other v1-shipped-but-undogfooded paths
([R14](../../reference/risks.md), [R17](../../reference/risks.md), [R31](../../reference/risks.md)).

### Operator-facing register

Every operator-facing surface this module adds — the audit auth-secret step, the **vault-read credential
turn-on** (a heavy-consent gate owned by [provisioning](../systems/infrastructure/provisioning.md)),
the Cloud-Routine walkthrough, the digest's memory-coverage notice, the staleness re-arm prompt — is written in
**plain language**, explaining each platform term where the operator meets it (a *fine-grained read-only
token*, an *Actions secret*) and carrying **no backstage vocabulary** (persona, lens, function-probe,
concern-list, R-numbers). The audit digest itself stays the plain self-attestation the
[audits](../systems/guardrails/audits.md) doc fixes.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The laws are audits'; the delivery is this module** — no duplication of the posture laws here. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **required core, not one of the eleven foundations** — deployed-repo self-audit hygiene ships in every generated repo and is not an install choice ([D-067](../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md)). | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Wires nothing** — persona, workflow, and concern-list are all active by presence; install/uninstall is add/remove files. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Present-by-default substrate, swappable runner** — the committed cron workflow arms automatically; the digest + staleness backstop is runner-independent, so the optional Cloud-Routine path adds no dependency and the engine never relies on a research-preview feature. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Honest coverage** — the local-memory limit of any cloud/CI substrate is bridged through a least-privilege read-only read of memory's own backup (a provisioning-owned, heavy-consent turn-on), with belief content gated to a private project repo and the gap disclosed in plain language whenever either precondition is unmet — never silently skipped, never pretending memory is empty. | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
