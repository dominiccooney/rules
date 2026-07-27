#!/usr/bin/env python3
"""Subprocess integration tests for worklist.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("worklist.py")


class WorklistCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "worklist.json"

    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--path", str(self.path), *args],
            text=True,
            capture_output=True,
            check=False,
        )
        if check and result.returncode:
            self.fail(f"{args}\nstdout: {result.stdout}\nstderr: {result.stderr}")
        return result

    def add(self, number: int = 123) -> None:
        self.run_cli("init")
        self.run_cli("add", "--repo", "owner/repo", "--number", str(number), "--title", "Fix a thing")

    def start(self, number: int = 123) -> None:
        self.run_cli("start", "--next-step", "Read live metadata")
        self.assertEqual(self.summary()["active"], f"owner/repo#{number}")

    def summary(self) -> dict[str, object]:
        return json.loads(self.run_cli("summary", "--json").stdout)

    def test_add_start_update_done(self) -> None:
        self.add()
        self.start()
        self.run_cli(
            "update",
            "--pr",
            "owner/repo#123",
            "--note",
            "metadata verified",
            "--target-branch",
            "main",
            "--base",
            "a" * 40,
            "--head",
            "b" * 40,
            "--evidence",
            "Open and non-draft",
            "--resource",
            "ref refs/review/base",
        )
        self.run_cli(
            "update",
            "--pr",
            "owner/repo#123",
            "--note",
            "head ref acquired",
            "--resource",
            "ref refs/review/head",
        )
        data = json.loads(self.path.read_text())
        self.assertEqual(data["items"][0]["resources"], ["ref refs/review/base", "ref refs/review/head"])
        blocked = self.run_cli(
            "done",
            "--pr",
            "owner/repo#123",
            "--note",
            "complete",
            "--outcome",
            "Gate 2 — superseded",
            "--evidence",
            "Replacement merged",
            "--action",
            "Closed",
            "--remote-state",
            "CLOSED",
            check=False,
        )
        self.assertNotEqual(blocked.returncode, 0)
        self.run_cli("update", "--pr", "owner/repo#123", "--note", "resources removed", "--clear-resources")
        self.run_cli(
            "done",
            "--pr",
            "owner/repo#123",
            "--note",
            "remote state and cleanup verified",
            "--outcome",
            "Gate 2 — superseded",
            "--evidence",
            "Replacement merged",
            "--action",
            "Closed — https://github.com/owner/repo/pull/123",
            "--remote-state",
            "CLOSED at " + "b" * 40,
        )
        self.assertEqual(
            self.summary(),
            {"todo": 0, "in_progress": 0, "waiting": 0, "done": 1, "active": None},
        )
        self.assertEqual(self.run_cli("validate").stdout.strip(), "valid")

    def test_wait_and_restart(self) -> None:
        self.add()
        self.start()
        self.run_cli(
            "wait",
            "--pr",
            "owner/repo#123",
            "--note",
            "paused",
            "--waiting-for",
            "contributor update",
            "--recheck-when",
            "head SHA changes",
            "--next-step",
            "Read changed diff",
            "--evidence",
            "Requested one change",
        )
        self.assertEqual(self.summary()["waiting"], 1)
        self.run_cli("start", "--pr", "owner/repo#123", "--note", "head changed", "--next-step", "Verify head")
        data = json.loads(self.path.read_text())
        item = data["items"][0]
        self.assertEqual(item["state"], "in_progress")
        self.assertIn("Resumed from waiting", item["evidence"])

    def test_duplicate_and_wrong_active_fail_without_writing(self) -> None:
        self.add()
        before = self.path.read_bytes()
        duplicate = self.run_cli(
            "add", "--repo", "owner/repo", "--number", "123", "--title", "Duplicate", check=False
        )
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)
        self.start()
        before = self.path.read_bytes()
        wrong = self.run_cli("update", "--pr", "owner/repo#999", "--note", "wrong", check=False)
        self.assertNotEqual(wrong.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)


    def test_invalid_optional_field_is_reported_without_rewrite(self) -> None:
        self.path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "items": [
                        {
                            "repo": "owner/repo",
                            "number": 123,
                            "url": 42,
                            "title": "Bad URL type",
                            "opened": 20260101,
                            "state": "todo",
                        }
                    ],
                }
            )
        )
        before = self.path.read_bytes()
        result = self.run_cli("validate", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.path.read_bytes(), before)

    def test_invalid_json_is_not_rewritten(self) -> None:
        self.path.write_text('{"version": 1, "items": [}')
        before = self.path.read_bytes()
        result = self.run_cli("validate", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
