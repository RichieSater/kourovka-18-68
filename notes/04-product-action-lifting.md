# Product-action and prime-divisibility lifting

**Status:** the lemmas in Sections 1--5 are **proved** below, except for the
explicitly cited LPS consequence, which is **published input**.  This note
replaces the product-action blocker recorded in the first research report.

Throughout, (S) is a nonabelian finite simple group and
(S\leq X\leq\operatorname{Aut}(S)).

## 1. The coordinate group of a monolithic quotient

Let (L) have unique self-centralizing minimal normal subgroup

\[
N=S_1\times\cdots\times S_k\cong S^k.
\]

The action of (L) on the factors is transitive: otherwise the product of
the factors in one orbit is a second nontrivial proper normal subgroup of
(L).  Put

\[
X=N_L(S_1)/C_L(S_1),
\]

identifying (S_1\cong S\) with its inner automorphism group.  Then
(S\leq X\leq\operatorname{Aut}(S)).  The standard wreath embedding gives

\[
L\hookrightarrow X\wr P\leq X\wr\operatorname{Sym}(k),
\tag{4.1}
\]

where (P) is transitive, (N) is the base socle (S^k), and the component
induced by a coordinate stabilizer is (X).  Faithfulness follows from
(C_L(N)=1).

## 2. Building a new primitive action of the same group

Let (H<X) be core-free and maximal, put
(Delta=X/H), and let (V=H\cap S).  Since (S\not\leq H), normality and
maximality give (X=SH); hence (S) is transitive on (Delta).  Assume
(V\ne1), as will hold for every action used in the family audit.

Use (4.1) to let (L) act on (Omega=Delta^k) in product action.

### Lemma 4.1 (primitivity of the induced product action)

The action of (L) on (Delta^k) is faithful and primitive.

#### Proof

Faithfulness follows because the action of (X) on (X/H) is faithful and
(4.1) is faithful.  Let (omega=(H,\ldots,H)) and (M=L_\omega).  The
socle (N=S^k) is transitive, so (L=MN) and
(M\cap N=V^k).

Suppose (M\leq J\leq L), and put (D=J\cap N).  Dedekind's identity gives
(J=MD), while (D\trianglelefteq M) and (V^k\leq D).

The image of (M) on the (k) factors is transitive.  Indeed, an element
of (L) with any prescribed top permutation can be multiplied by an
element of the transitive base group (N) so that it fixes (omega).  The
subgroup of (M) stabilizing coordinate (i) induces (H) on that
coordinate: one inclusion is immediate, and the reverse inclusion follows
by correcting all other coordinates with elements of (N).

Let (D_i) be the projection of (D) to (S_i\cong S).  Then
(V\leq D_i\leq S), and (D_i) is normalized by (H).  Since (H) is
maximal in (X), either (D_i=V) or (HD_i=X).  In the latter case,

\[
S=(HD_i)\cap S=(H\cap S)D_i=VD_i=D_i.
\]

Transitivity on the factors makes the same alternative hold for every
coordinate.  If all (D_i=V), then (D=V^k) and (J=M).  If all
(D_i=S), then (D) is subdirect in (S^k).  Scott's lemma expresses such
a subgroup as a direct product of full diagonal strips.  Because (D)
contains (V^k) and (V\ne1), no strip can involve two coordinates;
therefore (D=S^k) and (J=L).  Thus (M) is maximal.  \(square\)

This is a product-action action: its socle point stabilizer is the direct
product (V^k), with nontrivial proper projection to every simple factor.

## 3. The LPS coordinate obstruction

Call the primitive action ((X,Delta)) **factor-free** if it has no
core-free transitive subgroup; equivalently, there is no core-free
(C<X) with (X=HC).

### Published input 4.2 (LPS coordinate consequence)

Corollary 3(iv) of Liebeck--Praeger--Saxl, *J. Algebra* 234 (2000), says
that if a primitive product-action group with socle (S^k), (k\ge2),
contains a regular subgroup, then its almost-simple coordinate action has a
core-free transitive subgroup.

Consequently, if ((X,X/H)) is factor-free, the action in Lemma 4.1 has no
regular subgroup.  For (k=1) the same conclusion is immediate: a regular
subgroup of (X) on (X/H) is itself core-free and transitive.

### Corollary 4.3

If (L) has property `CMP`, then no coordinate group (X) of (L) admits
a factor-free action of the kind above.

#### Proof

The point stabilizer in Lemma 4.1 is maximal.  `CMP(L)` would give it a
complement, which is regular on (Delta^k), contradicting Published input
4.2 (or the direct (k=1) observation).  \(square\)

