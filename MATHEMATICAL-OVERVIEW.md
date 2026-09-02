# Mathematical overview

## The theorem

Let \(\mathrm{CMP}(G)\) mean that every maximal subgroup of the finite group
\(G\) has an exact complement. The manuscript proves that the nonabelian
composition factors of a \(\mathrm{CMP}\)-group are among

\[
\operatorname{PSL}_2(7),\qquad
\operatorname{PSL}_2(11),\qquad
\operatorname{PSL}_5(2),
\]

and that all three possibilities occur.

## Reduction to a monolithic quotient

The central difficulty is that \(\mathrm{CMP}\) is quotient-closed but not
section-closed. Given a nonabelian composition factor \(S\) of \(G\), choose a
chief factor isomorphic to \(S^k\) and factor by its centralizer. This gives a
quotient \(L\) with \(\mathrm{CMP}\) whose unique minimal normal subgroup is a
self-centralizing socle \(S^k\).

Writing \(S^k=S_1\times\cdots\times S_k\), the stabilizer of \(S_1\) induces
an almost-simple group

\[
X=N_L(S_1)/C_L(S_1),\qquad S\leq X\leq\operatorname{Aut}(S).
\]

For a core-free maximal subgroup \(H<X\) with \(1<H\cap S<S\), the standard
wreath embedding turns the action of \(X\) on \(X/H\) into a faithful
primitive action of the same group \(L\) on \((X/H)^k\). Thus no inheritance
of \(\mathrm{CMP}\) by \(S\) or \(X\) is asserted. Instead,
\(\mathrm{CMP}(L)\) supplies a regular complement to the point stabilizer in
this new action.

## Excluding a coordinate action

There are three mathematical ways to rule out that regular subgroup.

1. If no core-free subgroup \(C<X\) satisfies \(X=HC\), Corollary 3(iv) of
   Liebeck--Praeger--Saxl (2000) excludes a regular subgroup in the primitive
   product action.
2. If a prime \(p\) divides \(\lvert X:H\rvert\) and every element of order
   \(p\) fixes a point, the fixed-point property passes to every Cartesian
   power.
3. It is enough for the socle to have that fixed-point property when
   \[
   v_p(\lvert X:H\rvert)>v_p(\lvert X:S\rvert),
   \]
   because a regular subgroup would then contain a nonidentity element of
   order \(p\) in the base socle.

The first alternative is reduced to published classifications of maximal
factorizations. The alternating groups of degree at least \(13\) are handled
by a 6-subset stabilizer and Theorem D of Liebeck--Praeger--Saxl (1990).
The classical, exceptional, and sporadic families are treated with their
respective factorization classifications. The only remaining infinite
family, \(\operatorname{PSp}_4(2^f)\), is excluded using a prime-degree
subfield subgroup and the 2-adic inequality above.

## Finite computations and mathematical yield

GAP 4.15.1 with TomLib 1.2.11 verifies the required factorization property
for five small alternating coordinate groups and all ten almost-simple
groups with socle \(\operatorname{PSL}_3(4)\). Nine sporadic rows are checked
separately, and an AtlasRep calculation checks the corrected \(q=4\)
symplectic example. The general \(\operatorname{PSp}_4(2^f)\) argument is the
subfield and valuation proof described above.

The reusable idea is the passage from a quotient-closed maximal-subgroup
property to a primitive product action of a monolithic quotient. It explains
why classifications of almost-simple factorizations can control a direct
power \(S^k\) of arbitrary multiplicity, while the valuation argument shows
how a fixed-point obstruction for the socle can survive outer automorphisms
and arbitrary Cartesian powers.
