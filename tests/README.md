# Tests

Run:

```sh
gap --quitonbreak -q tests/test-cmp-tom.g
gap --quitonbreak -q gap/generate-tomlib-scan.g
python3 tests/check-tomlib-scan.py
gap --quitonbreak -q tests/test-factor-free-tom.g
gap --quitonbreak -q gap/generate-factor-free-scan.g
python3 tests/check-factor-free-scan.py
gap --quitonbreak -q tests/test-sp4-subfield.g
python3 scripts/check-public-corpus.py
python3 tests/test-mutation-controls.py
tests/test-fail-closed.sh
```

The GAP suite checks the three published positive simple groups; negative
controls `A5`, `S5`, `L2(7).2`, and `(A5xA5):2`; the zero-candidate failure
for the index-28 maximal of `L2(7).2`; and the normal-inheritance pair
`C4 <| D8` using tables computed directly by GAP.

The Python checker independently parses both generated TSVs, checks all 414
summary rows against all 2,395 maximal rows, verifies order arithmetic and
witness multiplicities, and checks the published simple fixtures and the
nonabelian chief-factor order spectrum.

The factor-free GAP tests include a positive factorization control, a
negative control, and an outer almost-simple socle/intersection control. The
Python checker pins all 24 rows, their maximal orders and indices, nontrivial
socle intersections, metadata, and SHA-256.

The symplectic regression reconstructs the corrected maximal subfield
normalizer for `S4(4).4` under AtlasRep 2.1.11 and checks its degree,
supplement property, normalizer property, 2-valuations, and involution-class
coverage. `test-fail-closed.sh` verifies that GAP errors return nonzero and
runs the evidence-critical Python checkers under optimization; the checkers
use explicit exceptions rather than optimization-sensitive assertions.

The public-corpus checker scans every tracked text file and extracts the
tracked PDF. With `--paths-file` it scans the explicit release allowlist;
with `--archive` it safely extracts and scans every member, rejects special
or nested archive members, and can require exact agreement with that
allowlist. It enforces the publication-language boundary, the unique
manuscript disclosure, and standard subgroup-index notation.

`test-mutation-controls.py` copies proof certificates, checkers, producer
scripts, the PDF, and the build receipt into isolated temporary trees. Its
65 mutations cover byte and semantic corruption, missing data, receipt/PDF
changes, stale TeX/PDF pairs, structurally invalid or inconsistent CFF and CI
metadata, forced producer-version failures, prohibited process and
conditional-publication wording, model-named and duplicate disclosure
terminology, styled subgroup-index failures, forbidden tracked paths, symbolic
links, archive identity and Git binding, manifest digests, and artifact-sidecar
digests. Failed producers must remove stale outputs.
