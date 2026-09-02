# Classification details

The cited classification theorems give the exhaustive lists of maximal
factorizations used below. The containment deductions are given here; the
fifteen remaining finite cases are computed from complete tables of marks.

## 1. Reduction to maximal factorizations

Let \(1<V<S\), with its \(S\)-conjugacy class invariant under
\(S\leq X\leq\operatorname{Aut}(S)\). If a core-free subgroup is transitive on
the resulting coset action, the maximal-factorization lemma gives a group
\(S\leq Y\leq X\) and a nontrivial maximal factorization \(Y=AB\) with
\(V\leq A\cap S\), after exchanging the factors if necessary. The family
arguments below choose \(V\), identify every possible factor intersection,
and prove that none contains \(V\).

Class invariance gives \(N_X(V)S=X\), so any maximal overgroup \(H<X\) of
\(N_X(V)\) is core-free and supplements \(S\). Thus \(V\) itself need not be
maximal. When \(V\) is maximal in \(S\), containment in a proper factor
intersection forces equality; this applies to the standard maximal
parabolics and full decomposition stabilizers used below.

Notation follows Xia--Li: \(P_i\) is a maximal parabolic, \(P_{ij}\) is the
intersection of two standard parabolics sharing a Borel, and \(N_i\) is a
nonsingular-subspace stabilizer.

## 2. Alternating socles

Let \(n\geq13\), let \(A_n\leq X\leq S_n\), and let \(H\) be a 6-set
stabilizer. If \(X=HC\) with \(C\) core-free, Theorem D and Remark 2 of
Liebeck--Praeger--Saxl (1990) apply with \(L=A_n\), \(A=H\), and \(B=C\).
Neither factor contains \(L\), and the exceptional degrees \(6,8,10\) do not
occur. Hence \(A_{n-j}\leq H\leq S_{n-j}\times S_j\) for some
\(1\leq j\leq5\), while \(C\) is \(j\)-homogeneous. Maximality of \(H\)
would make it a \(j\)-set stabilizer, contradicting its natural orbit sizes
\(6,n-6\).
Thus the 6-subset action is factor-free.

For \(5\le n\le12\), the manuscript gives explicit elusive actions except
for the five named coordinate groups
\(A_6.2_2,A_6.2_3,A_6.2^2,A_7,S_7\).  Those five maximal classes are
exhausted by complete TomLib tables in `data/tomlib-factor-free.tsv`.  The
exceptional outer automorphisms of \(A_6\) are therefore covered individually,
not inferred from the natural symmetric action.

## 3. Classical socles: exact Xia--Li rows

**Exhaustive source.** Xia--Li, Theorem 2.15 and Appendix Tables A.1--A.7,
which state the socle intersections in every nontrivial maximal
factorization with classical socle.  The two omissions in A.7 are supplied by
Gill--Giudici--Spiga, Section 2 and Table 2.

### 3.1 Table A.1: \(S=\operatorname{PSL}_n(q)\)

