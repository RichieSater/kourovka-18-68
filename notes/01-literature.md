# Literature and relation to earlier results

The [21st Kourovka Notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/07/21tkt.pdf),
Problem 18.68, asks for the nonabelian composition factors of a finite
nonsoluble group whose maximal subgroups all have exact complements. We are
not aware of an earlier solution.

## Complemented and Hall maximal subgroups

Levchuk and Likharev,
[“Finite simple groups with complemented maximal subgroups”](https://www.mathnet.ru/eng/smj896),
prove that the nonabelian simple groups with this property are exactly

\[
L_2(7),\qquad L_2(11),\qquad L_5(2).
\]

Their definition is the one used here: a complement \(K\) to \(M\) satisfies
\(M\cap K=1\) and \(MK=G\). Their theorem concerns simple groups and does not
by itself apply to a simple section of a larger group.

Maslova,
[“Nonabelian composition factors of a finite group whose all maximal
subgroups are Hall”](https://www.mathnet.ru/eng/smj2330), obtained the same
composition-factor list under the stronger hypothesis that every maximal
subgroup is a Hall subgroup. Maslova and Revin,
[“Finite groups whose maximal subgroups have the Hall
property”](https://www.mathnet.ru/eng/mt242), describe the structure under
that stronger hypothesis and prove that it implies the complemented-maximal
property. The converse is false, so these results do not settle Problem
18.68. Maslova's 2015 article
[“Finite groups with arithmetic restrictions on maximal
subgroups”](https://www.mathnet.ru/eng/al678) gives further context.

Monakhov and Sokhor,
[“On Indices of Maximal Chains in Finite
Groups”](https://doi.org/10.1007/s00025-025-02468-5), study monotone index
sequences along maximal chains. Their results concern a different condition
and do not address exact complements.

## Primitive groups and factorizations

For a core-free maximal subgroup \(M<G\), a complement to \(M\) is exactly a
regular subgroup in the primitive coset action of \(G\). The structural
background includes Aschbacher--Scott on maximal subgroups through minimal
normal subgroups, Kovács on maximal subgroups of composite groups, and Kovács
on primitive subgroups of wreath products in product action.

Liebeck--Praeger--Saxl classify transitive subgroups of primitive permutation
groups and, in Corollary 3(iv) of their 2000 paper, relate a regular subgroup
in product-action type to a core-free transitive subgroup of the
almost-simple component. Their 1990 memoir classifies maximal factorizations
of finite simple groups and their automorphism groups. Li--Wang--Xia later
completed the classification of exact factorizations of almost-simple groups.
These results control the coordinate groups in the present proof; the
monolithic reduction explains how they apply when the ambient socle is
\(S^k\) with arbitrary \(k\).

## The assertion about \(PGL_2(7)\)

The 2012 Russian paper of Maslova--Revin gives \(PGL_2(7)\) as a nonsoluble
example with complemented maximal subgroups. Under its stated exact
complement convention, this assertion is false. The complete TomLib table
“L2(7).2” has a maximal subgroup of order \(12\), hence index \(28\), but no
subgroup class of order \(28\).

There is also a direct order argument. If \(K\leq PGL_2(7)\) had order \(28\),
its Sylow \(7\)-subgroup \(P\) would be normal in \(K\), so
\(K\leq N_G(P)\). In the natural degree-eight action there are eight Sylow
\(7\)-subgroups, and therefore \(\lvert N_G(P)\rvert=336/8=42\). Since
\(28\nmid42\), no such \(K\) exists. The 2015 article retains the valid
example \(PSL_2(7)\times C_3\) and does not repeat the \(PGL_2(7)\) assertion.
