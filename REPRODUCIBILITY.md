# Reproducibility

## Pinned acceptance environment

The version 1.0.2 certificates and PDF were produced on macOS/arm64 on
2026-08-11 with:

- GAP 4.15.1;
- TomLib 1.2.11;
- AtlasRep 2.1.11;
- Python 3.14.6, using only the standard library in the checkers; and
- Tectonic 0.17.0.

The PDF wrapper enforces UTC, SOURCE_DATE_EPOCH=1786406400, deterministic
mode, and Tectonic bundle v33 with content hash

    6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c

It performs two isolated clean builds and accepts the PDF only when their
bytes agree. [paper/BUILD-RECEIPT.txt](paper/BUILD-RECEIPT.txt) records the
result.

## Clean-clone verification

From the repository root, run:

    make check
    make release-check
    git status --short

The final command must print nothing. The full release target:

1. enforces the exact GAP, TomLib, AtlasRep, Python, Tectonic, and bundle
   versions;
2. runs direct GAP tests for the complemented-maximal and factor-free
   Table-of-Marks predicates;
3. reconstructs the corrected
   $\operatorname{Aut}(\operatorname{Sp}_4(4))$ subfield subgroup with
   AtlasRep;
4. regenerates the 414-table survey and all 24 pinned factor-free rows;
5. independently checks hashes, row inventories, arithmetic, complement
   witnesses, and factor-free counts;
6. runs the Python acceptance checkers under optimization and forces a GAP
   error to verify nonzero failure;
7. exercises seven isolated missing, changed, stale, and version-mismatch
   mutations;
8. builds the PDF twice in clean temporary directories;
9. verifies the deterministic receipt and [SHA256SUMS](SHA256SUMS); and
10. rejects whitespace errors or regenerated data/PDF differences.

The commands behind these targets are documented in
[tests/README.md](tests/README.md), [gap/README.md](gap/README.md), and
[paper/README.md](paper/README.md).

## Expected accepted output

The key counts and regression data are:

    414 Table-of-Marks summaries
    2,395 maximal-subgroup classes
    73 CMP-positive tables
    24 pinned factor-free rows
    |X:H| = 1360, |H| = 2880, |H intersect S| = 720
    involution coverage = [true, true, true]
    7 deliberate mutations rejected

The final PDF SHA-256 is

    9fa44095bcfde9c0592b6bdd7529f86da7e31ed59d875cf5a63a72eadc3948fb

## Evidence boundary

The Table-of-Marks files are exact finite certificates relative to the
complete subgroup and intersection data in the named TomLib tables. They are
not a census of finite groups and are not used to extrapolate an infinite
family. The universal theorem is conditional on CFSG and on the exhaustive
published maximal-factorization classifications identified in the manuscript
and [references/README.md](references/README.md).

The graph-outer $\operatorname{PSp}_4(2^f)$ family is closed by the written
subfield and valuation proof. The AtlasRep computation at $q=4$ is a
regression test, not the infinite proof.

Source PDFs are not redistributed because their redistribution rights were
not established. The reference ledger records stable links and SHA-256 hashes
for the copies actually audited.

## Review provenance

The internal review reports retain commit hashes from the original portfolio
workspace in which they were performed. Version 1.0.2 of this standalone
repository contains the reviewed final tree. No independent external
finite-group specialist has yet reviewed the proof.
