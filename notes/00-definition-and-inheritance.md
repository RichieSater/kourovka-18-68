# Exact definition and inheritance audit

**Date:** 2026-08-11
**Status:** proved unless a paragraph is explicitly labelled otherwise.

## 1. Convention

For subgroups \(M,K\leq G\), \(K\) is a **complement** to \(M\) in \(G\)
when

\[
G=MK\qquad\text{and}\qquad M\cap K=1.
\]

The order formula then gives \(|K|=\lvert G:M\rvert\). This is the convention used by
Levchuk--Likharev and Maslova--Revin, not the weaker notion of a supplement.
Write `CMP(G)` when every maximal subgroup of \(G\) has a complement.

## 2. Quotient closure

### Proposition 2.1

If `CMP(G)` and \(N\trianglelefteq G\), then `CMP(G/N)`.

### Proof

Let \(\pi:G\to G/N\), and let \(\overline M\) be maximal in \(G/N\). Its full
preimage \(M=\pi^{-1}(\overline M)\) is maximal in \(G\), and \(N\leq M\).
Choose \(K\leq G\) with \(G=MK\) and \(M\cap K=1\). Then

\[
G/N=\overline M\,\pi(K).
\]

If \(\pi(k)\in\overline M\) for \(k\in K\), then \(k\in M\), since
\(N\leq M\). Hence \(k\in M\cap K=1\). Thus
\(\overline M\cap\pi(K)=1\), and \(\pi(K)\) complements \(\overline M\).
\(\square\)

This proves quotient closure for an arbitrary normal subgroup; no Frattini or
solubility hypothesis is needed.

## 3. Exact factorization and regular action

### Proposition 3.1

Let \(M\leq G\). A subgroup \(K\leq G\) complements \(M\) if and only if
\(K\) is regular in its action by right multiplication on the cosets of
\(M\).

### Proof

Transitivity of \(K\) on \(G/M\) is equivalent to \(G=MK\). The stabilizer in
\(K\) of the base coset is \(M\cap K\). Thus the action is transitive with
trivial point stabilizer exactly when the factorization is exact. \(\square\)

When \(M\) is maximal and core-free, this is a faithful primitive action.

## 4. Normal-subgroup inheritance fails

### Proposition 4.1

`CMP` is not inherited by normal subgroups.

### Proof

Let

\[
D_8=\langle r,s\mid r^4=s^2=1,\ srs=r^{-1}\rangle.
\]

Its three maximal subgroups are

\[
\langle r\rangle,\qquad
\langle r^2,s\rangle,\qquad
\langle r^2,rs\rangle.
\]

They are complemented respectively by
\(\langle s\rangle,\langle rs\rangle,\langle s\rangle\). Hence `CMP(D8)`.
The normal subgroup \(\langle r\rangle\cong C_4\), however, has the unique
maximal subgroup \(\langle r^2\rangle\). A complement would be another
subgroup of order \(2\), but \(C_4\) has only one such subgroup. Therefore
`CMP(C4)` is false. \(\square\)

The GAP tests independently reproduce both conclusions from complete tables
of marks.

## 5. Consequence for Problem 18.68

Quotient closure permits a reduction through a chief factor, but Proposition
4.1 forbids the tempting step “a composition factor of a `CMP` group is
itself `CMP`.” A composition factor is a section, and neither the normal
subgroup step nor arbitrary section inheritance has been established. The
published simple-group classification therefore cannot be applied directly.
