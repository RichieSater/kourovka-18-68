# A reduction for Kourovka Problem 18.68 and an exact finite audit

> **Superseded on 2026-08-11.**  This report accurately records the earlier
> obstruction but predates the product-action lifting lemma, the exhaustive
> factor screen, and the 2-adic closeout.  The current complete candidate is
> [`../paper/kourovka-18-68.tex`](../paper/kourovka-18-68.tex).

**Research report dated 2026-08-11**
**Submission status:** incomplete; **not a solution of Problem 18.68**

## Abstract

Let `CMP(G)` mean that every maximal subgroup \(M\) of the finite group \(G\)
has a subgroup \(K\) such that \(G=MK\) and \(M\cap K=1\). Kourovka Problem
18.68 asks for the nonabelian composition factors of nonsoluble `CMP` groups.
The expected list is

\[
\operatorname{PSL}_2(7),\qquad
\operatorname{PSL}_2(11),\qquad
\operatorname{PSL}_5(2),
\]

which is known when the ambient group is simple and under the stronger
assumption that every maximal subgroup is Hall.

This report does not prove that expected answer. It proves that `CMP` is
quotient closed and that every nonabelian composition factor \(S\) of a `CMP`
group gives rise to a `CMP` monolithic quotient \(L\) with unique,
self-centralizing socle \(S^t\), together with a faithful primitive action of
\(L\) containing a regular subgroup. It then identifies the missing theorem:
one must classify such monolithic `CMP` groups, including the
non-almost-simple product-action cases and outer-automorphism fusion. Existing
almost-simple exact-factorization classifications do not supply that theorem.

As a finite check, a complete Table-of-Marks test was run on all 414 tables in
TomLib 1.2.11. Exactly 73 are `CMP`; among 88 nonabelian-simple tables, exactly
the three groups above are positive, and no positive table has another
nonabelian chief-factor order. These are exact bounded certificates, not an
exhaustive proof over all finite groups.

## 1. Problem and evidence status

For \(M\leq G\), “complement” is used in the exact sense

\[
G=MK,\qquad M\cap K=1.
\tag{1.1}
\]

This agrees with both original sources. The [21st Kourovka Notebook, July
2026](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/07/21tkt.pdf),
page 123, still asks for the nonabelian composition factors of a nonsoluble
group all of whose maximal subgroups have complements.

Thus the latest official source found still treats the question as open. A
dated English/Russian citation search found no later complete solution. The
official status is **published input**; the assertion that no solution exists
anywhere outside the searched literature is necessarily **unchecked**.

