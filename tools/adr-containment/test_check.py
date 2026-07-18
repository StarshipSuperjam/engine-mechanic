"""Self-tests for the ADR-containment guardrail.

Every scanner is exercised on both sides: input it must flag and input it must leave alone.
Token literals that the scanners hunt are assembled at runtime so this file never carries a
matchable string of its own (the guardrail's own directory is excluded from the tree scan,
but the tests should not depend on that exclusion to stay green).
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check  # noqa: E402

ADR_REF = "ADR-" + "0042"
D_REF = "D-" + "123"
PLANNING_REF = "engine-" + "planning"


def _git(cwd, *args):
    subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )


class TokenScanTest(unittest.TestCase):
    def test_bites_bare_adr_token(self):
        self.assertTrue(check._scan_text(f"per {ADR_REF}", [check.ADR_TOKEN], "x"))

    def test_bites_lowercase_variant(self):
        self.assertTrue(check._scan_text(f"per {ADR_REF.lower()}", [check.ADR_TOKEN], "x"))

    def test_quiet_on_eadr_any_casing(self):
        for text in ("per eADR-0042", "per EADR-0042", "per acme-eADR-0042", "per eadr-0042"):
            self.assertFalse(check._scan_text(text, [check.ADR_TOKEN], "x"), text)

    def test_quiet_on_unnumbered_mentions(self):
        self.assertFalse(check._scan_text("the product's own ADR system", [check.ADR_TOKEN], "x"))

    def test_outgoing_patterns_bite_d_and_planning(self):
        pats = [check.ADR_TOKEN, check.D_TOKEN, check.PLANNING_TOKEN]
        self.assertTrue(check._scan_text(f"restores {D_REF}", pats, "x"))
        self.assertTrue(check._scan_text(f"see the {PLANNING_REF} repo", pats, "x"))
        self.assertFalse(check._scan_text("a plain description", pats, "x"))


class TreeScanTest(unittest.TestCase):
    def _repo_with(self, rel, content):
        d = tempfile.mkdtemp()
        _git(d, "init", "-q")
        p = Path(d) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        _git(d, "add", "-A")
        _git(d, "commit", "-qm", "seed")
        return d

    def test_bites_token_in_tracked_file(self):
        d = self._repo_with("src/example.py", f"# per {ADR_REF} the widget frobs\n")
        self.assertTrue(check.check_tree(d))

    def test_quiet_inside_sanctioned_homes(self):
        for home in ("docs/adr/x.md", ".engine/tools/t.py", "tools/adr-containment/n.py"):
            d = self._repo_with(home, f"per {ADR_REF}\n")
            self.assertFalse(check.check_tree(d), home)

    def test_quiet_on_clean_tree(self):
        d = self._repo_with("README.md", "a plain readme\n")
        self.assertFalse(check.check_tree(d))


class OutgoingScanTest(unittest.TestCase):
    def _repo_with_branch(self, added_line, message):
        d = tempfile.mkdtemp()
        _git(d, "init", "-q", "-b", "main")
        Path(d, "f.txt").write_text("base\n", encoding="utf-8")
        _git(d, "add", "-A")
        _git(d, "commit", "-qm", "base")
        _git(d, "checkout", "-qb", "work")
        Path(d, "f.txt").write_text(f"base\n{added_line}\n", encoding="utf-8")
        _git(d, "add", "-A")
        _git(d, "commit", "-qm", message)
        return d

    def test_bites_added_line(self):
        d = self._repo_with_branch(f"per {ADR_REF} we frob", "clean message")
        self.assertTrue(check.check_outgoing("main", cwd=d))

    def test_bites_commit_message(self):
        d = self._repo_with_branch("clean line", f"restores {D_REF} behavior")
        self.assertTrue(check.check_outgoing("main", cwd=d))

    def test_quiet_on_clean_branch(self):
        d = self._repo_with_branch("a plain line", "a plain message")
        self.assertFalse(check.check_outgoing("main", cwd=d))

    def test_preexisting_lines_not_flagged(self):
        d = tempfile.mkdtemp()
        _git(d, "init", "-q", "-b", "main")
        Path(d, "f.txt").write_text(f"per {ADR_REF}\n", encoding="utf-8")
        _git(d, "add", "-A")
        _git(d, "commit", "-qm", "base carries the token already")
        _git(d, "checkout", "-qb", "work")
        Path(d, "g.txt").write_text("clean addition\n", encoding="utf-8")
        _git(d, "add", "-A")
        _git(d, "commit", "-qm", "clean")
        self.assertFalse(check.check_outgoing("main", cwd=d))


class MapCheckTest(unittest.TestCase):
    def _map_file(self, skip=None, duplicate=None, disposition="construction-era — not carried"):
        f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        f.write("| Decision | Title | Disposition |\n| --- | --- | --- |\n")
        for i in range(check.D_FIRST, check.D_LAST + 1):
            if i == skip:
                continue
            f.write(f"| D-{i:03d} | t | {disposition} |\n")
            if i == duplicate:
                f.write(f"| D-{i:03d} | t | {disposition} |\n")
        f.close()
        return f.name

    def test_complete_map_passes(self):
        self.assertFalse(check.check_map(self._map_file()))

    def test_missing_decision_bites(self):
        self.assertTrue(check.check_map(self._map_file(skip=7)))

    def test_duplicate_decision_bites(self):
        self.assertTrue(check.check_map(self._map_file(duplicate=7)))

    def test_unrecognized_disposition_bites(self):
        self.assertTrue(check.check_map(self._map_file(disposition="left as an exercise")))


class DemoTest(unittest.TestCase):
    def test_demo_passes_on_healthy_scanners(self):
        self.assertEqual(check.demo(), 0)


if __name__ == "__main__":
    unittest.main()