| A.1 row | Published factor intersections | Subgroup choice and containment |
|---:|---|---|
| 1 | extension-field \(\widehat{GL}_a(q^b).b\) versus \(P_1\) or \(P_{n-1}\) | For \(n=2\), this is the nonsplit-torus normalizer: the split-torus normalizer fixes no projective point and its order does not divide the nonsplit normalizer. For \(n=3\), the split-torus normalizer fixes neither a point nor a hyperplane and its order is incompatible with the extension-field factor (the explicit calculation is in Section 3.2 below). For \(n\ge4\), the chosen parabolic is a distinct maximal parabolic; the graph-stable \(P_{2,n-2}\) case is handled in Section 3.3. |
| 2 | \(PSp_n(q).a\) versus \(P_1\) or \(P_{n-1}\) | Applies only for even \(n\ge4\).  The middle parabolic \(P_{n/2}\) is a different maximal subgroup, so it is contained in neither factor. |
| 3 | \(PSp_n(q).a\) versus \(\operatorname{Stab}(V_1\oplus V_{n-1})\) | Again even \(n\ge4\); neither factor is the maximal parabolic \(P_{n/2}\). |
| 4 | \(\widehat{GL}_{n/2}(q^2).2\) versus \(\operatorname{Stab}(V_1\oplus V_{n-1})\), \(q=2,4\) | Neither factor is \(P_{n/2}\). |
| 5 | \(P_1\) versus \(A_5\), \(q=11,19,29,59\) | Rank-one order check; \(q=11\) is allowed, and for \(q=19,29,59\) the split-normalizer order excludes containment in \(A_5\). |
| 6 | \(P_1\) versus \(S_4\), \(q=7,23\) | \(q=7\) is allowed; at \(q=23\) the split-normalizer order excludes containment in \(S_4\). |
| 7 | \(P_1\) versus \(A_4\) in \(PGL_2(11)\) | The socle is the allowed \(L_2(11)\); no exclusion is required. |
| 8 | \(D_{34}\) versus \(L_2(4)\) in \(P\Gamma L_2(16)\) | The split normalizer has order 30.  It is in neither factor; containment in \(A_5\cong L_2(4)\) would have index 2. |
| 9 | \(L_2(7)\) versus \(A_6\), \(n=3,q=4\) | All ten coordinate groups with socle \(L_3(4)\) are verified individually by complete tables of marks. |
| 10 | \(31{:}5\) versus \(P_2\) or \(P_3\), \(n=5,q=2\) | This is the allowed socle \(L_5(2)\), the low parameter excluded from the odd-dimensional parabolic argument. |

#### 3.2 The two torus normalizers

For \(L_2(q)\), a split-torus normalizer has order
\(2(q-1)/(2,q-1)\) and interchanges the two fixed points of the torus, so it
is not contained in \(P_1\).  In A.1:1 the other factor is specifically the
**nonsplit** torus normalizer.  Containment there would force
\(q-1\mid q+1\), outside the nonsimple parameters.  Rows A.1:5--8 are the
finite order checks displayed above.  Diagonal and field automorphisms
preserve the split-torus-normalizer class.

For \(L_3(q)\), put \(e=(3,q-1)\).  The split-torus normalizer has order
\(6(q-1)^2/e\), while the A.1:1 extension-field intersection has order
\(3(q^2+q+1)/e\).  At \(q=3\), the first order does not divide the second;
for \(q\ge5\), it is larger.  Its monomial action fixes neither a point nor a
hyperplane.  Diagonal, field, and graph automorphisms preserve its class.
The cases \(q=2\) and 4 route respectively to the allowed \(L_2(7)\) and the
ten finite computations.

#### 3.3 Odd-dimensional graph automorphisms

For odd \(n\ge5\), graph automorphisms exchange \(P_2\) and \(P_{n-2}\), so
choose \(P_{2,n-2}=P_2\cap P_{n-2}\). It contains a Borel. Any
proper overgroup containing it is parabolic, and its only maximal proper
overgroups are \(P_2\) and \(P_{n-2}\).  Inspection of A.1:1--4,10 therefore
excludes containment except in A.1:10, the allowed \((n,q)=(5,2)\).  Without
a graph automorphism, \(P_2\) itself is invariant and maximal.  For even
\(n\), the middle node is fixed by graph automorphisms, so \(P_{n/2}\) is
invariant under the full automorphism group.

### 3.4 Table A.2: \(S=\operatorname{PSp}_{2m}(q)\)

For \(m\ge3\), choose the maximal parabolic \(P_2\). For \(m=2\)
and odd \(q\), choose the full stabilizer of a nonsingular \(2+2\)
decomposition, a standard maximal geometric subgroup.  Field and diagonal
automorphisms preserve these classes.  The even \(m=2\) family is handled
separately by the prime-degree subfield action in Section 3.9.

