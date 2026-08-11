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
negative control, and an outer almost-simple socle/intersection control.  The
Python checker pins all 24 rows, their maximal orders and indices, nontrivial
socle intersections, metadata, and SHA-256.

The symplectic regression reconstructs the corrected maximal subfield
normalizer for `S4(4).4` under AtlasRep 2.1.11 and checks its degree,
supplement property, normalizer property, 2-valuations, and involution-class
coverage.  `test-fail-closed.sh` verifies that GAP errors return nonzero and
runs both acceptance-critical Python checkers with `python3 -O`; the checkers
use explicit exceptions rather than optimization-sensitive assertions.

`test-mutation-controls.py` copies the proof certificates, checkers, producer scripts, PDF, and build receipt into isolated temporary trees. It verifies that byte/semantic corruption, missing data, receipt/PDF changes, and forced producer-version failures are rejected; failed producers must remove stale outputs.
