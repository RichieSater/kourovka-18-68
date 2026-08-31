# Product-action and prime-divisibility lifting

**Status:** the lemmas in Sections 1--5 are **proved** below, except for the
explicitly formulated LPS consequence, which is a **source assumption whose
exact primary-text match is unchecked**.  This note
replaces the product-action blocker recorded in the first research report.

Throughout, \(S\) is a nonabelian finite simple group and
\(S\leq X\leq\operatorname{Aut}(S)\).

## 1. The coordinate group of a monolithic quotient

Let \(L\) have unique self-centralizing minimal normal subgroup

\[
N=S_1\times\cdots\times S_k\cong S^k.
\]

The action of \(L\) on the factors is transitive: otherwise the product of
the factors in one orbit is a second nontrivial proper normal subgroup of
\(L\).  Put

\[
X=N_L(S_1)/C_L(S_1),
\]

identifying \(S_1\cong S\) with its inner automorphism group.  Then
\(S\leq X\leq\operatorname{Aut}(S)\).  The standard wreath embedding gives

\[
L\hookrightarrow X\wr P\leq X\wr\operatorname{Sym}(k),
\tag{4.1}
\]

where \(P\) is transitive, \(N\) is the base socle \(S^k\), and the component
induced by a coordinate stabilizer is \(X\).  Faithfulness follows from
\(C_L(N)=1\).

## 2. Building a new primitive action of the same group

Let \(H<X\) be core-free and maximal, put
\(\Delta=X/H\), and let \(V=H\cap S\).  Since \(S\not\leq H\), normality and
maximality give \(X=SH\); hence \(S\) is transitive on \(\Delta\).  Assume
\(V\ne1\), as will hold for every action used in the family audit.

Use (4.1) to let \(L\) act on \(\Omega=\Delta^k\) in product action.

### Lemma 4.1 (primitivity of the induced product action)

The action of \(L\) on \(\Delta^k\) is faithful and primitive.

#### Proof

Faithfulness follows because the action of \(X\) on \(X/H\) is faithful and
(4.1) is faithful.  Let \(\omega=(H,\ldots,H)\) and \(M=L_\omega\).  The
socle \(N=S^k\) is transitive, so \(L=MN\) and
\(M\cap N=V^k\).

Suppose \(M\leq J\leq L\), and put \(D=J\cap N\).  Dedekind's identity gives
\(J=MD\), while \(D\trianglelefteq M\) and \(V^k\leq D\).

The image of \(M\) on the \(k\) factors is transitive.  Indeed, an element
of \(L\) with any prescribed top permutation can be multiplied by an
element of the transitive base group \(N\) so that it fixes \(\omega\).  The
subgroup of \(M\) stabilizing coordinate \(i\) induces \(H\) on that
coordinate: one inclusion is immediate, and the reverse inclusion follows
by correcting all other coordinates with elements of \(N\).

Let \(D_i\) be the projection of \(D\) to \(S_i\cong S\).  Then
\(V\leq D_i\leq S\), and \(D_i\) is normalized by \(H\).  Since \(H\) is
maximal in \(X\), either \(D_i=V\) or \(HD_i=X\).  In the latter case,

\[
S=(HD_i)\cap S=(H\cap S)D_i=VD_i=D_i.
\]

Transitivity on the factors makes the same alternative hold for every
coordinate.  If all \(D_i=V\), then \(D=V^k\) and \(J=M\).  If all
\(D_i=S\), then \(D\) is subdirect in \(S^k\).  Scott's lemma expresses such
a subgroup as a direct product of full diagonal strips.  Because \(D\)
contains \(V^k\) and \(V\ne1\), no strip can involve two coordinates;
therefore \(D=S^k\) and \(J=L\).  Thus \(M\) is maximal.  \(\square\)

This is a product-action action: its socle point stabilizer is the direct
product \(V^k\), with nontrivial proper projection to every simple factor.

## 3. The LPS coordinate obstruction

Call the primitive action \((X,\Delta)\) **factor-free** if it has no
core-free transitive subgroup; equivalently, there is no core-free
\(C<X\) with \(X=HC\).

### Source assumption 4.2 (LPS coordinate consequence)

The paper attributes the following consumed consequence to Corollary 3(iv) of
Liebeck--Praeger--Saxl, *J. Algebra* 234 (2000): if a primitive product-action
group with socle \(S^k\), \(k\ge2\), contains a regular subgroup, then its
almost-simple coordinate action has a core-free transitive subgroup.  The
exact primary text was not reopened in source traces through 2026-08-31, so
this match remains an explicit assumption rather than an audited quotation.

