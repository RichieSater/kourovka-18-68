#!/usr/bin/env python3
"""Check internal completeness and consistency of the generated TomLib TSVs."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "tomlib-cmp-scan.tsv"
MAXIMALS = ROOT / "data" / "tomlib-cmp-maximals.tsv"
EXPECTED_SHA256 = {
    SUMMARY: "e8057a728dca589e6c431cc9779ce02b37f8a5daac83a0be879e98ba8bc6f9b4",
    MAXIMALS: "adbd9590e769136eab7fea84139de0bec2f068252a68228e454066cc7f473c55",
}


def read_tsv(path: Path) -> tuple[dict[str, str], list[dict[str, str]]]:
    metadata: dict[str, str] = {}
    data_lines: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            key, value = line[2:].split("\t", 1)
            metadata[key] = value
        else:
            data_lines.append(line)
    return metadata, list(csv.DictReader(data_lines, delimiter="\t"))


def parse_bool(value: str) -> bool:
    if value not in {"true", "false"}:
        raise AssertionError(f"invalid GAP boolean {value!r}")
    return value == "true"


def parse_candidates(value: str) -> dict[int, int]:
    if value == "none":
        return {}
    result: dict[int, int] = {}
    for item in value.split(","):
        class_position, multiplicity = map(int, item.split(":"))
        assert class_position > 0
        assert multiplicity >= 0
        assert class_position not in result
        result[class_position] = multiplicity
    return result


def main() -> None:
    for path, expected in EXPECTED_SHA256.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected

    summary_metadata, summaries = read_tsv(SUMMARY)
    maximal_metadata, maximals = read_tsv(MAXIMALS)

    assert summary_metadata["producer"] == "gap -q gap/generate-tomlib-scan.g"
    assert maximal_metadata["producer"] == summary_metadata["producer"]
    assert summary_metadata["gap_version"] == maximal_metadata["gap_version"]
    assert summary_metadata["tomlib_version"] == maximal_metadata["tomlib_version"]
    assert len(summaries) == 414
    assert len({row["table_name"] for row in summaries}) == 414

    by_name: dict[str, list[dict[str, str]]] = {}
    for row in maximals:
        by_name.setdefault(row["table_name"], []).append(row)
        candidates = parse_candidates(row["candidates"])
        complemented = parse_bool(row["complemented"])
        witness = (
            int(row["witness_class"])
            if row["witness_class"] != "none"
            else None
        )
        assert int(row["group_order"]) == (
            int(row["maximal_order"]) * int(row["index"])
        )
        if complemented:
            assert witness is not None
            assert candidates[witness] > 0
        else:
            assert witness is None
            assert not any(candidates.values())

    summary_by_name = {row["table_name"]: row for row in summaries}
    assert set(by_name) == set(summary_by_name)
    for name, summary in summary_by_name.items():
        rows = by_name[name]
        assert len(rows) == int(summary["maximal_classes"])
        failed = [
            int(row["maximal_class"])
            for row in rows
            if not parse_bool(row["complemented"])
        ]
        recorded = (
            [int(value) for value in summary["failed_maximal_classes"].split(",")]
            if summary["failed_maximal_classes"] != "none"
            else []
        )
        assert failed == recorded
        assert parse_bool(summary["cmp"]) == (not failed)
        if parse_bool(summary["cmp"]):
            assert summary["solvable"] in {"true", "false"}
            chief_orders = [
                int(value)
                for value in summary["chief_factor_orders"].split(",")
            ]
            product = 1
            for value in chief_orders:
                product *= value
            assert product == int(summary["group_order"])
        else:
            assert summary["solvable"] == "fail"
            assert summary["chief_factor_orders"] == "not_computed"

    expected = {
        "L2(7)": True,
        "L2(11)": True,
        "L5(2)": True,
        "A5": False,
        "S5": False,
        "L2(7).2": False,
        "(A5xA5):2": False,
    }
    for name, status in expected.items():
        assert parse_bool(summary_by_name[name]["cmp"]) is status

    positive_simple = {
        row["table_name"]
        for row in summaries
        if parse_bool(row["nonabelian_simple"]) and parse_bool(row["cmp"])
    }
    assert positive_simple == {"L2(7)", "L2(11)", "L5(2)"}
    assert sum(parse_bool(row["cmp"]) for row in summaries) == 73

    def is_prime_power(number: int) -> bool:
        prime = next((p for p in range(2, number + 1) if number % p == 0), None)
        assert prime is not None
        while number % prime == 0:
            number //= prime
        return number == 1

    positive_nonabelian_chief_orders = {
        factor
        for row in summaries
        if parse_bool(row["cmp"])
        for factor in map(int, row["chief_factor_orders"].split(","))
        if not is_prime_power(factor)
    }
    assert positive_nonabelian_chief_orders == {168, 660, 9_999_360}

    print(
        "TOMLIB TSV CHECK PASSED: "
        f"{len(summaries)} tables, {len(maximals)} maximal classes, "
        "73 CMP-positive tables"
    )


if __name__ == "__main__":
    main()
