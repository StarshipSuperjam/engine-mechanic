#!/usr/bin/env python3
"""Reference containment — the wall around this repository's own reference vocabulary.

WHAT THIS PROTECTS. engine-template is distributed by GitHub "Use this template", which
copies the FILE TREE as one commit. Issues, pull requests and history do not travel. So the
harm this guards against is exactly one thing: a repository deployed from engine-template
holding a pointer to something that exists only in engine-mechanic. The containment surface
is therefore precisely the committed file tree that ships — nothing else.

WHAT IS DELIBERATELY NOT SCANNED. engine-template's own Issues and pull-request bodies
legitimately cite this repository's decision records, and must keep doing so: the build spec
for engine-template lives here, so an engine-template Issue with no reference to it could not
point its build session at the spec that defines the build. Those references never reach a
deployed repository. Scanning them would fight the system, not protect it.

THE VOCABULARY. This deployment's references are the decision numbering D-### (records
0001-0319 under docs/adr/, cited in prose as D-24 and in full as D-0024), the record paths
themselves, and the retired design workspace name. The engine's own eADR-#### records are a
separate, sanctioned system and are never flagged — the negative lookbehind below exempts
them by construction, not by an exclusion list.

WHY IT LIVES IN PRODUCT TERRITORY, NOT AS AN ENGINE CHECK. An engine-side module cannot host
it: a module on disk but absent from the engine manifest's packages map fails the
release-integrity check, and one listed in packages makes every engine upgrade refuse (a
release never contains an instance-specific module). Product territory is walled off from
engine upgrades by contract. The workflow that runs this sits under the engine
weakening-guard's watched prefix, and this directory is declared in
.engine/operator-guarded-paths.json, so editing the scanner itself now requires a deliberate
acknowledgement. Recorded in .engine/contracts/instance/.

Modes:
  surfaces [--baseline P]  scan the traveling engine corners as this repository received them
                           — a faithful mirror of what engine-template ships — and compare
                           against the committed baseline. Exits 1 only when the leak set
                           GREW; a set that is unchanged or smaller is clean. The known
                           residue is upstream's to fix, so it is recorded, not re-alarmed.
  diff BASE [HEAD]         scan an outbound code submission to engine-template: changed
      [--cwd DIR]          paths, the full content of added-or-renamed files, and added lines
                           of modified files. Commit messages are NOT scanned — history does
                           not travel to a deployed repository.
  outbound PATH... | -     scan named files, or a patch on stdin.
  demo                     falsification: every scanner must bite its seeded-bad input and
                           stay quiet on its clean twin; non-zero if any fails to bite.

HONEST BOUNDS. A clean result is a literal token match only — it narrows the risk, it never
proves absence (split, encoded or homoglyph tokens pass, and paraphrase passes trivially).
A clean run means no local token was found; it does NOT mean the surface names its
capabilities rather than its references — no scanner can check that. The token scan is
case-sensitive, so a lowercase `d-296` in prose passes. The review gate stays the real wall.

Exit status: 0 clean, 1 findings (or demo falsified), 2 usage/environment error.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# This deployment's decision numbering. Range is D-1..D-319, written short in prose (D-24) and
# zero-padded four digits as the record id (D-0024) — docs/adr/README.md states both spellings.
# The (?!\d) tail stops a five-digit run being clipped into a false match; an earlier draft used
# (?![\d-]) which made D-0042 match NOTHING, trading a real blind spot for a D-1234 collision
# that cannot exist in a 1..319 range. CASE-SENSITIVE: the lowercase form appears inside
# slugified record filenames (0315-amend-d-314-...md), which are not references.
D_TOKEN = re.compile(r"(?<![A-Za-z0-9])D-\d{1,4}(?!\d)")

# The record path/link form, absolute and corpus-relative. The `.md` suffix is load-bearing: it
# excludes `docs/adr/0007-slug` used as a generic illustration in the engine's own tools.
ADR_PATH = re.compile(r"(?<![\w.-])(?:\.\./)*(?:docs/)?adr/\d{4}-[a-z0-9][a-z0-9-]*\.md")

# The alternate spelling, near-vestigial here but cheap to keep armed. The negative lookbehind
# is what exempts eADR-#### BY CONSTRUCTION — never replace it with an exclusion list. Note the
# exemption covers letter-prefixed schemes only: `-ADR-0037` still matches.
ADR_TOKEN = re.compile(r"(?<![A-Za-z])ADR-\d{3,4}", re.IGNORECASE)

# The retired design workspace's name.
PLANNING_TOKEN = re.compile(r"engine-planning", re.IGNORECASE)

PATTERNS = (D_TOKEN, ADR_PATH, ADR_TOKEN, PLANNING_TOKEN)

# The corners that TRAVEL: engine-template ships these, so a deployed repository receives them.
# This repository's copies arrive from engine releases, which makes them a faithful mirror of
# what ships. docs/ is the vocabulary's sanctioned home and never travels (engine-template has
# no docs/ at all); README/LICENSE/SECURITY here are this deployment's own, not the template's.
TRAVELING_SCOPES = (".engine/", ".claude/", ".codex/", ".agents/", ".github/",
                    "CLAUDE.md", "AGENTS.md", ".gitignore")

# Carved out of the corners above: paths that sit under .engine/ but belong to THIS deployment and
# never ship. The engine preserves each of them across an upgrade precisely because they are the
# operator's, not the engine's — which is the same reason they cannot leak into a deployed
# repository. `contracts/instance/` is this deployment's own decision stream, and a record
# explaining a containment rule has to be able to name the vocabulary it contains — the same
# sanctioned-home argument that excludes docs/. Discovered by the guard biting its own record.
LOCAL_SCOPES = (".engine/contracts/instance/", ".engine/operator-guarded-paths.json",
                ".engine/operator-overrides.json", ".engine/conduct/operator.md",
                ".engine/provisioning/readme-seed.md", ".engine/provisioning/conduct-seed.md",
                ".engine/provisioning/security-seed.md", ".engine/state/", ".engine/memory/")

# This directory necessarily discusses the vocabulary it bans. The tests do not RELY on this
# exclusion — they assemble token literals at runtime, so no matchable string sits in them.
SELF_PREFIX = "tools/reference-containment/"

BASELINE_REL = SELF_PREFIX + "surfaces-baseline.txt"


def _git(args, cwd=None):
    res = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True,
                         encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError("git " + " ".join(args) + " failed: " + res.stderr.strip())
    return res.stdout


def _repo_root(cwd=None):
    return Path(_git(["rev-parse", "--show-toplevel"], cwd=cwd).strip())


def _origin(cwd=None):
    """The origin remote URL, or '' when there is none. Used to tell repositories apart —
    resolved paths cannot, because this repository is normally worked in a git worktree."""
    try:
        return _git(["remote", "get-url", "origin"], cwd=cwd).strip()
    except RuntimeError:
        return ""


def _repo_slug(url):
    """owner/name from a remote URL, lowercased; '' when it cannot be parsed."""
    if not url:
        return ""
    s = url.strip()
    if s.endswith(".git"):
        s = s[:-4]
    s = s.split("://")[-1]
    if "@" in s.split("/")[0]:
        s = s.split("@", 1)[1]
    s = s.replace(":", "/")
    parts = [p for p in s.split("/") if p]
    return "/".join(parts[-2:]).lower() if len(parts) >= 2 else ""


def _scan_text(text, patterns, origin):
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for pat in patterns:
            for m in pat.finditer(line):
                findings.append((origin, lineno, m.group(0)))
    return findings


def _scan_path_string(rel, patterns):
    """A changed path travels too: a file NAMED after a record carries the token with no
    scannable content line (a pure rename produces no diff hunks at all)."""
    out = []
    for pat in patterns:
        for m in pat.finditer(rel):
            out.append(("changed path '" + rel + "'", 0, m.group(0)))
    return out


def _fmt(f):
    origin, lineno, token = f
    where = origin if lineno == 0 else origin + ":" + str(lineno)
    return where + ": contains '" + token + "'"


def _key(f):
    """Baseline identity: file plus token, deliberately WITHOUT the line number — engine
    releases move these lines wholesale, and a baseline keyed to line numbers would need
    re-cutting every upgrade, which is churn with no signal."""
    return f[0] + "\t" + f[2]


# --------------------------------------------------------------------------- surfaces

def scan_surfaces(root=None):
    """Returns (findings, files_scanned). The traveling corners as received here."""
    root = Path(root) if root else _repo_root()
    findings = []
    scanned = 0
    for rel in _git(["ls-files", "-z"], cwd=root).split("\0"):
        if not rel or rel.startswith(SELF_PREFIX) or rel.startswith(LOCAL_SCOPES):
            continue
        if not rel.startswith(TRAVELING_SCOPES):
            continue
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binary, gitlink, or unreadable — not scannable text
        scanned += 1
        findings.extend(_scan_text(text, PATTERNS, rel))
    return findings, scanned


def read_baseline(path):
    """The recorded, upstream-owned residue. Absent file -> empty set (a first run records
    everything as new, which is the loud and correct behavior)."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError:
        return None
    keys = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        keys.add(line)
    return keys


