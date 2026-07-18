#!/usr/bin/env python3
"""ADR containment — the wall around this repository's product decision-record numbering.

This repository (engine-mechanic) is the deployed Engine whose product is engine-template.
Its product decision records live in docs/adr/ under ADR-#### numbering, and its retired
design workspace used D-### numbering. Neither vocabulary may ever travel to engine-template
or any repository deployed from it: a deployed repo keeps its own product ADR system, and a
foreign decision number reaching it reads as one of its own and misleads. The engine's own
eADR-#### records are a separate, sanctioned system and are never flagged.

This is deliberately a PRODUCT-territory guardrail, not an engine check. An engine-side
module cannot host it: a module on disk but absent from the engine manifest's packages map
fails the release-integrity check, and one listed in packages makes every engine upgrade
refuse (the release never contains an instance-specific module). Product territory is walled
off from engine upgrades by contract (the engine/product wall), and the workflow that runs
this sits under the engine weakening-guard's watched prefix, so silent removal is alarmed.
One honest bound: a pull request that edits THIS directory is itself a guardrail change that
no alarm watches — review such diffs as guardrail-touching. Recorded in
.engine/contracts/instance/engine-mechanic-eADR-0001.

Modes:
  tree                    scan git-tracked files (excluding docs/, .engine/, this directory)
                          for ADR-numbered tokens — the vocabulary must never enter content
                          that could ride an outbound channel
  outgoing BASE [HEAD]    run inside an engine-template checkout: scan added diff lines,
                          changed file paths, and commit messages of BASE..HEAD (HEAD
                          defaults to the checked-out head) for ADR-#### / D-### /
                          engine-planning references
  scan-file PATH...       scan drafted issue or PR bodies ('-' reads stdin) with the
                          outgoing patterns
  map                     prove the disposition map in docs/adr/index.md covers every
                          retired decision exactly once, with a recognized disposition whose
                          record pointer resolves to a real file
  demo                    falsification: assert every scanner bites on seeded-bad input and
                          stays quiet on clean input; non-zero if any scanner fails to bite

A clean result is a literal token match only — it narrows the risk, it never proves absence
(split, encoded, or homoglyph tokens pass; the review gate stays the wall).

Exit status: 0 clean, 1 findings (or demo falsified), 2 usage/environment error.
"""

import re
import subprocess
import sys
from pathlib import Path

# (?<![A-Za-z]) keeps eADR-#### (any casing) out of scope by construction: the letter before
# "ADR" blocks the match. Case-insensitive so adr-0012 cannot slip the wall.
ADR_TOKEN = re.compile(r"(?<![A-Za-z])ADR-\d{3,4}", re.IGNORECASE)
D_TOKEN = re.compile(r"\bD-\d{3}\b")
PLANNING_TOKEN = re.compile(r"engine-planning", re.IGNORECASE)

TREE_EXCLUDES = ("docs/", ".engine/", "tools/adr-containment/")

D_FIRST, D_LAST = 1, 319
DISPOSITION_PREFIXES = (
    "carried → ADR-",
    "collapsed into ADR-",
    "engine-canon",
    "construction-era — not carried",
    "moot — build diverged",
)


def _git(args, cwd=None):
    res = subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                         encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {res.stderr.strip()}")
    return res.stdout


def _repo_root(cwd=None):
    return Path(_git(["rev-parse", "--show-toplevel"], cwd=cwd).strip())


def _scan_text(text, patterns, origin):
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for pat in patterns:
            for m in pat.finditer(line):
                findings.append(f"{origin}:{lineno}: contains '{m.group(0)}'")
    return findings


def check_tree(root=None):
    """The in-repo containment invariant: the ADR-numbered vocabulary stays inside docs/
    (its sanctioned home) and out of everything else that is tracked. .engine/ is excluded
    because its content arrives from engine releases (it is not an outbound channel from
    here, and upstream test fixtures legitimately carry decision-record examples)."""
    root = Path(root) if root else _repo_root()
    findings = []
    files = _git(["ls-files", "-z"], cwd=root).split("\0")
    for rel in files:
        if not rel or rel.startswith(TREE_EXCLUDES):
            continue
        path = root / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binary, gitlink, or unreadable — not scannable text
        findings.extend(_scan_text(text, [ADR_TOKEN], rel))
    return findings


_DIFF_HEADERS = ("+++ b/", '+++ "b/', "+++ /dev/null")


