"""Run the pinned Gitleaks scanner against staged blobs or Git history."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

from check_git_policy import git, repository_root, staged_entries
from git_policy_config import GITLEAKS_VERSION


def scanner_path(root: Path) -> Path:
    configured = os.environ.get("GITLEAKS_BIN")
    return Path(configured) if configured else root / ".tools" / (
        "gitleaks.exe" if os.name == "nt" else "gitleaks"
    )


def verify_scanner(root: Path) -> Path | None:
    scanner = scanner_path(root)
    if not scanner.is_file():
        print(
            f"FAIL: secret-scanner.missing: Gitleaks {GITLEAKS_VERSION} is required; "
            "run python3 scripts/install_gitleaks.py"
        )
        return None
    result = subprocess.run([str(scanner), "version"], capture_output=True, text=True)
    if result.returncode != 0 or result.stdout.strip() != GITLEAKS_VERSION:
        print(
            f"FAIL: secret-scanner.version: expected Gitleaks {GITLEAKS_VERSION}; "
            "run python3 scripts/install_gitleaks.py"
        )
        return None
    return scanner


def report_findings(report: Path, prefix: Path | None = None) -> int:
    try:
        findings = json.loads(report.read_text(encoding="utf-8")) if report.exists() else []
    except (OSError, ValueError):
        print("FAIL: secret-scanner.report: unable to read the redacted scanner report")
        return 2
    for finding in findings:
        raw_path = str(finding.get("File", "unknown"))
        if prefix:
            try:
                raw_path = str(Path(raw_path).resolve().relative_to(prefix.resolve()))
            except ValueError:
                raw_path = Path(raw_path).name
        path = json.dumps(raw_path, ensure_ascii=False)
        rule = str(finding.get("RuleID", "unknown-rule"))
        line = int(finding.get("StartLine") or 0)
        commit = str(finding.get("Commit") or "")[:12]
        location = f"line {line}" if not commit else f"commit {commit}, line {line}"
        print(f"FAIL: {path}: secret.{rule}: {location}; value redacted")
    return 1 if findings else 0


def run_gitleaks(scanner: Path, args: list[str], report: Path, prefix: Path | None = None) -> int:
    ignore = report.parent / "empty-gitleaks-ignore"
    ignore.write_text("", encoding="utf-8")
    command = [
        str(scanner), *args, "--config", str(Path(__file__).with_name("gitleaks.toml")),
        "--gitleaks-ignore-path", str(ignore), "--no-banner", "--redact=100", "--no-color",
        "--report-format", "json", "--report-path", str(report), "--exit-code", "1",
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode not in {0, 1}:
        print(f"FAIL: secret-scanner.execution: Gitleaks exited with code {result.returncode}")
        return 2
    finding_result = report_findings(report, prefix)
    if result.returncode == 1 and finding_result == 0:
        print("FAIL: secret-scanner.report: scanner found a secret without a readable report")
        return 2
    return finding_result


def blob_bytes(root: Path, object_id: str) -> bytes:
    result = subprocess.run(
        ["git", "cat-file", "blob", object_id], cwd=root, capture_output=True, check=False
    )
    if result.returncode:
        raise RuntimeError(f"unable to read staged blob {object_id}")
    return result.stdout


def scan_staged(root: Path, scanner: Path) -> int:
    entries = staged_entries(root)
    with tempfile.TemporaryDirectory(prefix="resonance-index-scan-") as directory:
        temporary = Path(directory)
        scan_root = temporary / "index"
        scan_root.mkdir()
        for entry in entries:
            destination = (scan_root / entry.path).resolve()
            if not destination.is_relative_to(scan_root.resolve()):
                raise RuntimeError("staged path escapes the temporary scan root")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(blob_bytes(root, entry.object_id))
        result = run_gitleaks(
            scanner, ["dir", str(scan_root)], temporary / "report.json", scan_root
        )
    if result == 0:
        print(f"PASS: secret scan checked {len(entries)} staged blobs")
    return result


def scan_history(root: Path, scanner: Path, options: list[str]) -> int:
    results: list[int] = []
    for index, value in enumerate(options):
        with tempfile.TemporaryDirectory(prefix="resonance-history-scan-") as directory:
            report = Path(directory) / f"report-{index}.json"
            results.append(run_gitleaks(
                scanner, ["git", str(root), "--log-opts", value], report
            ))
    if all(result == 0 for result in results):
        print(f"PASS: secret scan checked {len(options)} Git revision range(s)")
        return 0
    return max(results, default=0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--staged", action="store_true")
    selection.add_argument("--log-opts", action="append")
    selection.add_argument("--history", action="store_true")
    selection.add_argument("--verify-tool", action="store_true")
    args = parser.parse_args()
    try:
        root = repository_root(Path.cwd())
        scanner = verify_scanner(root)
        if scanner is None:
            return 2
        if args.verify_tool:
            print(f"PASS: Gitleaks {GITLEAKS_VERSION} is available")
            return 0
        if args.log_opts:
            for value in args.log_opts:
                shlex.split(value)
            return scan_history(root, scanner, args.log_opts)
        if args.history:
            return scan_history(root, scanner, ["--all"])
        return scan_staged(root, scanner)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"FAIL: secret-scanner.internal: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
