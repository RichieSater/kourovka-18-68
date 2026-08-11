# Referee pass 4 — hard-final theorem and release audit

- **Frozen candidate reviewed:**
  `3a39b3d2ec29aab0d0a156aff93d35dc330f567d`
- **Review date:** 2026-08-11
- **Clone mode:** local `git clone --no-local`, detached at the exact candidate
- **Role boundary:** internal adversarial hard-final review; not external
  specialist peer review
- **Recommendation:** **circulate for external specialist review**

## Scope and method

This pass began from a clean fresh clone of the frozen release candidate, not
from the author's Revision 4 working tree. It reread the complete manuscript,
the claim ledger, the classification-containment ledger, the previous referee
reports, and the finite-certificate interfaces. It then regenerated every
committed certificate and the PDF through `make release-check`, rendered all
twelve PDF pages, and checked the final status and disclosure language.

The earlier referee verdicts were treated as audit trails rather than as proof.
This pass specifically reconstructed the arbitrary-composition-factor route
and the replacement for the former graph-outer symplectic argument, the two
places at greatest risk of invalidating the stated universal theorem.

## Theorem-scope reconstruction

The manuscript proves the theorem for an arbitrary nonabelian composition
factor, not merely for a socle chosen in a minimal counterexample:

1. A nonabelian composition factor $S$ is selected through a chief factor
   $A/B\cong S^k$.
2. Quotienting by $C_{G/B}(A/B)$ gives a `CMP` quotient $L$ with unique
   self-centralizing minimal normal subgroup $S^k$. Only quotient closure is
   used; no inheritance to a normal subgroup or section is assumed.
3. The coordinate group $S\leq X\leq\operatorname{Aut}(S)$ is obtained from
   the normalizer of one direct factor. For each supplied core-free maximal
   $H<X$ with $H\cap S\ne1$, the same abstract group $L$ has a faithful
   primitive action on $(X/H)^k$.
4. Scott's lemma closes the intermediate-subgroup argument. The separate
   $k=1$ branch proves core-freeness of a hypothetical regular complement
   from almost simplicity; it no longer asserts that every regular subgroup
   is automatically core-free.
5. A factor-free coordinate action invokes the cited LPS product-action
   theorem. A $p$-elusive action invokes the full-wreath lemma. The remaining
   even-symplectic action invokes the socle-valuation lemma. Each route rules
   out a regular subgroup in the manufactured primitive action, contradicting
   `CMP(L)`.
6. The positive direction needs no extension construction: the cited
   Levchuk--Likharev theorem says that each of the three listed simple groups
   itself has `CMP`.

Thus the conclusion has the same quantifiers as the statement: every
nonabelian composition factor of every finite `CMP` group is one of
$L_2(7),L_2(11),L_5(2)$, conditional on the declared published inputs.

## Recheck of the former P1 defect

The withdrawn subgroup $N_X(\Omega_4^+(q))$ is not used anywhere in the
live proof. For $S=\operatorname{Sp}_4(2^f)$, the candidate instead chooses
a prime $r\mid f$, sets $d=f/r$, and takes the standard subfield subgroup

\[
V=\operatorname{Sp}_4(2^d).
\]

Prime extension degree gives maximality of $V$ in $S$, as a published
classification input. The exceptional graph-field generator satisfies
$\rho^2=\varphi$ and commutes with Frobenius, so it normalizes $V$. Hence,
for every $S\leq X\leq\operatorname{Aut}(S)$, the subgroup
$H=N_X(V)$ satisfies

\[
X=SH,\qquad H\cap S=V,
\]

and the manuscript's two-case overgroup argument proves that $H$ is maximal
and core-free. The three involution classes have representatives
$(u,1),(u,u),\tau$ already defined over
$\mathbb F_2$, so every class meets
$\operatorname{Sp}_4(2)\leq V$. Finally,

\[
a=4(f-d),\qquad
o\leq 1+v_2(f)<2f\leq4(f-d)=a,
\]

which closes every field-only or graph-outer coordinate group and every
socle multiplicity $k$.

At the original countercheck point
$X=\operatorname{Aut}(\operatorname{Sp}_4(4))$, the regenerated AtlasRep
test gives

\[
|H|=2880,\qquad |H\cap S|=720,\qquad |X:H|=1360,
\]

and verifies that all three involution classes meet $H\cap S$. These data
are a regression test for the replacement, not the proof of the infinite
family.