def check_outgoing(base, head="HEAD", cwd=None):
    """Run inside the engine-template checkout before anything leaves it: added lines,
    changed file paths, and commit messages must carry no ADR-####, D-###, or
    engine-planning reference."""
    # Refuse to run against engine-mechanic itself: a clean result here would be read as
    # "the template submission was scanned" when nothing relevant was.
    root = _repo_root(cwd=cwd)
    if (root / "tools" / "adr-containment" / "check.py").exists():
        raise RuntimeError("outgoing mode runs inside the engine-template checkout, but the "
                           "current directory is engine-mechanic itself — cd to the "
                           "engine-template checkout and re-run")
    patterns = [ADR_TOKEN, D_TOKEN, PLANNING_TOKEN]
    findings = []
    # Changed file paths travel too (a file named after a decision record carries the token
    # with no scannable content line, e.g. a pure rename).
    for rel in _git(["diff", "--name-only", "-z", f"{base}...{head}"], cwd=cwd).split("\0"):
        if not rel:
            continue
        for pat in patterns:
            for m in pat.finditer(rel):
                findings.append(f"changed path '{rel}': contains '{m.group(0)}'")
    diff = _git(["diff", "-U0", f"{base}...{head}"], cwd=cwd)
    current = "?"
    prev_was_old_header = False
    for line in diff.splitlines():
        # A "+++ " line is a header ONLY right after its "--- " partner — an added content
        # line that itself begins with "++" also renders as "+++…" and must still be scanned.
        if prev_was_old_header and line.startswith("+++ "):
            if line.startswith(_DIFF_HEADERS[0]) or line.startswith(_DIFF_HEADERS[1]):
                current = line.split("b/", 1)[1].rstrip().rstrip('"').rstrip("\t")
            prev_was_old_header = False
            continue
        prev_was_old_header = line.startswith("--- ")
        if line.startswith("+"):
            for pat in patterns:
                for m in pat.finditer(line[1:]):
                    findings.append(f"added line in {current}: contains '{m.group(0)}'")
    # Commit messages ride into the upstream history and PR UI; label findings per commit.
    log = _git(["log", f"{base}..{head}", "--format=%x00%H%n%B"], cwd=cwd)
    for block in log.split("\0"):
        if not block.strip():
            continue
        sha, _, body = block.partition("\n")
        findings.extend(_scan_text(body, patterns, f"message of commit {sha[:10]}"))
    return findings


def check_files(paths):
    """Scan drafted bodies. Returns (findings, errors) — an unreadable path is an
    environment error (exit 2), never silently skipped, and never aborts the other scans."""
    patterns = [ADR_TOKEN, D_TOKEN, PLANNING_TOKEN]
    findings, errors = [], []
    for p in paths:
        try:
            text = sys.stdin.read() if p == "-" else Path(p).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            errors.append(f"could not read {p}: {e}")
            continue
        findings.extend(_scan_text(text, patterns, p if p != "-" else "stdin"))
    return findings, errors


def check_map(index_path=None):
    """docs/adr/index.md must disposition every retired decision exactly once, and every
    disposition's pointer must resolve: a carried/collapsed row to a real record file
    beside the index, an engine-canon row to a real engine contract."""
    if index_path is None:
        root = _repo_root()
        path = root / "docs" / "adr" / "index.md"
        contracts_dir = root / ".engine" / "contracts"
    else:
        path = Path(index_path)
        contracts_dir = path.parent / ".engine-contracts"  # fixture-relative stand-in
    if not path.exists():
        return [f"disposition index not found at {path}"]
    adr_dir = path.parent
    seen = {}
    findings = []
    row = re.compile(r"^\|\s*(D-\d{3})\s*\|.*\|\s*(.+?)\s*\|\s*$")
    ptr = re.compile(r"ADR-\d{4}")
    eptr = re.compile(r"eADR-\d{4}")
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = row.match(line)
        if not m:
            continue
        d, disp = m.group(1), m.group(2)
        if d in seen:
            findings.append(f"{d}: dispositioned twice (lines {seen[d]} and {lineno})")
        seen[d] = lineno
        if not disp.startswith(DISPOSITION_PREFIXES):
            findings.append(f"{d}: unrecognized disposition '{disp}' (line {lineno})")
            continue
        if disp.startswith(("carried → ADR-", "collapsed into ADR-")):
            target = ptr.search(disp.replace("eADR-", ""))
            if not target or not list(adr_dir.glob(f"{target.group(0)}-*.md")):
                findings.append(f"{d}: disposition points at a record that does not exist "
                                f"('{disp}', line {lineno})")
        elif disp.startswith("engine-canon"):
            cited = eptr.findall(disp)
            if not cited:
                findings.append(f"{d}: engine-canon row cites no engine record (line {lineno})")
            else:
                for e in cited:
                    if not list(contracts_dir.glob(f"{e}-*.md")):
                        findings.append(f"{d}: cited engine record {e} not found (line {lineno})")
    for i in range(D_FIRST, D_LAST + 1):
        d = f"D-{i:03d}"
        if d not in seen:
            findings.append(f"{d}: missing from the disposition map")
    extra = [d for d in seen if not (D_FIRST <= int(d[2:]) <= D_LAST)]
    findings.extend(f"{d}: outside the retired decision range" for d in sorted(extra))
    return findings


