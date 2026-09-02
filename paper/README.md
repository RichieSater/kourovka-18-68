# Manuscript

[kourovka-18-68.tex](kourovka-18-68.tex) is the preprint source for the
solution of Kourovka Problem 18.68. The proof uses CFSG and the published
classification and factorization results cited where they enter.

Build from the repository root with the version- and bundle-pinned wrapper:

    make paper

The wrapper requires Tectonic 0.17.0, bundle v33 with content SHA-256

    6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c

and enforces `SOURCE_DATE_EPOCH=1788307200`, UTC, and deterministic mode. It
compares two clean builds byte-for-byte and writes
[BUILD-RECEIPT.txt](BUILD-RECEIPT.txt).

For an empty Tectonic cache, first run:

    make bootstrap-bundle

The bootstrap compiles the actual manuscript against the pinned remote
bundle, then verifies the bundle content hash. The paper build itself uses
only cached resources. The PDF carries title, author, and language metadata
but is intentionally untagged; no PDF/UA or structural-accessibility
conformance is claimed.

The proof depends on the published exhaustive factorization classifications
listed in the bibliography. The finite computation covers five named small
alternating coordinate groups and the ten almost-simple groups with socle
\(L_3(4)\):

    gap --quitonbreak -q gap/generate-factor-free-scan.g
    python3 tests/check-factor-free-scan.py
    gap --quitonbreak -q tests/test-sp4-subfield.g

The first two commands generate and check the fifteen finite Table-of-Marks
cases used in the proof. The final command checks the \(q=4\) instance of
the uniform \(\operatorname{PSp}_4(2^f)\) argument.

The current TeX and PDF hashes, page count, date, epoch, and PDF tagging state
are recorded in [BUILD-RECEIPT.txt](BUILD-RECEIPT.txt). The source bundle is
constructed from `scripts/public-files.txt`, carries a verified per-file
`SOURCE-MANIFEST.txt`, and is scanned after safe extraction. The tracked
artifact hashes are also recorded in [SHA256SUMS](../SHA256SUMS).
