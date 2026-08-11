#!/usr/bin/env python3
"""Check the pinned finite factor-free Table-of-Marks certificate."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tomlib-factor-free.tsv"

# Filled after regeneration; changing this requires an intentional certificate
# update and a rerun of the GAP producer above.
EXPECTED_SHA256 = "82bcf695617014f0124839c5a01983a6c8904fc5bc92e0893c9c2601c43bd3a0"

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


def read() -> tuple[dict[str, str], list[dict[str, str]]]:
    metadata: dict[str, str] = {}
    body: list[str] = []
    for line in DATA.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            key, value = line[2:].split("\t", 1)
            metadata[key] = value
        else:
            body.append(line)
    return metadata, list(csv.DictReader(body, delimiter="\t"))


def main() -> None:
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == EXPECTED_SHA256
    metadata, rows = read()
    assert metadata == {
        "producer": "gap -q gap/generate-factor-free-scan.g",
        "gap_version": "4.15.1",
        "tomlib_version": "1.2.11",
    }
    assert len(rows) == len(EXPECTED)
    assert {row["table_name"] for row in rows} == set(EXPECTED)

    for row in rows:
        name = row["table_name"]
        maximal_order, index, scope = EXPECTED[name]
        assert int(row["maximal_order"]) == maximal_order
        assert int(row["index"]) == index
        assert int(row["group_order"]) == maximal_order * index
        assert int(row["socle_order"]) > 1
        assert int(row["socle_order"]) <= int(row["group_order"])
        assert int(row["socle_intersection_order"]) == (
            maximal_order
            * int(row["socle_order"])
            // int(row["group_order"])
        )
        assert int(row["socle_intersection_order"]) > 1
        assert int(row["maximal_class"]) > 0
        assert int(row["socle_class"]) > 0
        assert row["scope"] == scope
        assert row["corefree_factor_count"] == "0"
        assert row["factor_free"] == "true"

    print(f"FACTOR-FREE TSV CHECK PASSED: {len(rows)} pinned maximal classes")


if __name__ == "__main__":
    main()
