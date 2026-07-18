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
Recorded in .engine/contracts/instance/engine-mechanic-eADR-0001.

Modes:
  tree               scan git-tracked files (excluding docs/, .engine/, this directory) for
                     ADR-numbered tokens — the vocabulary must never enter content that could
                     ride an outbound channel
  outgoing BASE      run inside an engine-template checkout: scan added diff lines and commit
                     messages of BASE..HEAD for ADR-#### / D-### / engine-planning references
  scan-file PATH...  scan drafted issue or PR bodies ('-' reads stdin) with the outgoing patterns
  map                prove the disposition map in docs/adr/index.md covers D-001..D-319 exactly
                     once each with a recognized disposition
  demo               falsification: assert every scanner bites on seeded-bad input and stays
                     quiet on clean input; non-zero if any scanner fails to bite

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
    res = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {res.stderr.strip()}")
    return res.stdout


def _repo_root():
    return Path(_git(["rev-parse", "--show-toplevel"]).strip())


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
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        findings.extend(_scan_text(text, [ADR_TOKEN], rel))
    return findings


def check_outgoing(base, cwd=None):
    """Run inside the engine-template checkout before submitting: added lines and commit
    messages must carry no ADR-####, D-###, or engine-planning reference."""
    patterns = [ADR_TOKEN, D_TOKEN, PLANNING_TOKEN]
    findings = []
    diff = _git(["diff", "-U0", f"{base}...HEAD"], cwd=cwd)
    current = "?"
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current = line[6:]
            continue
        if line.startswith("+") and not line.startswith("+++"):
            for pat in patterns:
                for m in pat.finditer(line[1:]):
                    findings.append(f"added line in {current}: contains '{m.group(0)}'")
    messages = _git(["log", f"{base}..HEAD", "--format=%H %B"], cwd=cwd)
    findings.extend(_scan_text(messages, patterns, "commit message"))
    return findings


def check_files(paths):
    patterns = [ADR_TOKEN, D_TOKEN, PLANNING_TOKEN]
    findings = []
    for p in paths:
        text = sys.stdin.read() if p == "-" else Path(p).read_text(encoding="utf-8")
        findings.extend(_scan_text(text, patterns, p if p != "-" else "stdin"))
    return findings


def check_map(index_path=None):
    """docs/adr/index.md must disposition every retired decision exactly once."""
    path = Path(index_path) if index_path else _repo_root() / "docs" / "adr" / "index.md"
    if not path.exists():
        return [f"disposition index not found at {path}"]
    seen = {}
    findings = []
    row = re.compile(r"^\|\s*(D-\d{3})\s*\|.*\|\s*(.+?)\s*\|\s*$")
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
    for i in range(D_FIRST, D_LAST + 1):
        d = f"D-{i:03d}"
        if d not in seen:
            findings.append(f"{d}: missing from the disposition map")
    extra = [d for d in seen if not (D_FIRST <= int(d[2:]) <= D_LAST)]
    findings.extend(f"{d}: outside the retired D-001..D-319 range" for d in sorted(extra))
    return findings


def demo():
    """Falsification: every scanner must bite its seeded-bad input and pass its clean twin.
    A scanner that cannot fail is not evidence — any miss exits non-zero."""
    # Bad tokens are assembled at runtime so this file never carries a matchable literal.
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

    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write("| Decision | Title | Disposition |\n| --- | --- | --- |\n")
        for i in range(D_FIRST, D_LAST + 1):
            if i == 7:
                continue  # seeded gap: D-007 missing
            f.write(f"| D-{i:03d} | t | construction-era — not carried |\n")
        gap_map = f.name
    expect("map check bites a missing decision", check_map(gap_map), True)

    print("DEMO " + ("FAILED" if failures else "PASSED"))
    return 1 if failures else 0


def _report(findings, label):
    if findings:
        print(f"ADR containment: {len(findings)} finding(s) [{label}] — this repository's "
              "decision-record numbering must not appear here (see docs/adr/index.md and "
              ".engine/contracts/instance/engine-mechanic-eADR-0001):")
        for f in findings:
            print(f"  - {f}")
        return 1
    print(f"ADR containment: clean [{label}]")
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
            if len(argv) != 3:
                print("usage: check.py outgoing <base-ref>  (run inside the engine-template checkout)")
                return 2
            return _report(check_outgoing(argv[2]), f"outgoing vs {argv[2]}")
        if mode == "scan-file":
            if len(argv) < 3:
                print("usage: check.py scan-file <path|-> [...]")
                return 2
            return _report(check_files(argv[2:]), "drafted body")
        if mode == "map":
            return _report(check_map(), "disposition map")
        if mode == "demo":
            return demo()
    except RuntimeError as e:
        print(f"ADR containment: could not run — {e}")
        return 2
    print(f"unknown mode '{mode}'")
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
