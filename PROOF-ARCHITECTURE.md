# Proof architecture

The manuscript proves the composition-factor classification through a
section-safe reduction. The structural chain is:

\[
S\ \leadsto\ L\text{ with }\operatorname{Soc}(L)=S^k
\ \leadsto\ X=N_L(S_1)/C_L(S_1)
\ \leadsto\ L\curvearrowright (X/H)^k.
\]

The symbols \(\leadsto\) denote constructions, not homomorphisms. In
particular, \(X\) is induced by a coordinate stabilizer; there is no asserted
quotient map \(L\to X\).

## 1. The inheritance boundary

Property CMP means that every maximal subgroup has an exact complement.
It passes to quotients, but it does not pass to normal subgroups: \(D_8\)
has CMP, while its normal subgroup \(C_4\) does not. The proof therefore
never assigns CMP directly to a composition factor.

Given a nonabelian composition factor \(S\) of a CMP group \(G\), the
centralizer construction produces a quotient \(L\) with a unique
self-centralizing minimal normal subgroup \(S^k\). Quotient closure preserves
CMP.

## 2. The section-safe product action

Writing \(S^k=S_1\times\cdots\times S_k\), define

\[
X=N_L(S_1)/C_L(S_1),\qquad S\leq X\leq\operatorname{Aut}(S).
\]

For a core-free maximal \(H<X\) with \(H\cap S\ne1\), the standard wreath
embedding gives a faithful primitive action of the same group \(L\) on
\((X/H)^k\). If the point stabilizer had a complement, that complement would
be regular. Liebeck--Praeger--Saxl then force a core-free transitive subgroup
in the coordinate action when \(k\ge2\); the case \(k=1\) is an
almost-simple argument.

This is the main reusable mechanism: it replaces false inheritance by a new
primitive action that still tests a maximal subgroup of the ambient CMP
quotient.

## 3. Three coordinate obstructions

The coordinate action is excluded in one of three ways.

1. **Factor-free:** no core-free \(C<X\) satisfies \(X=HC\).
2. **Prime-elusive:** a prime divides \(\lvert X:H\rvert\), while every
   element of that order fixes a point.
3. **Socle valuation:** the socle is prime-elusive and
   \[
   v_p(\lvert X:H\rvert)>v_p(\lvert X:S\rvert).
   \]

Published maximal-factorization classifications make the first screen
exhaustive across the CFSG families. The only infinite screen survivor is
\(\operatorname{PSp}_4(2^f)\). A prime-degree subfield subgroup and the
socle-valuation inequality eliminate it uniformly for every coordinate group
and every exponent \(k\).

## 4. Verification boundary

| Layer | Establishes |
|---|---|
| Ordinary mathematics | Quotient closure, monolithic reduction, product-action lifting, the three obstructions, family-table deductions, the symplectic subfield argument, and theorem assembly |
| Published classifications | CFSG-family exhaustiveness, the audited maximal-factorization lists, and the cited symplectic structural inputs |
| Explicit source assumptions | The two precise consequences attributed to LPS (2000), Corollary 3(iv), and LPS (1990), Theorem D with Remark 2; their exact primary-text matches remain unchecked |
| GAP with complete tables of marks | Five small alternating coordinate groups and ten groups with socle \(\operatorname{PSL}_3(4)\) |
| Separate finite checks | Nine sporadic cross-checks and the \(q=4\) symplectic regression |

No bounded computation is used for an infinite family. No formal proof
assistant is part of the evidence chain.

## 5. Reusable yield and open direction

The demonstrated method applies a quotient-closed maximal-subgroup property
to a composition factor by constructing a primitive product action. It
suggests a broader framework for properties that force regular or suitably
transitive partners to maximal point stabilizers. No general framework is
claimed here: precise axioms and a further application would be needed.
