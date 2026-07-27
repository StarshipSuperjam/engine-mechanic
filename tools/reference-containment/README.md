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
`2`, never `0` — "I found nothing" and "I examined nothing" must not print the same word.

## Installing the push hook (optional)

For an engine-template checkout you push to, `hooks/pre-push` scans what the push would add:

```
cp tools/reference-containment/hooks/pre-push <engine-template>/.git/hooks/pre-push
chmod +x <engine-template>/.git/hooks/pre-push
export REFCON_CHECK="$PWD/tools/reference-containment/check.py"
```

`REFCON_CHECK` is required — the hook runs in a different checkout and cannot find the scanner on
its own. If it is unset the push is **refused**, not allowed: a scan that did not run must not look
like one that passed. `REFCON_SKIP=1` pushes anyway, deliberately.

The hook is local, uncommitted, absent on other clones, and bypassable with `--no-verify`. It is a
convenience layer, never the wall.

## When a finding is legitimate

Reporting a leak means quoting it. An issue that says *"this file contains `D-296`, please remove
it"* will trip the scanner, and that is correct — the token is the subject, not a citation nobody
can follow. Waive it consciously and say so in the body: one line noting the tokens appear as
evidence of a defect rather than as references. Do not add an escape syntax to the scanner; an
escape syntax is a hole the scanner then has to defend, and it is the first thing anyone reaches
for to silence a finding they would rather not think about.

## Bounds worth knowing

- A literal token match **narrows** risk; it never proves absence. Split, encoded or homoglyph
  tokens pass, and a paraphrase passes trivially. The review at merge stays the real wall.
- A clean run means no token was found. It does **not** mean the surface names its capabilities —
  prose that names neither passes. No scanner can check the positive half of the rule.
- The scan is case-sensitive, so a lowercase `d-296` passes. That is a deliberate trade: the
  lowercase form appears inside slugified record filenames, which are not references.
- The `.engine/` copies here arrive from engine releases and are replaced wholesale on upgrade, so
  a fix applied here does not survive. The recorded baseline entries are tracked upstream instead.

## Changing any of this

`tools/reference-containment/` is declared in `.engine/operator-guarded-paths.json`, so a pull
request that edits the scanner, its tests, or this file needs the operator's deliberate
`guardrail-ack` — a separate act from clicking merge. The reasoning behind every choice here,
including the token classes that were considered and rejected, is in the decision record under
`.engine/contracts/instance/`.
