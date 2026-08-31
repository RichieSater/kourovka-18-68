#!/usr/bin/env python3
"""Build and scan a deterministic, explicitly allowlisted source bundle."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "scripts" / "public-files.txt"
METADATA = ROOT / "artifact-metadata.json"


def fail(message: str) -> NoReturn:
    raise RuntimeError(f"source archive build failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run(command: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def load_metadata() -> tuple[int, str, str]:
    try:
        data = json.loads(METADATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"could not read authoritative metadata: {error}")
    require(data.get("publication_status") == "preprint", "publication status")
    version = data.get("artifact_version")
    require(isinstance(version, str) and re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version),
            "artifact version")
    require(data.get("version_tag") == f"v{version}", "version tag")
    require(data.get("version_doi") is None, "premature version DOI")
    epoch = data.get("source_date_epoch")
    stem = data.get("source_archive_stem")
    require(isinstance(epoch, int) and epoch > 0, "source date epoch")
    require(isinstance(stem, str) and stem == f"kourovka-18-68-v{version}",
            "source archive stem")
    return epoch, stem, data["publication_status"]


def allowlisted_paths() -> list[Path]:
    require(ALLOWLIST.is_file(), f"missing {ALLOWLIST.relative_to(ROOT)}")
    paths: list[Path] = []
    seen: set[Path] = set()
    for number, raw in enumerate(ALLOWLIST.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        path = Path(line)
        require(not path.is_absolute() and ".." not in path.parts,
                f"unsafe path at allowlist line {number}: {line}")
        require(path not in seen, f"duplicate allowlist path: {line}")
        seen.add(path)
        paths.append(path)
    require(paths == sorted(paths, key=lambda item: item.as_posix()),
            "allowlist must be sorted")
    return paths


def tracked_entries() -> dict[Path, str]:
    result = run(["git", "ls-files", "-s", "-z"])
    require(result.returncode == 0, "git could not enumerate tracked files")
    raw_entries = result.stdout.split(b"\0")
    require(raw_entries and raw_entries[-1] == b"", "malformed Git index stream")
    entries: dict[Path, str] = {}
    for raw in raw_entries[:-1]:
        try:
            prefix, name = raw.split(b"\t", 1)
            mode, _object_id, stage = prefix.decode("ascii").split()
            path = Path(name.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as error:
            fail(f"malformed Git index entry: {error}")
        require(stage == "0", f"unmerged Git index entry: {path}")
        require(mode in {"100644", "100755"},
                f"tracked entry is not a regular file: {path} ({mode})")
        require(path not in entries, f"duplicate Git index entry: {path}")
        entries[path] = mode
    return entries


def require_source_state(paths: list[Path], *, working_tree: bool) -> tuple[str, dict[Path, str]]:
    entries = tracked_entries()
    require(sorted(entries, key=lambda item: item.as_posix()) == paths,
            "tracked inventory differs from scripts/public-files.txt")
    for path in paths:
        full = ROOT / path
        require(not full.is_symlink(), f"symbolic link is not allowed: {path}")
        require(full.is_file(), f"allowlisted regular file is missing: {path}")
    if working_tree:
        return "none", entries
    status = run(["git", "status", "--porcelain=v1", "--untracked-files=no"])
    require(status.returncode == 0, "could not inspect source state")
    require(status.stdout == b"", "strict source bundle requires a clean tracked tree")
    head = run(["git", "rev-parse", "HEAD"])
    require(head.returncode == 0, "could not identify source commit")
    commit = head.stdout.decode("ascii").strip()
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
            "unexpected source commit identifier")
    tree = run(["git", "ls-tree", "-r", "-z", "HEAD"])
    require(tree.returncode == 0, "could not inspect source commit tree")
    committed: dict[Path, str] = {}
    for raw in tree.stdout.split(b"\0")[:-1]:
        prefix, name = raw.split(b"\t", 1)
        mode, object_type, _object_id = prefix.decode("ascii").split()
        path = Path(name.decode("utf-8"))
        require(object_type == "blob", f"non-blob source entry: {path}")
        committed[path] = mode
    require(committed == entries, "index inventory or modes differ from HEAD")
    return commit, entries


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_bytes(path: Path, *, working_tree: bool) -> bytes:
    if working_tree:
        return (ROOT / path).read_bytes()
    result = run(["git", "show", f"HEAD:{path.as_posix()}"])
    require(result.returncode == 0, f"could not read Git blob for {path}")
    return result.stdout


def source_manifest(
    paths: list[Path],
    modes: dict[Path, str],
    contents: dict[Path, bytes],
    commit: str,
    *,
    working_tree: bool,
    epoch: int,
    publication_status: str,
) -> bytes:
    lines = [
        "schema_version=1",
        f"publication_status={publication_status}",
        f"source_date_epoch={epoch}",
        f"snapshot_kind={'working-tree' if working_tree else 'git-commit'}",
        f"source_commit={commit}",
        "hash_algorithm=SHA-256",
        "entry_format=sha256 git-mode path",
        "",
    ]
    for path in paths:
        lines.append(
            f"{sha256_bytes(contents[path])}  {modes[path]}  {path.as_posix()}"
        )
    lines.append("")
    return "\n".join(lines).encode("utf-8")


def tar_info(name: str, *, directory: bool, mode: int, epoch: int, size: int = 0) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name + ("/" if directory and not name.endswith("/") else ""))
    info.type = tarfile.DIRTYPE if directory else tarfile.REGTYPE
    info.mode = mode
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = epoch
    info.size = 0 if directory else size
    return info


def write_archive(
    output: Path,
    top: str,
    paths: list[Path],
    modes: dict[Path, str],
    contents: dict[Path, bytes],
    manifest: bytes,
    epoch: int,
) -> None:
    directories = {Path(".")}
    for path in [*paths, Path("SOURCE-MANIFEST.txt")]:
        directories.update(path.parents)
    ordered_directories = sorted(
        (path for path in directories if path != Path(".")),
        key=lambda item: (len(item.parts), item.as_posix()),
    )
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=epoch) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as handle:
                handle.addfile(tar_info(top, directory=True, mode=0o755, epoch=epoch))
                for directory in ordered_directories:
                    handle.addfile(
                        tar_info(f"{top}/{directory.as_posix()}", directory=True,
                                 mode=0o755, epoch=epoch)
                    )
                for path in paths:
                    data = contents[path]
                    mode = 0o755 if modes[path] == "100755" else 0o644
                    info = tar_info(f"{top}/{path.as_posix()}", directory=False,
                                    mode=mode, epoch=epoch, size=len(data))
                    handle.addfile(info, io.BytesIO(data))
                manifest_info = tar_info(
                    f"{top}/SOURCE-MANIFEST.txt",
                    directory=False,
                    mode=0o644,
                    epoch=epoch,
                    size=len(manifest),
                )
                handle.addfile(manifest_info, io.BytesIO(manifest))


def scan(command: list[str], context: str) -> None:
    result = run(command)
    require(result.returncode == 0,
            f"{context} failed:\n{result.stdout.decode('utf-8', errors='replace')}")
    sys.stdout.write(result.stdout.decode("utf-8"))


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--working-tree", action="store_true",
                        help="build an explicitly labelled working-tree snapshot")
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    args = parser.parse_args()

    epoch, stem, publication_status = load_metadata()
    paths = allowlisted_paths()
    commit, modes = require_source_state(paths, working_tree=args.working_tree)
    contents = {
        path: source_bytes(path, working_tree=args.working_tree)
        for path in paths
    }
    scan(
        [sys.executable, "scripts/check-public-corpus.py", "--paths-file",
         "scripts/public-files.txt"],
        "allowlisted working-tree scan",
    )
    manifest = source_manifest(
        paths, modes, contents, commit,
        working_tree=args.working_tree,
        epoch=epoch,
        publication_status=publication_status,
    )
    suffix = "-working-tree" if args.working_tree else ""
    top = f"{stem}{suffix}"
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{top}-source.tar.gz"
    pdf_source = ROOT / "paper" / "kourovka-18-68.pdf"
    require(pdf_source.is_file(), "manuscript PDF is missing")
    pdf = output_dir / f"{top}.pdf"
    sidecar = output_dir / f"{top}-SHA256SUMS.txt"

    with tempfile.TemporaryDirectory(prefix="k186-source-build-") as directory:
        first = Path(directory) / "one.tar.gz"
        second = Path(directory) / "two.tar.gz"
        write_archive(first, top, paths, modes, contents, manifest, epoch)
        write_archive(second, top, paths, modes, contents, manifest, epoch)
        require(first.read_bytes() == second.read_bytes(),
                "two deterministic source-bundle builds differ")
        archive.write_bytes(first.read_bytes())

    pdf.write_bytes(pdf_source.read_bytes())
    scan(
        [sys.executable, "scripts/check-public-corpus.py", "--archive", str(archive),
         "--paths-file", "scripts/public-files.txt"],
        "extracted source-archive scan",
    )
    artifacts = sorted((pdf, archive), key=lambda item: item.name)
    entries = [
        f"{sha256_bytes(artifact.read_bytes())}  {artifact.name}"
        for artifact in artifacts
    ]
    sidecar.write_text("\n".join(entries) + "\n", encoding="utf-8")
    scan(
        [sys.executable, "scripts/check-artifact-sidecar.py", str(sidecar),
         *(str(artifact) for artifact in artifacts)],
        "artifact-sidecar verification",
    )
    print(f"SOURCE ARCHIVE PASSED: {display_path(archive)}")
    print(f"ARTIFACT HASHES: {display_path(sidecar)}")


if __name__ == "__main__":
    main()