| A.2 row | Published factor intersections | Containment disposition |
|---:|---|---|
| 1 | extension-field symplectic subgroup versus \(P_1\) | Neither \(P_2\) (for \(m\ge3\)) nor the odd-\(q\), \(m=2\) decomposition stabilizer is either factor. |
| 2 | extension-field subgroup versus \(O_{2m}^{+}(q)\) or \(O_{2m}^{-}(q)\), \(q\) even | For \(m\ge3\), none is \(P_2\); \(m=2\) even is routed to Section 3.9. |
| 3 | \(O_{2m}^{-}(q)\) versus \(P_m\), \(q\) even | For \(m\ge3\), \(P_m\ne P_2\); \(m=2\) is routed away. |
| 4 | \(O_{2m}^{-}(q)\) versus \(Sp_m(q)\wr S_2\), \(m,q\) even | Neither is \(P_2\) for \(m\ge3\); \(m=2\) is routed away. |
| 5 | \(Sp_m(4).2\) versus \(N_2\), \(m\ge4,q=2\) | The nonsingular stabilizer \(N_2\) is not the parabolic \(P_2\); neither factor equals the chosen maximal subgroup. |
| 6 | \(O_{2m}^{-}(2)\) versus \(O_{2m}^{+}(2)\) | Neither is \(P_2\) for \(m\ge3\). |
| 7 | \(O_{2m}^{-}(4)\) versus \(O_{2m}^{+}(4)\) | Same; the extra \(m=2\) classes are routed to Section 3.9. |
| 8 | \(Sp_m(16).2\) versus \(N_2\), \(m\ge4,q=4\) | Neither equals \(P_2\). |
| 9 | \(O_{2m}^{-}(4)\) versus \(Sp_{2m}(2)\) | Neither equals \(P_2\) for \(m\ge3\); \(m=2\) is routed away. |
| 10 | \(O_{2m}^{-}(16)\) versus \(Sp_{2m}(4)\) | Same. |
| 11 | \(Sz(q)\) versus \(O_4^+(q)\), \(m=2,q=2^f\), \(f\) odd | Entire row is routed to the prime-degree subfield action. |
| 12 | \(G_2(q)\) versus \(O_6^+(q),O_6^-(q),P_1,N_2\), \(m=3,q\) even | No listed factor is \(P_2\). |
| 13 | \(2^4.A_5\) versus \(P_1\) or \(P_2\), \(m=2,q=3\) | The odd-\(q\) full \(2+2\) decomposition stabilizer is a different maximal subgroup. |
| 14 | \(L_2(13)\) versus \(P_1\), \(m=3,q=3\) | Neither factor is \(P_2\). |
| 15 | \(O_8^-(2)\) versus \(S_{10}\), \(m=4,q=2\) | Neither factor is \(P_2\). |
| 16 | \(L_2(17)\) versus \(O_8^+(2)\), \(m=4,q=2\) | Neither factor is \(P_2\). |

### 3.5 Table A.3: \(S=\operatorname{PSU}_n(q)\)

Choose \(N_1\) for \(n=3\), the full nonsingular \(2+2\)
decomposition stabilizer for \(n=4,q\ge3\), and \(N_2\) for \(n\ge5\).
These are standard maximal geometric classes and are invariant under the
available diagonal and field/graph-field automorphisms.

| A.3 rows | Published intersections | Containment disposition |
|---:|---|---|
| 1--4 | \(N_1\) paired with \(P_m\), \(PSp_{2m}(q).a\), \(\widehat{SL}_m(4).2\), or \(\widehat{SL}_m(16).3.2\) | For \(n=4\), none is the full \(2+2\) decomposition stabilizer.  For \(n\ge5\), none is \(N_2\). |
| 5--7 | \(L_2(7),A_7,19{:}3\) versus \(P_1\), for \(n=3\) | None is \(N_1\). |
| 8 | \(3^3.S_4\) versus \(P_2\), \(n=4,q=2\) | Routed through \(U_4(2)\cong PSp_4(3)\). |
| 9 | \(L_3(4)\) versus \(P_1,PSp_4(3),P_2\), \(n=4,q=3\) | None is the full \(2+2\) decomposition stabilizer. |
| 10 | \(N_1\) versus \(U_4(3).2\) or \(M_{22}\), \(n=6,q=2\) | None is \(N_2\). |
| 11 | \(J_3\) versus \(P_1\), \(n=9,q=2\) | Neither is \(N_2\). |
| 12 | \(Suz\) versus \(N_1\), \(n=12,q=2\) | Neither is \(N_2\). |