def compare_to_baseline(findings, baseline):
    """Returns (new, resolved). `new` is what must alarm: a reference that reached a traveling
    surface after the residue was recorded. `resolved` is good news, reported not alarmed."""
    seen = {}
    for f in findings:
        seen.setdefault(_key(f), []).append(f)
    new = []
    for k in sorted(seen):
        if k not in baseline:
            new.extend(seen[k])
    resolved = sorted(baseline - set(seen))
    return new, resolved


# --------------------------------------------------------------------------- diff

_DIFF_HEADERS = ("+++ b/", '+++ "b/')


def _changed_paths(base, head, cwd, filt=None):
    args = ["diff", "--name-only", "-z"]
    if filt:
        args.append("--diff-filter=" + filt)
    args.append(base + "..." + head)
    return [r for r in _git(args, cwd=cwd).split("\0") if r]


def check_diff(base, head="HEAD", cwd=None, allow_self=False):
    """An outbound code submission to engine-template. Commit messages are NOT scanned:
    history does not travel to a repository deployed from the template."""
    if not allow_self:
        here = _repo_slug(_origin())
        there = _repo_slug(_origin(cwd=cwd))
        # Compare by remote, not by resolved path: this repository is normally worked in a git
        # worktree, so two paths of the SAME repository would otherwise read as different ones.
        if here and there and here == there:
            raise RuntimeError(
                "diff mode scans a submission bound for engine-template, but the target "
                "checkout is this same repository (" + there + ") — point --cwd at the "
                "engine-template checkout and re-run")
    findings = []
    for rel in _changed_paths(base, head, cwd):
        findings.extend(_scan_path_string(rel, PATTERNS))

    # Added or renamed files: scan their FULL content. A pure rename lists only the destination
    # path and emits no content hunks, so a diff-line scan alone would miss a file of references
    # moved into the template wholesale.
    whole = set(_changed_paths(base, head, cwd, filt="AR"))
    for rel in sorted(whole):
        try:
            text = _git(["show", head + ":" + rel], cwd=cwd)
        except RuntimeError:
            continue
        findings.extend(_scan_text(text, PATTERNS, rel))

    # Added lines of everything else.
    diff = _git(["diff", "-U0", base + "..." + head], cwd=cwd)
    current = "?"
    prev_was_old_header = False
    for line in diff.splitlines():
        # A "+++ " line is a header ONLY right after its "--- " partner — an added content line
        # that itself begins with "++" also renders as "+++…" and must still be scanned.
        if prev_was_old_header and line.startswith("+++ "):
            if line.startswith(_DIFF_HEADERS[0]) or line.startswith(_DIFF_HEADERS[1]):
                current = line.split("b/", 1)[1].rstrip().rstrip('"').rstrip("\t")
            prev_was_old_header = False
            continue
        prev_was_old_header = line.startswith("--- ")
        if line.startswith("+") and current not in whole:
            for pat in PATTERNS:
                for m in pat.finditer(line[1:]):
                    findings.append(("added line in " + current, 0, m.group(0)))
    return findings