Consequently, if \((X,X/H)\) is factor-free, the action in Lemma 4.1 has no
regular subgroup.  For \(k=1\), note first that \(L=X\).  If \(R\) were regular
on \(X/H\), then \(R\cap H=1\).  Every nontrivial normal subgroup of the
almost-simple group \(X\) contains its socle \(S\).  Thus a nontrivial core of
\(R\) would force \(S\le R\), contradicting
\(1\ne H\cap S\le H\) and \(R\cap H=1\).  Hence \(R\) would be core-free and
transitive, contrary to factor-freeness.  (Regularity alone does **not**
imply core-freeness for an arbitrary group action.)

### Corollary 4.3

If \(L\) has property `CMP`, then no coordinate group \(X\) of \(L\) admits
a factor-free action of the kind above.

#### Proof

The point stabilizer in Lemma 4.1 is maximal.  `CMP(L)` would give it a
complement, which is regular on \(\Delta^k\), contradicting Source assumption
4.2 (or the direct \(k=1\) observation).  \(\square\)

## 4. A factor-screen lemma

The next lemma is what makes the published almost-simple factorization
tables sufficient even though \(k\) is arbitrary.

### Lemma 4.4 (maximal-factor screen)

Let \(1<V<S\), and suppose the \(S\)-conjugacy class of \(V\) is invariant
under \(X\).  Choose a maximal subgroup \(H<X\) containing \(N_X(V)\).
Then \(H\) is core-free and \(X=HS\).  If \(X/H\) is not factor-free, there
are

* an almost-simple group \(Y\), with \(S\leq Y\leq X\), and
* a nontrivial maximal factorization \(Y=AB\)

such that \(V\leq A\cap S\), after interchanging \(A,B\) if necessary.

#### Proof

Class invariance gives \(N_X(V)S=X\).  Hence no proper overgroup of
\(N_X(V)\) contains \(S\), so \(H\) is core-free and \(HS=X\).

If \(C<X\) is core-free and transitive on \(X/H\), then \(X=HC\).  Put
\(Y=CS\).  Since \(C\leq Y\), the factorization restricts to

\[
Y=(H\cap Y)C.
\]

Moreover, both \(H\cap Y\) and \(C\) supplement \(S\) in \(Y\).  Therefore
every proper maximal overgroup of either factor is core-free.  Enlarge the
two factors to core-free maximal subgroups \(A,B<Y\).  Then \(Y=AB\), and
\(V\leq H\cap S\leq A\cap S\).  \(\square\)

Thus a subgroup \(V\) gives a factor-free action as soon as no factor on the
published maximal-factorization list has intersection with \(S\) containing
\(V\).

## 5. Prime lifting

An action is **\(p\)-elusive** if \(p\) divides its degree and every element
of order \(p\) fixes a point.

### Lemma 4.5 (full-coordinate lifting)

If \(X\) is \(p\)-elusive on \(\Delta\), then
\(X\wr\operatorname{Sym}(k)\) is \(p\)-elusive on \(\Delta^k\).

#### Proof

Let \(w=(x_1,\ldots,x_k)\sigma\) have order \(p\).  On a fixed point of
\(\sigma\), the corresponding \(x_i\) has order \(1\) or \(p\), and hence
fixes a point of \(\Delta\).  On a \(p\)-cycle of \(\sigma\), the cycle
product of the \(x_i\) is \(1\), because \(w^p=1\); the coordinate fixed
point equations can therefore be solved successively around the cycle.
Combining the solutions gives a fixed tuple.  \(\square\)

In particular, no subgroup of this wreath product can be regular on
\(\Delta^k\): its order would be divisible by \(p\), so Cauchy's theorem
would supply a fixed-point element of order \(p\).

### Lemma 4.6 (socle-valuation lifting)

Suppose \(S\) is \(p\)-elusive on \(\Delta=X/H\).  Set

\[
a=v_p(\lvert\Delta\rvert),\qquad o=v_p(\lvert X:S\rvert).
\]

If \(a>o\), then no group \(L\leq X\wr\operatorname{Sym}(k)\) containing
\(S^k\) has a regular subgroup on \(\Delta^k\).

#### Proof

Suppose \(R\) is regular and put \(Q=R\cap S^k\).  Since
\(R/Q\hookrightarrow L/S^k\),

\[
v_p(\lvert R:Q\rvert)\leq ko+v_p(k!).
\]

Regularity gives \(v_p(\lvert R\rvert)=ka\), and hence

\[
v_p(\lvert Q\rvert)\geq k(a-o)-v_p(k!)>0,
\]

because \(a-o\ge1\) and \(v_p(k!)<k\).  Thus \(Q\) has an element
\(z=(z_1,\ldots,z_k)\) of order \(p\).  Each nonidentity coordinate \(z_i\)
fixes a point of \(\Delta\), while an identity coordinate fixes every point.
So \(z\) fixes a tuple, contradicting regularity.  \(\square\)