### 3.6 Tables A.4--A.6: orthogonal groups away from triality

In every row here, choose the maximal parabolic \(P_2\), invariant
under diagonal and field automorphisms.  Accordingly, type inequality is a
containment proof.

| Source rows | Published intersections | Why \(P_2\) is absent |
|---|---|---|
| A.4:1--8, \(\Omega_{2m+1}(q)\) | \(N_1^-\), \(P_m\), \(G_2(q)\), \(P_1\), \(N_1^\pm\), nonsingular \(N_2^\pm\), \(PSp_6(q).a\), \(F_4(q)\), and the stated \(q=3\) exceptions (including \(P_3\)) | The symbol \(N_2^-\) in A.4:2 is nonsingular, not parabolic.  None of A.4:1--8 equals \(P_2\). |
| A.5:1--5, \(P\Omega_{2m}^-(q)\) | \(P_1,N_1,N_2^+\), unitary/subfield factors, and \(A_{12}\) | The only parabolic displayed is \(P_1\); \(N_2^+\ne P_2\). |
| A.6:1--13, \(P\Omega_{2m}^+(q),m\ge5\) | \(N_1,N_2^\pm,P_1,P_m,P_{m-1}\), linear/unitary/tensor factors, \(\Omega_9(q).a\), and \(Co_1\) | None equals \(P_2\). |

The standard maximality statements for these parabolics and for the
nonsingular and decomposition subgroups above are in Kleidman--Liebeck, Chapters
3--4.  For the low-dimensional symplectic subfield used below, the sharper
source is Bray--Holt--Roney-Dougal, Table 8.14.

### 3.7 Table A.7 and its correction: \(P\Omega_8^+(q)\)

Triality permutes the three outer nodes and fixes the central node, so the
central-node maximal parabolic \(P_2\) is invariant under diagonal, field,
and all graph/triality automorphisms.

| A.7 rows | Published intersections | Containment disposition |
|---:|---|---|
| 1--7 | \(\Omega_7(q)\), outer-node \(P_1,P_3,P_4\), nonsingular/extension-field/tensor factors | None is central \(P_2\). |
| 8--9 | the stated \(q=2\) factors, again including only \(P_1,P_3,P_4\) | None is \(P_2\). |
| 10--13 | the stated \(q=3\) factors, including \(P_1,P_3,P_4\) and \(P_{13},P_{14},P_{34}\) | A maximal parabolic \(P_2\) cannot lie in any distinct proper factor. |
| 14--15 | the stated \(q=4\) factors | None is \(P_2\). |
| GGS correction, Section 2/Table 2 | \(N_2^-\) paired with a triality image of \(\Omega_8^-(q^{1/2})\), \(q=4,16\) | The first factor is nonsingular and the second is subfield/triality type; neither is \(P_2\). |

### 3.8 Low-parameter routing

The following isomorphisms prevent double counting and close the exceptional
defining parameters:

\[
L_2(4)\cong L_2(5)\cong A_5,\quad L_2(9)\cong A_6,\quad
L_3(2)\cong L_2(7),\quad L_4(2)\cong A_8,\quad
U_4(2)\cong PSp_4(3).
\]

The standard \(B_2=C_2\), \(D_3=A_3\), and
\({}^2D_3={}^2A_3\) identifications route the remaining overlaps.  Nonsimple
small defining parameters are not CFSG socles.

