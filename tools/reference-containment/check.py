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
capabilities rather than its references — no scanner can check that. A file that cannot be read
as text is named and left out of the clean count, never folded into it. The review gate stays
the real wall.

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
# that cannot exist in a 1..319 range.
#
# CASE-INSENSITIVE, on measurement. An earlier draft was case-sensitive, justified by the
# lowercase form appearing inside slugified record filenames (0315-amend-d-314-...md). That
# reasoning does not survive: those filenames live under docs/, which never travels and is out of
# every scope here, and where a record PATH is scanned as a string ADR_PATH already matches it
# whatever its case. Across the scanned surfaces the whole cost of matching case-insensitively is
# ONE additional hit, of the same benign kind as the recorded ADR-0001 fixture — against a real
# blind spot in which a lowercase reference walked straight through.
D_TOKEN = re.compile(r"(?<![A-Za-z0-9])D-\d{1,4}(?!\d)", re.IGNORECASE)

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
    """Returns (findings, files_scanned, unreadable). The traveling corners as received here."""
    root = Path(root) if root else _repo_root()
    findings = []
    scanned = 0
    unreadable = []
    for rel in _git(["ls-files", "-z"], cwd=root).split("\0"):
        if not rel or rel.startswith(SELF_PREFIX) or rel.startswith(LOCAL_SCOPES):
            continue
        if not rel.startswith(TRAVELING_SCOPES):
            continue
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Not UTF-8. Almost always a genuine binary (an image, a compiled asset), which
            # carries no scannable prose — but it could be UTF-16 text holding a real reference,
            # so it is COUNTED and named rather than silently dropped into the clean tally.
            unreadable.append(rel)
            continue
        except OSError:
            unreadable.append(rel)
            continue
        scanned += 1
        findings.extend(_scan_text(text, PATTERNS, rel))
    return findings, scanned, unreadable


def read_baseline(path):
    """The recorded, upstream-owned residue as {key: count}. Absent file -> None, which the caller
    treats as an environment error: an absent baseline read as "suppress nothing" would alarm on
    every known finding, and read as "suppress everything" would be worse."""
    try:
        text = Path(path).read_text(encoding="utf-8-sig")  # -sig: a BOM must not corrupt entry 1
    except OSError:
        return None
    counts = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        key = parts[0] + "\t" + parts[1] if len(parts) >= 2 else line
        try:
            n = int(parts[2]) if len(parts) >= 3 else 1
        except ValueError:
            n = 1
        counts[key] = counts.get(key, 0) + n
    return counts


def compare_to_baseline(findings, baseline):
    """Returns (new, resolved). `new` is what must alarm: a reference that reached a traveling
    surface after the residue was recorded.

    COUNTS MATTER, not just presence. Keying on file+token alone would make a SECOND citation of
    an already-recorded token in an already-recorded file invisible forever — and `boot.py` today
    holds three separate citations of one token, so a fourth landing in a future release is
    exactly the event this guard exists to catch. `resolved` is good news, reported not alarmed."""
    seen = {}
    for f in findings:
        seen.setdefault(_key(f), []).append(f)
    new = []
    for k in sorted(seen):
        allowed = max(0, baseline.get(k, 0))
        if len(seen[k]) > allowed:
            new.extend(seen[k][allowed:])
    # `resolved` must catch a count that merely DROPPED, not only one that vanished. An allowance
    # left higher than reality is a silent hole: upstream fixes two of three citations, nothing
    # says so, and two brand-new ones later land back inside the stale allowance and never alarm.
    resolved = sorted(k for k in baseline if len(seen.get(k, [])) < baseline[k])
    return new, resolved


# --------------------------------------------------------------------------- diff

_DIFF_HEADERS = ("+++ b/", '+++ "b/')