# --------------------------------------------------------------------------- outbound

def check_files(paths):
    """Returns (findings, errors, scanned). An unreadable path is an environment error
    (exit 2), never silently skipped, and never aborts the remaining scans."""
    findings, errors, scanned = [], [], 0
    for p in paths:
        try:
            text = sys.stdin.read() if p == "-" else Path(p).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            errors.append("could not read " + p + ": " + str(e))
            continue
        scanned += 1
        findings.extend(_scan_text(text, PATTERNS, p if p != "-" else "stdin"))
    return findings, errors, scanned


# --------------------------------------------------------------------------- reporting

_LEAD = "reference containment"


def _report(findings, label, scanned, unit="file"):
    """A clean warrant states the VOLUME actually examined. "I found nothing" and "I examined
    nothing" must never print the same word, so a scan that reached zero inputs is an
    environment error, not a clean pass."""
    if findings:
        print(_LEAD + ": " + str(len(findings)) + " finding(s) [" + label + "] — this "
              "repository's reference vocabulary must not reach a surface that travels to a "
              "repository deployed from engine-template, where it names something that does "
              "not exist there. Name the capability instead of the reference:")
        for f in findings:
            print("  - " + _fmt(f))
        return 1
    if scanned == 0:
        print(_LEAD + ": could not run — nothing was examined [" + label + "]. A clean "
              "result over zero " + unit + "s is not evidence; check the arguments.")
        return 2
    print(_LEAD + ": clean [" + label + "] — examined " + str(scanned) + " " + unit +
          ("" if scanned == 1 else "s") + ". Literal token match only; a clean result "
          "narrows the risk, it never proves absence.")
    return 0


