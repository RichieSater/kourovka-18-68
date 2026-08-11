# Exhaustive family factor screen

**Status:** the reduction to the rows below is **proved** in
[`04-product-action-lifting.md`](04-product-action-lifting.md).  The
factorization lists and standard maximal-subgroup descriptions are
**published input**.  The five marked small alternating rows are
**computationally certified** by complete tables of marks.  This note is an
audit of every CFSG family, not a bounded search.

## 1. Published exhaustive inputs

1. Liebeck--Praeger--Saxl (LPS), *The maximal factorizations of the finite
   simple groups and their automorphism groups*, Memoirs AMS 86 (1990),
   no. 432.
2. Xia--Li, arXiv:1408.0350, Theorem 2.15 and Appendix Tables A.1--A.7,
   which restate the LPS maximal factorizations for almost-simple classical
   groups, including the precise intersections with the socle.
3. Gill--Giudici--Spiga, *Vietnam J. Math.* 52 (2024), Section 2, which
   supplies the two maximal factorizations with socle
   (\operatorname{P}\Omega_8^+(4)) or
   (\operatorname{P}\Omega_8^+(16)) omitted from the original LPS table.
4. Hering--Liebeck--Saxl, *J. Algebra* 106 (1987), Theorems 1--2, for all
   factorizations of exceptional simple groups and their automorphism
   groups.
5. Giudici, *J. Algebra* 304 (2006), Theorems 1.1--1.2 and Tables 1--4,
   for all factorizations with sporadic socle.

Exact table-row coverage, containment arguments, outer behavior, maximality
sources, and low-parameter routing are recorded separately in
[`07-classification-containment-ledger.md`](07-classification-containment-ledger.md).

Here (P_i) denotes a standard maximal parabolic, (P_{ij}=P_i\cap P_j)
with a common Borel, and (N_i) a nonsingular-subspace stabilizer, in the
notation of LPS and Xia--Li.

## 2. Alternating socles

For (n\ne6), the coordinate group is (A_n) or (S_n).  The following
table supplies either a factor-free primitive action (F) or a (p)-elusive
primitive action (E).

| Socle / coordinate group | Action | Type | Verification |
|---|---|---:|---|
| (A_5\le X\le S_5) | 2-subsets, degree 10 | E, (p=2) | an involution fixes the support of one 2-cycle |
| (X=A_6) | natural degree 6 | E, (p=2) | every (A_6)-involution is a double transposition |
| (X=S_6) | unordered (3+3) partitions, degree 10 | E, (p=2) | check cycle types (2,2^2,2^3) |
| (A_6.2_2,A_6.2_3,A_6.2^2) | TomLib maximal of index (45,36,45) | F | finite certificate |
| (A_7,S_7) | TomLib maximal of index 35 | F | finite certificate |
| (A_8\le X\le S_8) | 2-subsets, degree 28 | E, (p=2) | support of a 2-cycle |
| (A_9\le X\le S_9) | 2-subsets, degree 36 | E, (p=2) | support of a 2-cycle |
| (A_{10}\le X\le S_{10}) | 4-subsets, degree 210 | E, (p=2) | every involution has an invariant union of two 2-cycles, or one 2-cycle plus two fixed points |
| (A_{11}\le X\le S_{11}) | 3-subsets, degree 165 | E, (p=3) | support of one 3-cycle |
| (A_{12}\le X\le S_{12}) | 2-subsets, degree 66 | E, (p=2) | support of a 2-cycle |
| (n\ge13) | 6-subsets | F | LPS Theorem D: an intransitive factor in a maximal factorization stabilizes a (k)-set with (k\le5) |

For (n\ge13), the 6-set stabilizer is maximal because (6<n/2).  The
small factor-free certificates are in
[`../data/tomlib-factor-free.tsv`](../data/tomlib-factor-free.tsv).

## 3. Classical socles

The next table gives (V<S) for Lemma 4.4.  Its conjugacy class is invariant
under the relevant coordinate group (X).  When a graph automorphism fuses
two parabolic classes, the intersection shown is graph-stable.  Standard
small isomorphisms are routed to the alternating or earlier classical rows.

