# Reproducibility

## Pinned producer environment

The committed certificates and PDF were produced on macOS/arm64 on
2026-08-11 with:

- GAP 4.15.1;
- TomLib 1.2.11;
- Python 3.14.6 (the checkers require only the Python standard library); and
- Tectonic 0.17.0.

The PDF target sets `SOURCE_DATE_EPOCH=1786406400` (2026-08-11 00:00:00 UTC)
so repeated builds of the frozen source are byte-for-byte reproducible.

The GAP producer for the proof-critical certificate fails closed unless the
GAP and TomLib versions match exactly.  The Python checkers pin file hashes,
row inventories, metadata, group orders, maximal-subgroup indices, witness
multiplicities, and the declared finite scope.

[`SHA256SUMS`](SHA256SUMS) additionally pins the manuscript source, built PDF,
and all three committed data files; `make check` verifies it.

## Clean-clone verification

From the repository root, run:

```sh
make check
make regenerate
make paper
git diff --exit-code
```

Equivalently, `make release-check` performs the proof-path tests,
regeneration, PDF build, whitespace check, and generated-artifact comparison.

The commands behind those targets are also listed in `tests/README.md`,
`gap/README.md`, and `paper/README.md`.

## Evidence boundary

The Table-of-Marks files are exact finite certificates relative to the
complete subgroup and intersection data in the named TomLib tables.  They are
not a census of finite groups and are not used to extrapolate any infinite
family.  The universal theorem is conditional on CFSG and on the exhaustive
published maximal-factorization classifications identified in the manuscript
and `references/README.md`.

Source PDFs are not redistributed because their redistribution rights were
not established.  The reference ledger records stable links and SHA-256
hashes for the copies actually audited.