## 4. A factor-screen lemma

The next lemma is what makes the published almost-simple factorization
tables sufficient even though (k) is arbitrary.

### Lemma 4.4 (maximal-factor screen)

Let (1<V<S), and suppose the (S)-conjugacy class of (V) is invariant
under (X).  Choose a maximal subgroup (H<X) containing (N_X(V)).
Then (H) is core-free and (X=HS).  If (X/H) is not factor-free, there
are

* an almost-simple group (Y), with (S\leq Y\leq X), and
* a nontrivial maximal factorization (Y=AB)

such that (V\leq A\cap S), after interchanging (A,B) if necessary.

#### Proof

Class invariance gives (N_X(V)S=X).  Hence no proper overgroup of
(N_X(V)) contains (S), so (H) is core-free and (HS=X).

If (C<X) is core-free and transitive on (X/H), then (X=HC).  Put
(Y=CS).  Since (C\leq Y), the factorization restricts to

\[
Y=(H\cap Y)C.
\]

Moreover, both (H\cap Y) and (C) supplement (S) in (Y).  Therefore
every proper maximal overgroup of either factor is core-free.  Enlarge the
two factors to core-free maximal subgroups (A,B<Y).  Then (Y=AB), and
(V\leq H\cap S\leq A\cap S).  \(square\)

Thus a subgroup (V) gives a factor-free action as soon as no factor on the
published maximal-factorization list has intersection with (S) containing
(V).

## 5. Prime lifting

An action is **(p)-elusive** if (p) divides its degree and every element
of order (p) fixes a point.

### Lemma 4.5 (full-coordinate lifting)

If (X) is (p)-elusive on (Delta), then
(X\wr\operatorname{Sym}(k)) is (p)-elusive on (Delta^k).

#### Proof

Let (w=(x_1,\ldots,x_k)\sigma) have order (p).  On a fixed point of
(sigma), the corresponding (x_i) has order (1) or (p), and hence
fixes a point of (Delta).  On a (p)-cycle of (sigma), the cycle
product of the (x_i) is (1), because (w^p=1); the coordinate fixed
point equations can therefore be solved successively around the cycle.
Combining the solutions gives a fixed tuple.  \(square\)

In particular, no subgroup of this wreath product can be regular on
(Delta^k): its order would be divisible by (p), so Cauchy's theorem
would supply a fixed-point element of order (p).

### Lemma 4.6 (socle-valuation lifting)

Suppose (S) is (p)-elusive on (Delta=X/H).  Set

\[
a=v_p(|\Delta|),\qquad o=v_p(|X/S|).
\]

If (a>o), then no group (L\leq X\wr\operatorname{Sym}(k)) containing
(S^k) has a regular subgroup on (Delta^k).

#### Proof

Suppose (R) is regular and put (Q=R\cap S^k).  Since
(R/Q\hookrightarrow L/S^k),

\[
v_p(|R/Q|)\leq ko+v_p(k!).
\]

Regularity gives (v_p(|R|)=ka), and hence

\[
v_p(|Q|)\geq k(a-o)-v_p(k!)>0,
\]

because (a-o\ge1) and (v_p(k!)<k).  Thus (Q) has an element
(z=(z_1,\ldots,z_k)) of order (p).  Each nonidentity coordinate (z_i)
fixes a point of (Delta), while an identity coordinate fixes every point.
So (z) fixes a tuple, contradicting regularity.  \(square\)

## 6. The infinite symplectic survivor

Let (S=\operatorname{PSp}_4(q)=\operatorname{Sp}_4(q)), where
(q=2^f) and (f\ge2).  Put (U=\Omega_4^+(q)) and
(H=N_X(U)).  LPS (2010), Section 10, case (10.1), gives that (H) is
maximal and (H\cap S=O_4^+(q)).  Its degree is

\[
d=\lvert S:O_4^+(q)\rvert=\frac{q^2(q^2+1)}2,
\qquad v_2(d)=2f-1.
\]

LPS (2010), Corollary 2.3, shows that (O_4^+(q)) meets every involution
class of (S).  Hence (S) is 2-elusive on (X/H).  Also

\[
|X/S|\mid 2f,
\qquad v_2(|X/S|)\le1+v_2(f)<2f-1.
\]

The divisibility is the standard outer-automorphism description recorded in
Xia--Li, Table 2.1; only this upper bound, not equality for a particular
coordinate group (X), is used.

Lemma 4.6 therefore excludes a regular subgroup for every (k\ge1).
This is the prime-divisibility step that closes the only infinite classical
factor-screen survivor.
