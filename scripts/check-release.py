#!/usr/bin/env python3
"""Check the deterministic paper receipt and release-facing invariants."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "paper" / "kourovka-18-68.pdf"
RECEIPT = ROOT / "paper" / "BUILD-RECEIPT.txt"


def fail(message: str) -> NoReturn:
    raise RuntimeError(f"release check failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    require(PDF.is_file(), f"missing {PDF}")
    require(RECEIPT.is_file(), f"missing {RECEIPT}")
    fields: dict[str, str] = {}
    for number, line in enumerate(RECEIPT.read_text(encoding="utf-8").splitlines(), 1):
        parts = line.split("=", 1)
        require(len(parts) == 2, f"malformed receipt line {number}")
        key, value = parts
        require(key not in fields, f"duplicate receipt key {key}")
        fields[key] = value
    expected_fixed = {
        "artifact": "paper/kourovka-18-68.pdf",
        "tectonic_version": "0.17.0",
        "bundle_url": "https://relay.fullyjustified.net/default_bundle_v33.tar",
        "bundle_content_sha256": "6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c",
        "source_date_epoch": "1786406400",
        "timezone": "UTC",
        "deterministic_mode": "true",
        "clean_builds_compared": "2",
    }
    for key, value in expected_fixed.items():
        require(fields.get(key) == value, f"receipt field {key}")
    digest = hashlib.sha256(PDF.read_bytes()).hexdigest()
    require(fields.get("pdf_sha256") == digest, "PDF hash does not match receipt")
    require(len(fields) == len(expected_fixed) + 1, "unexpected receipt fields")
    print(f"RELEASE RECEIPT PASSED: {digest}")


if __name__ == "__main__":
    main()