# --------------------------------------------------------------------------- demo

def demo():
    """Falsification: every scanner must bite its seeded-bad input and pass its clean twin. A
    scanner that cannot fail is not evidence — any miss exits non-zero. Bad tokens are
    assembled at runtime so the demo's own seeds never sit in this file as matchable text."""
    d_short = "D-" + "24"
    d_long = "D-" + "309"
    d_padded = "D-" + "0042"
    adr_ref = "ADR-" + "0042"
    rec_path = "docs/" + "adr/" + "0042-a-slug.md"
    planning = "engine-" + "planning"
    failures = []

    def expect(name, got, want_bite):
        bit = bool(got)
        ok = bit == want_bite
        print(("PASS" if ok else "FAIL") + ": " + name + " — " +
              ("bit" if bit else "quiet") + " (wanted " +
              ("bite" if want_bite else "quiet") + ")")
        if not ok:
            failures.append(name)

    def scan(s, pats=PATTERNS):
        return _scan_text(s, pats, "demo")

    expect("bites the short decision form", scan("per " + d_short + " we do X"), True)
    expect("bites the three-digit decision form", scan("per " + d_long + " we do X"), True)
    expect("bites the zero-padded four-digit form", scan("per " + d_padded + " we do X"), True)
    expect("bites a record path", scan("see " + rec_path), True)
    expect("bites the retired workspace name", scan("the " + planning + " workspace"), True)
    expect("bites the alternate ADR spelling", scan("per " + adr_ref), True)
    expect("bites the alternate spelling lowercased", scan("per " + adr_ref.lower()), True)

    expect("quiet on the engine's own sanctioned records",
           scan("per eADR-0037 and acme-eADR-0007"), False)
    expect("quiet on a record path without the .md suffix",
           scan("an id like docs/" + "adr/0007-slug"), False)
    # Pins the case-sensitivity decision. An earlier draft pinned this with a string whose
    # lowercase token was followed by a hyphen — which the lookahead rejected regardless of
    # case, so the assertion passed under IGNORECASE and locked nothing.
    expect("quiet on a lowercase decision token (case-sensitivity is deliberate)",
           scan("per " + d_long.lower() + " we do X"), False)
    # Pins the rejected token classes, so a later broadening breaks a test rather than
    # silently landing. Each was rejected on a measured collision rate; see the record.
    expect("quiet on the rejected token classes",
           scan("see R6, Q4, principles " + chr(167) + "15, and #553"), False)
    expect("quiet on ordinary prose", scan("a plain change description"), False)

    # The report contract: a scan that examined nothing must not read as clean.
    code = _report([], "demo empty", 0)
    expect("an empty scan reports as could-not-run, not clean", [code == 2], True)

    # The baseline contract: a recorded finding does not alarm; an unrecorded one does.
    known = [("a/f.py", 3, d_long)]
    fresh = [("a/f.py", 3, d_long), ("b/g.py", 9, d_short)]
    base = set(_key(f) for f in known)
    new_only, _ = compare_to_baseline(fresh, base)
    expect("baseline suppresses recorded residue and surfaces a new leak",
           [len(new_only) == 1 and new_only[0][0] == "b/g.py"], True)

    print("DEMO " + ("FAILED" if failures else "PASSED"))
    return 1 if failures else 0