### 3.9 Even \(PSp_4\): the graph-outer-safe replacement

Let \(S=Sp_4(2^f)\), \(f\ge2\).  Choose a prime \(r\mid f\), put
\(d=f/r\), and let \(V=Sp_4(2^d)\).  Bray--Holt--Roney-Dougal, Table 8.14
(and Burness, Proposition 4.2/Table 3) gives maximality in \(S\) because
\(r\) is prime.  Harper's setup before Lemma 2.1 and Theorem 4(a) gives
\(\rho^2=\varphi\), while Lemma 2.1 gives
\(\operatorname{Aut}(S)=\langle S,\rho\rangle\).  Thus \(\rho\) commutes with Frobenius and normalizes
the \(\varphi^d\)-fixed subgroup \(V\); the class is invariant even for
graph-outer coordinates.

For every \(S\le X\le\operatorname{Aut}(S)\), the subgroup
\(H=N_X(V)\) supplements \(S\), satisfies \(H\cap S=V\), and is maximal:
for \(H<K<X\), the intersection \(K\cap S\) is \(V\) or \(S\); normality
of the former forces \(K\le H\), while the latter forces \(K=X\).  It is
core-free because it does not contain \(S\).

LPS (2010), Lemmas 2.1--2.2 and Corollary 2.3, together with
\(O_4^+(q)\cong(SL_2(q)\times SL_2(q)).2\), show that the three involution
classes have representatives \((u,1),(u,u),\tau\) already in
\(O_4^+(2)\le Sp_4(2)\le V\).  Hence the action is 2-elusive for the socle.
Finally

\[
v_2(\lvert X:H\rvert)=v_2(\lvert S:V\rvert)=4(f-d),\qquad
v_2(\lvert X:S\rvert)\le1+v_2(f)<2f\le4(f-d).
\]

The socle-valuation lemma closes every exponent and every coordinate group.
The separate AtlasRep calculation at \(q=4\) checks the replacement for the formerly
incorrect \(O_4^+\)-normalizer construction.

## 4. Exceptional groups of Lie type

**Exhaustive source.** Hering--Liebeck--Saxl, Theorems 1--2.  Their only
factorable socles are \(G_2(4)\), \(G_2(3^f)\), and \(F_4(2^f)\), with one
additional outer factorization for \(G_2(4).2\).  The displayed factors are
of \(A_2\)-, \(B_4\)-, \({}^3D_4\)-, Suzuki-, or \(J_2\)-type; none is
parabolic.

Outside these families, an automorphism-invariant Sylow subgroup in defining
characteristic can be placed in a core-free maximal overgroup, and the
classification contains no factorization at all.  Inside them:

- without a graph automorphism, use any listed maximal parabolic; its
  maximality turns type inequality into noncontainment;
- in \(G_2(3^f)\) with graph fusion, use the graph-stable parabolic
  intersection \(P_1\cap P_2\), containing a Borel and having \(p\)-part
  \(q^6\), while every listed factor has \(p\)-part at most \(q^3\);
- in \(F_4(2^f)\) with graph fusion, use the graph-stable parabolic
  intersection \(P_1\cap P_4\), **not a Borel**, but containing a common
  Borel.  Its \(p\)-part is at least \(q^{24}\), while every listed factor
  has \(p\)-part at most \(q^{16}\).

Thus containment is excluded by divisibility in the two nonmaximal,
graph-stable subgroups. The small derived-group isomorphisms
\(G_2(2)'\cong U_3(3)\) and \({}^2G_2(3)'\cong L_2(8)\) route to the
classical cases.

## 5. Sporadic socles

