---
schema_version: 2
reviewed_at: 2026-08-16
content_modified_at: 2026-08-16
audited_sha: "5a2c4d1ccea6268f40f34b585a6d0c51472a1f8b"
run_id: "31934796181/1"
fingerprint: sha256:1cff88238b66e1ace7b2f256f193d0fc9a509d0243767af018385370d70a3f6b
---

All eleven conformance clusters are back and this cycle's cold read is done. I have what I need to write the digest.

---

**⚠ Project status: couldn't verify the safety gate**

Before the review itself — one governance item I have to pass on, because it reached me and not you: **I could not verify your safety gate this session (no GitHub access from here), so don't assume `main` is protected.** Confirm branch protection is on before you merge anything you care about. (Your live memory and wiring-map helpers are both switched on this session, so nothing to flag there.)

---

# Engine self-review

## What I looked at
Your debt register (the 4 open engine issues, read in full), the soft nudges firing right now, the engine's own checks, your seeded concern-list, one artifact read cold, and — the big piece this cycle — a full conformance pass over all **243 settled spec criteria** in `docs/spec/`, judged against the machinery actually built in this repo (`.engine/`, `.claude/`, `.github/`). I could **not** review your saved memory this run, and I have **no earlier self-reviews to compare against** (the fetch returned a 404) — so everything below is a fresh read of what's here now, not a trend.

## Your saved memory — not reviewed this cycle
There's **no memory backup set up** for this review to read from, so I'm treating your saved decisions and notes as **not reviewed** — not as empty. I genuinely can't see them from here; that's a gap, not a clean bill. To turn this on, just ask me (in an ordinary session) to set up a memory backup — after that, future reviews can check your saved decisions for contradictions and staleness. Declining is fine; this stays honestly-unreviewed without nagging.

