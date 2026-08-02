---
schema_version: 1
generated: 2026-08-02
fingerprint: sha256:e07d777003d1a7f2b04ffd5ba81c77af60844e3c06869fa91a76a7ec83ad2bed
---

## Engine self-review

### What I looked at
I ran cold, as if new to this project. This is the development repo for your engine template itself, so its `.engine/` corner is the *installed* engine machinery (overlaid wholesale on each update) while your product is the template those files come from — a distinction that matters below. This cycle I read the seeded concern checklist, your one instance decision record in full (cold), the guarded-paths declaration, your installed-module manifest, and swept the local surfaces (operations, skills, agents, policies, instance contracts). I was also handed your open engine issues (4), the soft nudges firing now (4), and the engine's own checks.

### What I couldn't see this run — three honest gaps
- **Your saved memory was not reviewed.** A backup is set up, but this review wasn't granted access to it — its read key is missing, expired, or pointed at the wrong place. This is a standing setup gap, not a passing glitch. The fix is to re-issue the backup's read-only key and re-set the `MEMORY_VAULT_TOKEN` secret. Note this is **not** `claude setup-token` (that's the separate key that runs this review), so re-running that won't help. I can't tell you whether any saved decisions now contradict each other until this is restored — and I'm not concluding your memory is empty; I simply couldn't see it.
- **No earlier self-reviews to compare against.** The fetch of my own prior reviews failed (a 404). So everything below rests only on what I can check right now — I'm not claiming any trend over time, because I can't see one.
- **The safety gate couldn't be verified** (already relayed at the top): don't assume `main` is protected — confirm before merging anything important.

### What I found

**Your debt register is small and honestly triageable — 4 open items, all engine machinery.** Three are length-budget nudges on engine operation files (`build-orchestration` 326/250, `boot-session-start` 166/150, `product-intake` 127/120); one is a health flag that the engine keeps failing to save session conversations to memory (#22). That memory-capture flag is consistent with what I hit myself this run, so I have no reason to think it's gone stale — it still looks live. All four are engine machinery, so a fix made in this installed copy is wiped on the next update. The durable home for all of them is the engine-template source — which, unusually, *is* the product you develop in this repo, so these are genuinely actionable for you rather than a distant upstream. Ignoring the length nudges stays fair — they never block anything.

**Soft nudges firing now — four, classified:**
- *Self-review isn't scheduled yet.* This is a setup step you can enable (or ask me to): once the engine's health review runs on a schedule, this notice clears. Purely optional.
- *`engine-arrival.md` (128/120) and `engine-upgrade.md` (122/120) over budget* — both engine machinery, same story as the register items above: trim them in the template source, not the installed copy, or leave them.
- *Your instance decision record `eADR-0001` is 123/120* — this one is **yours** (local state, preserved across updates), so a trim here would actually stick. But I read it in full and every line earns its place; the 3-line overage buys real precision. I'd leave it unless you're tidying anyway.

**Your one instance decision (reference-containment) is healthy and load-bearing.** I read it cold: it addresses you as a capable adult, avoids jargon, its references all resolve (the `tools/reference-containment/` scanner, the workflow, the guarded-paths file, and `test_seed.py` all exist as described), and its "confirm after every upgrade" checklist is genuinely actionable. Nothing in it reads as stale or as build-schedule narration — the open gaps it names are durable facts about why the code is shaped as it is. No finding.

**One standing local stop-gap, working as intended.** That same record discloses a local patch to an engine-owned file (`.engine/tools/test_seed.py`), held over until engine-template issue 638 ships upstream. This is the calm, steady state — it's still doing its job and nothing changed this cycle, so it's a standing line, not a fresh recommendation. When you want to retire it, the record already carries the upstream link; you (not I) follow it to confirm the fix actually shipped before removing the patch. I did not re-verify the patch is still physically applied this run — worth a glance next time you touch that file.

**Installed optional modules — a question, not a verdict.** You have six optional add-ons installed (dependency-discipline, design-review, external-contribution, github-projects-sync, migration-discipline, qa-review). I did **not** run a per-module usage probe this cycle, so I'm not nominating any for retirement — on their face each maps to a plausible need for a repo that develops an engine template. If any of these feels like it never actually fires for you, that's the one to ask about: *what does it do that nothing else does?*

**Clean reads:** every one of the engine's own file-scoped checks matches at least one file here (no dead checks), and no orphaned local surfaces or abandoned proposals turned up.

### Is there anything to retire? No — and here's me scrutinising that
My standing bias is to retire local cruft, so I looked hard. The honest answer this cycle is nothing. Testing that claim: the instance record is actively guarding a documented leak (not dormant); all six checklist concerns still catch something the generic sweep misses — I confirmed concern #5 specifically by finding the `test_seed.py` stop-gap it exists to surface, which the plain debt-register row would never nudge; and the only clearly-local, clearly-remediable artifact (the over-budget instance record) earns its length. The one place I'm genuinely blind is the optional modules' actual usage, so if a hollow keep is hiding anywhere, it's there — which is why I've put it to you as a question rather than pretending I cleared it.

### What I recommend
1. **Restore this review's access to your saved memory** — re-issue the backup's read-only key and re-set `MEMORY_VAULT_TOKEN`. *Cost of not acting:* every future self-review stays blind to whether your saved decisions have gone contradictory or stale. *Keep-it-as-is:* fine if you review memory yourself in ordinary chat sessions instead.
2. **Optionally schedule the self-review** so the engine checks its own health on a cadence. *Cost of not acting:* these reviews only happen when you ask. *Ignore:* perfectly reasonable if you prefer running them by hand.
3. **The five over-budget engine operation files are machinery** — decide whether to trim them in your engine-template source (where it'll stick) or leave them. *Cost of not acting:* nothing blocks; longer files are just harder for a fresh session to read whole.
4. **No upstream bug to file** this cycle — the machinery nudges are ordinary length budgets, not defects, and their durable home is a product you already own.

I changed nothing — this is a report only.


## Memory recall completeness

Memory recall reaches both the summaries of past sessions and the word-for-word conversation behind them, so something said once and never summarised can be found — not only read back if you already know which session to look in. Nothing was forgotten or deleted. What comes back is the conversation as it was captured, and it was never cleaned of things like passwords or personal details, so treat a recalled answer as unreviewed text and ask to see the exact wording of anything it rests on.