def _unquote_path(raw):
    """Undo git's C-quoting of a path in a diff header. A path with a non-ASCII, tab, quote or
    backslash character arrives as "b/caf\\303\\251.md"; leaving it encoded means it never matches
    the raw path list from `-z` output, so the file gets scanned twice and the second finding names
    a path that does not exist."""
    s = raw.rstrip("\t")
    if not s.endswith('"'):
        return s
    s = s[:-1]
    out = bytearray()
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt in "01234567" and i + 3 < len(s):
                try:
                    out.append(int(s[i + 1:i + 4], 8))
                    i += 4
                    continue
                except ValueError:
                    pass
            out.extend({"n": b"\n", "t": b"\t", "r": b"\r",
                        '"': b'"', "\\": b"\\"}.get(nxt, nxt.encode()))
            i += 2
            continue
        out.extend(s[i].encode())
        i += 1
    return out.decode("utf-8", "replace")


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
        # "This repository" must come from where THIS FILE lives, never from the process working
        # directory. A git pre-push hook runs with its cwd at the top of the repository being
        # pushed, so a cwd-based read returns the TARGET on both sides, compares equal, and
        # refuses every push — telling the operator to do the thing they already did, whose only
        # documented escape is to turn scanning off. Compare by remote rather than resolved path,
        # because this repository is normally worked in a git worktree and two paths of the same
        # repository would otherwise read as different ones.
        here = _repo_slug(_origin(cwd=str(Path(__file__).resolve().parent)))
        there = _repo_slug(_origin(cwd=cwd))
        # Fail closed on BOTH sides. Only checking the target leaves the mirror case open: a copy
        # of this file placed outside any checkout makes `here` empty, the equality guard is
        # skipped, and a scan of this repository against itself reports as an outbound submission.
        if not here:
            raise RuntimeError(
                "could not determine which repository this scanner belongs to — run it from "
                "inside its own checkout rather than a copy, or pass --confirmed-target if you "
                "have verified the target yourself")
        if not there:
            raise RuntimeError(
                "could not determine which repository the target checkout belongs to (no origin "
                "remote) — refusing rather than reporting a scan of an unknown target as clean; "
                "pass --confirmed-target if you have verified the target yourself")
        if here == there:
            raise RuntimeError(
                "diff mode scans a submission bound for engine-template, but the target "
                "checkout is this same repository (" + there + ") — point --cwd at the "
                "engine-template checkout and re-run")
    findings = []
    # Deletions are excluded: removing a file whose NAME carries a reference is the fix, not the
    # leak, and flagging it would make the upstream cleanup submission fail its own guard.
    for rel in _changed_paths(base, head, cwd, filt="ACMRT"):
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
    #
    # Distinguishing a file header from content is the subtle part. A "+++ " line is a header only
    # inside the per-file preamble; an ADDED content line beginning "++" also renders as "+++…",
    # and a REMOVED content line beginning "-- " renders as "--- ". Keying off "the previous line
    # started with '--- '" therefore mis-fires on the second case: a removed "-- " line makes the
    # scanner swallow the next added line as a header and never scan it. `-- ` opens a comment in
    # SQL and Lua, so that is a live miss, and under -U0 a replaced line puts the two adjacent.
    # Anchor on "diff --git" instead — the preamble always starts there and always ends at the
    # first hunk header — so content can never be mistaken for a header.
    diff = _git(["diff", "-U0", base + "..." + head], cwd=cwd)
    current = "?"
    in_preamble = False
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            in_preamble = True
            current = "?"
            continue
        if in_preamble:
            if line.startswith("@@"):
                in_preamble = False
            elif line.startswith(_DIFF_HEADERS):
                current = _unquote_path(line.split("b/", 1)[1].rstrip())
            continue
        if line.startswith("@@"):
            continue
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


def _report(findings, label, scanned, unit="file", zero_is_clean=False):
    """A clean warrant states the VOLUME actually examined. "I found nothing" and "I examined
    nothing" must never print the same word, so a scan that reached zero inputs is normally an
    environment error rather than a clean pass.

    `zero_is_clean` is for the one case where zero is a real answer instead of a broken one: a
    submission whose net diff changes nothing genuinely carries nothing, and refusing it would
    block a legitimate push with a message telling the operator to fix arguments that are fine.
    The count is still printed, so nobody has to take "clean" on trust."""
    if findings:
        print(_LEAD + ": " + str(len(findings)) + " finding(s) [" + label + "] — this "
              "repository's reference vocabulary must not reach a surface that travels to a "
              "repository deployed from engine-template, where it names something that does "
              "not exist there. Name the capability instead of the reference:")
        for f in findings:
            print("  - " + _fmt(f))
        return 1
    if scanned == 0 and not zero_is_clean:
        print(_LEAD + ": could not run — nothing was examined [" + label + "]. A clean "
              "result over zero " + unit + "s is not evidence; check the arguments.")
        return 2
    if scanned == 0:
        print(_LEAD + ": clean [" + label + "] — this submission changes no files, so it "
              "carries nothing that could travel.")
        return 0
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
        # `got` is normally a findings list. A bool is accepted explicitly, because wrapping a
        # comparison in a list — `[code == 2]` — makes it truthy either way, so the assertion can
        # never fail. Two assertions here were written that way and were permanently green.
        bit = got if isinstance(got, bool) else bool(got)
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
    # Pins case-INsensitivity, which was a measured decision: matching only uppercase let a
    # lowercase reference through, and closing that costs one benign fixture hit across the
    # scanned surfaces. An earlier pin used a string whose lowercase token was followed by a
    # hyphen — rejected by the lookahead regardless of case, so it locked nothing either way.
    expect("bites a lowercase decision token", scan("per " + d_long.lower() + " we do X"), True)
    # Pins the rejected token classes, so a later broadening breaks a test rather than
    # silently landing. Each was rejected on a measured collision rate; see the record.
    expect("quiet on the rejected token classes",
           scan("see R6, Q4, principles " + chr(167) + "15, and #553"), False)
    expect("quiet on ordinary prose", scan("a plain change description"), False)

    # The report contract: a scan that examined nothing must not read as clean.
    code = _report([], "demo empty", 0)
    expect("an empty scan reports as could-not-run, not clean", code == 2, True)

    # The baseline contract: a recorded finding does not alarm; an unrecorded one does.
    known = [("a/f.py", 3, d_long)]
    base = {_key(f): 1 for f in known}
    new_only, _ = compare_to_baseline(known + [("b/g.py", 9, d_short)], base)
    expect("baseline suppresses recorded residue and surfaces a new leak",
           len(new_only) == 1 and new_only[0][0] == "b/g.py", True)
    # A SECOND occurrence of an already-recorded token in an already-recorded file must alarm —
    # the count, not just the file-and-token pair, is what the baseline records.
    repeat, _ = compare_to_baseline(known + [("a/f.py", 99, d_long)], base)
    expect("baseline surfaces a repeat of a recorded token in a recorded file",
           len(repeat) == 1, True)
    # Path unquoting: a C-quoted header path must resolve to the real name, or the file is scanned
    # twice and the duplicate names a path that does not exist.
    # The header's leading `"b/` is already consumed by the split, so the input is the tail only.
    expect("a C-quoted diff path is decoded to its real name",
           _unquote_path('caf\\303\\251.md"') == "café.md", True)

    print("DEMO " + ("FAILED" if failures else "PASSED"))
    return 1 if failures else 0


