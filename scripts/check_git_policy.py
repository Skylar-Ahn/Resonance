"""Validate paths and sizes of the exact blobs selected from Git."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fnmatch import fnmatch
import json
import os
from pathlib import Path, PurePosixPath
import shlex
import subprocess


LIMIT_BYTES = 5 * 1024 * 1024
APPROVED_OVERSIZE_PATHS: frozenset[str] = frozenset()


@dataclass(frozen=True)
class IndexEntry:
    path: str
    object_id: str


@dataclass(frozen=True)
class Violation:
    path: str
    rule: str
    detail: str


def git(root: Path, *args: str, input_text: str | None = None) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, input=input_text, capture_output=True,
        text=True, check=False,
    )
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return result.stdout


def repository_root(start: Path) -> Path:
    return Path(git(start, "rev-parse", "--show-toplevel").strip())


def index_entries(root: Path) -> list[IndexEntry]:
    entries: list[IndexEntry] = []
    for record in git(root, "ls-files", "-s", "-z").split("\0"):
        if not record:
            continue
        metadata, path = record.split("\t", 1)
        _, object_id, stage = metadata.split()
        if stage == "0":
            entries.append(IndexEntry(path=path, object_id=object_id))
    return entries


def staged_entries(root: Path) -> list[IndexEntry]:
    output = git(
        root, "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"
    )
    paths = {path for path in output.split("\0") if path}
    return [entry for entry in index_entries(root) if entry.path in paths]


def revision_entries(root: Path, revision_args: list[str]) -> list[IndexEntry]:
    commits = git(root, "rev-list", *revision_args).splitlines()
    entries: set[IndexEntry] = set()
    for commit in commits:
        changed_paths = {
            path for path in git(
                root, "diff-tree", "-r", "-m", "--root", "--no-commit-id",
                "--name-only", "--diff-filter=ACMR", "-z", commit,
            ).split("\0") if path
        }
        for path in changed_paths:
            for record in git(root, "ls-tree", "-z", commit, "--", path).split("\0"):
                if not record:
                    continue
                metadata, tree_path = record.split("\t", 1)
                _, object_type, object_id = metadata.split()
                if object_type == "blob" and tree_path == path:
                    entries.add(IndexEntry(path=path, object_id=object_id))
    return sorted(entries, key=lambda entry: (entry.path, entry.object_id))


def object_sizes(root: Path, object_ids: set[str]) -> dict[str, int]:
    if not object_ids:
        return {}
    output = git(
        root, "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)",
        input_text="\n".join(sorted(object_ids)) + "\n",
    )
    sizes: dict[str, int] = {}
    for line in output.splitlines():
        object_id, object_type, size = line.split()
        if object_type != "blob":
            raise RuntimeError(f"selected object {object_id} is not a blob")
        sizes[object_id] = int(size)
    return sizes


def path_rule(path: str) -> str | None:
    posix = PurePosixPath(path)
    parts = set(posix.parts)
    name = posix.name

    if name == ".env.example":
        return None
    if name == ".env" or name.startswith(".env."):
        return "security.env"
    if name == ".gitleaksignore":
        return "security.scanner-bypass"
    if name in {".DS_Store", "Thumbs.db", "next-env.d.ts"}:
        return "local.generated"
    if fnmatch(name, "storage-state*.json") or fnmatch(name, "cookies*.json"):
        return "security.auth-state"
    if fnmatch(name, "service-account*.json") or fnmatch(name, "credentials*.json"):
        return "security.credentials"
    if any(fnmatch(name, pattern) for pattern in (
        "*.private.pem", "*.private.key", "*.p12", "*.pfx"
    )):
        return "security.private-key"
    if name.endswith(".tsbuildinfo") or name.endswith(".log"):
        return "generated.output"
    if name.endswith((".pyc", ".pyo", ".swp", ".swo", ".tmp")) or name.endswith("~"):
        return "generated.local-file"

    def under(*prefixes: str) -> bool:
        return any(path == prefix or path.startswith(f"{prefix}/") for prefix in prefixes)

    if under(".local-data", "data/private", "data/exports", "data/dumps"):
        return "private.local-data"
    if under(
        ".local-assets", "data/raw", "data/crawls", "data/datasets",
        "models/weights", "backups",
    ):
        return "source.local-assets"

    directory_rules = {
        "security.local": {".local-secrets", "secrets"},
        "security.auth-state": {".auth"},
        "generated.dependencies": {"node_modules"},
        "generated.build": {".next", "out", "dist", "coverage"},
        "generated.test": {"playwright-report", "test-results", "blob-report"},
        "generated.cache": {".tools", ".cache", ".turbo", ".parcel-cache", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv"},
        "generated.logs": {"logs"},
        "local.ide": {".idea"},
    }
    for rule, forbidden_parts in directory_rules.items():
        if parts & forbidden_parts:
            return rule
    if ".vscode" in parts and name not in {"settings.json", "extensions.json"}:
        return "local.ide"
    return None


def validate_entries(root: Path, entries: list[IndexEntry]) -> list[Violation]:
    sizes = object_sizes(root, {entry.object_id for entry in entries})
    violations: list[Violation] = []
    for entry in entries:
        if rule := path_rule(entry.path):
            violations.append(Violation(entry.path, rule, "path is not allowed in Git"))
        size = sizes[entry.object_id]
        if size > LIMIT_BYTES and entry.path not in APPROVED_OVERSIZE_PATHS:
            violations.append(
                Violation(
                    entry.path, "size.max-5-mib",
                    f"blob is {size} bytes and exceeds 5 MiB",
                )
            )
    return violations


def ci_log_options() -> list[str] | None:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        return None
    try:
        event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if pull_request := event.get("pull_request"):
        return [f"{pull_request['base']['sha']}..{pull_request['head']['sha']}"]
    before, after = event.get("before"), event.get("after")
    if after and before and set(before) != {"0"}:
        return [f"{before}..{after}"]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--staged", action="store_true")
    selection.add_argument("--tracked", action="store_true")
    selection.add_argument("--range")
    selection.add_argument("--log-opts", action="append")
    selection.add_argument("--history", action="store_true")
    selection.add_argument("--ci", action="store_true")
    args = parser.parse_args()

    try:
        root = repository_root(Path.cwd())
        mode = "staged"
        if args.tracked:
            entries, mode = index_entries(root), "tracked"
        elif args.range:
            entries, mode = revision_entries(root, [args.range]), f"range {args.range}"
        elif args.log_opts:
            entries = []
            for value in args.log_opts:
                entries.extend(revision_entries(root, shlex.split(value)))
            entries = sorted(set(entries), key=lambda entry: (entry.path, entry.object_id))
            mode = "requested revisions"
        elif args.history:
            entries, mode = revision_entries(root, ["--all"]), "full history"
        elif args.ci and (options := ci_log_options()):
            entries, mode = revision_entries(root, options), "CI range"
        elif args.ci:
            entries, mode = index_entries(root), "CI tracked fallback"
        else:
            entries = staged_entries(root)
        violations = validate_entries(root, entries)
    except (KeyError, RuntimeError, ValueError) as error:
        print(f"FAIL: file-policy.internal: {error}")
        return 2

    for violation in violations:
        path = json.dumps(violation.path, ensure_ascii=False)
        print(f"FAIL: {path}: {violation.rule}: {violation.detail}")
    if violations:
        return 1
    print(f"PASS: file policy checked {len(entries)} {mode} blobs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
