#!/usr/bin/env python3
"""Self-tests for the reference-containment scanner.

Two disciplines this file keeps deliberately:

1. Every token literal is ASSEMBLED AT RUNTIME ("D-" + "309"). The scanner excludes its own
   directory, but these tests must not RELY on that exclusion — if the exclusion were ever
   dropped, a test file full of matchable tokens would light up the guard it is testing.

2. Every scanner is tested on BOTH sides — it must bite its bad input AND stay quiet on the
   clean twin. A test that only proves a scanner fires cannot tell a working pattern from one
   that matches everything.

Run:  python3 -m unittest discover -s tools/reference-containment -p 'test_*.py' -b
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check  # noqa: E402

D_SHORT = "D-" + "24"
D_MID = "D-" + "309"
D_PADDED = "D-" + "0042"
ADR_REF = "ADR-" + "0042"
REC_PATH = "docs/" + "adr/" + "0042-a-slug.md"
PLANNING = "engine-" + "planning"


def _scan(text):
    return check._scan_text(text, check.PATTERNS, "t")


class TokenTest(unittest.TestCase):
    def test_bites_every_decision_spelling(self):
        for tok in (D_SHORT, D_MID, D_PADDED, "D-" + "1"):
            self.assertTrue(_scan("per " + tok + " we do X"), tok)

    def test_bites_record_path_absolute_and_relative(self):
        self.assertTrue(_scan("see " + REC_PATH))
        self.assertTrue(_scan("see ../../" + "adr/" + "0042-a-slug.md"))

    def test_bites_planning_and_adr_spellings(self):
        self.assertTrue(_scan("the " + PLANNING + " workspace"))
        self.assertTrue(_scan("per " + ADR_REF))
        self.assertTrue(_scan("per " + ADR_REF.lower()))

    def test_quiet_on_engine_sanctioned_records_any_casing(self):
        for s in ("eADR-0042", "EADR-0042", "eadr-0042", "acme-eADR-0007",
                  "engine-mechanic-eADR-0001-x.md"):
            self.assertFalse(_scan("per " + s), s)

    def test_quiet_on_lowercase_decision_token(self):
        """Case-sensitivity is deliberate: the lowercase form appears inside slugified record
        filenames, which are not references. Its cost is stated in the module docstring."""
        self.assertFalse(_scan("per " + D_MID.lower() + " we do X"))

    def test_quiet_on_record_id_without_md_suffix(self):
        """The .md requirement is load-bearing — the engine's own tools use the bare form as a
        generic illustration of what an ADR id looks like."""
        self.assertFalse(_scan("an id like docs/" + "adr/0007-slug"))

    def test_quiet_on_rejected_token_classes(self):
        """Pins the deliberate exclusions so a later broadening breaks a test rather than
        silently landing. Each was rejected on a measured collision rate; see the record."""
        self.assertFalse(_scan("see R6, Q4, principles " + chr(167) + "15, and #553"))

    def test_quiet_on_embedded_digit_runs(self):
        for s in ("LED-1234", "3D-12", "AD-309"):
            self.assertFalse(_scan(s), s)

    def test_quiet_on_ordinary_prose(self):
        self.assertFalse(_scan("a plain change description with no references"))


class _TempRepoTest(unittest.TestCase):
    def _mkrepo(self):
        d = tempfile.mkdtemp()
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", d]))
        env = dict(os.environ)
        # Isolate from the developer's global config: a gpg-signing or hooksPath setting would
        # otherwise make these tests fail for reasons unrelated to the scanner.
        env.update({"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
                    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e",
                    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e"})
        self._env = env
        self._git(d, "init", "-q", "-b", "main")
        return d

    def _git(self, d, *args):
        r = subprocess.run(["git"] + list(args), cwd=d, env=self._env,
                           capture_output=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            raise AssertionError("git " + " ".join(args) + ": " + r.stderr)
        return r.stdout

    def _write(self, d, rel, text):
        p = Path(d) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def _commit(self, d, msg="c"):
        self._git(d, "add", "-A")
        self._git(d, "commit", "-q", "-m", msg)


class SurfacesScopeTest(_TempRepoTest):
    def test_scans_traveling_corners_and_skips_local_ones(self):
        d = self._mkrepo()
        self._write(d, ".engine/tools/x.py", "# per " + D_MID + "\n")   # travels
        self._write(d, "CLAUDE.md", "per " + D_SHORT + "\n")            # travels
        self._write(d, "docs/adr/0001-x.md", "per " + D_MID + "\n")     # does NOT travel
        self._write(d, "README.md", "per " + D_MID + "\n")              # does NOT travel
        self._commit(d)
        findings, scanned = check.scan_surfaces(d)
        origins = sorted(set(f[0] for f in findings))
        self.assertEqual(origins, [".engine/tools/x.py", "CLAUDE.md"])
        self.assertEqual(scanned, 2)

    def test_skips_this_deployments_own_records_but_not_the_engine_canon(self):
        """`.engine/contracts/instance/` is this deployment's own decision stream — preserved
        across upgrades because it is the operator's, and never shipped. A record explaining a
        containment rule must be able to name the vocabulary it contains. The engine's own
        canon one directory up DOES travel, so it stays in scope."""
        d = self._mkrepo()
        self._write(d, ".engine/contracts/instance/x-eADR-0001-y.md", "per " + D_MID + "\n")
        self._write(d, ".engine/contracts/eADR-0037-z.md", "per " + D_MID + "\n")
        self._commit(d)
        findings, _ = check.scan_surfaces(d)
        self.assertEqual(sorted(set(f[0] for f in findings)),
                         [".engine/contracts/eADR-0037-z.md"])

    def test_skips_operator_owned_config_under_the_engine_directory(self):
        d = self._mkrepo()
        self._write(d, ".engine/conduct/operator.md", "per " + D_MID + "\n")
        self._write(d, ".engine/conduct/defaults.md", "per " + D_MID + "\n")
        self._commit(d)
        findings, _ = check.scan_surfaces(d)
        self.assertEqual(sorted(set(f[0] for f in findings)), [".engine/conduct/defaults.md"])

    def test_skips_the_scanner_directory(self):
        d = self._mkrepo()
        self._write(d, ".engine/x.md", "clean\n")
        self._write(d, check.SELF_PREFIX + "notes.md", "per " + D_MID + "\n")
        self._commit(d)
        findings, _ = check.scan_surfaces(d)
        self.assertEqual(findings, [])

    def test_binary_file_skipped_not_fatal(self):
        d = self._mkrepo()
        (Path(d) / ".engine").mkdir()
        (Path(d) / ".engine" / "blob.bin").write_bytes(b"\xff\xfe\x00\x01")
        self._write(d, ".engine/ok.md", "clean\n")
        self._commit(d)
        findings, scanned = check.scan_surfaces(d)
        self.assertEqual(findings, [])
        self.assertEqual(scanned, 1)


class BaselineTest(unittest.TestCase):
    def test_recorded_residue_does_not_alarm_but_a_new_one_does(self):
        recorded = ("a/f.py", 3, D_MID)
        fresh = ("b/g.py", 9, D_SHORT)
        base = set([check._key(recorded)])
        new, resolved = check.compare_to_baseline([recorded, fresh], base)
        self.assertEqual([f[0] for f in new], ["b/g.py"])
        self.assertEqual(resolved, [])

    def test_line_movement_does_not_create_a_false_new_finding(self):
        """Engine releases move these lines wholesale. A baseline keyed to line numbers would
        alarm on every upgrade — the churn that trains people to ignore the check."""
        base = set([check._key(("a/f.py", 3, D_MID))])
        new, _ = check.compare_to_baseline([("a/f.py", 871, D_MID)], base)
        self.assertEqual(new, [])

    def test_reports_a_reference_upstream_has_fixed(self):
        base = set([check._key(("a/f.py", 3, D_MID))])
        new, resolved = check.compare_to_baseline([], base)
        self.assertEqual(new, [])
        self.assertEqual(len(resolved), 1)

    def test_absent_baseline_is_an_error_not_an_empty_set(self):
        """Treating an absent baseline as empty would make every known finding alarm; treating
        it as 'suppress everything' would be worse. It is an environment error."""
        self.assertIsNone(check.read_baseline("/nonexistent/baseline.txt"))

    def test_committed_baseline_matches_the_live_surface(self):
        """The shipped baseline must describe reality, or the guard is measuring a fiction."""
        root = check._repo_root()
        findings, _ = check.scan_surfaces(root)
        base = check.read_baseline(str(root / check.BASELINE_REL))
        self.assertIsNotNone(base)
        new, resolved = check.compare_to_baseline(findings, base)
        self.assertEqual(new, [], "baseline is stale — a new reference reached a traveling surface")
        self.assertEqual(resolved, [], "baseline is stale — re-cut it, these are fixed")


class DiffTest(_TempRepoTest):
    def _branch_with(self, mutate, msg="c"):
        d = self._mkrepo()
        self._write(d, "seed.md", "base\n")
        self._commit(d)
        base = self._git(d, "rev-parse", "HEAD").strip()
        mutate(d)
        self._commit(d, msg)
        return d, base

    def test_bites_an_added_line(self):
        d, base = self._branch_with(
            lambda d: self._write(d, "f.md", "per " + D_MID + "\n"))
        self.assertTrue(check.check_diff(base, "HEAD", cwd=d, allow_self=True))

    def test_bites_an_added_line_that_itself_starts_with_plus_plus(self):
        """A content line beginning '++' renders as '+++…' in the diff and would be mistaken
        for a file header by a naive parser, silently skipping it."""
        d, base = self._branch_with(
            lambda d: self._write(d, "f.md", "++ per " + D_MID + "\n"))
        self.assertTrue(check.check_diff(base, "HEAD", cwd=d, allow_self=True))

    def test_bites_a_pure_rename_into_a_referencing_filename(self):
        """A rename lists only the destination path and emits no content hunks."""
        def mutate(d):
            self._git(d, "mv", "seed.md", "notes-" + D_MID + ".md")
        d, base = self._branch_with(mutate)
        self.assertTrue(check.check_diff(base, "HEAD", cwd=d, allow_self=True))

    def test_bites_content_moved_in_by_rename_with_no_hunks(self):
        """The hole a diff-line scan alone leaves: a file full of references moved wholesale
        produces a rename entry and zero '+' lines."""
        d = self._mkrepo()
        self._write(d, "local/notes.md", "per " + D_MID + " and " + D_SHORT + "\n")
        self._commit(d)
        base = self._git(d, "rev-parse", "HEAD").strip()
        self._git(d, "mv", "local/notes.md", "shipped.md")
        self._commit(d)
        findings = check.check_diff(base, "HEAD", cwd=d, allow_self=True)
        self.assertTrue(any(f[0] == "shipped.md" for f in findings))

    def test_does_not_scan_commit_messages(self):
        """History does not travel: 'Use this template' copies the file tree as one commit, so
        a commit message can never reach a deployed repository."""
        d, base = self._branch_with(
            lambda d: self._write(d, "f.md", "clean\n"), msg="restores " + D_MID + " behavior")
        self.assertEqual(check.check_diff(base, "HEAD", cwd=d, allow_self=True), [])

    def test_preexisting_lines_are_not_flagged(self):
        d = self._mkrepo()
        self._write(d, "old.md", "per " + D_MID + "\n")
        self._commit(d)
        base = self._git(d, "rev-parse", "HEAD").strip()
        self._write(d, "new.md", "clean\n")
        self._commit(d)
        self.assertEqual(check.check_diff(base, "HEAD", cwd=d, allow_self=True), [])

    def test_non_utf8_diff_does_not_crash(self):
        d = self._mkrepo()
        self._write(d, "seed.md", "base\n")
        self._commit(d)
        base = self._git(d, "rev-parse", "HEAD").strip()
        (Path(d) / "bin.dat").write_bytes(b"\xff\xfe binary \x00")
        self._commit(d)
        check.check_diff(base, "HEAD", cwd=d, allow_self=True)  # must not raise

    def test_refuses_when_the_target_is_this_same_repository(self):
        """A clean result must never be readable as 'the outbound submission was scanned' when
        the thing scanned was this repository itself."""
        with self.assertRaises(RuntimeError):
            check.check_diff("HEAD~1", "HEAD", cwd=str(check._repo_root()))

    def test_repo_slug_parses_the_remote_forms(self):
        for url in ("https://github.com/Owner/Name.git", "git@github.com:Owner/Name.git",
                    "https://github.com/Owner/Name"):
            self.assertEqual(check._repo_slug(url), "owner/name", url)
        self.assertEqual(check._repo_slug(""), "")


class OutboundTest(unittest.TestCase):
    def test_unreadable_path_is_an_error_and_other_inputs_still_scan(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("per " + D_MID + "\n")
            good = f.name
        self.addCleanup(lambda: os.unlink(good))
        findings, errors, scanned = check.check_files(["/nonexistent.md", good])
        self.assertTrue(errors)
        self.assertTrue(findings)
        self.assertEqual(scanned, 1)


class ReportTest(unittest.TestCase):
    def test_a_scan_that_examined_nothing_is_an_error_not_clean(self):
        """'I found nothing' and 'I examined nothing' must not print the same word."""
        self.assertEqual(check._report([], "empty", 0), 2)

    def test_a_scan_that_examined_something_and_found_nothing_is_clean(self):
        self.assertEqual(check._report([], "ok", 5), 0)

    def test_findings_exit_one(self):
        self.assertEqual(check._report([("f", 1, D_MID)], "x", 1), 1)


class DemoTest(unittest.TestCase):
    def test_demo_passes_on_healthy_scanners(self):
        """The falsification harness is itself under test, so its failure path is real."""
        self.assertEqual(check.demo(), 0)


class CliTest(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(Path(check.__file__)), *args],
            capture_output=True, encoding="utf-8", cwd=str(check._repo_root())).returncode

    def test_no_mode_and_unknown_mode_are_usage_errors(self):
        self.assertEqual(self._run(), 2)
        self.assertEqual(self._run("bogus-mode"), 2)

    def test_surfaces_is_clean_against_the_committed_baseline(self):
        self.assertEqual(self._run("surfaces"), 0)

    def test_diff_without_refs_is_a_usage_error(self):
        self.assertEqual(self._run("diff"), 2)


if __name__ == "__main__":
    unittest.main()
