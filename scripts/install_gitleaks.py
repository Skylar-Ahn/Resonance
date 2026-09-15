"""Install the pinned Gitleaks binary into the ignored .tools directory."""

from __future__ import annotations

import hashlib
import platform
from pathlib import Path
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile

from git_policy_config import GITLEAKS_VERSION


ROOT = Path(__file__).resolve().parents[1]
IS_WINDOWS = platform.system() == "Windows"
BINARY = ROOT / ".tools" / ("gitleaks.exe" if IS_WINDOWS else "gitleaks")
SHA256 = {
    "linux_x64": "79a3ab579b53f71efd634f3aaf7e04a0fa0cf206b7ed434638d1547a2470a66e",
    "linux_arm64": "b4cbbb6ddf7d1b2a603088cd03a4e3f7ce48ee7fd449b51f7de6ee2906f5fa2f",
    "darwin_x64": "ca221d012d247080c2f6f61f4b7a83bffa2453806b0c195c795bbe9a8c775ed5",
    "darwin_arm64": "b251ab2bcd4cd8ba9e56ff37698c033ebf38582b477d21ebd86586d927cf87e7",
    "windows_x64": "54fe94f644b832dd08e8c3a5915efb3bfa862386d59fb27ca0792cb687a83573",
}


def platform_key() -> str:
    operating_system = {
        "Linux": "linux", "Darwin": "darwin", "Windows": "windows",
    }.get(platform.system())
    architecture = {
        "x86_64": "x64", "amd64": "x64", "arm64": "arm64", "aarch64": "arm64",
    }.get(platform.machine().lower())
    key = f"{operating_system}_{architecture}"
    if operating_system is None or architecture is None or key not in SHA256:
        raise RuntimeError(
            f"unsupported platform {platform.system()}/{platform.machine()}; "
            "install the pinned version manually and set GITLEAKS_BIN"
        )
    return key


def installed_version() -> str | None:
    if not BINARY.is_file():
        return None
    result = subprocess.run([str(BINARY), "version"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def main() -> int:
    if installed_version() == GITLEAKS_VERSION:
        print(f"PASS: Gitleaks {GITLEAKS_VERSION} is already installed")
        return 0
    try:
        key = platform_key()
        suffix = "zip" if key.startswith("windows") else "tar.gz"
        asset = f"gitleaks_{GITLEAKS_VERSION}_{key}.{suffix}"
        url = (
            "https://github.com/gitleaks/gitleaks/releases/download/"
            f"v{GITLEAKS_VERSION}/{asset}"
        )
        with tempfile.TemporaryDirectory(prefix="resonance-gitleaks-") as directory:
            archive = Path(directory) / asset
            urllib.request.urlretrieve(url, archive)
            actual = hashlib.sha256(archive.read_bytes()).hexdigest()
            if actual != SHA256[key]:
                raise RuntimeError(f"checksum mismatch for {asset}")
            member = "gitleaks.exe" if IS_WINDOWS else "gitleaks"
            if suffix == "zip":
                with zipfile.ZipFile(archive) as bundle:
                    data = bundle.read(member)
            else:
                with tarfile.open(archive) as bundle:
                    extracted = bundle.extractfile(member)
                    if extracted is None:
                        raise RuntimeError(f"{member} is missing from the release archive")
                    data = extracted.read()
            BINARY.parent.mkdir(parents=True, exist_ok=True)
            BINARY.write_bytes(data)
            BINARY.chmod(0o755)
        if installed_version() != GITLEAKS_VERSION:
            raise RuntimeError("installed binary did not report the pinned version")
    except (OSError, RuntimeError, tarfile.TarError, zipfile.BadZipFile) as error:
        print(f"FAIL: unable to install Gitleaks {GITLEAKS_VERSION}: {error}")
        return 1
    print(f"PASS: installed Gitleaks {GITLEAKS_VERSION} with a verified SHA-256")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
