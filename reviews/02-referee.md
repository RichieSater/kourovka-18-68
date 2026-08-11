# Referee pass 2 — classification completeness and source scope

- **Frozen candidate reviewed:**
  `3bcf19c6ee90042bc392aaac508c559541fae272`
- **Review date:** 2026-08-11
- **Role boundary:** fresh internal source/classification review from a
  detached clean worktree; not external specialist peer review
- **Verdict:** **pass**

## Scope

This pass rebuilt the CFSG family inventory without treating the Revision 2
response or the manuscript's table as proof of completeness. It checked the
stated scope of each classification, inspected the row-by-row containment
ledger, repeated a separate ten-angle literature/correction search, and
rechecked the graph-field symplectic source chain. The elementary deductions
were accepted only after the Round 1 reconstruction.

## Family-by-family audit

### Alternating groups

The degrees (5\le n\le12) are exhaustive: the manuscript gives explicit
elusive actions except for the three exceptional outer groups over (A_6)
and the two groups (A_7,S_7), all of which have complete finite
certificates. For (n\ge13), the 6-set action is maximal because
(6<n/2), and LPS Theorem D/Remark 2 excludes a 6-set stabilizer from every
nontrivial maximal factorization. No exceptional (A_6) automorphism is
silently treated as a natural symmetric action.

### Classical groups

The independent checklist found the same required row ranges:

```text
A.1: 1--10       A.2: 1--16       A.3: 1--12
A.4: 1--8        A.5: 1--5        A.6: 1--13
A.7: 1--15       plus the two GGS correction rows
```

The ledger addresses every row. When the screen (V) is maximal in the
socle, containment in a proper factor intersection forces equality, so type
inequality suffices. The two nonmaximal graph-stable screens contain a Borel,
which restricts their proper overgroups to the stated parabolics. The
rank-one and (L_3(q)) torus rows use order and fixed-subspace arguments,
not a mere comparison of subgroup names. Triality fixes the central-node
(P_2), and the two omitted (P\Omega_8^+(4),P\Omega_8^+(16)) rows do not
contain it.

The even (PSp_4) family is not claimed to follow from this screen. It has a
separate prime-degree subfield action. Burness Proposition 4.2/Table 3
explicitly records the (Sp_4(q_0)) row when (q=q_0^r) and (r) is prime;
Harper identifies BHRD Table 8.14 as the complete maximal-subgroup source and
states the graph-field automorphism structure. LPS Lemmas 2.1--2.2 and
Corollary 2.3 give exactly three involution classes when the symplectic rank
is two and show that every one meets (O_4^+(q)). The manuscript's
prime-field representatives then follow inside the standard
((SL_2(q)\times SL_2(q)).2) model.

### Exceptional groups of Lie type

Hering--Liebeck--Saxl Theorems 1--2 cover the simple groups and their
relevant automorphism groups. The 2023 exact-factorization classification
continues to cite this as the exceptional-family classification; the search
found no later correction. The only factorable socles are the three families
listed in the manuscript, with the one additional outer (G_2(4).2) row.
The defining-characteristic divisibility screen excludes containment in all
listed factors. The derived small Ree/Suzuki parameters are routed through
explicit classical isomorphisms.

### Sporadic groups

Giudici's abstract and Theorems 1.1--1.2 have the necessary scope: all
factorizations for an almost-simple group with sporadic socle. Tables 1--3
cover simple coordinate groups; Table 4 contains new outer cases; Lemma
2.1(5) controls lifting. The ledger identifies the exact table block for each
factorable coordinate group and a maximal subgroup absent from both sides of
that block. The remaining groups have no nontrivial core-free factorization.
The (M_{24}) survivor is handled separately by the 2-elusive 2-subset
action.

## Low-parameter and outer-automorphism audit

The listed low-rank isomorphisms cover every overlap among linear, unitary,
symplectic, and orthogonal notation. The ten groups between (L_3(4)) and
its full automorphism group exhaust the subgroups of its dihedral outer group
up to isomorphism and are all certified. The alternating (A_6) extensions
and the factorable sporadic extensions are named individually. The
symplectic argument uses \(\operatorname{Aut}(Sp_4(2^f))=\langle S,\rho\rangle\)
with \(\rho^2=\varphi\), so every intermediate field-only or graph-field
coordinate group is covered.

No exceptional defining parameter or outer fusion identified in the cited
tables falls outside these routes.

## Independent literature and correction search

A second ten-query search used exact problem-number searches in English and
Russian, citation-chain searches around Levchuk--Likharev and
Maslova--Revin, 2025--2026 product-action/regular-subgroup searches, and
separate correction searches for the classical, exceptional, and sporadic
factorization classifications.

It recovered:

- the July 2026 Notebook, which still prints Problem 18.68 without a solution
  annotation;
- the 2006 simple-group theorem and the 2012/2013 stronger Hall-maximal
  theorem;
- the 2023 complete exact-factorization paper;
- the 2024 GGS correction to the two plus-orthogonal rows;
- Harper's 2024 graph-field description and use of BHRD Table 8.14; and
- current 2026 work on regular subgroups and derangements, none claiming this
  composition-factor theorem.

No indexed solution of Problem 18.68 and no further correction affecting the
screen were found. This only supports the manuscript's carefully dated status
sentence; it does not establish global novelty or current openness outside
the searched literature.

## Source labels and limitations

The candidate correctly distinguishes:

- elementary deductions labeled **proved**;
- CFSG and classification results labeled **published input**;
- complete named-table calculations labeled **computationally certified**;
- the bounded 414-table survey labeled as nonuniversal; and
- the absence of an independently found solution as **unchecked** beyond the
  dated search.

The full BHRD subscription monograph was not locally read page by page. The
specific subfield row is triangulated by two open papers and is precisely
identified. A journal referee with institutional access should still inspect
Table 8.14 directly; this is ordinary verification of a disclosed published
input, not an open proof gap.

## Issues

| ID | Severity | Observation | Status |
|---|---|---|---|
| `R186-F2-01` | P3 | Direct page-by-page local access to BHRD Table 8.14 was unavailable. | Nonblocking: exact locus disclosed and independently corroborated by Burness and Harper; flag for external referee verification. |
| `R186-F2-02` | P3 | A finite search cannot prove that no unindexed solution exists. | Closed by the manuscript's dated, non-novelty wording. |

No missing family, unsupported table scope, unhandled outer group, or open
P0--P2 issue was found.

## Clean-candidate check and verdict

The exact commit was opened in a detached clean worktree and `make check`
passed with the pinned GAP, TomLib, AtlasRep, Python, and Tectonic versions.
The proof PDF and certificate hashes remained those reviewed in Round 1.

The classification/source pass gate is satisfied. The manuscript has an
exhaustive source or a uniform proof for every infinite family and a complete
certificate for every finite exception it delegates to computation. The
appropriate verdict is **pass**, subject to the disclosed CFSG/classification
inputs and future external specialist review.
