# Initial solution candidate

- **Problem:** Kourovka 18.68
- **Candidate commit:** `915e4c4487aa5ed4fcd753b51ea07916a9aaf3ea`
- **Date frozen:** 2026-08-11
- **Claimed result:** the nonabelian composition factors are precisely
  \(L_2(7),L_2(11),L_5(2)\)
- **Evidence status:** proved in the manuscript conditional on CFSG and the
  named published factorization classifications; not externally reviewed or
  published

## Exact statement and convention

The exact statement is Theorem 1.1 of
[`paper/kourovka-18-68.tex`](../paper/kourovka-18-68.tex). A complement to
\(M\leq G\) means a subgroup \(K\leq G\) such that \(G=MK\) and
\(M\cap K=1\). Consequently \(|K|=\lvert G:M\rvert\).

## Literature and status boundary

The dated ten-angle search and its limitations are recorded in
[`notes/01-literature-status.md`](../notes/01-literature-status.md). The July
2026 Kourovka Notebook still states the problem without a solution note. No
complete solution was found, but this negative search does not establish
novelty, priority, or the absence of unindexed work.

## Main theorem and dependency graph

1. Property `CMP` passes to arbitrary quotients, but not to normal subgroups.
2. A nonabelian composition factor \(S\) yields a `CMP` quotient with unique
   self-centralizing socle \(S^k\).
3. For a suitable core-free maximal subgroup of the almost-simple coordinate
   group, the same quotient has a faithful primitive product action.
4. Liebeck--Praeger--Saxl Corollary 3(iv) turns a regular subgroup in that
   product action into a core-free transitive subgroup in the coordinate
   action.
5. Published exhaustive maximal-factorization classifications supply a
   factor-free or prime-elusive coordinate action for every simple \(S\)
   outside \(L_2(7),L_2(11),L_5(2)\).
6. A separate 2-adic argument closes the surviving
   \(\operatorname{PSp}_4(2^f)\) family for every \(k\).
7. Levchuk--Likharev's simple-group theorem shows that each of the three
   listed factors occurs.

## Evidence and reproducibility

- Claim labels and dependencies:
  [`CLAIM-LEDGER.md`](../CLAIM-LEDGER.md).
- Source URLs, pinpoints, and audited hashes:
  [`references/README.md`](../references/README.md).
- Proof-critical finite certificate: five small alternating coordinate groups
  and ten groups with socle \(L_3(4)\).
- Bounded cross-check: all 414 tables and 2,395 maximal-subgroup classes in
  TomLib 1.2.11.

The following commands succeeded before the candidate was frozen, using GAP
4.15.1, TomLib 1.2.11, Python 3.14.6, and Tectonic 0.17.0:

```sh
make check
cd problem-18-68
gap -q tests/test-cmp-tom.g
gap -q gap/generate-tomlib-scan.g
python3 tests/check-tomlib-scan.py
gap -q tests/test-factor-free-tom.g
gap -q gap/generate-factor-free-scan.g
python3 tests/check-factor-free-scan.py
cd paper && tectonic kourovka-18-68.tex
```

## Known limitations

- The candidate has not passed any of the four required internal referee
  rounds.
- External finite-group-specialist peer review is outstanding.
- The proof trusts CFSG and the stated published classifications; it does not
  reprove them.
- Several standard geometric-maximality and Atlas comparisons still require
  independent referee checking against the original sources.

## Initial-solution exit checklist

- [x] Complete proof-draft result rather than an intentionally partial route.
- [x] Claim ledger separates proved, published, computational, and unchecked
      statements.
- [x] Infinite-family claims are routed through named exhaustive sources.
- [x] Finite proof rows have committed, reproducible certificates.
- [x] Manuscript and project README state the same claimed scope.
- [x] Exact candidate commit frozen before the referee pass.
