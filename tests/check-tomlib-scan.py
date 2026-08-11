#!/usr/bin/env python3
"""Fail-closed consistency checks for the generated TomLib CMP TSVs."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import NoReturn, cast


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "tomlib-cmp-scan.tsv"
MAXIMALS = ROOT / "data" / "tomlib-cmp-maximals.tsv"
EXPECTED_SHA256 = {
    SUMMARY: "318ac4d55cde05e3e046497eba31b005ebe16832d1be59df98b5e48f9b951320",
    MAXIMALS: "ed322a51f286f104c4adc057c0b06a6cdbf8c3300f71e9bab8d6950071882b16",
}


def fail(message: str) -> NoReturn:
    raise RuntimeError(f"TomLib CMP certificate check failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_tsv(path: Path) -> tuple[dict[str, str], list[dict[str, str]]]:
    require(path.is_file(), f"missing data file {path}")
    metadata: dict[str, str] = {}
    data_lines: list[str] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if line.startswith("# "):
            fields = line[2:].split("\t", 1)
            require(
                len(fields) == 2,
                f"{path.name}:{line_number}: malformed metadata",
            )
            key, value = fields
            require(key not in metadata, f"{path.name}: duplicate metadata {key!r}")
            metadata[key] = value
        else:
            data_lines.append(line)
    require(bool(data_lines), f"{path.name}: empty TSV body")
    rows = list(csv.DictReader(data_lines, delimiter="\t"))
    require(bool(rows), f"{path.name}: no parsed rows")
    return metadata, rows


def parse_bool(value: str, context: str) -> bool:
    require(value in {"true", "false"}, f"{context}: invalid GAP boolean {value!r}")
    return value == "true"


def parse_candidates(value: str, context: str) -> dict[int, int]:
    if value == "none":
        return {}
    result: dict[int, int] = {}
    for item in value.split(","):
        fields = item.split(":")
        require(len(fields) == 2, f"{context}: malformed candidate {item!r}")
        class_position, multiplicity = map(int, fields)
        require(class_position > 0, f"{context}: nonpositive class position")
        require(multiplicity >= 0, f"{context}: negative multiplicity")
        require(class_position not in result, f"{context}: duplicate candidate")
        result[class_position] = multiplicity
    return result


def main() -> None:
    for path, expected in EXPECTED_SHA256.items():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected, f"{path.name}: SHA-256 {digest} != {expected}")

    summary_metadata, summaries = read_tsv(SUMMARY)
    maximal_metadata, maximals = read_tsv(MAXIMALS)

    producer = "gap --quitonbreak -q gap/generate-tomlib-scan.g"
    require(summary_metadata.get("producer") == producer, "summary producer metadata")
    require(maximal_metadata.get("producer") == producer, "maximal producer metadata")
    require(
        summary_metadata.get("gap_version") == maximal_metadata.get("gap_version") == "4.15.1",
        "GAP version metadata",
    )
    require(
        summary_metadata.get("tomlib_version")
        == maximal_metadata.get("tomlib_version")
        == "1.2.11",
        "TomLib version metadata",
    )
    require(len(summaries) == 414, f"expected 414 summaries, got {len(summaries)}")
    require(
        len({row["table_name"] for row in summaries}) == 414,
        "summary table names are not unique",
    )

    by_name: dict[str, list[dict[str, str]]] = {}
    for row_number, row in enumerate(maximals, start=1):
        name = row["table_name"]
        context = f"maximal row {row_number} ({name})"
        by_name.setdefault(name, []).append(row)
        candidates = parse_candidates(row["candidates"], context)
        complemented = parse_bool(row["complemented"], context)
        witness = int(row["witness_class"]) if row["witness_class"] != "none" else None
        require(
            int(row["group_order"])
            == int(row["maximal_order"]) * int(row["index"]),
            f"{context}: order arithmetic",
        )
        if complemented:
            require(witness is not None, f"{context}: missing witness")
            require(witness in candidates, f"{context}: unlisted witness")
            require(candidates[witness] > 0, f"{context}: zero witness multiplicity")
        else:
            require(witness is None, f"{context}: unexpected witness")
            require(not any(candidates.values()), f"{context}: positive hidden witness")

    summary_by_name = {row["table_name"]: row for row in summaries}
    require(set(by_name) == set(summary_by_name), "summary/maximal name sets differ")
    for name, summary in summary_by_name.items():
        context = f"summary {name}"
        rows = by_name[name]
        require(
            len(rows) == int(summary["maximal_classes"]),
            f"{context}: maximal-row count",
        )
        failed = [
            int(row["maximal_class"])
            for row in rows
            if not parse_bool(row["complemented"], context)
        ]
        recorded = (
            [int(value) for value in summary["failed_maximal_classes"].split(",")]
            if summary["failed_maximal_classes"] != "none"
            else []
        )
        require(failed == recorded, f"{context}: failed-class list")
        cmp_value = parse_bool(summary["cmp"], context)
        require(cmp_value == (not failed), f"{context}: CMP flag")
        if cmp_value:
            require(summary["solvable"] in {"true", "false"}, f"{context}: solvable flag")
            chief_orders = [
                int(value) for value in summary["chief_factor_orders"].split(",")
            ]
            require(bool(chief_orders), f"{context}: missing chief factors")
            product = 1
            for value in chief_orders:
                require(value > 1, f"{context}: invalid chief-factor order")
                product *= value
            require(product == int(summary["group_order"]), f"{context}: chief product")
        else:
            require(summary["solvable"] == "fail", f"{context}: negative solvable marker")
            require(
                summary["chief_factor_orders"] == "not_computed",
                f"{context}: negative chief marker",
            )

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
        require(name in summary_by_name, f"missing fixture {name}")
        require(
            parse_bool(summary_by_name[name]["cmp"], f"fixture {name}") is status,
            f"fixture {name}: unexpected CMP status",
        )

    positive_simple = {
        row["table_name"]
        for row in summaries
        if parse_bool(row["nonabelian_simple"], row["table_name"])
        and parse_bool(row["cmp"], row["table_name"])
    }
    require(
        positive_simple == {"L2(7)", "L2(11)", "L5(2)"},
        f"positive simple set changed: {positive_simple}",
    )
    positive_count = sum(parse_bool(row["cmp"], row["table_name"]) for row in summaries)
    require(positive_count == 73, f"expected 73 positive tables, got {positive_count}")

    def is_prime_power(number: int) -> bool:
        require(number > 1, f"invalid factor order {number}")
        prime = next((p for p in range(2, number + 1) if number % p == 0), None)
        require(prime is not None, f"no prime divisor found for {number}")
        prime = cast(int, prime)
        while number % prime == 0:
            number //= prime
        return number == 1

    positive_nonabelian_chief_orders = {
        factor
        for row in summaries
        if parse_bool(row["cmp"], row["table_name"])
        for factor in map(int, row["chief_factor_orders"].split(","))
        if not is_prime_power(factor)
    }
    require(
        positive_nonabelian_chief_orders == {168, 660, 9_999_360},
        f"chief-factor spectrum changed: {positive_nonabelian_chief_orders}",
    )

    print(
        "TOMLIB TSV CHECK PASSED: "
        f"{len(summaries)} tables, {len(maximals)} maximal classes, "
        "73 CMP-positive tables"
    )


if __name__ == "__main__":
    main()
