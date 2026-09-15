"""Shared entry point for local Git hooks, CI, and historical audits."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

from check_git_policy import git, repository_root
from git_policy_config import POLICY_BASELINE


SCRIPTS = Path(__file__).resolve().parent


def run(script: str, *args: str) -> int:
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args]).returncode


def run_revision_checks(options: list[str]) -> int:
    if not options:
        return run("check_secrets.py", "--verify-tool")
    arguments = [item for value in options for item in ("--log-opts", value)]
    results = [
        run("check_git_policy.py", *arguments),
        run("check_secrets.py", *arguments),
        run("check_commit_message.py", *arguments),
    ]
    return 1 if any(results) else 0


def peel_commit(root: Path, object_id: str) -> str:
    return git(root, "rev-parse", f"{object_id}^{{commit}}").strip()


def has_baseline(root: Path) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{POLICY_BASELINE}^{{commit}}"],
        cwd=root, capture_output=True,
    )
    return result.returncode == 0


def new_ref_options(root: Path, local_commit: str) -> str:
    if has_baseline(root):
        return f"{local_commit} --not {POLICY_BASELINE}"
    print("NOTICE: policy baseline is unavailable; scanning the new ref's complete history")
    return local_commit


def pre_push_options(root: Path, input_text: str) -> tuple[list[str], bool]:
    options: list[str] = []
    invalid = False
    for raw_line in input_text.splitlines():
        fields = raw_line.split()
        if len(fields) != 4:
            print("FAIL: push.refs: malformed pre-push ref input")
            invalid = True
            continue
        local_ref, local_oid, remote_ref, remote_oid = fields
        shown_ref = json.dumps(remote_ref, ensure_ascii=False)
        if set(local_oid) == {"0"}:
            print(f"PASS: ref deletion {shown_ref} introduces no Git objects")
            continue
        try:
            local_commit = peel_commit(root, local_oid)
            if set(remote_oid) == {"0"}:
                option = new_ref_options(root, local_commit)
            else:
                remote_commit = peel_commit(root, remote_oid)
                if remote_ref.startswith("refs/heads/"):
                    ancestor = subprocess.run(
                        ["git", "merge-base", "--is-ancestor", remote_commit, local_commit],
                        cwd=root, capture_output=True,
                    )
                    if ancestor.returncode != 0:
                        print(f"FAIL: {shown_ref}: push.non-fast-forward")
                        invalid = True
                        continue
                option = f"{remote_commit}..{local_commit}"
            count = git(root, "rev-list", "--count", *shlex.split(option)).strip()
            print(f"CHECK: {shown_ref}: {count} commit(s)")
            options.append(option)
        except RuntimeError:
            print(f"FAIL: {shown_ref}: push.range-unavailable")
            invalid = True
    return list(dict.fromkeys(options)), invalid


def ci_options(root: Path) -> list[str]:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if event_path:
        try:
            event = json.loads(Path(event_path).read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise RuntimeError("unable to read GitHub event metadata") from error
        if pull_request := event.get("pull_request"):
            return [f"{pull_request['base']['sha']}..{pull_request['head']['sha']}"]
        before, after = event.get("before"), event.get("after")
        if after:
            if set(after) == {"0"}:
                print("PASS: deleted push ref introduces no Git objects")
                return []
            if before and set(before) != {"0"}:
                return [f"{before}..{after}"]
            return [new_ref_options(root, peel_commit(root, after))]
    head = peel_commit(root, "HEAD")
    return [new_ref_options(root, head)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("pre-commit")
    commit_message = subcommands.add_parser("commit-msg")
    commit_message.add_argument("message_file")
    pre_push = subcommands.add_parser("pre-push")
    pre_push.add_argument("remote_name")
    pre_push.add_argument("remote_url")
    subcommands.add_parser("ci")
    subcommands.add_parser("audit")
    args = parser.parse_args()

    if args.command == "pre-commit":
        results = [
            run("check_git_policy.py", "--staged"),
            run("check_secrets.py", "--staged"),
        ]
        return 1 if any(results) else 0
    if args.command == "commit-msg":
        return run("check_commit_message.py", "--file", args.message_file)
    if args.command == "audit":
        results = [
            run("check_git_policy.py", "--history"),
            run("check_secrets.py", "--history"),
            run("check_commit_message.py", "--history"),
        ]
        return 1 if any(results) else 0

    try:
        root = repository_root(Path.cwd())
        if args.command == "pre-push":
            options, invalid = pre_push_options(root, sys.stdin.read())
            result = run_revision_checks(options)
            return 1 if invalid or result else 0
        options = ci_options(root)
        return run_revision_checks(options)
    except (KeyError, RuntimeError, ValueError):
        print("FAIL: git-checks.range: unable to determine a complete revision range")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
