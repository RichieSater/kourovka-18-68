# Chief-factor reduction to a monolithic primitive quotient

**Date:** 2026-08-11
**Status:** proved. The standard fact that the Frattini subgroup of a finite
group is nilpotent is used.

## Theorem

Let \(G\) be a finite group satisfying `CMP`, and let \(S\) be a nonabelian
composition factor of \(G\). Then there are a positive integer \(t\), a
quotient \(L\) of \(G\), a maximal subgroup \(M<L\), and a subgroup
\(K\leq L\) such that:

1. `CMP(L)`;
2. \(N=\operatorname{Soc}(L)\cong S^t\) is the unique minimal normal subgroup
   of \(L\);
3. \(C_L(N)=1\);
4. \(M\) is core-free and \(N\nleq M\);
5. \(L=MK\) and \(M\cap K=1\);
6. consequently, \(L\) has a faithful primitive action with socle \(S^t\) in
   which \(K\) is regular.

## Proof

Choose a chief factor \(A/B\) of \(G\) whose composition factors include
\(S\). Since a finite characteristically simple group is a direct power of a
simple group, \(A/B\cong S^t\) for some \(t\geq1\).

Let

\[
C/B=C_{G/B}(A/B)
\]

and put \(L=G/C\), \(N=AC/C\). The group \(A/B\) is centerless, so

\[
A\cap C=B,
\]

and hence \(N\cong A/B\cong S^t\). The chief property of \(A/B\) makes
\(N\) a minimal normal subgroup of \(L\).

By construction, \(L\) acts faithfully by conjugation on \(A/B\). Under this
embedding into \(\operatorname{Aut}(N)\), the subgroup \(N\) is the inner
automorphism group. An automorphism centralizing every inner automorphism of
a centerless group is the identity: for every \(x\in N\), commutation with
conjugation by \(x\) gives \(\alpha(x)x^{-1}\in Z(N)=1\). Therefore

\[
C_L(N)=1.
\]

If \(R\) were a second minimal normal subgroup of \(L\), then
\([R,N]\leq R\cap N=1\), so \(R\leq C_L(N)=1\), a contradiction. Thus \(N\)
is the unique minimal normal subgroup and equals \(\operatorname{Soc}(L)\).

By quotient closure, proved in
[`00-definition-and-inheritance.md`](00-definition-and-inheritance.md),
`CMP(L)` holds. The nonabelian group \(N\) cannot lie in \(\Phi(L)\), because
the Frattini subgroup of a finite group is nilpotent. Hence some maximal
subgroup \(M\) of \(L\) does not contain \(N\). Minimal normality gives
\(L=MN\).

The core \(\operatorname{Core}_L(M)\) is normal in \(L\). If it were
nontrivial, it would contain the unique minimal normal subgroup \(N\),
contrary to \(N\nleq M\). Hence \(M\) is core-free.

Finally `CMP(L)` supplies \(K\leq L\) with \(L=MK\) and \(M\cap K=1\). The
coset action on \(L/M\) is faithful and primitive, and the exact-factorization
criterion makes \(K\) regular. Its unique minimal normal subgroup, and hence
its socle, is \(N\cong S^t\). \(\square\)

## What the theorem does and does not prove

This is a section-safe reduction: it reaches an arbitrary nonabelian
composition factor without asserting that `CMP` passes to sections.

It does **not** imply `CMP(S)`. Even when \(t=1\), the quotient \(L\) can be an
almost-simple extension \(S\leq L\leq\operatorname{Aut}(S)\). When \(t>1\),
the primitive action can lie in a non-almost-simple O'Nan--Scott type. Existing
almost-simple exact-factorization tables therefore do not finish the proof.

At the end of this reduction, the remaining obligation was the following
statement:

> If a finite monolithic group \(L\) with self-centralizing socle \(S^t\)
> satisfies `CMP`, then
> \(S\in\{L_2(7),L_2(11),L_5(2)\}\).

This obligation is now discharged in 04-product-action-lifting.md and
05-family-factor-screen.md.  The key improvement is that one does not
classify all primitive actions of \(L\).  Instead, one manufactures a
primitive product action from any suitable almost-simple coordinate action;
LPS Corollary 3(iv) and the prime-valuation lemma then handle every \(t\),
including outer fusion.  Thus the paragraph above records the historical
boundary of this reduction, not a remaining gap.
