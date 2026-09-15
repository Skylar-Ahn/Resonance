"""Activate repository hooks while preserving an existing local hooks path."""

from __future__ import annotations

from pathlib import Path
import shlex
import stat
import subprocess

from check_git_policy import git, repository_root


HOOKS = ("pre-commit", "commit-msg", "pre-push")


def config_get(root: Path, key: str) -> str | None:
    result = subprocess.run(
        ["git", "config", "--local", "--get", key], cwd=root,
        capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def config_get_effective(root: Path, key: str) -> str | None:
    result = subprocess.run(
        ["git", "config", "--get", key], cwd=root,
        capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def config_set(root: Path, key: str, value: str) -> None:
    result = subprocess.run(
        ["git", "config", "--local", key, value], cwd=root,
        capture_output=True, text=True,
    )
    if result.returncode:
        raise RuntimeError("unable to update repository-local Git configuration")


def executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def resolve_hooks_path(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def write_integrating_hook(
    target: Path, previous: Path, repository_hook: Path, hook_name: str
) -> None:
    header = (
        "#!/bin/sh\nset -eu\n"
        f"previous={shlex.quote(str(previous))}\n"
        f"repository_hook={shlex.quote(str(repository_hook))}\n"
    )
    if hook_name == "pre-push":
        body = (
            "umask 077\n"
            'input=$(mktemp "${TMPDIR:-/tmp}/resonance-pre-push.XXXXXX")\n'
            'trap \'rm -f "$input"\' EXIT HUP INT TERM\n'
            'cat > "$input"\n'
            'if [ -x "$previous" ]; then "$previous" "$@" < "$input"; fi\n'
            '"$repository_hook" "$@" < "$input"\n'
        )
    else:
        body = (
            'if [ -x "$previous" ]; then "$previous" "$@"; fi\n'
            'exec "$repository_hook" "$@"\n'
        )
    target.write_text(header + body, encoding="utf-8")
    executable(target)


def main() -> int:
    try:
        root = repository_root(Path.cwd())
        repository_hooks = root / ".githooks"
        for name in HOOKS:
            executable(repository_hooks / name)
        current = config_get_effective(root, "core.hooksPath")
        if not current or resolve_hooks_path(root, current) == repository_hooks.resolve():
            config_set(root, "core.hooksPath", ".githooks")
            print("PASS: repository-local core.hooksPath=.githooks")
            return 0

        git_directory = Path(git(root, "rev-parse", "--absolute-git-dir").strip())
        integration = git_directory / "resonance-hooks"
        integration.mkdir(parents=True, exist_ok=True)
        saved = config_get(root, "resonance.previousHooksPath")
        if saved and resolve_hooks_path(root, current) == integration.resolve():
            previous_root = Path(saved)
        else:
            previous_root = resolve_hooks_path(root, current)
            config_set(root, "resonance.previousHooksPath", str(previous_root))
        for name in HOOKS:
            write_integrating_hook(
                integration / name, previous_root / name, repository_hooks / name, name
            )
        config_set(root, "core.hooksPath", str(integration))
        print("PASS: existing hooks path preserved and chained before Resonance hooks")
        return 0
    except (OSError, RuntimeError) as error:
        print(f"FAIL: hook-install: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
