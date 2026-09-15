from pathlib import Path
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run_git_checks import ci_options, pre_push_options


PROJECT = Path(__file__).resolve().parents[2]
HOOK_NAMES = ("pre-commit", "commit-msg", "pre-push")
SCRIPT_NAMES = (
    "check_commit_message.py", "check_git_policy.py", "check_secrets.py",
    "git_policy_config.py", "gitleaks.toml", "run_git_checks.py",
)


def run(command, cwd, **kwargs):
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, **kwargs)


def make_executable(path):
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


class HookChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def init_repo(self, name="repo"):
        root = self.base / name
        root.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Hook Test"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "hook@example.invalid"], cwd=root, check=True)
        return root

    def copy_policy_tools(self, root):
        scripts = root / "scripts"
        scripts.mkdir()
        for name in SCRIPT_NAMES:
            shutil.copy2(PROJECT / "scripts" / name, scripts / name)
        shutil.copytree(PROJECT / ".githooks", root / ".githooks")
        for name in HOOK_NAMES:
            make_executable(root / ".githooks" / name)

    def dummy_hooks(self, root, body="exit 0\n"):
        hooks = root / ".githooks"
        hooks.mkdir()
        for name in HOOK_NAMES:
            path = hooks / name
            path.write_text(f"#!/bin/sh\n{body}", encoding="utf-8")
            make_executable(path)

    def test_installer_sets_repository_local_hooks_path(self):
        root = self.init_repo()
        self.dummy_hooks(root)
        installer = PROJECT / "scripts" / "install_git_hooks.py"
        result = run([sys.executable, str(installer)], root)
        self.assertEqual(result.returncode, 0, result.stdout)
        configured = run(["git", "config", "--local", "--get", "core.hooksPath"], root)
        self.assertEqual(configured.stdout.strip(), ".githooks")

    def test_installer_chains_existing_hooks_before_repository_hooks(self):
        root = self.init_repo()
        marker = self.base / "hook-order.txt"
        self.dummy_hooks(root, 'printf "repository\\n" >> "$HOOK_MARKER"\n')
        legacy = root / "legacy-hooks"
        legacy.mkdir()
        for name in HOOK_NAMES:
            path = legacy / name
            path.write_text(
                '#!/bin/sh\nprintf "legacy\\n" >> "$HOOK_MARKER"\n',
                encoding="utf-8",
            )
            make_executable(path)
        subprocess.run(
            ["git", "config", "--local", "core.hooksPath", "legacy-hooks"],
            cwd=root, check=True,
        )
        installer = PROJECT / "scripts" / "install_git_hooks.py"
        installed = run([sys.executable, str(installer)], root)
        self.assertEqual(installed.returncode, 0, installed.stdout)
        configured = run(
            ["git", "config", "--local", "--get", "core.hooksPath"], root
        ).stdout.strip()
        environment = os.environ.copy()
        environment["HOOK_MARKER"] = str(marker)
        invoked = run([str(Path(configured) / "pre-commit")], root, env=environment)
        self.assertEqual(invoked.returncode, 0, invoked.stdout)
        self.assertEqual(marker.read_text(encoding="utf-8").splitlines(), ["legacy", "repository"])

        ref_line = "refs/heads/main local refs/heads/main remote"
        (legacy / "pre-push").write_text(
            '#!/bin/sh\nIFS= read -r line\nprintf "legacy:%s\\n" "$line" >> "$HOOK_MARKER"\n',
            encoding="utf-8",
        )
        make_executable(legacy / "pre-push")
        (root / ".githooks" / "pre-push").write_text(
            '#!/bin/sh\nIFS= read -r line\nprintf "repository:%s\\n" "$line" >> "$HOOK_MARKER"\n',
            encoding="utf-8",
        )
        make_executable(root / ".githooks" / "pre-push")
        installed = run([sys.executable, str(installer)], root)
        self.assertEqual(installed.returncode, 0, installed.stdout)
        invoked = run(
            [str(Path(configured) / "pre-push"), "origin", "example.invalid"],
            root, env=environment, input=ref_line + "\n",
        )
        self.assertEqual(invoked.returncode, 0, invoked.stdout)
        self.assertEqual(
            marker.read_text(encoding="utf-8").splitlines()[-2:],
            [f"legacy:{ref_line}", f"repository:{ref_line}"],
        )

    def test_installer_preserves_effective_global_hooks_path(self):
        root = self.init_repo()
        marker = self.base / "global-hook-order.txt"
        self.dummy_hooks(root, 'printf "repository\n" >> "$HOOK_MARKER"\n')
        global_hooks = root / "global-hooks"
        global_hooks.mkdir()
        previous = global_hooks / "pre-commit"
        previous.write_text(
            '#!/bin/sh\nprintf "global\n" >> "$HOOK_MARKER"\n', encoding="utf-8"
        )
        make_executable(previous)
        global_config = self.base / "global.gitconfig"
        environment = os.environ.copy()
        environment["GIT_CONFIG_GLOBAL"] = str(global_config)
        subprocess.run(
            ["git", "config", "--global", "core.hooksPath", str(global_hooks)],
            cwd=root, env=environment, check=True,
        )

        installer = PROJECT / "scripts" / "install_git_hooks.py"
        installed = run([sys.executable, str(installer)], root, env=environment)
        self.assertEqual(installed.returncode, 0, installed.stdout)
        configured = run(
            ["git", "config", "--local", "--get", "core.hooksPath"], root,
            env=environment,
        ).stdout.strip()
        environment["HOOK_MARKER"] = str(marker)
        invoked = run([str(Path(configured) / "pre-commit")], root, env=environment)
        self.assertEqual(invoked.returncode, 0, invoked.stdout)
        self.assertEqual(marker.read_text(encoding="utf-8").splitlines(), ["global", "repository"])

    def test_commit_message_hook_accepts_and_rejects_expected_subjects(self):
        root = self.init_repo()
        self.copy_policy_tools(root)
        message = self.base / "COMMIT_EDITMSG"
        message.write_text("feat(repo): 정상 메시지\n", encoding="utf-8")
        accepted = run([str(root / ".githooks" / "commit-msg"), str(message)], root)
        self.assertEqual(accepted.returncode, 0, accepted.stdout)
        message.write_text("invalid message content\n", encoding="utf-8")
        rejected = run([str(root / ".githooks" / "commit-msg"), str(message)], root)
        self.assertEqual(rejected.returncode, 1)
        self.assertNotIn("invalid message content", rejected.stdout)

    def test_pre_commit_allows_required_sources_then_blocks_forced_files(self):
        root = self.init_repo()
        self.copy_policy_tools(root)
        allowed = {
            ".env.example": "API_KEY=CHANGEME\n",
            "package-lock.json": "{}\n",
            "public/images/app.png": "synthetic image fixture",
            "tests/fixtures/좌석 예시.json": "{}\n",
        }
        for name, content in allowed.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "add", *allowed], cwd=root, check=True)
        environment = os.environ.copy()
        environment["GITLEAKS_BIN"] = str(
            PROJECT / ".tools" / ("gitleaks.exe" if os.name == "nt" else "gitleaks")
        )
        accepted = run([str(root / ".githooks" / "pre-commit")], root, env=environment)
        self.assertEqual(accepted.returncode, 0, accepted.stdout)

        forbidden = root / ".env.local"
        oversized = root / "too-large.bin"
        forbidden.write_text("placeholder", encoding="utf-8")
        oversized.write_bytes(b"0" * (5 * 1024 * 1024 + 1))
        subprocess.run(["git", "add", "-f", forbidden.name, oversized.name], cwd=root, check=True)
        rejected = run([str(root / ".githooks" / "pre-commit")], root, env=environment)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("security.env", rejected.stdout)
        self.assertIn("size.max-5-mib", rejected.stdout)

    def test_pre_push_range_selection_handles_new_multiple_and_deleted_refs(self):
        root = self.init_repo()
        seed = root / "seed.txt"
        seed.write_text("seed", encoding="utf-8")
        subprocess.run(["git", "add", seed.name], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "chore: seed"], cwd=root, check=True)
        seed_oid = run(["git", "rev-parse", "HEAD"], root).stdout.strip()
        first = root / "first.txt"
        first.write_text("first", encoding="utf-8")
        subprocess.run(["git", "add", first.name], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "feat: first"], cwd=root, check=True)
        first_oid = run(["git", "rev-parse", "HEAD"], root).stdout.strip()
        second = root / "second.txt"
        second.write_text("second", encoding="utf-8")
        subprocess.run(["git", "add", second.name], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "feat: second"], cwd=root, check=True)
        second_oid = run(["git", "rev-parse", "HEAD"], root).stdout.strip()
        zero = "0" * len(seed_oid)
        input_text = "\n".join([
            f"refs/heads/current {first_oid} refs/heads/current {seed_oid}",
            f"refs/heads/new {second_oid} refs/heads/new {zero}",
            f"(delete) {zero} refs/heads/old {seed_oid}",
        ])
        options, invalid = pre_push_options(root, input_text)
        self.assertFalse(invalid)
        self.assertEqual(len(options), 2)
        self.assertIn(f"{seed_oid}..{first_oid}", options)
        self.assertIn(second_oid, options)

    def test_ci_uses_exact_pull_request_and_push_ranges(self):
        root = self.init_repo()
        seed = root / "seed.txt"
        seed.write_text("seed", encoding="utf-8")
        subprocess.run(["git", "add", seed.name], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "chore: seed"], cwd=root, check=True)
        base = run(["git", "rev-parse", "HEAD"], root).stdout.strip()
        seed.write_text("changed", encoding="utf-8")
        subprocess.run(["git", "add", seed.name], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "fix: change"], cwd=root, check=True)
        head = run(["git", "rev-parse", "HEAD"], root).stdout.strip()
        event_path = self.base / "event.json"

        event_path.write_text(json.dumps({
            "pull_request": {
                "base": {"sha": base},
                "head": {"sha": head},
            }
        }), encoding="utf-8")
        with patch.dict(os.environ, {"GITHUB_EVENT_PATH": str(event_path)}):
            self.assertEqual(ci_options(root), [f"{base}..{head}"])

        event_path.write_text(json.dumps({"before": base, "after": head}), encoding="utf-8")
        with patch.dict(os.environ, {"GITHUB_EVENT_PATH": str(event_path)}):
            self.assertEqual(ci_options(root), [f"{base}..{head}"])

        zero = "0" * len(head)
        event_path.write_text(json.dumps({"before": zero, "after": head}), encoding="utf-8")
        with patch.dict(os.environ, {"GITHUB_EVENT_PATH": str(event_path)}):
            self.assertEqual(ci_options(root), [head])

        event_path.write_text(json.dumps({"before": head, "after": zero}), encoding="utf-8")
        with patch.dict(os.environ, {"GITHUB_EVENT_PATH": str(event_path)}):
            self.assertEqual(ci_options(root), [])

    def test_pre_push_blocks_intermediate_forbidden_and_large_blobs(self):
        root = self.init_repo()
        remote = self.base / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
        subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=root, check=True)
        seed = root / "seed.txt"
        seed.write_text("seed", encoding="utf-8")
        subprocess.run(["git", "add", seed.name], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "chore: seed"], cwd=root, check=True)
        subprocess.run(["git", "push", "-q", "origin", "HEAD:refs/heads/main"], cwd=root, check=True)

        forbidden = root / ".env.local"
        large = root / "temporary-large.bin"
        secret_file = root / "temporary-config.txt"
        body = "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        synthetic_secret = "ghp_" + body[:36]
        forbidden.write_text("placeholder", encoding="utf-8")
        large.write_bytes(b"0" * (5 * 1024 * 1024 + 1))
        secret_file.write_text(f"token={synthetic_secret}\n", encoding="utf-8")
        subprocess.run(
            ["git", "add", "-f", forbidden.name, large.name, secret_file.name],
            cwd=root, check=True,
        )
        subprocess.run(["git", "commit", "-qm", "test: add temporary violations"], cwd=root, check=True)
        forbidden.unlink()
        large.unlink()
        secret_file.unlink()
        subprocess.run(["git", "add", "-u"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "test: remove temporary violations"], cwd=root, check=True)

        self.copy_policy_tools(root)
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], cwd=root, check=True)
        environment = os.environ.copy()
        environment["GITLEAKS_BIN"] = str(
            PROJECT / ".tools" / ("gitleaks.exe" if os.name == "nt" else "gitleaks")
        )
        pushed = run(
            ["git", "push", "origin", "HEAD:refs/heads/main"], root,
            env=environment,
        )
        output = pushed.stdout + pushed.stderr
        self.assertNotEqual(pushed.returncode, 0)
        self.assertIn(".env.local", output)
        self.assertIn("temporary-large.bin", output)
        self.assertIn("secret.github-pat", output)
        self.assertIn("value redacted", output)
        self.assertNotIn(synthetic_secret, output)
        remote_head = run(["git", "--git-dir", str(remote), "rev-parse", "refs/heads/main"], root)
        self.assertNotEqual(remote_head.stdout.strip(), run(["git", "rev-parse", "HEAD"], root).stdout.strip())


if __name__ == "__main__":
    unittest.main()
