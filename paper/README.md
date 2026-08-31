# Manuscript

[kourovka-18-68.tex](kourovka-18-68.tex) is the preprint source for the
conditional three-factor answer to Kourovka Problem 18.68. The theorem assumes
CFSG and the external statements listed in Appendix C; the two daggered LPS
source matches are explicitly unresolved.

Build from the repository root with the version- and bundle-pinned wrapper:

    make paper

The wrapper requires Tectonic 0.17.0, bundle v33 with content SHA-256

    6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c

and enforces `SOURCE_DATE_EPOCH=1788134400`, UTC, and deterministic mode. It
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
listed in the bibliography. The proof-critical computation consists of five
named small alternating coordinate groups and the ten almost-simple groups
with socle \(L_3(4)\):

    gap --quitonbreak -q gap/generate-factor-free-scan.g
    python3 tests/check-factor-free-scan.py
    gap --quitonbreak -q tests/test-sp4-subfield.g

The first two commands generate and check the fifteen finite Table-of-Marks
closeouts. The final command is a separate finite regression for the uniform
\(\operatorname{PSp}_4(2^f)\) argument; it does not prove the infinite
family.

The current TeX and PDF hashes, page count, date, epoch, and PDF tagging state
are recorded in [BUILD-RECEIPT.txt](BUILD-RECEIPT.txt). The source bundle is
constructed from `scripts/public-files.txt`, carries a verified per-file
`SOURCE-MANIFEST.txt`, and is scanned after safe extraction. The tracked
artifact hashes are also recorded in [SHA256SUMS](../SHA256SUMS).
