#!/usr/bin/env python3
"""Negative controls for certificates, artifacts, producers, and public text."""

from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Callable, NoReturn

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
    (tmp / ".github" / "workflows").mkdir(parents=True)
    shutil.copy2(ROOT / "scripts" / "check-release.py", tmp / "scripts")
    for name in ["kourovka-18-68.pdf", "kourovka-18-68.tex", "BUILD-RECEIPT.txt"]:
        shutil.copy2(ROOT / "paper" / name, tmp / "paper" / name)
    for name in [
        "artifact-metadata.json", "CITATION.cff", "README.md",
        "REPRODUCIBILITY.md", "RELEASE-NOTES-v1.1.0.md",
    ]:
        shutil.copy2(ROOT / name, tmp / name)
    shutil.copy2(ROOT / "paper" / "README.md", tmp / "paper" / "README.md")
    shutil.copy2(
        ROOT / ".github" / "workflows" / "release-check.yml",
        tmp / ".github" / "workflows" / "release-check.yml",
    )

    command = ["python3", "-O", "scripts/check-release.py"]
    require_success(command, tmp, "artifact checker")

    receipt = tmp / "paper" / "BUILD-RECEIPT.txt"
    original_receipt = receipt.read_text(encoding="utf-8")
    receipt.write_text(
        original_receipt.replace("deterministic_mode=true", "deterministic_mode=false"),
        encoding="utf-8",
    )
    require_failure(command, tmp, "receipt-field mutation")
    receipt.write_text(original_receipt, encoding="utf-8")

    pdf = tmp / "paper" / "kourovka-18-68.pdf"
    original_pdf = pdf.read_bytes()
    pdf.write_bytes(original_pdf + b"deliberate mutation")
    require_failure(command, tmp, "PDF mutation")
    pdf.write_bytes(original_pdf)

    tex = tmp / "paper" / "kourovka-18-68.tex"
    original_tex = tex.read_bytes()
    tex.write_bytes(original_tex + b"% deliberate mutation\n")
    require_failure(command, tmp, "TeX/PDF staleness mutation")
    tex.write_bytes(original_tex)

    metadata_path = tmp / "artifact-metadata.json"
    original_metadata = metadata_path.read_text(encoding="utf-8")
    metadata = json.loads(original_metadata)
    metadata["manuscript_date"] = "2039-01-01"
    metadata["artifact_version"] = "9.9.9"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    require_failure(command, tmp, "authoritative-metadata mutation")
    metadata_path.write_text(original_metadata, encoding="utf-8")

    citation = tmp / "CITATION.cff"
    original_citation = citation.read_text(encoding="utf-8")
    citation.write_text(original_citation + "version: 9.9.9\n", encoding="utf-8")
    require_failure(command, tmp, "citation-version mutation")
    citation.write_text(original_citation, encoding="utf-8")

    citation.write_text(
        original_citation.replace("family-names: Sater", "family-names: Wrong", 1),
        encoding="utf-8",
    )
    require_failure(command, tmp, "citation-author mutation")
    citation.write_text(
        original_citation.replace("year: 2026", "year: 2039", 1),
        encoding="utf-8",
    )
    require_failure(command, tmp, "citation-year mutation")
    citation.write_text("cff-version: [\n", encoding="utf-8")
    require_failure(command, tmp, "malformed-citation mutation")
    citation.write_text(original_citation, encoding="utf-8")

    deposition = tmp / ".zenodo.json"
    deposition.write_text(
        '{"version":"9.9.9","publication_date":"2039-01-01"}\n',
        encoding="utf-8",
    )
    require_failure(command, tmp, "unsupported-deposition-metadata mutation")
    deposition.unlink()

    workflow = tmp / ".github" / "workflows" / "release-check.yml"
    original_workflow = workflow.read_text(encoding="utf-8")
    workflow.write_text(
        original_workflow.replace("make GAP=gap release-check", "make release-check"),
        encoding="utf-8",
    )
    require_failure(command, tmp, "CI GAP override mutation")
    workflow.write_text(
        original_workflow.replace(
            "run: make GAP=gap release-check",
            "run: echo 'make GAP=gap release-check'",
        ),
        encoding="utf-8",
    )
    require_failure(command, tmp, "CI echo-command mutation")

    reproducibility = tmp / "REPRODUCIBILITY.md"
    original_reproducibility = reproducibility.read_text(encoding="utf-8")
    reproducibility.write_text(
        original_reproducibility.replace("1788134400", "1787961600"),
        encoding="utf-8",
    )
    require_failure(command, tmp, "documented-epoch mutation")
    return 12


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


