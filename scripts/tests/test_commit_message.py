from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_commit_message import valid_subject


class CommitMessageChecks(unittest.TestCase):
    def test_valid_messages(self):
        for subject in [
            "feat: 좌석 선택 추가",
            "fix(seat-map): 강조 위치 수정",
            "docs(repo): Git 정책 기록",
            "revert: 잘못된 변경 복구",
        ]:
            with self.subTest(subject=subject):
                self.assertTrue(valid_subject(subject))

    def test_invalid_messages(self):
        for subject in [
            "Add feature", "feature: 추가", "feat(좌석): 추가",
            "fix(scope):",
        ]:
            with self.subTest(subject=subject):
                self.assertFalse(valid_subject(subject))

    def test_cli_does_not_echo_invalid_message(self):
        with tempfile.TemporaryDirectory() as directory:
            message = "invalid-message-content"
            path = Path(directory) / "COMMIT_EDITMSG"
            path.write_text(message, encoding="utf-8")
            script = Path(__file__).resolve().parents[1] / "check_commit_message.py"
            result = subprocess.run(
                [sys.executable, str(script), "--file", str(path)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertNotIn(message, result.stdout)


if __name__ == "__main__":
    unittest.main()