# --------------------------------------------------------------------------- cli

def _run_surfaces(baseline_path):
    root = _repo_root()
    findings, scanned, unreadable = scan_surfaces(root)
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
    if unreadable:
        # Named, never folded into the clean tally: one of these could be UTF-16 text carrying a
        # real reference, and a file the scanner could not read must not be counted as one it
        # read and found clean.
        print(_LEAD + ": " + str(len(unreadable)) + " file(s) could not be read as text and "
              "were NOT scanned:")
        for rel in unreadable:
            print("  ? " + rel)
    if new:
        print(_LEAD + ": " + str(len(new)) + " NEW finding(s) [traveling surfaces] — a "
              "reference reached a surface that ships to every repository deployed from "
              "engine-template, where it names something that does not exist there:")
        for f in new:
            print("  - " + _fmt(f))
        # The remediation differs from the outbound one and must be said here: almost every
        # finding on THIS surface arrives from upstream in a file the engine overwrites, so
        # "name the capability instead" is the wrong advice — the action is to work out who owns
        # the file, then either fix it (if it is yours) or record and report it (if it is not).
        print("")
        print("What to do. This check is advisory: it cannot block your merge. If the file is")
        print("one this project owns, reword it to name the capability rather than the record —")
        print("a reader in a deployed repository cannot follow the reference. If it arrived from")
        print("an engine release (anything under .engine/ usually did), the fix belongs upstream:")
        print("report it there, then add a line to " + BASELINE_REL + " so")
        print("this stays quiet until the fix comes back down. " + SELF_PREFIX + "README.md")
        print("explains both paths.")
        return 1
    if scanned == 0:
        print(_LEAD + ": could not run — nothing was examined [traveling surfaces].")
        return 2
    # When something could not be read, the summary must not be the bare word "clean" — an
    # unreadable file could be UTF-16 text carrying a real reference, and a non-UTF-8 encoding is
    # the cheapest way to walk one past this scan.
    verdict = ("clean apart from what could not be read" if unreadable else "clean")
    print(_LEAD + ": " + verdict + " [traveling surfaces] — examined " + str(scanned) +
          " files" + (", " + str(len(unreadable)) + " unread" if unreadable else "") + "; " +
          str(sum(baseline.values())) + " known reference(s) recorded as upstream's to fix, none "
          "new. Literal token match only; a clean result narrows the risk, it never proves "
          "absence.")
    return 0


def main(argv):
    if any(a in ("-h", "--help") for a in argv[1:]):
        print(__doc__)
        return 0
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("mode", nargs="?")
    ap.add_argument("refs", nargs="*")
    ap.add_argument("--baseline")
    ap.add_argument("--cwd")
    ap.add_argument("--confirmed-target", action="store_true")
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
            findings = check_diff(base, head, cwd=args.cwd, allow_self=args.confirmed_target)
            # Count what was SCANNED, not what changed: deletions are excluded from the scan,
            # so an unfiltered count would warrant "examined 5 changed files" having read none.
            changed = len(_changed_paths(base, head, args.cwd, filt="ACMRT"))
            return _report(findings, "outbound " + base + ".." + head, changed,
                           unit="changed file", zero_is_clean=True)
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
