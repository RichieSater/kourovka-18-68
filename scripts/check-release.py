#!/usr/bin/env python3
"""Check deterministic paper, metadata, and publication-facing invariants."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "paper" / "kourovka-18-68.pdf"
RECEIPT = ROOT / "paper" / "BUILD-RECEIPT.txt"
TEX = ROOT / "paper" / "kourovka-18-68.tex"
METADATA = ROOT / "artifact-metadata.json"
CITATION = ROOT / "CITATION.cff"
README = ROOT / "README.md"
REPRODUCIBILITY = ROOT / "REPRODUCIBILITY.md"
PAPER_README = ROOT / "paper" / "README.md"
RELEASE_NOTES = ROOT / "RELEASE-NOTES-v1.1.1.md"
WORKFLOW = ROOT / ".github" / "workflows" / "release-check.yml"


def fail(message: str) -> NoReturn:
    raise RuntimeError(f"release check failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, object]:
    """Parse YAML through Ruby's standard Psych parser, then return JSON data."""
    executable = shutil.which("ruby")
    require(executable is not None, "Ruby is required for structural YAML validation")
    program = (
        'require "yaml"; require "json"; '
        'data = YAML.safe_load(File.read(ARGV[0]), permitted_classes: [], '
        'permitted_symbols: [], aliases: false); puts JSON.generate(data)'
    )
    result = subprocess.run(
        [executable, "-e", program, str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    require(
        result.returncode == 0,
        f"could not parse YAML {path.name}: {result.stderr.strip()}",
    )
    try:
        document = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        fail(f"YAML parser emitted malformed JSON for {path.name}: {error}")
    require(isinstance(document, dict), f"YAML root is not an object: {path.name}")
    return document


def load_receipt() -> dict[str, str]:
    fields: dict[str, str] = {}
    for number, line in enumerate(RECEIPT.read_text(encoding="utf-8").splitlines(), 1):
        parts = line.split("=", 1)
        require(len(parts) == 2, f"malformed receipt line {number}")
        key, value = parts
        require(key not in fields, f"duplicate receipt key {key}")
        fields[key] = value
    return fields


def load_metadata() -> dict[str, object]:
    try:
        metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"could not read authoritative metadata: {error}")
    require(isinstance(metadata, dict), "metadata root is not an object")
    expected_keys = {
        "schema_version",
        "publication_status",
        "title",
        "author",
        "author_given_names",
        "author_family_names",
        "author_orcid",
        "author_affiliation",
        "manuscript_date",
        "publication_year",
        "source_date_epoch",
        "repository",
        "artifact_version",
        "version_tag",
        "version_doi",
        "pdf_version",
        "pdf_tagged",
        "pdf_subject",
        "tectonic_version",
        "tectonic_bundle_url",
        "tectonic_bundle_content_sha256",
        "source_archive_stem",
    }
    require(set(metadata) == expected_keys, "authoritative metadata key inventory")
    require(metadata["schema_version"] == 1, "metadata schema version")
    require(metadata["publication_status"] == "preprint", "publication status")
    require(metadata["author"] == "Richie Sater", "authoritative author")
    require(metadata["author_given_names"] == "Richie", "author given names")
    require(metadata["author_family_names"] == "Sater", "author family names")
    require(
        metadata["author_orcid"] == "https://orcid.org/0009-0007-9051-8207",
        "author ORCID",
    )
    require(metadata["author_affiliation"] == "Independent Researcher",
            "author affiliation")
    require(
        metadata["repository"] == "https://github.com/RichieSater/kourovka-18-68",
        "authoritative repository",
    )
    require(metadata["artifact_version"] == "1.1.1", "artifact version")
    require(metadata["version_tag"] == "v1.1.1", "version tag")
    require(metadata["version_doi"] is None, "unissued version DOI")
    require(metadata["pdf_tagged"] is False, "PDF tagging status in metadata")
    require(
        metadata["pdf_subject"] == "Conditional classification for Kourovka Problem 18.68",
        "neutral PDF subject",
    )
    require(metadata["source_archive_stem"] == "kourovka-18-68-v1.1.1",
            "source archive stem")
    date = datetime.strptime(str(metadata["manuscript_date"]), "%Y-%m-%d").replace(
        tzinfo=timezone.utc
    )
    require(int(date.timestamp()) == metadata["source_date_epoch"],
            "manuscript date and deterministic epoch disagree")
    require(metadata["publication_year"] == date.year, "publication year and date disagree")
    return metadata


def pdf_information() -> dict[str, str]:
    executable = shutil.which("pdfinfo")
    require(executable is not None, "pdfinfo is required")
    result = subprocess.run(
        [executable, str(PDF)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    require(result.returncode == 0, "pdfinfo could not inspect the manuscript")
    fields: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key] = value.strip()
    return fields


def qpdf_catalog() -> dict[str, object]:
    executable = shutil.which("qpdf")
    require(executable is not None, "qpdf is required")
    result = subprocess.run(
        [executable, "--json", str(PDF)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, "qpdf could not inspect the manuscript")
    try:
        document = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        fail(f"qpdf emitted malformed JSON: {error}")
    objects = document.get("qpdf", [{}])[-1]
    require(isinstance(objects, dict), "qpdf object inventory")
    trailers = [value for key, value in objects.items() if key.startswith("trailer")]
    require(len(trailers) == 1, "qpdf trailer inventory")
    trailer = trailers[0].get("value", {})
    root_ref = trailer.get("/Root")
    require(isinstance(root_ref, str), "PDF catalog reference")
    catalog_entry = objects.get(f"obj:{root_ref}")
    require(isinstance(catalog_entry, dict), "PDF catalog object")
    catalog = catalog_entry.get("value", {})
    require(isinstance(catalog, dict), "PDF catalog value")
    return catalog


def check_text_metadata(metadata: dict[str, object]) -> None:
    tex = TEX.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    display_date = datetime.strptime(str(metadata["manuscript_date"]), "%Y-%m-%d").strftime(
        "%d %B %Y"
    ).lstrip("0")
    require(f"\\date{{Preprint, {display_date}}}" in tex, "TeX manuscript date")
    require(f"pdfsubject={{{metadata['pdf_subject']}}}" in tex, "TeX PDF subject")
    author = {
        "family-names": metadata["author_family_names"],
        "given-names": metadata["author_given_names"],
        "orcid": metadata["author_orcid"],
        "affiliation": metadata["author_affiliation"],
    }
    expected_citation: dict[str, object] = {
        "cff-version": "1.2.0",
        "message": "If you use this work, please cite the preprint and this repository.",
        "title": metadata["title"],
        "type": "software",
        "version": metadata["artifact_version"],
        "date-released": str(metadata["manuscript_date"]),
        "authors": [author],
        "repository-code": metadata["repository"],
        "url": metadata["repository"],
        "keywords": [
            "finite groups",
            "composition factors",
            "complemented maximal subgroups",
            "primitive groups",
            "maximal factorizations",
            "Kourovka Notebook",
        ],
        "preferred-citation": {
            "type": "article",
            "authors": [author],
            "title": metadata["title"],
            "year": metadata["publication_year"],
            "url": metadata["repository"],
        },
    }
    require(load_yaml(CITATION) == expected_citation,
            "CFF structure or authoritative values")
    require("**Publication status:** preprint." in readme, "README publication status")
    require("**Current version:** [1.1.1]" in readme, "README current version")
    require(("rele" + "ase candidate") not in readme.lower(), "README process status")
    require(not (ROOT / ".zenodo.json").exists(), "unsupported Zenodo metadata present")
    require(RELEASE_NOTES.is_file(), "version notes missing")
    require("Corollary~3(iv)" in tex and "Theorem~D" in tex,
            "front-matter LPS verification boundary")
    expected_epoch = str(metadata["source_date_epoch"])
    epoch_pattern = re.compile(r"SOURCE_DATE_EPOCH\s*=\s*([0-9]{10})")
    for path in (REPRODUCIBILITY, PAPER_README):
        values = epoch_pattern.findall(path.read_text(encoding="utf-8"))
        require(values == [expected_epoch],
                f"documented deterministic epoch in {path.relative_to(ROOT)}")


def check_workflow() -> None:
    workflow = load_yaml(WORKFLOW)
    require(workflow.get("name") == "release-check", "CI workflow name")
    require(workflow.get("on") == {
        "push": None,
        "pull_request": None,
        "workflow_dispatch": None,
    }, "CI trigger inventory")
    require(workflow.get("permissions") == {"contents": "read"}, "CI permissions")
    jobs = workflow.get("jobs")
    require(isinstance(jobs, dict) and set(jobs) == {"release-check"},
            "CI job inventory")
    job = jobs["release-check"]
    require(isinstance(job, dict), "CI release job")
    require(job.get("runs-on") == "ubuntu-latest", "CI runner")
    require(job.get("timeout-minutes") == 45, "CI timeout")
    steps = job.get("steps")
    require(isinstance(steps, list) and all(isinstance(step, dict) for step in steps),
            "CI step inventory")
    named_steps = {step.get("name"): step for step in steps}
    require(len(named_steps) == len(steps), "CI step names must be unique")
    require(set(named_steps) == {
        "Check out exact source",
        "Install system dependencies",
        "Install GAP 4.15.1 and distributed packages",
        "Install checksum-pinned AtlasRep 2.1.11",
        "Install pinned Tectonic 0.17.0",
        "Bootstrap the pinned Tectonic bundle",
        "Run the complete release gate",
    }, "CI step-name inventory")
    require(named_steps["Install system dependencies"].get("run") ==
            "sudo apt-get update && sudo apt-get install --yes poppler-utils qpdf ruby",
            "CI system dependencies")
    require(named_steps["Bootstrap the pinned Tectonic bundle"].get("run") ==
            "make bootstrap-bundle", "CI bundle command")
    require(named_steps["Run the complete release gate"] == {
        "name": "Run the complete release gate",
        "run": "make GAP=gap release-check",
    }, "CI executable release command")
    atlas_step = named_steps["Install checksum-pinned AtlasRep 2.1.11"]
    atlas_command = atlas_step.get("run")
    require(isinstance(atlas_command, str), "CI AtlasRep command")
    require("atlasrep-2.1.11.tar.gz" in atlas_command, "CI AtlasRep source")
    require(
        "1ccb65af694d53f60ba41f85b2293e505c42a2fecf90b36747c1d841a5ce0b47"
        in atlas_command,
        "CI AtlasRep checksum",
    )


def main() -> None:
    for path in (
        PDF, RECEIPT, TEX, METADATA, CITATION, README,
        REPRODUCIBILITY, PAPER_README, RELEASE_NOTES, WORKFLOW,
    ):
        require(path.is_file(), f"missing {path}")
    metadata = load_metadata()
    fields = load_receipt()
    expected_fixed = {
        "artifact": "paper/kourovka-18-68.pdf",
        "publication_status": str(metadata["publication_status"]),
        "manuscript_date": str(metadata["manuscript_date"]),
        "tectonic_version": str(metadata["tectonic_version"]),
        "bundle_url": str(metadata["tectonic_bundle_url"]),
        "bundle_content_sha256": str(metadata["tectonic_bundle_content_sha256"]),
        "source_date_epoch": str(metadata["source_date_epoch"]),
        "timezone": "UTC",
        "deterministic_mode": "true",
        "clean_builds_compared": "2",
        "tagged_pdf": "false",
    }
    for key, value in expected_fixed.items():
        require(fields.get(key) == value, f"receipt field {key}")
    require(fields.get("metadata_sha256") == sha256(METADATA),
            "metadata hash does not match receipt")
    require(fields.get("pdf_sha256") == sha256(PDF), "PDF hash does not match receipt")
    require(fields.get("tex_sha256") == sha256(TEX), "TeX hash does not match receipt")
    pages = fields.get("page_count", "")
    require(pages.isdigit() and int(pages) > 0, "invalid receipt page count")
    require(len(fields) == len(expected_fixed) + 4, "unexpected receipt fields")

    info = pdf_information()
    require(info.get("Title") == metadata["title"], "PDF title metadata")
    require(info.get("Author") == metadata["author"], "PDF author metadata")
    require(info.get("Subject") == metadata["pdf_subject"], "PDF subject metadata")
    require(info.get("Tagged") == "no", "PDF must be intentionally untagged")
    require(info.get("PDF version") == metadata["pdf_version"], "PDF version")
    require(info.get("Pages") == pages, "PDF page count does not match receipt")

    catalog = qpdf_catalog()
    require(catalog.get("/Lang") == "u:en-US", "PDF language metadata")
    require("/StructTreeRoot" not in catalog, "unexpected PDF structure tree")
    require("/MarkInfo" not in catalog, "unexpected PDF marked-content catalog entry")
    check_text_metadata(metadata)
    check_workflow()
    print(f"RELEASE RECEIPT PASSED: {fields['pdf_sha256']} ({pages} pages, untagged)")


if __name__ == "__main__":
    main()