def manifest_bytes(
    contents: dict[str, bytes],
    modes: dict[str, str],
    *,
    snapshot_kind: str,
    source_commit: str,
) -> bytes:
    metadata = json.loads(contents["artifact-metadata.json"])
    lines = [
        "schema_version=1",
        "publication_status=preprint",
        f"source_date_epoch={metadata['source_date_epoch']}",
        f"snapshot_kind={snapshot_kind}",
        f"source_commit={source_commit}",
        "hash_algorithm=SHA-256",
        "entry_format=sha256 git-mode path",
        "",
    ]
    for name in sorted(contents):
        lines.append(f"{hashlib.sha256(contents[name]).hexdigest()}  {modes[name]}  {name}")
    lines.append("")
    return "\n".join(lines).encode("utf-8")


def write_archive(
    archive: Path,
    contents: dict[str, bytes],
    *,
    corrupt_manifest: bool = False,
    link_name: str | None = None,
    root: str = "kourovka-18-68-preprint-working-tree",
    snapshot_kind: str = "working-tree",
    source_commit: str = "none",
) -> None:
    epoch = 1787961600
    modes = {name: "100644" for name in contents}
    manifest = manifest_bytes(
        contents,
        modes,
        snapshot_kind=snapshot_kind,
        source_commit=source_commit,
    )
    if corrupt_manifest:
        lines = manifest.decode("utf-8").splitlines()
        for index, line in enumerate(lines):
            if "  100" not in line:
                continue
            replacement = "0" if line[0] != "0" else "1"
            lines[index] = replacement + line[1:]
        manifest = ("\n".join(lines) + "\n").encode("utf-8")
    with tarfile.open(archive, "w:gz") as handle:
        directories = {root}
        for name in contents:
            path = Path(name)
            for parent in path.parents:
                if parent != Path("."):
                    directories.add(f"{root}/{parent.as_posix()}")
        for name in sorted(directories, key=lambda item: (item.count("/"), item)):
            info = tarfile.TarInfo(name + "/")
            info.type = tarfile.DIRTYPE
            info.mode = 0o755
            info.mtime = epoch
            handle.addfile(info)
        for name, data in sorted(contents.items()):
            info = tarfile.TarInfo(f"{root}/{name}")
            info.size = len(data)
            info.mode = 0o644
            info.mtime = epoch
            handle.addfile(info, io.BytesIO(data))
        info = tarfile.TarInfo(f"{root}/SOURCE-MANIFEST.txt")
        info.size = len(manifest)
        info.mode = 0o644
        info.mtime = epoch
        handle.addfile(info, io.BytesIO(manifest))
        if link_name is not None:
            info = tarfile.TarInfo(f"{root}/{link_name}")
            info.type = tarfile.SYMTYPE
            info.linkname = "README.md"
            info.mode = 0o777
            info.mtime = epoch
            handle.addfile(info)


