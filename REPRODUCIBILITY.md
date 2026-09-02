# Reproducibility

## Preprint artifact identity

The publication status is **preprint**. [`artifact-metadata.json`](artifact-metadata.json)
is the single source for the manuscript date, deterministic epoch, repository,
PDF properties, Tectonic inputs, version 1.2.0, tag `v1.2.0`, and the
source-archive stem. No version DOI has been issued. `scripts/check-release.py`
cross-checks this record
against the TeX front matter, `CITATION.cff`, the build receipt, the PDF catalog,
and the public documentation.

Version 1.0.2 remains a separate historical artifact. Its archived hashes are:

    TeX  d01d3a0212eaf1b965f25d5076254b6500933c13c2bb95665b5f4aeedf7d81f4
    PDF  9fa44095bcfde9c0592b6bdd7529f86da7e31ed59d875cf5a63a72eadc3948fb

Those hashes do not describe the current preprint, and its historical source
bundle is not reused.

## Pinned environment

The calculations and PDF use:

- GAP 4.15.1;
- TomLib 1.2.11;
- AtlasRep 2.1.11;
- Python 3.10 or later;
- Ruby with its standard YAML parser, used for structural CFF and workflow
  validation;
- Tectonic 0.17.0; and
- Poppler `pdfinfo` and `pdftotext` for metadata and corpus checks.

The PDF wrapper enforces UTC, `SOURCE_DATE_EPOCH=1788307200`, deterministic
mode, and Tectonic bundle v33 with content hash

    6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c

It performs two isolated clean builds and accepts the PDF only when their
bytes agree. [paper/BUILD-RECEIPT.txt](paper/BUILD-RECEIPT.txt) binds the TeX
and PDF hashes to the manuscript date, epoch, page count, and build inputs.

## Empty-home bootstrap and Linux workflow

The executable Linux reference is
[`.github/workflows/release-check.yml`](.github/workflows/release-check.yml).
It installs GAP 4.15.1, replaces the distributed AtlasRep with version 2.1.11
from the upstream archive after verifying SHA-256

    1ccb65af694d53f60ba41f85b2293e505c42a2fecf90b36747c1d841a5ce0b47

and installs the pinned Tectonic binary, Poppler, qpdf, and Ruby. The workflow invokes
`make GAP=gap release-check`, avoiding any multiword `GAP` environment value
exported by the GAP setup action.

An empty Tectonic home has no bundle cache. Populate it with the manuscript's
actual dependencies and authenticate the resulting bundle record by running:

    make bootstrap-bundle

The bootstrap is the only PDF step allowed to fetch bundle resources. The
paper build uses `--only-cached`, so a missing or altered cache fails closed.

## Verification commands

From the repository root, run:

    make bootstrap-bundle
    make check
    make working-archive

`make check` regenerates the proof data before comparing it with the tracked
TSV files, so changes in the calculation cannot leave stale results in place.
The build receipt rejects a stale TeX/PDF pair. The working-tree archive is
labelled as such in its manifest and makes no commit-binding claim.

For a clean committed source tree, run:

    make release-check
    git status --short

The final command must print nothing. The complete gate:

1. enforces the exact GAP, TomLib, AtlasRep, Tectonic, bundle, and supported
   Python versions;
2. runs direct GAP tests for the complemented-maximal and factor-free
   Table-of-Marks predicates;
3. reconstructs the corrected
   `Aut(Sp(4,4))` subfield subgroup with AtlasRep;
4. regenerates the 414-table survey and all 24 specified factor-free rows,
   distinguishing 15 cases used in the proof from nine cross-checks;
5. checks hashes, row inventories, arithmetic, complement witnesses, and
   factor-free counts;
6. runs the Python integrity checkers under optimization and forces a GAP
   error to verify nonzero failure;
7. runs mutation tests for the computed data, producer, stale-pair, metadata, corpus,
   disclosure, notation, manifest, symlink, and archive mutations;
8. parses the CFF and Linux workflow structurally, then builds the PDF twice
   in clean temporary directories and verifies its title, author, neutral
   subject, language, PDF version, page count, and untagged status;
9. verifies [SHA256SUMS](SHA256SUMS), the deterministic receipt, and all
   digests in the extracted `SOURCE-MANIFEST.txt`;
10. packages exactly the regular files in `scripts/public-files.txt`, safely
    extracts the archive, checks its inventory and Git modes, and scans every
    extracted member; and
11. rejects whitespace errors or any tracked source difference.

The commands behind these targets are documented in
[tests/README.md](tests/README.md), [gap/README.md](gap/README.md), and
[paper/README.md](paper/README.md).

## Source-bundle boundary

`scripts/public-files.txt` is the sole packaging inventory. The strict bundle
is `dist/kourovka-18-68-v1.2.0-source.tar.gz`; the explicitly labelled
working-tree bundle is
`dist/kourovka-18-68-v1.2.0-working-tree-source.tar.gz`. Both are built
twice byte-for-byte and scanned after safe extraction. The adjacent
`*-SHA256SUMS.txt` binds the PDF and source bundle, and
`scripts/check-artifact-sidecar.py` independently reparses that sidecar and
recomputes both digests. Because `dist/` is ignored,
the archive scanner is invoked explicitly on the artifact rather than relying
on the tracked-tree scan.

The archive builder requires the tracked inventory to equal the explicit
allowlist and rejects symbolic links or any other non-regular tracked entry.
Artifact filenames and the top-level archive directory are derived from the
authoritative source-archive stem and snapshot kind. For a strict bundle, the
builder also requires a clean index and worktree, reads every member from the
exact Git blob at `HEAD`, preserves the executable-bit mode, and records the
commit in `SOURCE-MANIFEST.txt`. The archive scanner rejects zero or unavailable
commit identifiers and checks every manifest path, mode, and digest against
that available Git tree. A working-tree bundle reads regular files from disk
and records no source commit.

## Expected mathematical output

The key counts and regression data are:

    414 Table-of-Marks summaries
    2,395 maximal-subgroup classes
    73 CMP-positive tables
    24 specified factor-free rows = 15 used in the proof + 9 cross-checks
    subgroup index \(\lvert X:H\rvert=1360\), order H = 2880,
      order H-intersect-S = 720
    involution coverage = [true, true, true]

The current TeX and PDF hashes and page count are recorded in
[paper/BUILD-RECEIPT.txt](paper/BUILD-RECEIPT.txt) and pinned with the
generated data in [SHA256SUMS](SHA256SUMS). The PDF carries title, author,
and language metadata. It is intentionally untagged because the pinned
XeTeX toolchain produced broken marked-content pairs under experimental
structural tagging; no PDF/UA or structural-accessibility conformance is
claimed.

## Scope of computation

The Table-of-Marks files record exact finite calculations from the complete
subgroup and intersection data in the named TomLib tables. The proof invokes
CFSG and the published maximal-factorization theorems identified in the
manuscript and [references/README.md](references/README.md).

The Python factor-free checker verifies serialization, inventory, metadata,
hashes, and arithmetic; it does not independently recompute TomLib's negative
intersection search. The graph-outer `PSp(4,2^f)` family is closed by the
written subfield and valuation proof. The AtlasRep calculation at `q=4` is a
regression test, not the infinite proof.

Source PDFs are not redistributed because their redistribution rights were
not established. The reference list records stable links and available
SHA-256 hashes for the copies actually examined.
