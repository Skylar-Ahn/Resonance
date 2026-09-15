from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest


class SecretChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Secret Test"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "secret@example.invalid"], cwd=self.root, check=True)
        scripts = Path(__file__).resolve().parents[1]
        self.script = scripts / "check_secrets.py"
        self.scanner = scripts.parent / ".tools" / (
            "gitleaks.exe" if os.name == "nt" else "gitleaks"
        )

    def run_check(self, *args, scanner=None):
        environment = os.environ.copy()
        environment["GITLEAKS_BIN"] = str(self.scanner if scanner is None else scanner)
        return subprocess.run(
            [sys.executable, str(self.script), *args], cwd=self.root,
            env=environment, capture_output=True, text=True,
        )

    @staticmethod
    def synthetic_secret():
        body = "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        return "ghp_" + body[:36]

    def test_missing_scanner_fails_with_install_command(self):
        result = self.run_check("--staged", scanner=self.root / "missing-gitleaks")
        self.assertEqual(result.returncode, 2)
        self.assertIn("install_gitleaks.py", result.stdout)

    def test_staged_secret_is_redacted(self):
        secret = self.synthetic_secret()
        path = self.root / "한글 secret sample.txt"
        path.write_text(f"aws_access_key_id = {secret}\n", encoding="utf-8")
        subprocess.run(["git", "add", path.name], cwd=self.root, check=True)
        result = self.run_check("--staged")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(path.name, result.stdout)
        self.assertIn("line 1", result.stdout)
        self.assertIn("value redacted", result.stdout)
        self.assertNotIn(secret, result.stdout + result.stderr)

    def test_partial_staging_and_deletion_use_index_state(self):
        path = self.root / "sample.txt"
        path.write_text("safe staged content", encoding="utf-8")
        subprocess.run(["git", "add", path.name], cwd=self.root, check=True)
        path.write_text(self.synthetic_secret(), encoding="utf-8")
        partial = self.run_check("--staged")
        self.assertEqual(partial.returncode, 0, partial.stdout)

        path.write_text(self.synthetic_secret(), encoding="utf-8")
        subprocess.run(["git", "add", path.name], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "test: fixture"], cwd=self.root, check=True)
        path.unlink()
        subprocess.run(["git", "add", "-u"], cwd=self.root, check=True)
        deleted = self.run_check("--staged")
        self.assertEqual(deleted.returncode, 0, deleted.stdout)

    def test_history_finds_secret_deleted_by_later_commit(self):
        seed = self.root / "seed.txt"
        seed.write_text("seed", encoding="utf-8")
        subprocess.run(["git", "add", seed.name], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "chore: seed"], cwd=self.root, check=True)
        base = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root,
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        secret = self.synthetic_secret()
        path = self.root / "temporary-secret.txt"
        path.write_text(f"aws_access_key_id = {secret}\n", encoding="utf-8")
        subprocess.run(["git", "add", path.name], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "test: add fixture"], cwd=self.root, check=True)
        path.unlink()
        subprocess.run(["git", "add", "-u"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "test: remove fixture"], cwd=self.root, check=True)
        result = self.run_check("--log-opts", f"{base}..HEAD")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("temporary-secret.txt", result.stdout)
        self.assertNotIn(secret, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