| Socle (S) | Conditions | Screen subgroup (V) | Maximal-factor table check |
|---|---|---|---|
| (\operatorname{PSL}_2(q)) | simple, excluding (q=7,11) and alternating isomorphisms | normalizer of a split torus | A.1:1 supplies the nonsplit-torus factor and (P_1); A.1:5--8 are the displayed small factors; the split normalizer lies in none of them |
| (\operatorname{PSL}_3(q)) | (q\ne4), excluding the allowed (q=2) | normalizer of a maximally split torus | not in (P_1), (P_2), or the extension-field factor in A.1 |
| (\operatorname{PSL}_3(4)) | every (X) | pinned maximal subgroup | all ten coordinate groups are certified by complete tables of marks |
| (\operatorname{PSL}_n(q)) | even (n\ge4) | (P_{n/2}) | absent from A.1 |
| (\operatorname{PSL}_n(q)) | odd (n\ge5), no graph | (P_2) | absent from A.1 except ((n,q)=(5,2)) |
| (\operatorname{PSL}_n(q)) | odd (n\ge5), graph present | (P_{2,n-2}) | only proper overgroups (P_2,P_{n-2}); absent except ((5,2)) |
| (\operatorname{PSp}_{2m}(q)) | (m\ge3) | (P_2) | absent from A.2 |
| (\operatorname{PSp}_4(q)) | (q) odd | stabilizer of a nonsingular (2+2) decomposition | absent from A.2 |
| (\operatorname{PSp}_4(2^f)) | (f\ge2) | prime-degree subfield (V=\operatorname{Sp}_4(2^{f/r})) for a prime (r\mid f), with (H=N_X(V)) | (H) is maximal for every field-only or graph-outer (X); all involution classes meet (\operatorname{Sp}_4(2)\le V); Lemma 4.6 applies with (a=4(f-f/r)) |
| (\operatorname{PSU}_3(q)) | simple | (N_1) | absent from the (n=3) rows of A.3 |
| (\operatorname{PSU}_4(q)) | (q\ge3) | full nonsingular (2+2) decomposition stabilizer | absent from A.3 |
| (\operatorname{PSU}_n(q)) | (n\ge5) | (N_2) | absent from A.3 |
| (\Omega_{2m+1}(q)) | (m\ge3, q) odd | (P_2) | absent from A.4 |
| (\operatorname{P}\Omega^-_{2m}(q)) | (m\ge4) | (P_2) | absent from A.5 |
| (\operatorname{P}\Omega^+_{2m}(q)) | (m\ge5) | (P_2) | absent from A.6 |
| (\operatorname{P}\Omega^+_8(q)) | triality allowed | central-node (P_2) | absent from A.7 and fixed by triality |

The two corrected rows at (q=4,16) have factor intersections (N_2^-)
and a triality image of (\Omega_8^-(q^{1/2})).  Neither contains the
central-node maximal parabolic (P_2), so the correction does not change the
screen.

### The (\operatorname{PSL}_2(q)) order check

The split-torus normalizer has order (2(q-1)/(2,q-1)) and has no fixed
point on the projective line, so it is not contained in (P_1).  It cannot
lie in the nonsplit-torus normalizer either: outside nonsimple parameters,
its order would force (q-1\mid q+1).  The only
other A.1 possibilities requiring attention are:

* (A_5) for (q=11,19,29,59);
* (S_4) for (q=7,23);
* (A_4) in (\operatorname{PGL}_2(11));
* (D_{34}) and (\operatorname{PSL}_2(4)) for (q=16).

The cases (q=7,11) are the two allowed socles.  In the others, subgroup
orders rule out containment; for (q=16), a subgroup of order 30 cannot
lie in the simple group (A_5) with index 2.  This completes the rank-one
row.

### The (\operatorname{PSL}_3(q)) split-torus check

Put (d=(3,q-1)).  A maximally split-torus normalizer (V) has order
(6(q-1)^2/d), is invariant up to conjugacy under all automorphisms, and
fixes neither a point nor a hyperplane.  The extension-field factor in row
1 of Table A.1 has intersection with the socle of order
(3(q^2+q+1)/d).  For (q=3), divisibility rules out containment; for
(q\ge5), (V) is larger.  The only additional row is at (q=4).  Since
(\operatorname{Out}(\operatorname{PSL}_3(4))\cong D_{12}), the ten
almost-simple coordinate-group types at that parameter are exactly the ten
TomLib rows certified in
[`../data/tomlib-factor-free.tsv`](../data/tomlib-factor-free.tsv).

### Low-rank routing

We use

\[
\operatorname{PSL}_2(4)\cong\operatorname{PSL}_2(5)\cong A_5,
\quad \operatorname{PSL}_2(9)\cong A_6,
\quad \operatorname{PSL}_3(2)\cong\operatorname{PSL}_2(7),
\quad \operatorname{PSL}_4(2)\cong A_8,
\quad \operatorname{PSU}_4(2)\cong\operatorname{PSp}_4(3),
\]

