from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_git_policy import LIMIT_BYTES


class GitPolicyChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Policy Test"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "policy@example.invalid"], cwd=self.root, check=True)
        self.script = Path(__file__).resolve().parents[1] / "check_git_policy.py"

    def run_check(self, *args):
        return subprocess.run(
            [sys.executable, str(self.script), *args],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_small_staged_blob_passes(self):
        (self.root / "source.txt").write_text("fixture", encoding="utf-8")
        subprocess.run(["git", "add", "source.txt"], cwd=self.root, check=True)
        result = self.run_check("--staged")
        self.assertEqual(result.returncode, 0)
        self.assertIn("1 staged blobs", result.stdout)

    def test_unstaged_blob_is_not_part_of_staged_check(self):
        (self.root / "local.bin").write_bytes(b"0" * (LIMIT_BYTES + 1))
        result = self.run_check("--staged")
        self.assertEqual(result.returncode, 0)
        self.assertIn("0 staged blobs", result.stdout)

    def test_oversized_index_blob_is_rejected_in_both_modes(self):
        path = self.root / "oversized.bin"
        path.write_bytes(b"0" * (LIMIT_BYTES + 1))
        subprocess.run(["git", "add", path.name], cwd=self.root, check=True)
        for mode in ["--staged", "--tracked"]:
            with self.subTest(mode=mode):
                result = self.run_check(mode)
                self.assertEqual(result.returncode, 1)
                self.assertIn("oversized.bin", result.stdout)
                self.assertIn("5 MiB", result.stdout)

    def test_range_rejects_blob_deleted_by_a_later_commit(self):
        seed = self.root / "seed.txt"
        seed.write_text("seed", encoding="utf-8")
        subprocess.run(["git", "add", seed.name], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "seed"], cwd=self.root, check=True)
        base = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root, capture_output=True,
            text=True, check=True,
        ).stdout.strip()

        oversized = self.root / "temporary-large.bin"
        forbidden = self.root / ".env.local"
        oversized.write_bytes(b"0" * (LIMIT_BYTES + 1))
        forbidden.write_text("placeholder", encoding="utf-8")
        subprocess.run(["git", "add", "-f", oversized.name, forbidden.name], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "add large"], cwd=self.root, check=True)
        oversized.unlink()
        forbidden.unlink()
        subprocess.run(["git", "add", "-u"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "remove large"], cwd=self.root, check=True)

        result = self.run_check("--range", f"{base}..HEAD")
        self.assertEqual(result.returncode, 1)
        self.assertIn("temporary-large.bin", result.stdout)
        self.assertIn(".env.local", result.stdout)

    def test_force_added_forbidden_file_is_rejected(self):
        path = self.root / ".env.local"
        path.write_text("placeholder", encoding="utf-8")
        subprocess.run(["git", "add", "-f", path.name], cwd=self.root, check=True)
        result = self.run_check("--staged")
        self.assertEqual(result.returncode, 1)
        self.assertIn("security.env", result.stdout)

    def test_range_rejects_rename_that_reuses_an_existing_blob(self):
        source = self.root / "allowed.txt"
        source.write_text("ordinary content\n", encoding="utf-8")
        subprocess.run(["git", "add", source.name], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "seed"], cwd=self.root, check=True)
        base = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root, capture_output=True,
            text=True, check=True,
        ).stdout.strip()

        destination = self.root / ".env.local"
        source.rename(destination)
        subprocess.run(["git", "add", "-f", destination.name], cwd=self.root, check=True)
        subprocess.run(["git", "add", "-u", source.name], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "rename"], cwd=self.root, check=True)

        result = self.run_check("--range", f"{base}..HEAD")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("security.env", result.stdout)

    def test_required_sources_and_placeholders_are_allowed(self):
        fixtures = {
            ".env.example": "API_KEY=CHANGEME\n",
            "package-lock.json": "{}\n",
            "public/images/app.png": "synthetic image fixture",
            "tests/fixtures/좌석 샘플.json": "{}\n",
            "db/migrations/001 schema.sql": "create table demo(id integer);\n",
        }
        for name, content in fixtures.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "add", *fixtures], cwd=self.root, check=True)
        result = self.run_check("--staged")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("5 staged blobs", result.stdout)

    def test_partial_staging_uses_index_blob_not_worktree_size(self):
        path = self.root / "부분 스테이징.txt"
        path.write_text("staged content", encoding="utf-8")
        subprocess.run(["git", "add", path.name], cwd=self.root, check=True)
        path.write_bytes(b"0" * (LIMIT_BYTES + 1))
        result = self.run_check("--staged")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_deletion_is_not_a_new_blob_but_forbidden_rename_is(self):
        source = self.root / "allowed.txt"
        source.write_text("fixture", encoding="utf-8")
        subprocess.run(["git", "add", source.name], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "seed"], cwd=self.root, check=True)
        source.unlink()
        subprocess.run(["git", "add", "-u"], cwd=self.root, check=True)
        deleted = self.run_check("--staged")
        self.assertEqual(deleted.returncode, 0, deleted.stdout)

        subprocess.run(["git", "restore", "--staged", source.name], cwd=self.root, check=True)
        subprocess.run(["git", "restore", source.name], cwd=self.root, check=True)
        destination = self.root / ".env.production"
        source.rename(destination)
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True)
        renamed = self.run_check("--staged")
        self.assertEqual(renamed.returncode, 1)
        self.assertIn(".env.production", renamed.stdout)


if __name__ == "__main__":
    unittest.main()
