# Generated data

## Files

- [`tomlib-cmp-scan.tsv`](tomlib-cmp-scan.tsv): one summary row for each of
  the 414 TomLib tables.
- [`tomlib-cmp-maximals.tsv`](tomlib-cmp-maximals.tsv): one row for each of
  the 2,395 maximal-subgroup classes, including every candidate complement
  class and its trivial-intersection multiplicity.
- [`tomlib-factor-free.tsv`](tomlib-factor-free.tsv): 24 pinned maximal
  classes with no core-free transitive factor.  Fifteen rows are
  proof-critical finite closeouts and nine are sporadic cross-checks.

Producers, run from the repository root:

```sh
gap -q gap/generate-tomlib-scan.g
gap -q gap/generate-factor-free-scan.g
```

Environment: GAP 4.15.1; TomLib 1.2.11. Generated on macOS/arm64 on
2026-08-11. Current SHA-256 hashes:

```text
e8057a728dca589e6c431cc9779ce02b37f8a5daac83a0be879e98ba8bc6f9b4  tomlib-cmp-scan.tsv
adbd9590e769136eab7fea84139de0bec2f068252a68228e454066cc7f473c55  tomlib-cmp-maximals.tsv
82bcf695617014f0124839c5a01983a6c8904fc5bc92e0893c9c2601c43bd3a0  tomlib-factor-free.tsv
```

**Scope label:** computationally certified relative to the complete tables
shipped by TomLib. TomLib is a finite library, not an exhaustive list of all
finite groups.  The universal proof uses it only for explicitly named finite
rows; published classifications supply every infinite-family statement.