**Exhaustive source.** Giudici, Theorems 1.1--1.3 and Tables 1--4.
Theorem 1.1 and Tables 1--2 cover simple sporadic groups.  Theorem 1.2 and
Table 3 give the genuinely new outer cases.  Theorem 1.3 and Table 4 list
only exact factorizations, so the factor-free argument uses Tables 1--3;
Lemma 2.1(5) lifts the applicable simple-socle rows to an outer extension.
Maximality of each displayed \(H\) follows from the *Atlas of Finite Groups*
maximal-subgroup list (and, where available, the official online ATLAS
list). For each factorable coordinate group, the applicable
Giudici group block was checked on both sides: the named \(H\) below is not a
factor in that block.  Because \(H\) itself is maximal, a transitive
core-free subgroup would enlarge to a maximal factorization having \(H\) as
one factor; hence absence is a containment proof.

| Coordinate \(X\) | Giudici factorization locus | Chosen maximal \(H\) | Computational status |
|---|---|---|---|
| \(M_{11}\) | Table 1, \(M_{11}\) block | \(S_5\) | TomLib cross-check |
| \(M_{12}\) | Table 1, \(M_{12}\) block | \(2^3{:}S_4\) | TomLib cross-check |
| \(M_{12}.2\) | Table 1, \(M_{12}\) block, lifted by Lemma 2.1(5) | \(3^{1+2}{:}D_8\) | TomLib cross-check |
| \(M_{22}.2\) | Table 3, \(\operatorname{Aut}(M_{22})\) block | \(A_6.2^2\) | TomLib cross-check |
| \(M_{23}\) | Table 2, \(M_{23}\) block | \(A_8\) | TomLib cross-check |
| \(J_2\) | Table 1, \(J_2\) block | \(3.A_6.2_2\) | TomLib cross-check |
| \(J_2.2\) | Table 3, \(\operatorname{Aut}(J_2)\) block | \(3.A_6.2^2\) | TomLib cross-check |
| \(HS\) | Table 2, \(HS\) block | \(L_3(4).2_1\) | TomLib cross-check |
| \(HS.2\) | Table 3, \(\operatorname{Aut}(HS)\) block, plus lifts of Table 2 | \(L_3(4).2^2\) | TomLib cross-check |
| \(He\) | Table 2, \(He\) block | \(2^2.L_3(4).S_3\) | published classification |
| \(He.2\) | Table 3, \(\operatorname{Aut}(He)\) block, plus lifts of Table 2 | \(2^2.L_3(4).D_{12}\) | published classification |
| \(Ru\) | Table 2, \(Ru\) block | \(2^6{:}U_3(3){:}2\) | published classification |
| \(Suz\) | Table 2, \(Suz\) block | \(J_2.2\) | published classification |
| \(Suz.2\) | Table 3, \(\operatorname{Aut}(Suz)\) block, plus lifts of Table 2 | \(J_2.2\times2\) | published classification |
| \(Fi_{22}\) | Table 2, \(Fi_{22}\) block | \(O_7(3)\) | published classification |
| \(Fi_{22}.2\) | Table 2, \(Fi_{22}\) block, lifted by Lemma 2.1(5) | \(G_2(3).2\) | published classification |
| \(Co_1\) | Table 2, \(Co_1\) block | \(2^{11}{:}M_{24}\) | published classification |

The simple group \(M_{22}\), and every remaining sporadic coordinate group
not appearing in Giudici's factorization tables, has no nontrivial core-free
factorization; any core-free maximal action with nontrivial socle intersection
is factor-free.

The remaining group is \(M_{24}\), whose Table 2 block contains the
well-known factorizations.  Instead use its degree-276 action on 2-subsets.
The point stabilizer \(M_{22}.2\) is maximal, and every involution fixes the
support of a 2-cycle, so the action is 2-elusive.

## 6. Coverage conclusion

CFSG partitions the nonabelian finite simple groups into alternating, Lie
type, and sporadic families.  Sections 2--5 cover each family, every allowed
outer coordinate group, and every low-parameter overlap.  The only socles
not excluded are

\[
L_2(7),\qquad L_2(11),\qquad L_5(2),
\]

which are exactly the three **published-input** simple `CMP` groups of
Levchuk--Likharev.
