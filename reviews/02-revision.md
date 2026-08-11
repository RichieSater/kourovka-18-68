# Revision 2 — classification and source audit

- **Revision date:** 2026-08-11
- **Predecessor:** Referee 1 pass at `reviews/01-referee.md`
- **Mathematical base:** `580255e809726fd224b75382220f7197612d81c2`
- **Role boundary:** author-side classification/source audit; not a referee
  verdict and not external peer review

## Purpose

Revision 1 had to replace an invalid infinite-family subgroup, so it already
added the row-by-row classification ledger that this protocol round would
normally request. This round rereads that ledger as a source audit, fixes the
scope assigned to each publication, repeats the current literature search,
and records every low-parameter and outer-automorphism route. No theorem or
formula in the manuscript needed a further change.

## Exhaustive source map

| Proof region | Exhaustive published input | Exact locus used |
|---|---|---|
| Product-action coordinate obstruction | Liebeck--Praeger--Saxl, *J. Algebra* 234 (2000) | Corollary 3(iv) |
| Alternating socles | Liebeck--Praeger--Saxl, Memoirs AMS 86 (1990) | Theorem D and Remark 2 |
| Classical socles | Xia--Li, Memoirs AMS 279 (2022) | Theorem 2.15 and Tables A.1--A.7 |
| Omitted plus-orthogonal rows | Gill--Giudici--Spiga (2024) | Section 2 and Table 2 |
| Exceptional Lie-type socles | Hering--Liebeck--Saxl (1987) | Theorems 1--2 |
| Sporadic socles and outer extensions | Giudici (2006) | Theorems 1.1--1.2, Tables 1--4, and Lemma 2.1(5) |
| Even (\operatorname{Sp}_4) subfield maximality | Bray--Holt--Roney-Dougal (2013) | Table 8.14; independently restated in Burness Proposition 4.2/Table 3 |
| Even (\operatorname{Sp}_4) outer automorphisms | Harper (2024) | Lemma 2.1 |
| Even (\operatorname{Sp}_4) involutions | Liebeck--Praeger--Saxl, Memoirs AMS 203 (2010) | Lemmas 2.1--2.2 and Corollary 2.3 |
| Positive simple examples | Levchuk--Likharev (2006) | Theorem 1 |

The manuscript does not ask the 2023 exact-factorization classification to do
work beyond the older maximal-factorization tables. It remains in the
reference ledger as an independently audited orientation source, not an
unstated proof dependency.

## Independent family inventory

CFSG gives alternating groups, classical groups, exceptional groups of Lie
type, and the sporadic groups.

1. **Alternating groups.** Degrees (5\) through (12) are handled by
   explicit elusive actions or five complete TomLib certificates. For
   (n\ge13), the 6-set stabilizer is maximal and Theorem D restricts an
   intransitive factor in a maximal factorization to a (j)-set stabilizer
   with (j\le5), apart from exceptions already below degree 13. The
   exceptional automorphism groups over (A_6) are listed individually.
2. **Classical groups.** The ledger checks every row A.1:1--10,
   A.2:1--16, A.3:1--12, A.4:1--8, A.5:1--5, A.6:1--13, and A.7:1--15,
   followed by the two GGS correction rows. Each screen records containment,
   not just nonequality, and explains invariance under all relevant outer
   automorphisms.
3. **Exceptional groups.** Hering--Liebeck--Saxl leave only
   (G_2(4)), (G_2(3^f)), and (F_4(2^f)) as factorable socles, plus one
   new outer (G_2(4).2) factorization. Parabolic screens close these rows;
   in graph-fused cases the intersections (P_1\cap P_2) and
   (P_1\cap P_4) contain a Borel, and their defining-characteristic parts
   are too large to lie in any listed factor.
4. **Sporadic groups.** Tables 1--3 of Giudici treat simple coordinate
   groups; Table 4 treats genuinely new outer factorizations; Lemma 2.1(5)
   supplies the lifted simple rows. Every factorable coordinate group has a
   named maximal screen in the ledger. (M_{24}), the only factor-cover
   survivor, is closed by its degree-276 2-subset action.
