"""Validate Conventional Commit subjects without echoing message contents."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import shlex

from check_git_policy import git, repository_root


SUBJECT_PATTERN = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(?:\([a-z0-9][a-z0-9._/-]*\))?: \S.*$"
)


def valid_subject(subject: str) -> bool:
    return bool(SUBJECT_PATTERN.fullmatch(subject.rstrip("\r\n")))


def commits_for(root: Path, log_options: list[str]) -> list[str]:
    commits: set[str] = set()
    for value in log_options:
        commits.update(git(root, "rev-list", *shlex.split(value)).splitlines())
    return sorted(commits)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--file", type=Path)
    selection.add_argument("--log-opts", action="append")
    selection.add_argument("--history", action="store_true")
    args = parser.parse_args()

    if args.file:
        try:
            subject = args.file.read_text(encoding="utf-8-sig").splitlines()[0]
        except (OSError, UnicodeError, IndexError):
            print("FAIL: commit-message.read: unable to read a UTF-8 commit subject")
            return 2
        if not valid_subject(subject):
            print(
                "FAIL: commit-message.format: expected "
                "type(scope): summary with an allowed English type and optional English scope"
            )
            return 1
        print("PASS: commit message format")
        return 0

    try:
        root = repository_root(Path.cwd())
        options = ["--all"] if args.history else args.log_opts
        commits = commits_for(root, options)
        invalid = [
            commit for commit in commits
            if not valid_subject(git(root, "show", "-s", "--format=%s", commit))
        ]
    except RuntimeError as error:
        print(f"FAIL: commit-message.internal: {error}")
        return 2
    for commit in invalid:
        print(f"FAIL: commit {commit[:12]}: commit-message.format")
    if invalid:
        return 1
    print(f"PASS: commit message format checked {len(commits)} commits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
