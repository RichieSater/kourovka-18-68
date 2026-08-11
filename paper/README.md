# Manuscript

`kourovka-18-68.tex` is the peer-review draft proving the three-factor
answer to Kourovka Problem 18.68.

Build from the repository root with the version- and bundle-pinned wrapper:

```sh
make paper
```

The wrapper requires Tectonic 0.17.0, bundle v33 with content SHA-256
`6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c`,
`SOURCE_DATE_EPOCH=1786406400`, UTC, and deterministic mode.  It compares two
clean builds byte-for-byte and writes [`BUILD-RECEIPT.txt`](BUILD-RECEIPT.txt).

The proof depends on the published exhaustive factorization classifications
listed in the bibliography.  The proof-critical computation consists of
five named small alternating coordinate groups and the ten almost-simple
groups with socle \(L_3(4)\), and is reproduced by:

```sh
cd ..
gap --quitonbreak -q gap/generate-factor-free-scan.g
python3 tests/check-factor-free-scan.py
gap --quitonbreak -q tests/test-sp4-subfield.g
```

The manuscript carries an explicit AI-use disclosure. The named author is
solely responsible for verification and submission; internal agent reviews
are not represented as external peer review.

The hard-final 12-page PDF has SHA-256
`9fa44095bcfde9c0592b6bdd7529f86da7e31ed59d875cf5a63a72eadc3948fb`;
`BUILD-RECEIPT.txt` is authoritative if the manuscript changes.