Levchuk and Likharev prove in
[Theorem 1](https://www.mathnet.ru/eng/smj896) that the nonabelian simple
`CMP` groups are exactly

\[
\operatorname{PSL}_2(7),\quad
\operatorname{PSL}_2(11),\quad
\operatorname{PSL}_5(2).
\tag{1.2}
\]

Maslova and Revin prove under the stronger Hall-maximal hypothesis that these
are the possible nonabelian composition factors and that every maximal
subgroup is complemented
([Theorems 1 and 2](https://www.mathnet.ru/eng/mt242)). Neither result proves
the desired assertion for an arbitrary `CMP` group: the Hall implication does
not reverse, and `CMP` is not inherited by sections.

## 2. Basic lemmas

### Lemma 2.1 — quotient closure

If `CMP(G)` and \(N\trianglelefteq G\), then `CMP(G/N)`.

#### Proof

Let \(\pi:G\to G/N\), and let \(\overline M\) be maximal in \(G/N\). Then
\(M=\pi^{-1}(\overline M)\) is maximal in \(G\) and contains \(N\). Choose a
complement \(K\) to \(M\). We have \(G/N=\overline M\pi(K)\). If
\(\pi(k)\in\overline M\) for \(k\in K\), then \(k\in M\), since \(N\leq M\),
and hence \(k=1\). Therefore \(\overline M\cap\pi(K)=1\). \(\square\)

### Lemma 2.2 — regular-action equivalence

A subgroup \(K\) complements \(M\leq G\) if and only if \(K\) is regular on
the coset space \(G/M\). If \(M\) is maximal and core-free, this is a faithful
primitive action.

#### Proof

Transitivity is equivalent to \(G=MK\), and the stabilizer in \(K\) of the
base coset is \(M\cap K\). \(\square\)

### Lemma 2.3 — normal inheritance is false

`CMP` does not pass to normal subgroups.

#### Proof

In

\[
D_8=\langle r,s\mid r^4=s^2=1,\ srs=r^{-1}\rangle,
\]

the maximal subgroups
\(\langle r\rangle,\langle r^2,s\rangle,\langle r^2,rs\rangle\) have
complements \(\langle s\rangle,\langle rs\rangle,\langle s\rangle\),
respectively. Thus `CMP(D8)`. But the normal subgroup
\(\langle r\rangle\cong C_4\) has a unique subgroup of order \(2\); its unique
maximal subgroup therefore has no complement. \(\square\)

Lemma 2.3 is the elementary obstruction to applying (1.2) directly to a
composition factor.

## 3. The valid reduction

### Theorem 3.1 — monolithic primitive reduction

Let \(G\) be a finite `CMP` group, and let \(S\) be a nonabelian composition
factor of \(G\). There exist \(t\geq1\), a quotient \(L\) of \(G\), a maximal
subgroup \(M<L\), and \(K\leq L\) such that:

1. `CMP(L)`;
2. \(\operatorname{Soc}(L)=N\cong S^t\) is the unique minimal normal subgroup
   of \(L\);
3. \(C_L(N)=1\);
4. \(M\) is core-free and \(N\nleq M\);
5. \(L=MK\) and \(M\cap K=1\).

In particular, \(L\) has a faithful primitive action with socle \(S^t\) and a
regular subgroup \(K\).

#### Proof

Choose a chief factor \(A/B\cong S^t\) of \(G\), and set

\[
C/B=C_{G/B}(A/B),\qquad L=G/C,\qquad N=AC/C.
\]

Since \(A/B\) is centerless, \(A\cap C=B\), so
\(N\cong A/B\cong S^t\). The chief property makes \(N\) a minimal normal
subgroup of \(L\).

The conjugation action embeds \(L\) faithfully into
\(\operatorname{Aut}(N)\), with \(N\) represented by its inner automorphisms.
An automorphism centralizing all inner automorphisms of the centerless group
\(N\) is trivial: for \(x\in N\), commutation with conjugation by \(x\) gives
\(\alpha(x)x^{-1}\in Z(N)=1\). Hence \(C_L(N)=1\).

If \(R\) were another minimal normal subgroup, then
\([R,N]\leq R\cap N=1\), whence \(R\leq C_L(N)=1\), a contradiction. Thus
\(N\) is the unique minimal normal subgroup and is the socle.

Lemma 2.1 gives `CMP(L)`. The nonabelian group \(N\) is not contained in
\(\Phi(L)\), since the Frattini subgroup of a finite group is nilpotent. Choose
a maximal subgroup \(M\) not containing \(N\). Then \(L=MN\). If
\(\operatorname{Core}_L(M)\ne1\), uniqueness of the minimal normal subgroup
forces \(N\leq\operatorname{Core}_L(M)\leq M\), a contradiction. Hence \(M\)
is core-free. Finally, `CMP(L)` supplies \(K\) satisfying (1.1), and Lemma 2.2
gives the stated primitive regular action. \(\square\)

### Corollary 3.2 — exact remaining theorem

Problem 18.68 would follow from the assertion:

> **(3.1)** If a finite monolithic group \(L\) has self-centralizing socle
> \(S^t\) and satisfies `CMP`, then
> \(S\cong L_2(7),L_2(11)\), or \(L_5(2)\).

No proof of (3.1) was found or obtained.

## 4. Why published exact-factorization classifications do not close (3.1)

For \(t=1\), \(L\) is almost simple. The almost-simple primitive regular
subgroup problem was classified by Liebeck--Praeger--Saxl, and the exact
factorizations of almost simple groups are now complete in work of
[Li--Wang--Xia](https://arxiv.org/abs/2012.09551), together with the
solvable-factor classification. A proof for \(t=1\) still requires an explicit
filter showing that **every** maximal subgroup of \(L\) occurs in one of the
exact rows and that no almost-simple extension with a different socle
survives. That filtering audit has not been completed here.

For \(t>1\), \(L\) is not almost simple. The O'Nan--Scott analysis admits
product-action, diagonal, and twisted-wreath configurations. The 2010
[Liebeck--Praeger--Saxl memoir](https://doi.org/10.1090/S0065-9266-09-00569-9)
explicitly left the product-action regular-subgroup case open. More
importantly, nothing in the almost-simple tables classifies all core-free
maximal subgroups of an arbitrary monolithic extension of \(S^t\).

One cannot evade this by fixing a maximal subgroup \(H<S\) and assuming that
\(H^t\) determines a maximal subgroup of \(L\). The action of \(L/N\) can fuse
\(S\)-conjugacy classes of maximal subgroups, so the corresponding product
subgroup need not have an overgroup supplementing \(N\). Proving that a
regular complement nevertheless yields a complement inside one component
would itself be a new inheritance/lifting lemma; no such lemma is proved in
the cited sources or in this report.

Thus (3.1), not a routine application of the simple classification, is the
decisive gap.

## 5. Exact finite certificates

### 5.1 Criterion

For a complete table of marks \(T\), let \(H_m\) represent a maximal-subgroup
class. A complement must have order \(\lvert G:H_m\rvert\), so its class
\(c\) lies in the
finite exhaustive list

\[
\{c:|H_c|=\lvert G:H_m\rvert\}.
\]

`IntersectionsTom(T,m,c)[1]` is positive precisely when some conjugate of
\(H_m\) meets some conjugate of \(H_c\) trivially. In that event, the order
formula gives \(|H_mH_c|=|G|\), and the pair is an exact factorization.
Therefore this criterion is necessary and sufficient relative to the complete
table.

### 5.2 Range and result

The producer used GAP 4.15.1 and TomLib 1.2.11:

```sh
gap -q tests/test-cmp-tom.g
gap -q gap/generate-tomlib-scan.g
python3 tests/check-tomlib-scan.py
```

It processed all 414 names returned by `AllLibTomNames()` and all 2,395
maximal classes in those tables.

| Result | Count |
|---|---:|
| `CMP` positive | 73 |
| `CMP` negative | 341 |
| nonabelian-simple tables | 88 |
| positive nonabelian-simple tables | 3 |
| positive nonsoluble tables | 13 |

The three positive simple tables are `L2(7)`, `L2(11)`, and `L5(2)`. Across
all positive tables, the non-prime-power chief-factor orders are exactly
\(168,660,9999360\), the orders of the groups in (1.2).

The summary certificate is
[`../data/tomlib-cmp-scan.tsv`](../data/tomlib-cmp-scan.tsv); the per-maximal
certificate is
[`../data/tomlib-cmp-maximals.tsv`](../data/tomlib-cmp-maximals.tsv). Missing
data cause an error rather than a negative verdict.

### 5.3 Scope

These conclusions are **computationally certified**, conditional on the
TomLib tables. They exhaust the bounded library, not all finite groups or all
monolithic extensions. They support (3.1) but do not prove it.

## 6. Correction to a published example

Maslova--Revin (2012), page 109 of the Russian edition, lists \(PGL_2(7)\) as
a nonsoluble `CMP` example. This conflicts with an exact certificate.
TomLib's `L2(7).2` table has a maximal subgroup of order \(12\), of index
\(28\), and no subgroup class of order \(28\). Hence this maximal subgroup has
no complement.

The nonexistence of an order-\(28\) subgroup also follows by Sylow theory. If
\(|K|=28\), its Sylow \(7\)-subgroup \(P\) is normal, so
\(K\leq N_{PGL_2(7)}(P)\). In the natural action on the eight points of the
projective line, each point stabilizer has shape \(7{:}6\) and contains the
unique Sylow \(7\)-subgroup fixing that point. Thus there are eight Sylow
\(7\)-subgroups and the normalizer has order \(336/8=42\). Since
\(28\nmid42\), no such \(K\) exists.

This correction does not affect the problem statement or its expected simple
list. It does show why every illustrative extension must be independently
checked.

## 7. Referee-facing claim matrix

| Claim | Status | Dependency |
|---|---|---|
| exact complement convention | **published input** | original papers |
| simple list (1.2) | **published input** | Levchuk--Likharev, Theorem 1 |
| quotient closure | **proved** | Lemma 2.1 |
| normal inheritance fails | **proved** | Lemma 2.3 |
| monolithic primitive reduction | **proved** | Theorem 3.1; finite Frattini nilpotence |
| 414-table verdict | **computationally certified** | GAP 4.15.1, TomLib 1.2.11 |
| universal three-factor answer | **conjectural** | missing assertion (3.1) |
| “no complete solution exists anywhere” | **unchecked** | a finite dated search cannot prove absence |

## 8. Conclusion

A peer-review-ready complete solution cannot honestly be claimed. The current
work establishes the correct reduction and removes several invalid shortcuts,
but assertion (3.1) remains. Any future manuscript claiming a solution must
at minimum:

1. filter the complete almost-simple exact-factorization classification for
   every maximal subgroup;
2. treat \(S^t\) for every \(t>1\), including product-action maximal
   subgroups and outer fusion;
3. prove any lifting from a regular subgroup of a primitive action to a
   complement in a simple component, rather than assume section inheritance;
4. connect every computational row to an exhaustive published
   classification.

Until those tasks are completed, the expected list (1.2) remains
**conjectural** for Problem 18.68.
