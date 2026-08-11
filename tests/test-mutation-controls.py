#!/usr/bin/env python3
"""Negative controls for certificates, release receipts, and stale producers."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> NoReturn:
    raise RuntimeError(f"mutation control failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def require_success(command: list[str], cwd: Path, context: str) -> None:
    result = run(command, cwd)
    require(result.returncode == 0, f"{context} baseline failed:\n{result.stdout}")


def require_failure(command: list[str], cwd: Path, context: str) -> None:
    result = run(command, cwd)
    require(result.returncode != 0, f"{context} mutation was accepted")


def certificate_controls(tmp: Path) -> int:
    (tmp / "tests").mkdir()
    (tmp / "data").mkdir()
    checkers = ["check-tomlib-scan.py", "check-factor-free-scan.py"]
    data_files = [
        "tomlib-cmp-scan.tsv",
        "tomlib-cmp-maximals.tsv",
        "tomlib-factor-free.tsv",
    ]
    for name in checkers:
        shutil.copy2(ROOT / "tests" / name, tmp / "tests" / name)
    for name in data_files:
        shutil.copy2(ROOT / "data" / name, tmp / "data" / name)

    for checker in checkers:
        require_success(["python3", "-O", f"tests/{checker}"], tmp, checker)

    factor = tmp / "data" / "tomlib-factor-free.tsv"
    original_factor = factor.read_bytes()
    factor.write_bytes(original_factor + b"# deliberate mutation\n")
    require_failure(
        ["python3", "-O", "tests/check-factor-free-scan.py"],
        tmp,
        "factor-free byte mutation",
    )
    factor.write_bytes(original_factor)
    factor.unlink()
    require_failure(
        ["python3", "-O", "tests/check-factor-free-scan.py"],
        tmp,
        "missing factor-free certificate",
    )

    summary = tmp / "data" / "tomlib-cmp-scan.tsv"
    original_summary = summary.read_bytes()
    summary.write_bytes(original_summary.replace(b"\t73\t", b"\t74\t", 1))
    if summary.read_bytes() == original_summary:
        summary.write_bytes(original_summary + b"# deliberate mutation\n")
    require_failure(
        ["python3", "-O", "tests/check-tomlib-scan.py"],
        tmp,
        "CMP summary mutation",
    )
    return 3


def release_controls(tmp: Path) -> int:
    (tmp / "scripts").mkdir()
    (tmp / "paper").mkdir()
    shutil.copy2(ROOT / "scripts" / "check-release.py", tmp / "scripts")
    for name in ["kourovka-18-68.pdf", "BUILD-RECEIPT.txt"]:
        shutil.copy2(ROOT / "paper" / name, tmp / "paper" / name)

    command = ["python3", "-O", "scripts/check-release.py"]
    require_success(command, tmp, "release checker")

    receipt = tmp / "paper" / "BUILD-RECEIPT.txt"
    original_receipt = receipt.read_text(encoding="utf-8")
    receipt.write_text(
        original_receipt.replace("deterministic_mode=true", "deterministic_mode=false"),
        encoding="utf-8",
    )
    require_failure(command, tmp, "receipt-field mutation")
    receipt.write_text(original_receipt, encoding="utf-8")

    pdf = tmp / "paper" / "kourovka-18-68.pdf"
    pdf.write_bytes(pdf.read_bytes() + b"deliberate mutation")
    require_failure(command, tmp, "PDF mutation")
    return 2


def producer_controls(tmp: Path) -> int:
    (tmp / "gap").mkdir()
    (tmp / "data").mkdir()
    files = [
        "factor_free_tom.g",
        "cmp_tom.g",
        "generate-factor-free-scan.g",
        "generate-tomlib-scan.g",
    ]
    for name in files:
        shutil.copy2(ROOT / "gap" / name, tmp / "gap" / name)
    for name in [
        "tomlib-factor-free.tsv",
        "tomlib-cmp-scan.tsv",
        "tomlib-cmp-maximals.tsv",
    ]:
        shutil.copy2(ROOT / "data" / name, tmp / "data" / name)

    for script, stale_outputs in [
        ("generate-factor-free-scan.g", ["tomlib-factor-free.tsv"]),
        (
            "generate-tomlib-scan.g",
            ["tomlib-cmp-scan.tsv", "tomlib-cmp-maximals.tsv"],
        ),
    ]:
        path = tmp / "gap" / script
        source = path.read_text(encoding="utf-8")
        mutated = source.replace(
            'GAPInfo.Version <> "4.15.1"',
            'GAPInfo.Version <> "0.0.0"',
            1,
        )
        require(mutated != source, f"could not inject version failure in {script}")
        path.write_text(mutated, encoding="utf-8")
        require_failure(
            ["gap", "--quitonbreak", "-q", f"gap/{script}"],
            tmp,
            f"{script} forced version failure",
        )
        for output in stale_outputs:
            require(
                not (tmp / "data" / output).exists(),
                f"{script} left stale {output} after failure",
            )
    return 2


def main() -> None:
    total = 0
    with tempfile.TemporaryDirectory(prefix="k186-cert-mutation-") as directory:
        total += certificate_controls(Path(directory))
    with tempfile.TemporaryDirectory(prefix="k186-release-mutation-") as directory:
        total += release_controls(Path(directory))
    with tempfile.TemporaryDirectory(prefix="k186-producer-mutation-") as directory:
        total += producer_controls(Path(directory))
    print(f"MUTATION CONTROLS PASSED: {total} deliberate failures rejected")


if __name__ == "__main__":
    main()