Related, and worth knowing: one of your open issues (**#69**) is the engine flagging that it **keeps failing to save session conversations to memory**. So two separate things are true — the engine is having trouble *writing* memory, and this review has no backup to *read*. Neither loses existing data, but together they mean your project's memory is thinner than it should be right now.

## Debt register — small and honestly triageable (4 open)
- **#69 — memory capture degraded.** Engine-opened health flag; benign but real (see above). The durable fix arrives as an engine update, not a repo edit.
- **#54 — record the engine-template relicense (Apache-2.0) in your decision records.** Legitimate tracked follow-up — real work still owed. Keep.
- **#38 / #39 — two engine operation files over their length budget** (`engine-arrival.md`, `engine-upgrade.md`). See below.

The register is short and every entry still reproduces against current state. Nothing here has gone stale or grown past triageable.

One thing the register exposes: your **status card is running on a badly stale cache**. It shows *"31 open engine findings as of 2026-07-12"* — but the live backlog I was handed is **4**. That five-week-old figure is a direct consequence of the next item.

## Soft nudges firing now
Four are live. Three are **engine machinery** and one is **your setup**:

- **The scheduled self-review has never run.** This is the one to act on. It's not just a health check — it's also what refreshes your offline status figures. Because it hasn't run, your cached debt count (31) and "where we are" are a month stale and now actively misleading. **To turn it on:** set up the scheduled review (I can walk you through the token/schedule). Cost of leaving it: your at-a-glance status stays wrong, and the engine never routinely checks its own health. Fair to defer, but it's the highest-value fix on this list.
- **`boot-session-start.md` is 210/200 lines**, **`engine-arrival.md` 128/120**, **`engine-upgrade.md` 144/120** (this last one has grown from 122 since it was first flagged — drifting the wrong way). These are engine-shipped files. **Fixing them by hand in this repo won't stick** — the next engine update overwrites engine machinery wholesale, wiping the edit. The durable fix belongs in your product, `engine-template` (which this engine builds), through a normal mechanic build against it. Note `boot-session-start.md` isn't tracked by any open issue yet, unlike the other two. All three are nudges — nothing blocks. Fine to leave.

## Engine checks and your concern-list — clean
Every one of the engine's file-scoped checks currently matches at least one real file — nothing looks like dead weight. And re-reading your seeded concern-list fresh: all six concerns still catch a drift the generic read would miss and still can't be reduced to a mechanical check. **No retire-candidate there.**

## Cold read this cycle — `.engine/docs/getting-started.md`
Read with no prior context. It addresses you as a capable adult, stays in plain language, leaks no internal jargon, and its references (`/engine-help`, `/engine-parts`, `/engine-design`, the memory-backup offer) all resolve to things that actually exist. No stale sibling, no talking-down. **Clean — no finding.** (It's engine machinery, so had I found a wording problem, the fix would've been product-build work, not a local edit.)

## Product-spec conformance — 243 of 243 checked, honestly partial
**Coverage, plainly:** I re-derived and judged all **243 settled criteria** this cycle (the feed marked every one recently-changed; none were left to a spot-check sample). But be clear on what that means: **every verdict is my judgment reading the built machinery against your frozen wording — no behavioral or runtime test was run.** These are prompts for you to look, adjudicated when you reconcile, not proven defects. This is **not** a clean whole-spec pass. Two things diverge, and about a dozen I honestly couldn't fully confirm.

**Two divergences worth your eyes:**

1. **Several "ships in every Engine" modules actually ship as optional add-ons.** Your newer spec wording (the three-axis distribution/applicability/activation grammar) says modules like **dependency-discipline** and **migration-discipline** are *required* — present in every Engine, not an install choice. But the built manifests still use a single `status` field, and dependency-discipline ships `status: optional` and appears in the offerable add-on catalog (migration-discipline's manifest reads optional too). One root cause: the three-axis manifest grammar the spec describes **isn't built yet**, so the "required" reclassification hasn't landed in the manifests. A reader following the spec would expect these always-present; the build makes them opt-in.

2. **The knowledge graph's "explicit skill-routing" is specced but not built.** `knowledge.md` says skill routing targets are derived from structured frontmatter (never a prose guess), with route-generation tests. As built, the generator emits **no routing edges from skills at all** — the schema has no routing field and no such tests exist. The "never a prose guess" guarantee holds only because no route derivation happens. A forward obligation with no implementing code behind it.

**What I couldn't fully confirm (~12 criteria, all in provisioning):** these describe first-run/instantiator behavior, and the instantiator **correctly self-retired** after setup, so its logic isn't inspectable from this repo. I verified the *surviving* side — seeded files present and correctly owned, overlay-preservation classifications right — and marked these **unsure** rather than fake a pass. Honest gap, not a finding.

**Minor drift noticed in passing (not criterion divergences):** a stale code comment in `boot_alarm_ledger.py` (names one retire-eligible class where the code has two — the code matches spec, the comment lagged); a `disposition-issue-resolution` check described in prose but not built; and a CODEOWNERS render that's drifted from its source list. All engine machinery — same fix path as the nudges above.

All of the conformance work points at one place: **your product, `engine-template`.** Every divergence and every machinery nudge is reconciled the same way — an ordinary mechanic build against engine-template — which needs the product checkout pointed at first (that setup offer is already on your card). A hand-edit to `.engine/` here would just be overwritten on the next update.

## Retirement — nothing clearly retireable, and I'll be honest about why
My standing job is to find local cruft that no longer earns its place. This cycle I found **none** — but I owe you the caveat that my "nothing to retire" is only partial. The conformance hunt-set (243 criteria) consumed most of this run. I did the standard sweeps and the cold read, but I did **not** deeply probe your project-authored local surfaces — your instance decision-record stream, any local operations or skills — for orphans or abandoned proposals. So read this as "no retire-candidate surfaced," not "I searched the retirement ground hard and it's clean." That deeper local-surface probe is the natural first target next cycle.

## What I recommend
Nothing here forces your hand; each is a real choice:
1. **Set up the scheduled self-review** (fixes the month-stale status figures and starts routine health-checking). Ignore it and your at-a-glance status stays wrong.
2. **Set up a memory backup** (lets future reviews actually read your saved decisions). Declining keeps memory honestly-unreviewed.
3. **When you're ready, point me at your `engine-template` checkout** — then the two conformance divergences, the length-budget trims, and the stale-comment/CODEOWNERS bits all become ordinary build work against your product. Leaving them costs nothing today; they're drift, not breakage.
4. **#69 (memory capture)** rides an engine update — nothing to do but know it's flagged.

## Memory recall completeness

Memory recall reaches both the summaries of past sessions and the word-for-word conversation behind them, so something said once and never summarised can be found — not only read back if you already know which session to look in. Nothing was forgotten or deleted. What comes back is the conversation as it was captured, and it was never cleaned of things like passwords or personal details, so treat a recalled answer as unreviewed text and ask to see the exact wording of anything it rests on.