def public_corpus_controls(tmp: Path) -> int:
    (tmp / "scripts").mkdir()
    (tmp / "paper").mkdir()
    shutil.copy2(
        ROOT / "scripts" / "check-public-corpus.py",
        tmp / "scripts" / "check-public-corpus.py",
    )

    heading = "\\section*{" + "Gen" + "erative-" + "A" + "I disclosure}"
    body = (
        "Gen" + "erative-" + "A" + "I tools " + "were used for literature search, "
        "proof exploration, code generation, drafting, and critical checking; the author "
        "checked and takes responsibility for the manuscript's arguments, citations, and "
        "computations."
    )
    principal = tmp / "paper" / "kourovka-18-68.tex"
    bibliography = "\\begin{" + "thebibliography}{99}"
    principal.write_text(
        heading + "\n" + body + "\n\n" + bibliography + "\n",
        encoding="utf-8",
    )
    readme = tmp / "README.md"
    baseline = (
        "# Public corpus\n\n"
        "Concrete mathematical status only.\n"
        "Readers can reconstruct the calculation from the certificate.\n"
        "Experts often call this action primitive.\n"
        "The board automorphism interchanges two nodes.\n"
        "A human-readable table records the output.\n"
        "Correct index: $\\lvert N_{\\Aut(S)}(H):M_{12}.2\\rvert$.\n"
    )
    readme.write_text(baseline, encoding="utf-8")

    require_success(["git", "init", "-q"], tmp, "corpus Git initialization")
    require_success(["git", "config", "user.name", "Richie Sater"], tmp,
                    "corpus Git author name")
    require_success(
        ["git", "config", "user.email", "15129476+RichieSater@users.noreply.github.com"],
        tmp,
        "corpus Git author email",
    )
    require_success(["git", "add", "."], tmp, "corpus Git inventory")
    command = ["python3", "-O", "scripts/check-public-corpus.py"]
    require_success(command, tmp, "public-corpus checker")
    require_success(
        ["git", "commit", "-q", "-m", "Publish concrete mathematical corpus"],
        tmp,
        "corpus commit baseline",
    )
    require_success(command, tmp, "committed public-corpus checker")
    bad_subject = (
        "Prepare final peer-"
        + "revi"
        + "ew submission"
    )
    require_success(
        ["git", "commit", "-q", "--allow-empty", "-m", bad_subject],
        tmp,
        "commit-subject mutation inventory",
    )
    require_failure(command, tmp, "commit-subject mutation")
    require_success(["git", "reset", "-q", "--hard", "HEAD^"], tmp,
                    "commit-subject mutation reset")

    mutations = [
        ("Internal adversarial " + "revi" + "ew passed.\n", "process mutation 1"),
        ("Vali" + "dation is assi" + "gned to Alice.\n", "assignment mutation"),
        (
            "Alice is assi" + "gned the final proof check.\n",
            "named proof-assignment mutation",
        ),
        ("Rele" + "ase requires " + "sign" + "-off.\n", "condition mutation 1"),
        ("Independent peer " + "revi" + "ew is pending.\n", "process mutation 2"),
        ("Gen" + "erative tooling revised the prose.\n", "disclosure mutation 1"),
        ("Artificial intel" + "ligence revised the prose.\n", "disclosure mutation 2"),
        ("A language mod" + "el revised the prose.\n", "disclosure mutation 3"),
        ("L" + "LM output was used.\n", "disclosure mutation 4"),
        ("Chat" + "GPT edited the text.\n", "disclosure mutation 5"),
        ("Cod" + "ex edited the text.\n", "disclosure mutation 6"),
        ("A" + "I was used for editing.\n", "disclosure mutation 7"),
        ("A chat" + "bot helped draft this file.\n", "disclosure mutation 8"),
        (
            "A neural "
            + "text gene"
            + "rator helped draft this file.\n",
            "disclosure mutation 9",
        ),
        ("Status: proof " + "candidate.\n", "status mutation"),
        ("Bad index: $" + "[" + "G:M" + "]$.\n", "square-index mutation"),
        ("Bad index: $|" + "G:M|$.\n", "raw-index mutation"),
        ("Bad subgroup in" + "dex X:H = 1360.\n", "textual-index mutation"),
        (
            "Release only after a special" + "ist reads the proof.\n",
            "condition mutation 2",
        ),
        (
            "Publication waits until an ex" + "pert checks the appendix.\n",
            "condition mutation 3",
        ),
        (
            "Completion depends on confirmation from a rea" + "der.\n",
            "condition mutation 4",
        ),
        (
            "The preprint may be submitted once a mathe" + "matician verifies the tables.\n",
            "condition mutation 5",
        ),
        (
            "A comm" + "ittee decides whether publication may proceed.\n",
            "comm" + "ittee-decision mutation",
        ),
        (
            "Publication is determined by a pan" + "el vote.\n",
            "pan" + "el-decision mutation",
        ),
        (
            "Alice is assi" + "gned as the release " + "manager.\n",
            "role-assignment mutation",
        ),
        (
            "Alice is the release " + "owner.\n",
            "process-owner mutation",
        ),
        (
            "The pre"
            + "print will be submi"
            + "tted only after Alice "
            + "signs it.\n",
            "named submission-gate mutation",
        ),
        (
            "Publication awaits Alice's as" + "sent.\n",
            "named assent-gate mutation",
        ),
        (
            "The project "
            + "lead decides whether this "
            + "manuscript may be publi"
            + "shed.\n",
            "named publication-decision mutation",
        ),
        (
            "The manu"
            + "script will be publi"
            + "shed after the committee gives con"
            + "sent.\n",
            "semantic dependency mutation A",
        ),
        (
            "Authori"
            + "zation from Alice is required before publi"
            + "cation.\n",
            "semantic dependency mutation B",
        ),
        ("Cla" + "ude revised the prose.\n", "named-model mutation 1"),
        ("Gem" + "ini revised the prose.\n", "named-model mutation 2"),
        ("Open" + "A" + "I revised the prose.\n", "named-model mutation 3"),
        ("G" + "PT-5 revised the prose.\n", "named-model mutation 4"),
        (
            "A writing-"
            + "bot drafted this documentation.\n",
            "semantic attribution mutation A",
        ),
        (
            "Synthetic-"
            + "text tooling revised the prose.\n",
            "semantic attribution mutation B",
        ),
        (
            "Bad index: $\\left" + "[\\mathrm{G}\\mathbin{:}\\mathrm{M}\\right]$.\n",
            "styled-square-index mutation",
        ),
        (
            "Bad index: $[" + "(G)\\mathbin{:}(M)]$.\n",
            "parenthesized-square-index mutation",
        ),
        (
            "Bad index: $|" + "\\mathrm{G}\\mathbin{:}\\operatorname{M}|$.\n",
            "styled-raw-index mutation",
        ),
        (
            "Bad index: $\\vert" + "\\operatorname{Aut}(S)\\mathbin{:}(H)\\vert$.\n",
            "operator-raw-index mutation",
        ),
        (
            "Bad index: $[" + "\\PSL_2(q):H]$.\n",
            "project-macro square-index mutation",
        ),
        (
            "Bad index: $|" + "\\PSL_2(q):H|$.\n",
            "project-macro raw-index mutation",
        ),
        (
            "Bad index: $[" + "\\mathrm{P}\\Omega_8^+(q):H]$.\n",
            "composite-macro square-index mutation",
        ),
        (
            "Bad index: $\\Bigl"
            + "[N_{\\Aut(S)}(H)\\colon M_{12}.2\\Bigr]$.\n",
            "sized-colon-dotted square-index mutation",
        ),
        (
            "Bad index: $\\left"
            + "|N_{\\Aut(S)}(H)\\colon "
            + "M_{12}.2\\right"
            + "|$.\n",
            "sized-colon-nested raw-index mutation",
        ),
        (
            "Bad index: $["
            + "N_{\\Aut(S)}(H)\\colon N_{M_{12}.2}(K)]$.\n",
            "nested-normalizer square-index mutation",
        ),
        (
            "The pre"
            + "print will be submi"
            + "tted only after Alice "
            + "signs it.\n"
            "A chat" + "bot helped draft this repository documentation.\n"
            "Bad index: $[" + "\\PSL_2(q):H]$.\n",
            "combined public-corpus bypass mutation",
        ),
        (
            "The manu"
            + "script requires con"
            + "sent before publi"
            + "cation.\n"
            + "A writing-"
            + "bot drafted this documentation.\n"
            + "Bad index: $\\Bigl"
            + "[N_{\\Aut(S)}(H)\\colon M_{12}.2\\Bigr]$.\n",
            "combined structural-bypass mutation",
        ),
    ]
    for content, context in mutations:
        readme.write_text(baseline + content, encoding="utf-8")
        require_failure(command, tmp, context)
    readme.write_text(baseline, encoding="utf-8")

    original_principal = principal.read_text(encoding="utf-8")
    principal.write_text("No disclosure here.\n", encoding="utf-8")
    require_failure(command, tmp, "missing-disclosure mutation")
    principal.write_text(original_principal * 2, encoding="utf-8")
    require_failure(command, tmp, "duplicate-disclosure mutation")
    principal.write_text(
        original_principal.replace(
            "\n\n" + bibliography,
            " An additional disclosure sentence.\n\n" + bibliography,
        ),
        encoding="utf-8",
    )
    require_failure(command, tmp, "second-disclosure-sentence mutation")
    principal.write_text(original_principal, encoding="utf-8")

    def add_path_then_reject(name: str, content: str, context: str) -> None:
        path = tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        require_success(["git", "add", "-f", name], tmp, f"{context} inventory")
        require_failure(command, tmp, context)
        require_success(["git", "rm", "--cached", "-q", name], tmp, f"{context} reset")
        path.unlink()
        parent = path.parent
        if parent != tmp and not any(parent.iterdir()):
            parent.rmdir()

    add_path_then_reject(
        ("revi" + "ews/status.md"),
        "Process artifact.\n",
        "forbidden-process-path mutation",
    )
    audit_name = "INDEPENDENT-" + "AUD" + "ITOR-NOTES.md"
    add_path_then_reject(audit_name, "Internal material.\n", "forbidden-audit-path mutation")
    add_path_then_reject(
        "technical-notes.md",
        "Release only after a special" + "ist reads the proof.\n",
        "neutral-path condition mutation",
    )

    link = tmp / "linked-notes.md"
    os.symlink("README.md", link)
    require_success(["git", "add", "linked-notes.md"], tmp, "symbolic-link inventory")
    require_failure(command, tmp, "tracked-symbolic-link mutation")
    require_success(["git", "rm", "--cached", "-q", "linked-notes.md"], tmp,
                    "symbolic-link reset")
    link.unlink()

    metadata = {
        "publication_status": "preprint",
        "source_date_epoch": 1787961600,
        "source_archive_stem": "kourovka-18-68-preprint",
    }
    archive_contents = {
        "artifact-metadata.json": (json.dumps(metadata) + "\n").encode(),
        "paper/kourovka-18-68.tex": original_principal.encode(),
        "README.md": baseline.encode(),
    }
    archive = tmp / "kourovka-18-68-preprint-working-tree-source.tar.gz"
    archive_command = [
        "python3",
        "-O",
        "scripts/check-public-corpus.py",
        "--archive",
        str(archive),
    ]
    write_archive(archive, archive_contents)
    require_success(archive_command, tmp, "archive scanner")

    write_archive(archive, archive_contents, corrupt_manifest=True)
    require_failure(archive_command, tmp, "manifest-digest mutation")

    bad_path_contents = dict(archive_contents)
    bad_path_contents[audit_name] = b"Internal material.\n"
    write_archive(archive, bad_path_contents)
    require_failure(archive_command, tmp, "archive-path mutation")

    bad_gate_contents = dict(archive_contents)
    bad_gate_contents["technical-notes.md"] = (
        "Publication waits until an ex" + "pert checks the appendix.\n"
    ).encode()
    write_archive(archive, bad_gate_contents)
    require_failure(archive_command, tmp, "archive-condition mutation")

    bad_disclosure_contents = dict(archive_contents)
    bad_disclosure_contents["technical-notes.md"] = (
        "A language mod" + "el revised this file.\n"
    ).encode()
    write_archive(archive, bad_disclosure_contents)
    require_failure(archive_command, tmp, "archive-disclosure mutation")

    combined_contents = dict(archive_contents)
    combined_contents["technical-notes.md"] = (
        "The manu"
        + "script requires con"
        + "sent before publi"
        + "cation.\n"
        + "A writing-"
        + "bot drafted this documentation.\n"
        + "Bad index: $\\Bigl"
        + "[N_{\\Aut(S)}(H)\\colon M_{12}.2\\Bigr]$.\n"
    ).encode()
    write_archive(archive, combined_contents)
    require_failure(archive_command, tmp, "archive-combined structural mutation")

    write_archive(archive, archive_contents, link_name="linked-notes.md")
    require_failure(archive_command, tmp, "archive-symbolic-link mutation")

    write_archive(archive, archive_contents, root="arbitrary-version-like-name")
    require_failure(archive_command, tmp, "archive-top-name mutation")

    wrong_name = tmp / "public-source.tar.gz"
    wrong_name_command = [
        "python3",
        "-O",
        "scripts/check-public-corpus.py",
        "--archive",
        str(wrong_name),
    ]
    write_archive(wrong_name, archive_contents)
    require_failure(wrong_name_command, tmp, "archive-filename mutation")

    strict_archive = tmp / "kourovka-18-68-preprint-source.tar.gz"
    strict_command = [
        "python3",
        "-O",
        "scripts/check-public-corpus.py",
        "--archive",
        str(strict_archive),
    ]
    write_archive(
        strict_archive,
        archive_contents,
        root="kourovka-18-68-preprint",
        snapshot_kind="git-commit",
        source_commit="0" * 40,
    )
    require_failure(strict_command, tmp, "all-zero source-commit mutation")

    write_archive(
        strict_archive,
        archive_contents,
        root="kourovka-18-68-preprint",
        snapshot_kind="git-commit",
        source_commit="1" * 40,
    )
    require_failure(strict_command, tmp, "unavailable source-commit mutation")

    return len(mutations) + 18


