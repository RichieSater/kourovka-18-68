# Version 1.1.1 — conditional preprint

- **Release date:** 2026-08-31
- **Publication status:** preprint

## Mathematical status

The main theorem is proved conditional on CFSG and the external classification
and factorization results listed in Appendix C. The consequences attributed to
LPS (2000), Corollary 3(iv), and LPS (1990), Theorem D with Remark 2, remain
explicit unverified source assumptions at the verification boundary.

## Changes in this version

- The public-corpus checker now normalizes additional TeX and Unicode colon and
  delimiter encodings, expands ordinary TeX macros, and distinguishes source
  indexing syntax from mathematical notation before enforcing subgroup-index
  style.
- Indented Markdown is scanned for the same notation violations as surrounding
  prose.
- Structural public-corpus detection covers additional forbidden phrase
  variants while retaining ordinary mathematical and deterministic-tooling
  prose.
- Source and rendered-text checks jointly enforce the manuscript's exact-one
  disclosure boundary.
- The mutation suite now rejects 164 deliberate corruptions while retaining
  positive controls for ordinary mathematical and programming usage.
- Test documentation now describes the executable mutation suite without a
  stale hard-coded count.

The mathematical manuscript and its 20-page PDF are unchanged from version
1.1.0. This version changes repository safeguards and their documentation.

## Reproducible evidence

The complete gate regenerates 414 TomLib tables, 2,395 maximal classes, 73
CMP-positive tables, and 24 factor-free certificate rows. The manuscript is
built twice byte-for-byte with the pinned toolchain. The release assets contain
the PDF, exact-commit source archive, and their SHA-256 sidecar.