## 6. The infinite symplectic survivor: prime-degree subfields

Let \(S=\operatorname{PSp}_4(q)=\operatorname{Sp}_4(q)\), where
\(q=2^f\) and \(f\ge2\).  Choose a prime \(r\mid f\), put
\(d=f/r\) and \(q_0=2^d\), and take the standard subfield subgroup

\[
V=\operatorname{Sp}_4(q_0)<S.
\]

### 6.1 Maximality and every outer coordinate group

**Published input.**  Bray--Holt--Roney-Dougal, Table 8.14, lists the
subfield subgroup \(\operatorname{Sp}_4(q_0)\) as maximal when
\(q=q_0^r\) and \(r\) is prime.  Burness, Proposition 4.2 and Table 3, is an
independent accessible statement of the same row.

Use the adjoint algebraic group of type \(B_2\) in characteristic two.  Let
\(\varphi\) be standard Frobenius and \(\rho\) the exceptional graph-field
endomorphism.  Harper's setup before Lemma 2.1 and Theorem 4(a) gives
\(\rho^2=\varphi\), while Lemma 2.1 gives the automorphism-group
description:

\[
\rho^2=\varphi,
\qquad \operatorname{Aut}(S)=\langle S,\rho\rangle.
\]

In particular, \(\rho\) commutes with \(\varphi\).  The standard subgroup
\(V\) is the \(\varphi^d\)-fixed subgroup, so \(\rho\) normalizes \(V\).  Thus
the \(S\)-class of \(V\) is invariant under the full automorphism group, not
only under field automorphisms.  This explicitly covers every
\(S\le X\le\operatorname{Aut}(S)\), including graph-outer \(X\).

Set \(H=N_X(V)\).  Class invariance gives \(X=SH\).  Since \(V\) is maximal
and nonnormal in the simple group \(S\),

\[
H\cap S=N_S(V)=V.
\]

The subgroup \(H\) is maximal in \(X\).  If \(H<K<X\), then
\(V\le K\cap S\le S\), so maximality of \(V\) gives
\(K\cap S=V\) or \(S\).  In the first case,
\(V=K\cap S\trianglelefteq K\), whence \(K\le N_X(V)=H\); in the second,
\(X=SH\le K\).  Both are impossible.  It is also core-free: every
nontrivial normal subgroup of an almost-simple group contains its socle,
whereas \(H\cap S=V<S\).

### 6.2 Involution coverage descends to the prime field

LPS (2010), Lemma 2.1, says that \(S\) has the three involution types
\(b_1,a_2,c_2\).  Lemma 2.2(i) says that conjugacy in \(O_4^+(q)\) agrees
with conjugacy in \(S\), and Corollary 2.3 says that every one of the three
classes meets \(O_4^+(q)\).

Write

\[
O_4^+(q)\cong
(\operatorname{SL}_2(q)\times\operatorname{SL}_2(q))
\rtimes\langle\tau\rangle,
\]

where \(\tau\) swaps the two factors.  If \(u\) represents the unique
nonidentity involution class of \(\operatorname{SL}_2(q)\), the three
involution classes in this semidirect product are represented by

\[
(u,1),\qquad (u,u),\qquad \tau.
\]

Indeed, an involution in the base has one of the first two forms up to
conjugacy and swapping, while every involution outside the base is conjugate
to \(\tau\).  Choose \(u\in\operatorname{SL}_2(2)\).  All three representatives
then belong to

\[
O_4^+(2)\le\operatorname{Sp}_4(2)\le V.
\]

Consequently every involution class of \(S\) meets \(V\), and \(S\) is
2-elusive on \(X/H\).

### 6.3 The valuation inequality

Since \(X=SH\),

\[
\lvert X:H\rvert=\lvert S:V\rvert
=\frac{q^4(q^2-1)(q^4-1)}
       {q_0^4(q_0^2-1)(q_0^4-1)},
\qquad
a=v_2(\lvert X:H\rvert)=4(f-d).
\]

The same outer description gives \(\lvert X:S\rvert\mid2f\), so

\[
o=v_2(\lvert X:S\rvert)\le1+v_2(f)<2f\le4(f-d)=a.
\]

Lemma 4.6 excludes a regular subgroup for every \(k\ge1\). At the finite
regression parameter \(q=4\), \(X=\operatorname{Aut}(S)\), the corrected normalizer
has order 2880, socle intersection 720, and index 1360.  This is separately
reproduced by `tests/test-sp4-subfield.g` under GAP 4.15.1 and AtlasRep
2.1.11.

This replaces the invalid \(N_X(\Omega_4^+(q))\) construction: that old
normalizer need not supplement the socle when graph-field automorphisms are
present.