def demo():
    """Falsification: every scanner must bite its seeded-bad input and pass its clean twin.
    A scanner that cannot fail is not evidence — any miss exits non-zero. The bad tokens are
    assembled at runtime so the demo's own seeds never sit in the file as matchable text."""
    import os
    import tempfile
    adr_ref = "ADR-" + "0042"
    d_ref = "D-" + "123"
    failures = []

    def expect(name, got_findings, want_bite):
        bit = bool(got_findings)
        ok = bit == want_bite
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {'bit' if bit else 'quiet'}"
              f" (wanted {'bite' if want_bite else 'quiet'})")
        if not ok:
            failures.append(name)

    expect("token scan bites a bare ADR reference",
           _scan_text(f"per {adr_ref} we do X", [ADR_TOKEN], "demo"), True)
    expect("token scan stays quiet on eADR references",
           _scan_text("per eADR-0042 and acme-eADR-0007", [ADR_TOKEN], "demo"), False)
    expect("token scan bites case variants",
           _scan_text(f"see {adr_ref.lower()}", [ADR_TOKEN], "demo"), True)
    expect("outgoing patterns bite a legacy D reference",
           _scan_text(f"restores {d_ref} behavior", [D_TOKEN], "demo"), True)
    expect("outgoing patterns bite an engine-planning reference",
           _scan_text("see the engine-planning workspace", [PLANNING_TOKEN], "demo"), True)
    expect("outgoing patterns stay quiet on clean prose",
           _scan_text("a plain change description", [ADR_TOKEN, D_TOKEN, PLANNING_TOKEN],
                      "demo"), False)

    def tmp_map(rows_disposition, skip=None):
        f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        f.write("| Decision | Title | Disposition |\n| --- | --- | --- |\n")
        for i in range(D_FIRST, D_LAST + 1):
            if i == skip:
                continue
            f.write(f"| D-{i:03d} | t | {rows_disposition} |\n")
        f.close()
        return f.name

    gap = tmp_map("construction-era — not carried", skip=7)
    dangling = tmp_map("carried → " + "ADR-9999")
    try:
        expect("map check bites a missing decision", check_map(gap), True)
        expect("map check bites a dangling record pointer", check_map(dangling), True)
    finally:
        os.unlink(gap)
        os.unlink(dangling)

    print("DEMO " + ("FAILED" if failures else "PASSED"))
    return 1 if failures else 0


def _report(findings, label, token_scan=True):
    if findings:
        print(f"ADR containment: {len(findings)} finding(s) [{label}] — this repository's "
              "decision-record numbering must not appear here (in the engine-mechanic "
              "repository, see docs/adr/index.md and .engine/contracts/instance/"
              "engine-mechanic-eADR-0001-adr-containment-guardrail.md):")
        for f in findings:
            print(f"  - {f}")
        return 1
    warrant = (" — literal token match only; a clean result narrows the risk, it never "
               "proves absence") if token_scan else ""
    print(f"ADR containment: clean [{label}]{warrant}")
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    mode = argv[1]
    try:
        if mode == "tree":
            return _report(check_tree(), "tracked tree")
        if mode == "outgoing":
            if len(argv) not in (3, 4):
                print("usage: check.py outgoing <base-ref> [<head-ref>]  "
                      "(run inside the engine-template checkout)")
                return 2
            head = argv[3] if len(argv) == 4 else "HEAD"
            return _report(check_outgoing(argv[2], head), f"outgoing {argv[2]}..{head}")
        if mode == "scan-file":
            if len(argv) < 3:
                print("usage: check.py scan-file <path|-> [...]")
                return 2
            findings, errors = check_files(argv[2:])
            code = _report(findings, "drafted body")
            if errors:
                for e in errors:
                    print(f"  ! {e}")
                print("ADR containment: some inputs could not be scanned — fix the paths "
                      "and re-run")
                return 2
            return code
        if mode == "map":
            return _report(check_map(), "disposition map", token_scan=False)
        if mode == "demo":
            return demo()
        print(f"unknown mode '{mode}'")
        print(__doc__)
        return 2
    except RuntimeError as e:
        print(f"ADR containment: could not run — {e}")
        return 2
    except Exception as e:  # an unexpected crash must never read as "findings"
        print(f"ADR containment: could not run — unexpected error: {e!r}")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
