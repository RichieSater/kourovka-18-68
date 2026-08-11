# Internal audit of the complete candidate proof

**Date:** 2026-08-11
**Status:** complete internal audit; independent external review pending

## Verdict

The manuscript [`../paper/kourovka-18-68.tex`](../paper/kourovka-18-68.tex)
contains a section-safe, CFSG-conditional proof that the nonabelian
composition factors are exactly

\[
L_2(7),\qquad L_2(11),\qquad L_5(2).
\]

The earlier arbitrary-power obstruction is removed rather than assumed away.
No assertion that `CMP` passes to a normal subgroup or arbitrary section is
used.

## Structural audit

1. **Quotients:** `CMP` is proved quotient closed by projecting an exact
   complement to the full preimage of a quotient maximal subgroup.
2. **Arbitrary composition factors:** a chief factor (S^k) produces a
   quotient with unique self-centralizing minimal normal subgroup (S^k).
3. **Coordinate action:** for each core-free maximal (H<X) with
   (H\cap S\ne1), the same quotient acts faithfully and primitively on
   ((X/H)^k).  The intermediate-subgroup proof treats both product and
   diagonal subdirect intersections via Scott's lemma.
4. **Unbounded (k):** LPS (2000), Corollary 3(iv), forces a core-free
   transitive subgroup in the almost-simple coordinate action whenever the
   product action has a regular subgroup.

## Classification audit

- **Alternating:** explicit elusive actions cover degrees at most 12 except
  five complete Table-of-Marks rows; LPS Theorem D covers every (n\ge13)
  with a 6-set stabilizer.
- **Classical:** Xia--Li Theorem 2.15 and Tables A.1--A.7, together with the
  two Gill--Giudici--Spiga corrected orthogonal rows, are filtered by
  automorphism-invariant geometric subgroups.  The rank-one exceptional
  parameters are checked by orders.  A split-torus normalizer handles
  (L_3(q)); all ten coordinate groups at (q=4) have complete finite
  certificates.
- **Exceptional:** Hering--Liebeck--Saxl Theorems 1--2 are exhaustive.  In
  graph-fused (G_2(3^f)) and (F_4(2^f)), defining-characteristic parts
  exclude containment in every listed factor.
- **Sporadic:** Giudici Theorems 1.1--1.3 and the Atlas maximal lists give
  factor-free rows.  (M_{24}) is closed by its 2-elusive action on
  2-subsets.

## Prime/divisibility audit

The only infinite factor-screen survivor is
(S=\operatorname{PSp}_4(2^f)).  With
(H=N_X(\Omega_4^+(2^f))), LPS gives
(H\cap S=O_4^+(2^f)), and this subgroup meets every involution class.
The action has

\[
v_2(|X:H|)=2f-1,
\qquad v_2(|X:S|)\le 1+v_2(f)<2f-1.
\]

For a hypothetical regular subgroup (R) in (k) coordinates, this forces
(R\cap S^k) to have even order.  Its involution fixes a tuple, contradicting
regularity.  This is uniform in both (f\) and (k).

## Computational audit

The proof-critical finite range is exactly 15 named almost-simple groups:
five alternating rows and ten (L_3(4)) rows.  Nine sporadic rows are
cross-checks.  GAP exhausts every core-free subgroup class and every possible
intersection class in each complete table of marks, and fails closed on
missing data.  The TSV SHA-256 is

```text
82bcf695617014f0124839c5a01983a6c8904fc5bc92e0893c9c2601c43bd3a0
```

## Remaining review risk

What remains is human verification of the family-by-family containment
filter against the cited printed tables and independent checking of the
standard maximal-subgroup assertions.  That is a peer-review task, not a
known mathematical gap in the current argument.
