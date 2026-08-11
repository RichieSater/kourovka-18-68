# Referee pass 1 — logical and structural correctness

- **Frozen candidate reviewed:**
  `580255e809726fd224b75382220f7197612d81c2`
- **Review date:** 2026-08-11
- **Role boundary:** fresh internal adversarial review from a detached clean
  worktree; not external specialist peer review
- **Verdict:** **pass**

## Scope

This pass reread the complete theorem rather than accepting the Revision 1
response as evidence. It reconstructed the quotient and chief-factor
reductions, the product-action construction, the two obstructions to a
regular subgroup, and the replacement for the defective graph-outer
symplectic argument. The detailed completeness and source-scope audit is
reserved for Referee 2, and reproducibility is reserved for Referee 3.

## Independent reconstruction

1. **Only quotients inherit `CMP`.** If a maximal subgroup of (G/N) has
   full preimage (M), then (N\le M). A complement (K) to (M) maps
   injectively to an exact complement in (G/N). No section or normal-
   subgroup inheritance is used.
2. **Every chosen nonabelian chief factor yields the required quotient.**
   For (A/B\cong S^k), quotienting by (C_{G/B}(A/B)) produces a `CMP`
   group (L) with unique minimal normal subgroup (N\cong S^k) and
   (C_L(N)=1). The uniqueness argument uses commutation of distinct minimal
   normal subgroups and does not assume the desired theorem.
3. **The coordinate action really is primitive.** In the wreath embedding,
   the point stabilizer meets (N) in (V^k). For an intermediate subgroup
   (J), the projections of (J\cap N) are all (V) or all (S). In the
   latter case Scott's lemma makes (J\cap N) a product of diagonal strips;
   (V^k\le J\cap N) and (V\ne1) force every strip to have length one.
   Hence the point stabilizer is maximal. Core-freeness of the coordinate
   subgroup gives faithfulness.
4. **The (k=1) case no longer assumes regular implies core-free.** If a
   regular subgroup (R<X) had nontrivial core, that core would contain the
   socle (S). This is incompatible with (R\cap H=1) and
   (1\ne H\cap S). For (k\ge2), the quoted LPS Corollary 3(iv) supplies
   the coordinate obstruction.
5. **The valuation obstruction closes all socle powers.** If (R) were
   regular and (Q=R\cap S^k), then

   \[
   v_p(|Q|)\ge k(a-o)-v_p(k!)>0.
   \]

   Cauchy's theorem gives an element of order (p) in (Q); coordinatewise
   (p)-elusiveness makes it fix a tuple, contradicting regularity.
6. **The new symplectic subgroup survives graph-field automorphisms.** For
   (S=\operatorname{Sp}_4(2^f)), choose a prime (r\mid f), set
   (d=f/r), and take (V=\operatorname{Sp}_4(2^d)). Prime extension
   degree gives maximality in (S). Since the exceptional endomorphism
   satisfies \(\rho^2=\varphi\), it commutes with Frobenius and normalizes
   the \(\varphi^d\)-fixed subgroup (V). Thus, for every
   (S\le X\le\operatorname{Aut}(S)), (H=N_X(V)) satisfies
   (X=SH), (H\cap S=V), and is maximal and core-free.
7. **Involution coverage is uniform, not extrapolated from (q=4).** The
   three symplectic involution classes meet (O_4^+(q)), and representatives
   ((u,1),(u,u),\tau) are already defined over \(\mathbb F_2\). Therefore
   every class meets (\operatorname{Sp}_4(2)\le V). Finally

   \[
   a=4(f-d),\qquad o\le1+v_2(f)<2f\le4(f-d),
   \]

   so the valuation lemma applies to every coordinate group and every (k).

## Edge and counterexample checks

- The referee's old subgroup in
  (X=\operatorname{Aut}(\operatorname{Sp}_4(4))) remains explicitly
  withdrawn; no argument silently reuses it.
- At the smallest new parameter (f=2,r=2,d=1), the strict valuation margin
  is (a-o=4-2=2).
- The AtlasRep regression reconstructs the replacement subgroup with

  \[
  |H|=2880,\quad |H\cap S|=720,\quad |X:H|=1360,
  \]

  and verifies all three involution classes meet (H\cap S).
- An independent integer enumeration for (2\le f\le10{,}000) and every
  prime divisor (r\mid f) found minimum valuation margin (2), attained at
  (f=r=2). This is only a sanity check; the displayed inequality is the
  proof.
- The (k=1) and (k\ge2) branches are disjoint and exhaustive. The
  hypotheses (1<V<S) are present wherever the product action is invoked.

## Clean-candidate verification

The commit was checked in a detached clean worktree. `make release-check`
passed under GAP 4.15.1, TomLib 1.2.11, AtlasRep 2.1.11, Python 3.14.6, and
Tectonic 0.17.0. It regenerated all finite data, ran the fail-closed
controls, built the PDF twice in deterministic mode, and left the worktree
clean. The reviewed hashes were:

```text
TeX  3913cafcfc2fa8792176921008a8b39db68b72d0533bf66d7cbc8fa092d67757
PDF  a48359e6d3be55e914216001cfddba33d316e79989a0aca02928f62f3de8f798
TSV  9b131720d41ef945a0696794c0493ae9c07e166d4d1f37b054a1d55f0c4837ae
```

All twelve PDF pages were also rendered and visually inspected; no clipping,
overflow, missing reference, or malformed formula was found.

## Issues

| ID | Severity | Observation | Status |
|---|---|---|---|
| `R186-F1-01` | P3 | Maximality of the prime-degree subfield subgroup is a published classification input rather than an elementary deduction. | Correctly labeled and deferred to the source-scope pass; BHRD Table 8.14 is corroborated by Burness Proposition 4.2/Table 3 and Harper's use of the same table. |
| `R186-F1-02` | P3 | The response file has a harmless missing backslash before one `\qquad`; the mathematical manuscript and PDF are unaffected. | Carry to the hard-final editorial cleanup. |

No P0, P1, or P2 logical/structural issue is open. All six findings in the
pre-revision report are either mathematically answered or assigned to their
later protocol pass.

## Verdict rationale

The original acceptance-level defect is repaired by a different subgroup,
and the repair covers the full infinite family, all graph-field coordinate
groups, and arbitrary socle multiplicity. The proof reaches an arbitrary
composition factor using quotient closure and a newly manufactured primitive
action, not an invalid section argument. The Round 1 pass gate is therefore
satisfied. This verdict does not replace the classification/source,
fresh-clone, hard-final, or external-specialist reviews.