def archive_builder_controls(tmp: Path) -> int:
    (tmp / "scripts").mkdir()
    (tmp / "paper").mkdir()
    for name in [
        "build-source-archive.py",
        "check-artifact-sidecar.py",
        "check-public-corpus.py",
    ]:
        shutil.copy2(ROOT / "scripts" / name, tmp / "scripts" / name)
    shutil.copy2(ROOT / "paper" / "kourovka-18-68.tex", tmp / "paper")
    shutil.copy2(ROOT / "paper" / "kourovka-18-68.pdf", tmp / "paper")
    shutil.copy2(ROOT / "artifact-metadata.json", tmp)
    allowlist = tmp / "scripts" / "public-files.txt"
    allowlist.write_text("", encoding="utf-8")
    require_success(["git", "init", "-q"], tmp, "archive-builder Git initialization")
    require_success(["git", "add", "."], tmp, "archive-builder inventory")

    def refresh_allowlist() -> None:
        result = run(["git", "ls-files", "-z"], tmp)
        require(result.returncode == 0, "archive-builder path enumeration")
        paths = sorted(item for item in result.stdout.split("\0") if item)
        allowlist.write_text("\n".join(paths) + "\n", encoding="utf-8")
        require_success(["git", "add", "scripts/public-files.txt"], tmp,
                        "archive-builder allowlist inventory")

    refresh_allowlist()
    command = [
        "python3",
        "scripts/build-source-archive.py",
        "--working-tree",
        "--output-dir",
        str(tmp / "absolute-output"),
    ]
    require_success(command, tmp, "archive builder")

    output = tmp / "absolute-output"
    sidecar = next(output.glob("*-SHA256SUMS.txt"))
    artifacts = sorted([
        next(output.glob("*.pdf")),
        next(output.glob("*-source.tar.gz")),
    ])
    sidecar_command = [
        "python3",
        "scripts/check-artifact-sidecar.py",
        str(sidecar),
        *(str(path) for path in artifacts),
    ]
    require_success(sidecar_command, tmp, "artifact sidecar baseline")
    original_sidecar = sidecar.read_text(encoding="utf-8")
    sidecar.write_text(("0" * 64) + original_sidecar[64:], encoding="utf-8")
    require_failure(sidecar_command, tmp, "artifact-sidecar digest mutation")
    sidecar.write_text(original_sidecar, encoding="utf-8")

    link = tmp / "linked-source.md"
    os.symlink("artifact-metadata.json", link)
    require_success(["git", "add", "linked-source.md"], tmp,
                    "archive-builder symbolic-link inventory")
    refresh_allowlist()
    require_failure(command, tmp, "archive-builder symbolic-link mutation")
    return 2


def main() -> None:
    total = 0
    with tempfile.TemporaryDirectory(prefix="k186-cert-mutation-") as directory:
        total += certificate_controls(Path(directory))
    with tempfile.TemporaryDirectory(prefix="k186-release-mutation-") as directory:
        total += release_controls(Path(directory))
    with tempfile.TemporaryDirectory(prefix="k186-producer-mutation-") as directory:
        total += producer_controls(Path(directory))
    with tempfile.TemporaryDirectory(prefix="k186-corpus-mutation-") as directory:
        total += public_corpus_controls(Path(directory))
    with tempfile.TemporaryDirectory(prefix="k186-archive-mutation-") as directory:
        total += archive_builder_controls(Path(directory))
    print(f"MUTATION CONTROLS PASSED: {total} deliberate failures rejected")


if __name__ == "__main__":
    main()