together with the standard (B_2=C_2), (D_3=A_3), and
({}^2D_3={}^2A_3) identifications.  Nonsimple defining parameters are not
CFSG socles and create no additional row.

## 4. Exceptional Lie-type socles

Hering--Liebeck--Saxl prove that a core-free factorization occurs only for

* (G_2(4));
* (G_2(3^f));
* (F_4(2^f));
* one additional factorization in (G_2(4).2).

Their factors are the (A_2)-type, (B_4)-type, ({}^3D_4)-type, Suzuki,
or (J_2) subgroups explicitly listed in their Theorems 1--2; no parabolic
is a factor.

For every exceptional socle outside these three factorable families, take
(V) to be a Sylow subgroup in the defining characteristic.  Automorphisms
preserve its (S)-conjugacy class, and Hering--Liebeck--Saxl give no
core-free factorization to survive the factor-screen lemma.  This also
covers coordinate groups containing graph automorphisms in the exceptional
families that admit no factorization.

For the three factorable families, if the relevant coordinate group has no
graph automorphism, choose a maximal parabolic.  For the exceptional graph
cases use:

* the graph-stable parabolic intersection (P_1\cap P_2) in
  (G_2(3^f)), where graph automorphisms fuse (P_1,P_2);
* the parabolic intersection (P_1\cap P_4) in (F_4(2^f)), where graph
  automorphisms fuse (P_1,P_4).

These subgroups contain a Borel.  Their (p)-parts are (q^6) and at least (q^{24}),
respectively, larger than the (p)-parts of every listed factor
((q^3) in the (G_2) case and at most (q^{16}) in the (F_4) case).
Thus no listed factor contains the screen subgroup.  Every other exceptional
family has no core-free factorization at all, so any core-free maximal action
is factor-free.  The conventional small isomorphisms
(G_2(2)'\cong\operatorname{PSU}_3(3)) and
({}^2G_2(3)'\cong\operatorname{PSL}_2(8)) are already covered.

## 5. Sporadic socles

Giudici's Tables 1--3 are complete for simple sporadic groups, Table 4 lists
the genuinely new outer-extension factorizations, and Lemma 2.1(5) accounts
for the lifted simple-socle rows.  The following maximal subgroups do not
occur as a factor in the applicable row, and hence give factor-free actions.

| Coordinate group (X) | Factor-free maximal subgroup (H) |
|---|---|
| (M_{11}) | (A_5.2) |
| (M_{12}) | (M_8{:}S_4) |
| (M_{12}.2) | (3^{1+2}{:}D_8) |
| (M_{22}.2) | (A_6.2^2) |
| (M_{23}) | (A_8) |
| (J_2) | (3.A_6.2_2) |
| (J_2.2) | (3.A_6.2^2) |
| (HS) | (L_3(4).2_1) (either Atlas class of the recorded order also works) |
| (HS.2) | (L_3(4).2^2) |
| (He) | (2^2.L_3(4).S_3) |
| (He.2) | (2^2.L_3(4).D_{12}) |
| (Ru) | (2^6{:}U_3(3){:}2) |
| (Suz) | (J_2.2) |
| (Suz.2) | (J_2.2\times2) |
| (Fi_{22}) | (O_7(3)) |
| (Fi_{22}.2) | (G_2(3).2) |
| (Co_1) | (2^{11}{:}M_{24}) |

The simple group (M_{22}), and every sporadic almost-simple group not
represented in the table, has no nontrivial core-free factorization; any
core-free maximal subgroup works.

The sole factor-cover survivor is (M_{24}).  Use its primitive action on
2-subsets of the natural 24-point set.  The degree is 276, and every
involution fixes the support of one of its 2-cycles.  Thus this action is
2-elusive and Lemma 4.5 applies.

The Atlas maximal-subgroup list supplies maximality in the displayed rows.
The twenty-four proof and cross-check rows available in TomLib are independently checked in
[`../data/tomlib-factor-free.tsv`](../data/tomlib-factor-free.tsv); the
published Giudici--Atlas screen, not TomLib's finite coverage, supplies the
universal sporadic proof.

## 6. Coverage conclusion

By CFSG, Sections 2--5 cover every nonabelian finite simple group.  The only
socles not excluded are

\[
\operatorname{PSL}_2(7),\qquad
\operatorname{PSL}_2(11),\qquad
\operatorname{PSL}_5(2).
\]

This is exhaustive family coverage, while the Table-of-Marks rows are used
only for named finite exceptions and independent cross-checks.
