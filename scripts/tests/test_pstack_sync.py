from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agents/skills/pstack-sync/scripts"))
import pstack_artifacts as artifacts
import pstack_sync as sync


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def initialize(root: Path) -> None:
    root.mkdir(parents=True)
    git(root, "init", "-b", "main")
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "config", "user.name", "Test")


def write(root: Path, path: str, text: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)


def commit(root: Path) -> str:
    git(root, "add", ".")
    git(root, "commit", "-m", "fixture")
    return git(root, "rev-parse", "HEAD")


class PortTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "bstack"
        self.upstream = Path(self.temporary.name) / "upstream"
        initialize(self.root)
        initialize(self.upstream)
        self.source = "pstack/skills/demo/SKILL.md"
        self.target = "skills/demo/SKILL.md"
        self.old = "# Demo\n\nOriginal instruction.\n"
        self.new = "# Demo\n\nUpdated instruction.\n"
        write(self.upstream, self.source, self.old)
        write(self.upstream, "pstack/skills/removed/SKILL.md", "Retired instruction.\n")
        self.base = commit(self.upstream)
        write(self.upstream, self.source, self.new)
        write(self.upstream, "pstack/skills/new/SKILL.md", "New instruction.\n")
        (self.upstream / "pstack/skills/removed/SKILL.md").unlink()
        self.head = commit(self.upstream)
        write(self.root, self.target, self.old)
        write(self.root, "skills/poteto-mode/SKILL.md", "Fixture\n")
        write(self.root, "skills/removed/SKILL.md", "Retired instruction.\n")
        commit(self.root)
        self.snapshot = {"base_commit": self.base, "head_commit": self.head,
                         "upstream_path": "pstack", "upstream_url": str(self.upstream),
                         "upstream_branch": "main", "observed_at": "2026-01-01T00:00:00Z"}
        self.review = artifacts.save_review(self.root, self.upstream, self.snapshot)

    def manifest(self, reviewed=True):
        data = artifacts.read_json(self.review / "dispositions.json")
        if reviewed:
            for entry in data["entries"]:
                entry["disposition"] = "port"
                entry["reason"] = "Adopt fixture change"
            artifacts.write_json(self.review / "dispositions.json", data)
        return data

    def preview(self):
        self.manifest()
        return artifacts.preview(self.root, self.upstream, self.review)

    def test_artifacts_and_repeat_inspection_preserve_decisions(self):
        data = self.manifest()
        saved = artifacts.save_review(self.root, self.upstream, self.snapshot)
        self.assertEqual(saved, self.review)
        self.assertEqual(artifacts.read_json(saved / "dispositions.json"), data)
        demo = next(e for e in data["entries"] if e["path"] == self.source)
        self.assertEqual((saved / demo["artifacts"] / "base").read_text(), self.old)
        self.assertIn("+Updated instruction.", (saved / demo["artifacts"] / "change.diff").read_text())

    def test_coverage_rejects_pending_missing_extra_duplicate_and_wrong_range(self):
        with self.assertRaisesRegex(artifacts.ArtifactError, "unreviewed"):
            artifacts.coverage(self.upstream, self.review)
        original = self.manifest()
        for mutation in (lambda d: d["entries"].pop(),
                         lambda d: d["entries"].append({"path": "pstack/extra", "status": "A", "disposition": "skip"}),
                         lambda d: d["entries"].append(d["entries"][0]),
                         lambda d: d.update(head_commit=self.base)):
            data = json.loads(json.dumps(original))
            mutation(data)
            artifacts.write_json(self.review / "dispositions.json", data)
            with self.assertRaises(artifacts.ArtifactError):
                artifacts.coverage(self.upstream, self.review)

    def test_preview_does_not_write_and_reports_deletions(self):
        preview = self.preview()
        self.assertEqual((self.root / self.target).read_text(), self.old)
        self.assertFalse((self.root / "skills/new/SKILL.md").exists())
        self.assertTrue((self.root / "skills/removed/SKILL.md").exists())
        plan = artifacts.read_json(preview / "plan.json")
        self.assertEqual(next(e for e in plan["entries"] if e["target"] == "skills/removed/SKILL.md")["status"], "deletion")

    def test_apply_selected_files_and_repeat(self):
        preview = self.preview()
        targets = [self.target, "skills/new/SKILL.md"]
        result = artifacts.apply_preview(self.root, preview, targets)
        self.assertEqual(result["applied"], targets)
        self.assertEqual((self.root / self.target).read_text(), self.new)
        self.assertEqual((self.root / "skills/new/SKILL.md").read_text(), "New instruction.\n")
        self.assertEqual(artifacts.apply_preview(self.root, preview, targets)["already_applied"], targets)
        self.assertTrue((self.root / "skills/removed/SKILL.md").exists())

    def test_preflight_rejects_stale_file_before_any_write(self):
        preview = self.preview()
        write(self.root, self.target, "Concurrent edit\n")
        with self.assertRaisesRegex(artifacts.ArtifactError, "changed since preview"):
            artifacts.apply_preview(self.root, preview, ["skills/new/SKILL.md", self.target])
        self.assertFalse((self.root / "skills/new/SKILL.md").exists())
        self.assertEqual((self.root / self.target).read_text(), "Concurrent edit\n")

    def test_post_apply_edit_and_mode_change_are_protected(self):
        preview = self.preview()
        artifacts.apply_preview(self.root, preview, [self.target])
        write(self.root, self.target, "Later edit\n")
        with self.assertRaises(artifacts.ArtifactError):
            artifacts.apply_preview(self.root, preview, [self.target])
        preview = self.preview()
        (self.root / self.target).chmod(0o755)
        with self.assertRaises(artifacts.ArtifactError):
            artifacts.apply_preview(self.root, preview, [self.target])

    def test_conflicts_must_be_resolved_in_candidate(self):
        write(self.root, self.target, "# Demo\n\nLocal instruction.\n")
        preview = self.preview()
        item = next(e for e in artifacts.read_json(preview / "plan.json")["entries"] if e["target"] == self.target)
        self.assertEqual(item["status"], "conflict")
        with self.assertRaisesRegex(artifacts.ArtifactError, "conflict markers"):
            artifacts.apply_preview(self.root, preview, [self.target])
        (preview / item["candidate"]).write_text("# Demo\n\nReviewed combined instruction.\n")
        artifacts.apply_preview(self.root, preview, [self.target])
        self.assertEqual((self.root / self.target).read_text(), "# Demo\n\nReviewed combined instruction.\n")

    def test_targets_cannot_escape_or_follow_symlinks(self):
        for target in ("../outside", "/tmp/outside", ".git/config", "skills/../../outside"):
            with self.assertRaises(artifacts.ArtifactError):
                artifacts.safe_target(self.root, target)
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        (self.root / "linked").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(artifacts.ArtifactError, "symlink"):
            artifacts.safe_target(self.root, "linked/file.md")
        preview = self.preview()
        (self.root / self.target).unlink()
        (self.root / self.target).symlink_to(outside / "file.md")
        with self.assertRaisesRegex(artifacts.ArtifactError, "symlink"):
            artifacts.apply_preview(self.root, preview, [self.target])

    def test_absent_local_file_requires_manual_decision(self):
        (self.root / self.target).unlink()
        preview = self.preview()
        item = next(e for e in artifacts.read_json(preview / "plan.json")["entries"] if e["target"] == self.target)
        self.assertEqual(item["status"], "manual")
        with self.assertRaisesRegex(artifacts.ArtifactError, "no candidate"):
            artifacts.apply_preview(self.root, preview, [self.target])
        self.assertFalse((self.root / self.target).exists())

    def test_binary_and_symlink_upstream_are_manual(self):
        (self.upstream / self.source).write_bytes(b"binary\0content")
        (self.upstream / "pstack/skills/new/SKILL.md").unlink()
        (self.upstream / "pstack/skills/new/SKILL.md").symlink_to("../demo/SKILL.md")
        self.snapshot["head_commit"] = commit(self.upstream)
        self.review = artifacts.save_review(self.root, self.upstream, self.snapshot)
        plan = artifacts.read_json(self.preview() / "plan.json")
        candidates = [e for e in plan["entries"] if e["target"] in {self.target, "skills/new/SKILL.md"}]
        self.assertEqual([e["status"] for e in candidates], ["manual", "manual"])
        self.assertEqual((self.root / self.target).read_text(), self.old)

    def test_rename_paths_and_spaces_are_individually_reviewable(self):
        moved = "pstack/skills/demo/notes [draft].md"
        (self.upstream / self.source).rename(self.upstream / moved)
        self.snapshot["head_commit"] = commit(self.upstream)
        self.review = artifacts.save_review(self.root, self.upstream, self.snapshot)
        manifest = self.manifest()
        entries = {e["path"]: e for e in manifest["entries"]}
        self.assertEqual(entries[self.source]["status"], "D")
        self.assertEqual(entries[moved]["status"], "A")
        preview = self.preview()
        target = "skills/demo/notes [draft].md"
        artifacts.apply_preview(self.root, preview, [target])
        self.assertEqual((self.root / target).read_text(), self.new)
        self.assertTrue((self.root / self.target).exists())

    def test_cli_review_coverage_mark_preview_apply_and_repeat(self):
        script_dir = self.root / ".agents/skills/pstack-sync/scripts"
        shutil.copytree(ROOT / ".agents/skills/pstack-sync/scripts", script_dir,
                        ignore=shutil.ignore_patterns("__pycache__"))
        state_path = script_dir.parent / "state.json"
        artifacts.write_json(state_path, {"upstream_url": str(self.upstream), "upstream_branch": "main",
                                         "upstream_path": "pstack", "last_checked_commit": self.base})

        def cli(*args):
            result = subprocess.run([sys.executable, str(script_dir / "pstack_sync.py"), *args],
                                    cwd=self.root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)

        inspected = cli("inspect")
        self.assertEqual(inspected["changed_file_count"], 3)
        self.manifest()
        self.assertEqual(cli("coverage", "--review", str(self.review))["reviewed_paths"], 3)
        self.assertEqual(cli("mark")["last_checked_commit"], self.head)
        preview = cli("port-preview", "--review", str(self.review))["preview_path"]
        self.assertEqual(cli("port-apply", "--preview", preview, "--path", self.target)["applied"], [self.target])
        self.assertEqual(cli("port-apply", "--preview", preview, "--path", self.target)["already_applied"], [self.target])
        self.assertEqual((self.root / self.target).read_text(), self.new)

    def test_inspect_mark_and_port_use_same_saved_range(self):
        state_path = self.root / "state.json"
        artifacts.write_json(state_path, {"upstream_url": str(self.upstream), "upstream_branch": "main",
                                         "upstream_path": "pstack", "last_checked_commit": self.base})
        with patch.object(sync, "STATE_PATH", state_path), contextlib.redirect_stdout(io.StringIO()):
            sync.inspect(self.root)
            with self.assertRaisesRegex(artifacts.ArtifactError, "unreviewed"):
                sync.mark(self.root)
            self.assertEqual(artifacts.read_json(state_path)["last_checked_commit"], self.base)
            self.manifest()
            sync.mark(self.root)
        self.assertEqual(artifacts.read_json(state_path)["last_checked_commit"], self.head)
        self.assertFalse((self.root / ".bstack/pstack-sync/pending.json").exists())
        cache = self.root / ".bstack/pstack-sync/upstream"
        preview = artifacts.preview(self.root, cache, self.review)
        artifacts.apply_preview(self.root, preview, [self.target])
        self.assertEqual((self.root / self.target).read_text(), self.new)


if __name__ == "__main__":
    unittest.main()
