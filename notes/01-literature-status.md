# Dated literature and status audit

**Search date:** 2026-08-31
**Status conclusion:** the current official Notebook still presents 18.68 as
an unsolved question; no complete solution was found in this search. The
second clause is a search result, not a proof that no unindexed solution
exists.

## Search protocol

The search used English and Russian exact phrases, author/title searches,
forward-citation searches, DOI/MathNet records, arXiv, recent permutation-group
work, and the current Kourovka Notebook. Query angles included:

1. the exact English problem sentence;
2. “all maximal subgroups have complements” with “composition factors”;
3. “complemented maximal subgroups” with finite groups;
4. the Russian phrase “все максимальные подгруппы имеют дополнения”;
5. the Russian phrase with “композиционные факторы”;
6. citations to Levchuk--Likharev (2006);
7. citations to Maslova (2012) and Maslova--Revin (2012/2013);
8. exact factorizations of almost simple groups;
9. regular subgroups of primitive product-action groups;
10. recent work by Li, Wang, Xia, Huang, Burness, Praeger, and collaborators.

## Source findings

### Current official status

The [21st Kourovka Notebook, July
2026](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/07/21tkt.pdf),
page 123, reproduces Problem 18.68 without a solution annotation. This is
**published input** and is the strongest dated status evidence found.

### Original classification input

Levchuk and Likharev,
[“Finite simple groups with complemented maximal
subgroups”](https://www.mathnet.ru/eng/smj896), *Siberian Mathematical
Journal* 47 (2006), Theorem 1, prove that the nonabelian simple groups with
the property are exactly

\[
L_2(7),\quad L_2(11),\quad L_5(2).
\]

Their opening definition is the exact one: \(M\cap K=1\) and \(MK=G\).
This is **published input**; it says nothing by itself about a simple section
of a larger group.

Maslova's 2012 paper
[“Nonabelian composition factors of a finite group whose all maximal
subgroups are Hall”](https://www.mathnet.ru/eng/smj2330), *Siberian
Mathematical Journal* 53 (2012), 853--861, first obtained the same
composition-factor list under the stronger Hall-maximal hypothesis.

Maslova and Revin,
[“Finite groups whose maximal subgroups have the Hall
property”](https://www.mathnet.ru/eng/mt242), *Matematicheskie Trudy* 15(2)
(2012), Theorem 1 and Corollary 1, classify the normal structure under the
stronger Hall-maximal hypothesis. Their Theorem 2 proves that the
Hall-maximal class is contained in the complemented-maximal class. On page
109 of the Russian edition they then pose the composition-factor question
that became Problem 18.68. These are **published inputs**, but the implication
cannot be reversed.

Maslova's 2015 survey,
[“Finite groups with arithmetic restrictions on maximal
subgroups”](https://www.mathnet.ru/eng/al678), again explicitly identifies the
composition-factor question for complemented maximals. This supplies
historical status, not a solution.

Monakhov and Sokhor's 2025 paper
[“On Indices of Maximal Chains in Finite
Groups”](https://doi.org/10.1007/s00025-025-02468-5) studies monotone
sequences of subgroup indices along maximal chains and derives structural
consequences such as supersolvability. Its publisher abstract does not
address exact complements or the nonabelian composition-factor problem, so
it supplies neighboring context rather than an overlapping theorem.

### Exact factorizations and primitive groups

The broad structural framework predates the present argument.  Aschbacher and
Scott's [“Maximal subgroups of finite
groups”](https://doi.org/10.1016/0021-8693(85)90145-0), *Journal of Algebra*
92 (1985), organizes maximal subgroups through minimal normal subgroups.
Kovács's [“Maximal subgroups in composite finite
groups”](https://doi.org/10.1016/0021-8693(86)90058-X), *Journal of Algebra*
99 (1986), and [“Primitive subgroups of wreath products in product
action”](https://doi.org/10.1112/plms/s3-58.2.306), *Proceedings of the London
Mathematical Society* (3) 58 (1989), develop the composite-group and
product-action settings.  These are structural background, not proof inputs.
The present contribution is positioned more narrowly: a CMP-specific lift
from an arbitrary composition factor, followed by a synthesis of three
coordinate obstructions.

For a core-free maximal subgroup, a complement is exactly a regular subgroup
in the associated primitive coset action. Liebeck, Praeger, and Saxl,
[“Regular subgroups of primitive permutation
groups”](https://doi.org/10.1090/S0065-9266-09-00569-9), *Memoirs AMS* 203
(2010), classify the almost-simple case. Their introduction explicitly says
that the product-action case was left open at that time.

Li, Wang, and Xia,
[“The Exact Factorizations of Almost Simple
Groups”](https://arxiv.org/abs/2012.09551), *Journal of the London
Mathematical Society* 108 (2023), with arXiv v6 dated 2024-12-26, complete the
almost-simple exact-factorization classification by combining the
nonsolvable-factor theorem with the solvable-factor results. This is
**published input**, but its scope is almost simple; it does not classify
monolithic groups with socle \(S^t\), \(t>1\).

Recent 2025 talks and workshop reports announce further work on regular
subgroups in other O'Nan--Scott types. They were inspected for orientation
but are not used as proof inputs here.

## Source anomaly: \(PGL_2(7)\)

The 2012 Russian paper states that \(PGL_2(7)\) is a nonsoluble example with
complemented maximal subgroups. Under the paper's own exact definition, this
assertion is false. The complete TomLib table `L2(7).2` contains a maximal
subgroup of order \(12\), hence index \(28\), and contains no subgroup class
of order \(28\). Therefore that maximal subgroup cannot have a complement.

There is also a short order check. If a subgroup \(K\leq PGL_2(7)\) had order
\(28\), its Sylow \(7\)-subgroup \(P\) would be normal in \(K\), so
\(K\leq N_G(P)\). In the natural degree-eight action, a point stabilizer has
shape \(7{:}6\), its normal subgroup of order \(7\) fixes that point uniquely,
and every Sylow \(7\)-subgroup arises this way. Hence there are eight Sylow
\(7\)-subgroups and \(|N_G(P)|=336/8=42\), while \(28\nmid42\), a
contradiction. The 2015 survey retains the valid example
\(PSL_2(7)\times C_3\) but does not repeat \(PGL_2(7)\). No inference about
the reason for that omission is made.

**Evidence label:** the contradiction is computationally certified relative
to the complete table of marks, with an independent Sylow-order argument.

## Audit verdict

No source located in this dated search supplies the missing passage from an
arbitrary nonabelian chief factor \(S^t\) of a `CMP` group to the three simple
groups. The exact point at which existing published classifications stop is
made explicit in [`02-chief-factor-reduction.md`](02-chief-factor-reduction.md).
