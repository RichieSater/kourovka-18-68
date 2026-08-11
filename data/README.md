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

Producers, run from `problem-18-68/`:

```sh
gap --quitonbreak -q gap/generate-tomlib-scan.g
gap --quitonbreak -q gap/generate-factor-free-scan.g
```

Environment: GAP 4.15.1; TomLib 1.2.11. Generated on macOS/arm64 on
2026-08-11.  The producer command and both versions are embedded in each
file; exact-version checks run before any output is retained. Current
SHA-256 hashes:

```text
318ac4d55cde05e3e046497eba31b005ebe16832d1be59df98b5e48f9b951320  tomlib-cmp-scan.tsv
ed322a51f286f104c4adc057c0b06a6cdbf8c3300f71e9bab8d6950071882b16  tomlib-cmp-maximals.tsv
9b131720d41ef945a0696794c0493ae9c07e166d4d1f37b054a1d55f0c4837ae  tomlib-factor-free.tsv
```

**Scope label:** computationally certified relative to the complete tables
shipped by TomLib. TomLib is a finite library, not an exhaustive list of all
finite groups.  The universal proof uses it only for explicitly named finite
rows; published classifications supply every infinite-family statement.