## Classification, exceptions, and finite computation

The alternating, classical, exceptional, and sporadic partitions agree
between the manuscript and the containment ledger. Low-rank isomorphisms,
the three exceptional outer groups over $A_6$, all ten coordinate groups
over $L_3(4)$, graph automorphisms, triality, and the two corrected
$P\Omega_8^+(4)$ and $P\Omega_8^+(16)$ factorization rows are routed
explicitly. No finite scan is used to extrapolate an infinite-family claim.

The proof delegates exactly fifteen small coordinate groups to complete
Table-of-Marks certificates: five alternating cases and ten $L_3(4)$
cases. The nine sporadic certificate rows are correctly described as
cross-checks. The finite producer searches all core-free factor classes and
all intersection classes for each pinned row; its independent checker binds
the resulting file and verifies the arithmetic and completeness conditions.

## Fresh-clone release reproduction

`make release-check` returned zero in the detached fresh clone and left it
clean. The enforced environment was:

```text
GAP       4.15.1
TomLib    1.2.11
AtlasRep  2.1.11
Python    3.14.6
Tectonic  0.17.0
```

The run regenerated 414 Table-of-Marks summaries, 2,395 maximal-class rows,
73 `CMP`-positive tables, and 24 pinned factor-free rows. It also reran the
three direct GAP tests, both Python certificate checkers, fail-closed checks,
seven mutation controls, two byte-compared deterministic PDF builds, the
release receipt, and `git diff --check`.

The regenerated hashes were:

```text
TeX
d01d3a0212eaf1b965f25d5076254b6500933c13c2bb95665b5f4aeedf7d81f4
PDF
9fa44095bcfde9c0592b6bdd7529f86da7e31ed59d875cf5a63a72eadc3948fb
CMP summary
318ac4d55cde05e3e046497eba31b005ebe16832d1be59df98b5e48f9b951320
CMP maximal rows
ed322a51f286f104c4adc057c0b06a6cdbf8c3300f71e9bab8d6950071882b16
factor-free rows
9b131720d41ef945a0696794c0493ae9c07e166d4d1f37b054a1d55f0c4837ae
```

The PDF has twelve letter-size pages. Rendering and visual inspection found
no clipping, overflow, missing formula, broken table, or disclosure/reference
collision.

## Disposition of earlier findings

| Earlier item | Final disposition |
|---|---|
| `R186-PR1-01` (P1) | Closed by the prime-degree subfield construction and valuation proof above. |
| `R186-PR1-02` (P2) | Closed by the separate almost-simple $k=1$ core argument. |
| `R186-PR1-03` (P2) | Closed by the row-by-row source and containment ledger, independently checked in Round 2. |
| `R186-PR1-04` (P2) | Closed by `--quitonbreak`, explicit version gates, optimized Python runs, independent checkers, and mutation controls. |
| `R186-PR1-05` (P3) | Terminology and rank-one factor descriptions are corrected. |
| `R186-PR1-06` (P3) | Closed by the deterministic build wrapper, receipt, release checker, metadata cleanup, and AI-use disclosure. |
| `R186-F1-02` (P3) | The response-file `\qquad` typo is corrected and recorded without altering the historical verdict. |

No open P0, P1, or P2 issue was found.

## What remains trusted or unverified

- CFSG is a declared published input, not reproved here.
- The exhaustive maximal-factorization classifications and the LPS
  product-action theorem are trusted at their cited scopes. Round 2 audited
  their family and exception routing, but this internal pass did not recreate
  those classification proofs.
- BHRD Table 8.14 was not available for a direct local page-by-page check.
  Its exact prime-degree subfield row is triangulated by Burness and Harper;
  an external referee with book access should inspect it directly.
- The computations are exact relative to the pinned GAP package data; they do
  not independently prove the correctness of TomLib or AtlasRep themselves.
- The July 2026 literature-status sentence is dated and deliberately does not
  claim absolute novelty or rule out unindexed or contemporaneous work.
- No independent external finite-group specialist has yet reviewed the proof.
  The four internal passes must not be described as journal peer review.

## Recommendation

The corrected candidate supplies a coherent proof path from an arbitrary
composition factor to the stated three-group list, closes the former
graph-outer infinite-family gap uniformly, binds every finite claim to a
reproducible certificate, and clearly states its dependencies and publication
status. All release checks pass and no P0--P2 issue remains. The appropriate
Round 4 recommendation is therefore **circulate for external specialist
review**.