# --------------------------------------------------------------------------- cli

def _run_surfaces(baseline_path):
    root = _repo_root()
    findings, scanned = scan_surfaces(root)
    path = baseline_path or str(root / BASELINE_REL)
    baseline = read_baseline(path)
    if baseline is None:
        print(_LEAD + ": could not run — no baseline at " + path + ". The recorded residue "
              "is what makes a NEW leak visible; without it every known finding would alarm "
              "on every run, which trains people to ignore it.")
        return 2
    new, resolved = compare_to_baseline(findings, baseline)
    if resolved:
        print(_LEAD + ": " + str(len(resolved)) + " recorded reference(s) no longer present "
              "— upstream fixed them. Re-cut the baseline:")
        for k in resolved:
            f, _, t = k.partition("\t")
            print("  - " + f + ": '" + t + "' (resolved)")
    if new:
        print(_LEAD + ": " + str(len(new)) + " NEW finding(s) [traveling surfaces] — a "
              "reference reached a surface that ships to every repository deployed from "
              "engine-template, where it names something that does not exist there:")
        for f in new:
            print("  - " + _fmt(f))
        return 1
    if scanned == 0:
        print(_LEAD + ": could not run — nothing was examined [traveling surfaces].")
        return 2
    print(_LEAD + ": clean [traveling surfaces] — examined " + str(scanned) + " files; " +
          str(len(baseline)) + " known reference(s) recorded as upstream's to fix, none new. "
          "Literal token match only; a clean result narrows the risk, it never proves absence.")
    return 0


def main(argv):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("mode", nargs="?")
    ap.add_argument("refs", nargs="*")
    ap.add_argument("--baseline")
    ap.add_argument("--cwd")
    ap.add_argument("--allow-self", action="store_true")
    try:
        args = ap.parse_args(argv[1:])
    except SystemExit:
        return 2
    if not args.mode:
        print(__doc__)
        return 2
    try:
        if args.mode == "surfaces":
            return _run_surfaces(args.baseline)
        if args.mode == "diff":
            if not 1 <= len(args.refs) <= 2:
                print("usage: check.py diff <base-ref> [<head-ref>] [--cwd DIR]")
                return 2
            base = args.refs[0]
            head = args.refs[1] if len(args.refs) == 2 else "HEAD"
            findings = check_diff(base, head, cwd=args.cwd, allow_self=args.allow_self)
            changed = len(_changed_paths(base, head, args.cwd))
            return _report(findings, "outbound " + base + ".." + head, changed,
                           unit="changed file")
        if args.mode == "outbound":
            if not args.refs:
                print("usage: check.py outbound <path|-> [...]")
                return 2
            findings, errors, scanned = check_files(args.refs)
            code = _report(findings, "named inputs", scanned, unit="input")
            if errors:
                for e in errors:
                    print("  ! " + e)
                print(_LEAD + ": some inputs could not be scanned — fix the paths and re-run")
                return 2
            return code
        if args.mode == "demo":
            return demo()
        print("unknown mode '" + str(args.mode) + "'")
        print(__doc__)
        return 2
    except RuntimeError as e:
        print(_LEAD + ": could not run — " + str(e))
        return 2
    except Exception as e:  # an unexpected crash must never read as "findings"
        print(_LEAD + ": could not run — unexpected error: " + repr(e))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
