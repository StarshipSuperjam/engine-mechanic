# Reference containment

This repository holds the spec and decision record for **engine-template** — 319 decision records
under `docs/adr/`, cited in prose as `D-###`. That corpus stays here on purpose: putting it in
engine-template would push it into every repository generated from the template.

engine-template is distributed by GitHub **"Use this template"**, which copies the *file tree* as
one commit. Issues, pull requests and history do not travel. So there is exactly one harm to guard
against: **a repository deployed from engine-template holding a pointer to something that exists
only here.** Someone lands in a fresh repo, reads `D-156` in a comment, and has nowhere to go.

The rule, stated positively: **a surface that travels names the capability, not the reference.**
Say *"the engine-managed tool runtime"*, not *"D-156"*.

## What is deliberately not scanned

engine-template's own **Issues and pull-request bodies** cite this repository's records freely, and
should keep doing so — the build spec for engine-template lives here, so an engine-template Issue
with no reference to it could not point its build session at the spec that defines the build. Those
never reach a deployed repository. Scanning them would fight the system rather than protect it.

Also never flagged: the engine's own `eADR-####` records. They are a separate, sanctioned system,
exempted by construction rather than by a list.

## Running it

```
python3 tools/reference-containment/check.py surfaces
```

Scans the corners that travel, as this repository received them, and compares against
`surfaces-baseline.txt` — the references that arrived from upstream and are upstream's to fix. It
alarms only on a **new** one. Runs on every pull request.

```
python3 tools/reference-containment/check.py outbound <path>...
python3 tools/reference-containment/check.py diff <base> [<head>] --cwd <engine-template-checkout>
python3 tools/reference-containment/check.py demo
```

`outbound` scans named files or a patch on stdin. `diff` scans a code submission bound for
engine-template — changed paths, the full content of added or renamed files, and added lines. It
does not scan commit messages, because history does not travel. `demo` proves each scanner still
bites its own seeded-bad input; it is the only thing that evidences the guard works at all.

Exit status: `0` clean, `1` findings, `2` could not run. A scan that examined zero inputs reports
`2`, never `0` — "I found nothing" and "I examined nothing" must not print the same word. The one
exception is a submission whose net diff changes nothing: that genuinely carries nothing, so `diff`
calls it clean and says so rather than refusing a legitimate push.

Two extra flags, rarely needed: `--baseline <path>` points `surfaces` at a different baseline, and
`--confirmed-target` tells `diff` to proceed when it cannot work out which repository the target
checkout is (it refuses by default rather than reporting an unknown target as clean).

## Installing the push hook (optional)

For an engine-template checkout you push to, `hooks/pre-push` scans what the push would add:

```
cp tools/reference-containment/hooks/pre-push "$(git -C <engine-template> rev-parse --git-path hooks)/pre-push"
chmod +x "$(git -C <engine-template> rev-parse --git-path hooks)/pre-push"
```

Use `rev-parse --git-path`, not a literal `.git/hooks` — in a git worktree `.git` is a *file*, and
the literal path fails with an unhelpful "Not a directory".

Then point the hook at this scanner, in a place that survives a new terminal — your shell profile,
not just the current session:

```
export REFCON_CHECK="/absolute/path/to/tools/reference-containment/check.py"
```

`REFCON_CHECK` is required — the hook runs in a different checkout and cannot find the scanner on
its own. If it is unset the push is **refused**, not allowed: a scan that did not run must not look
like one that passed. `REFCON_SKIP=1` pushes anyway, deliberately. Note a GUI git client will not
see a variable exported in your shell, so the hook refuses there until you set it another way.

The hook is local, uncommitted, absent on other clones, and bypassable with `--no-verify`. It is a
convenience layer, never the wall.

## When a finding is legitimate

Sometimes the token *is* the subject rather than a citation — a file that documents the rule, or a
test fixture using a reference as data. What to do depends on which check fired.

**`surfaces` (the one that runs in CI).** It is advisory: a red run cannot block your merge. If the
file is one this project owns, reword it. If it came from an engine release, report it upstream and
add a line to `surfaces-baseline.txt` so it stays quiet until the fix arrives — that is the
sanctioned way to accept a finding, and it leaves a record of what was accepted and why.

**`outbound` / `diff` (the ones you run by hand).** These have no baseline and no waiver mechanism.
If you have looked at the finding and it is fine, proceed — with `REFCON_SKIP=1` if it is the push
hook. Say in the submission why: one line noting the tokens appear as evidence of a defect rather
than as references. Nothing enforces that line; it is there so the next reader knows it was a
decision rather than an oversight.

There is deliberately **no escape syntax** in the scanner. An escape syntax is a hole the scanner
then has to defend, and it is the first thing anyone reaches for to silence a finding they would
rather not think about.

## After an engine upgrade

An upgrade replaces most of `.engine/`, so re-check: the workflow and this directory are still
present and the workflow is green; `surfaces` reports nothing new *and* nothing resolved (a
resolved entry means the baseline needs re-cutting); `.engine/operator-guarded-paths.json` still
names this directory; the local patch to `.engine/tools/test_seed.py` is still applied, or upstream
has fixed it; and `.gitignore`'s opening comment has not been re-leaked. The decision record carries
the same list.

## Bounds worth knowing

- A literal token match **narrows** risk; it never proves absence. Split, encoded or homoglyph
  tokens pass, and a paraphrase passes trivially. The review at merge stays the real wall.
- A clean run means no token was found. It does **not** mean the surface names its capabilities —
  prose that names neither passes. No scanner can check the positive half of the rule.
- A file that cannot be read as text is **named in the output and left out of the clean count**,
  never folded into it — it could be UTF-16 text carrying a real reference.
- The baseline records how many times each reference occurs, not just that it occurs, so a second
  citation of an already-recorded token in an already-recorded file still alarms.
- Most `.engine/` copies here arrive from engine releases and are replaced wholesale on upgrade, so
  a fix applied here does not survive; those are tracked upstream. The exceptions are `.gitignore`,
  `CLAUDE.md` and `AGENTS.md`, whose content outside the engine-managed fence is never re-delivered
  — so for those three this repository's copy can drift from what the template actually ships, and
  a clean result here is not evidence about the template.

## Changing any of this

`tools/reference-containment/` is declared in `.engine/operator-guarded-paths.json`, so a pull
request that edits **anything in this directory** — the scanner, its tests, this file, or
`surfaces-baseline.txt` — needs the operator's deliberate `guardrail-ack`, a separate act from
clicking merge. That includes routine baseline maintenance: the alarm is direction-agnostic, so
even deleting a line for a reference upstream has fixed will ask for the label. Expected, not a
fault. The reasoning behind every choice here,
including the token classes that were considered and rejected, is in the decision record under
`.engine/contracts/instance/`.
