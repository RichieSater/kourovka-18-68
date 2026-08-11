#!/usr/bin/env python3
"""Fail-closed checks for the finite factor-free TomLib certificate."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import NoReturn


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tomlib-factor-free.tsv"

# Updated only after an intentional regeneration under the pinned producer.
EXPECTED_SHA256 = "9b131720d41ef945a0696794c0493ae9c07e166d4d1f37b054a1d55f0c4837ae"

EXPECTED = {
    "A6.2_2": (16, 45, "alternating-small"),
    "A6.2_3": (20, 36, "alternating-small"),
    "A6.2^2": (32, 45, "alternating-small"),
    "A7": (72, 35, "alternating-small"),
    "S7": (144, 35, "alternating-small"),
    "L3(4)": (960, 21, "linear-small"),
    "L3(4).2_1": (384, 105, "linear-small"),
    "L3(4).2_2": (1920, 21, "linear-small"),
    "L3(4).2_3": (720, 56, "linear-small"),
    "L3(4).3": (216, 280, "linear-small"),
    "L3(4).2^2": (768, 105, "linear-small"),
    "L3(4).3.2_2": (432, 280, "linear-small"),
    "L3(4).3.2_3": (1152, 105, "linear-small"),
    "L3(4).6": (1152, 105, "linear-small"),
    "L3(4).D12": (2304, 105, "linear-small"),
    "M11": (120, 66, "sporadic-cross-check"),
    "M12": (192, 495, "sporadic-cross-check"),
    "M12.2": (216, 880, "sporadic-cross-check"),
    "M22.2": (1440, 616, "sporadic-cross-check"),
    "M23": (20160, 506, "sporadic-cross-check"),
    "J2": (2160, 280, "sporadic-cross-check"),
    "J2.2": (4320, 280, "sporadic-cross-check"),
    "HS": (40320, 1100, "sporadic-cross-check"),
    "HS.2": (80640, 1100, "sporadic-cross-check"),
}


def fail(message: str) -> NoReturn:
    raise RuntimeError(f"factor-free certificate check failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read() -> tuple[dict[str, str], list[dict[str, str]]]:
    require(DATA.is_file(), f"missing data file {DATA}")
    metadata: dict[str, str] = {}
    body: list[str] = []
    for line_number, line in enumerate(
        DATA.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if line.startswith("# "):
            fields = line[2:].split("\t", 1)
            require(len(fields) == 2, f"malformed metadata at line {line_number}")
            key, value = fields
            require(key not in metadata, f"duplicate metadata key {key!r}")
            metadata[key] = value
        else:
            body.append(line)
    require(bool(body), "TSV body is empty")
    return metadata, list(csv.DictReader(body, delimiter="\t"))


def main() -> None:
    digest = hashlib.sha256(DATA.read_bytes()).hexdigest()
    require(digest == EXPECTED_SHA256, f"SHA-256 {digest} != {EXPECTED_SHA256}")

    metadata, rows = read()
    expected_metadata = {
        "producer": "gap --quitonbreak -q gap/generate-factor-free-scan.g",
        "gap_version": "4.15.1",
        "tomlib_version": "1.2.11",
    }
    require(metadata == expected_metadata, f"metadata mismatch: {metadata!r}")
    require(len(rows) == len(EXPECTED), f"expected {len(EXPECTED)} rows, got {len(rows)}")
    names = {row.get("table_name", "") for row in rows}
    require(names == set(EXPECTED), "table-name set changed")

    for row_number, row in enumerate(rows, start=1):
        name = row["table_name"]
        maximal_order, index, scope = EXPECTED[name]
        prefix = f"row {row_number} ({name})"
        require(int(row["maximal_order"]) == maximal_order, f"{prefix}: maximal order")
        require(int(row["index"]) == index, f"{prefix}: index")
        require(
            int(row["group_order"]) == maximal_order * index,
            f"{prefix}: group order arithmetic",
        )
        socle_order = int(row["socle_order"])
        group_order = int(row["group_order"])
        require(1 < socle_order <= group_order, f"{prefix}: invalid socle order")
        expected_intersection = maximal_order * socle_order // group_order
        require(
            int(row["socle_intersection_order"]) == expected_intersection,
            f"{prefix}: socle intersection formula",
        )
        require(expected_intersection > 1, f"{prefix}: trivial socle intersection")
        require(int(row["maximal_class"]) > 0, f"{prefix}: maximal class")
        require(int(row["socle_class"]) > 0, f"{prefix}: socle class")
        require(row["scope"] == scope, f"{prefix}: scope")
        require(row["corefree_factor_count"] == "0", f"{prefix}: factor count")
        require(row["factor_free"] == "true", f"{prefix}: factor-free flag")

    print(f"FACTOR-FREE TSV CHECK PASSED: {len(rows)} pinned maximal classes")


if __name__ == "__main__":
    main()
