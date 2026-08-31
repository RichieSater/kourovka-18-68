#!/usr/bin/env python3
"""Verify an artifact SHA-256 sidecar against regular adjacent files."""

from __future__ import annotations

import argparse
import hashlib
import re
import stat
from pathlib import Path
from typing import NoReturn


def fail(message: str) -> NoReturn:
    raise RuntimeError(f"artifact sidecar check failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file(path: Path) -> None:
    require(not path.is_symlink(), f"symbolic link is not allowed: {path}")
    try:
        mode = path.stat().st_mode
    except OSError as error:
        fail(f"could not inspect {path}: {error}")
    require(stat.S_ISREG(mode), f"artifact is not a regular file: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sidecar", type=Path)
    parser.add_argument("artifacts", nargs="+", type=Path)
    args = parser.parse_args()

    sidecar = args.sidecar.resolve()
    regular_file(sidecar)
    artifacts = [path.resolve() for path in args.artifacts]
    require(len(artifacts) == len(set(artifacts)), "duplicate artifact argument")
    require(all(path.parent == sidecar.parent for path in artifacts),
            "all artifacts must be adjacent to the sidecar")
    for artifact in artifacts:
        regular_file(artifact)

    entries: dict[str, str] = {}
    pattern = re.compile(r"([0-9a-f]{64})  ([A-Za-z0-9][A-Za-z0-9._-]*)")
    try:
        lines = sidecar.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        fail(f"could not read sidecar: {error}")
    require(lines, "sidecar is empty")
    for line in lines:
        match = pattern.fullmatch(line)
        require(match is not None, "malformed sidecar entry")
        digest, name = match.groups()
        require(name not in entries, f"duplicate sidecar artifact: {name}")
        entries[name] = digest

    expected_names = sorted(path.name for path in artifacts)
    require(list(entries) == expected_names, "sidecar inventory or ordering")
    by_name = {path.name: path for path in artifacts}
    for name, digest in entries.items():
        require(sha256(by_name[name]) == digest, f"sidecar digest mismatch: {name}")
    print(f"ARTIFACT SIDECAR PASSED: {sidecar.name} ({len(entries)} files)")


if __name__ == "__main__":
    main()