5. **Even symplectic rank two.** The prime-degree subfield action is separate
   from the classical factor screen. Its maximality, graph-field invariance,
   involution coverage, and strict 2-adic inequality are all separately
   sourced or proved.

## Low parameters and outer automorphisms

The audit explicitly routes

\[
L_2(4)\cong L_2(5)\cong A_5,\quad L_2(9)\cong A_6,\quad
L_3(2)\cong L_2(7),\quad L_4(2)\cong A_8,\quad
U_4(2)\cong PSp_4(3),
\]

together with the standard (B_2=C_2), (D_3=A_3), and
\({}^2D_3={}^2A_3\) identifications. The ten coordinate groups over
(L_3(4)), all four coordinate groups over (A_6), and every factorable
sporadic outer extension are enumerated rather than inferred by analogy.
Triality is handled with the central-node (P_2) screen. Graph-field
coordinates over (\operatorname{Sp}_4(2^f)) are handled by the subfield
normalizer, not by the withdrawn orthogonal normalizer.

## Ten-angle literature refresh

The following ten searches were executed on 2026-08-11, using English,
Russian, citation, exact-phrase, recent-work, and adjacent-classification
angles:

1. `Kourovka Problem 18.68 complemented maximal subgroups solution nonabelian composition factors`
2. `Коуровская тетрадь проблема 18.68 дополнения максимальных подгрупп решение`
3. `"Finite simple groups with complemented maximal subgroups" citations Levchuk Likharev`
4. `"nonabelian composition factors" "maximal subgroups" complemented finite group`
5. `"every maximal subgroup has a complement" finite groups composition factors`
6. `Maslova Revin "Hall property" complemented maximal subgroups Kourovka 18.68`
7. `2024 2025 2026 "regular subgroups of primitive groups" product action finite groups`
8. `"Corollary 3(iv)" "Transitive subgroups of primitive permutation groups"`
9. `2023 exact factorizations almost simple groups Li Wang Xia arXiv 2012.09551`
10. `Sp4(2^f) graph field automorphism subfield subgroup Sp4(q0) maximal involution classes O4+`

The search recovered the original simple classification, the stronger
Hall-maximal result, the 2000/2010 primitive-group inputs, the 2023 exact-
factorization classification, the 2024 GGS correction and Harper paper, and
current 2025--2026 work on regular subgroups and derangements. It found no
indexed paper claiming a solution of Problem 18.68. The July 2026 official
Notebook still prints the problem without a solution annotation. This is a
dated search result, not proof that no unindexed or contemporaneous solution
exists, and the manuscript says exactly that.

## Source-integrity boundary

The locally audited PDFs and hashes are recorded in
`references/README.md`. In particular:

```text
LPS regular-subgroup memoir  00a76f52b998f4017127c5c4e5e971b36501475092f402cf7bff3e84f222c03b
Xia--Li                      4ef16aa4308f8c487a06e9c8e84ece77247d0e763146f0215d8e109e443e3a93
Burness 2007                 dcf25d06cf433dfa32734d6ceb7289f8913d34e8ba2360a89c0a520302bd31bf
Harper 2024                  b741f7dfecd2dc78d37a7f2a9d5a5bb928eceb94cde290193980a1ee6d3ff522
```

The subscription BHRD book was not locally audited page by page. Its precise
Table 8.14 row is corroborated by the open Burness table, while Harper
identifies Table 8.14 as the complete source for these maximal subgroups.
That disclosed reliance on a standard published classification is acceptable
for a submission; it is not represented as a machine-verified fact.

## Disposition

No missing CFSG family, low parameter, outer coordinate group, or known table
correction remains in the audit. The detailed evidence is
`notes/07-classification-containment-ledger.md`; the concise argument remains
in Proposition 5.1 of the manuscript. The exact post-audit candidate will be
the commit containing this response and is to be read afresh by Referee 2.
