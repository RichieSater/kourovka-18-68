# References

**Sources consulted through:** 2026-09-02. Source PDFs are not committed because
redistribution rights were not established.

## Primary problem and original results

1. *The Kourovka Notebook: Unsolved Problems in Group Theory*, 21st issue,
   July 2026, Problem 18.68, PDF/printed page 123.
   [Official PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/07/21tkt.pdf).
   Downloaded-file SHA-256:
   `301b0cdcc53abc88b57cc0732cad73bf8fbe1c9ba0de5a0a794070398e3395fe`.
2. V. M. Levchuk and A. G. Likharev, “Finite simple groups with
   complemented maximal subgroups,” *Siberian Mathematical Journal* 47(4)
   (2006), 659–668. [MathNet record](https://www.mathnet.ru/eng/smj896),
   [DOI](https://doi.org/10.1007/s11202-006-0077-7). Theorem 1 is the simple
   classification; Lemmas 4 and 6 supply the occurrence direction for the
   three listed groups. PDF SHA-256:
   `5523f61ed06d93cebeee41499db6c69d7f2419aaa325778ba89001b8bb6bca99`.
3. N. V. Maslova, “Nonabelian composition factors of a finite group whose
   all maximal subgroups are Hall,” *Siberian Mathematical Journal* 53(5)
   (2012), 853--861. [MathNet record](https://www.mathnet.ru/eng/smj2330),
   [DOI](https://doi.org/10.1134/S0037446612050102). Theorem 1 gives the
   three-factor list under the stronger Hall-maximal hypothesis. Russian PDF SHA-256:
   `bd961717ad2cd134fc76faa01fef739f4c634287128a26176c30c785b985d423`.
4. N. V. Maslova and D. O. Revin, “Finite groups whose maximal subgroups
   have the Hall property,” *Matematicheskie Trudy* 15(2) (2012), 105–126;
   English translation, *Siberian Advances in Mathematics* 23(3) (2013),
   196–209. [MathNet record](https://www.mathnet.ru/eng/mt242),
   [DOI](https://doi.org/10.3103/S105513441303005X). Theorem 1 and Corollary
   1 give the Hall-maximal structure; Theorem 2 proves the implication to
   complemented maximals; page 109 poses the present problem. Russian PDF
   SHA-256:
   `adddf276422b7fe2f0b2cd86bcebe987a38ca7130f6cd65128e18a58f4353032`.
5. N. V. Maslova, “Finite groups with arithmetic restrictions on maximal
   subgroups,” *Algebra and Logic* 54(1) (2015), 65–69.
   [MathNet record](https://www.mathnet.ru/eng/al678),
   [DOI](https://doi.org/10.1007/s10469-015-9324-y). Russian PDF
   SHA-256:
   `ce2bc32b1dd68eaf83b1dd10516adf7833e7918c552528267f0b8923bf525278`.

## Proof inputs: primitive groups and maximal factorizations

### Structural background (not consumed as proof input)

- M. Aschbacher and L. Scott, “Maximal subgroups of finite groups,”
  *Journal of Algebra* 92 (1985), 44--80.
  [DOI](https://doi.org/10.1016/0021-8693(85)90145-0).
- L. G. Kovács, “Maximal subgroups in composite finite groups,”
  *Journal of Algebra* 99 (1986), 114--131.
  [DOI](https://doi.org/10.1016/0021-8693(86)90058-X).
- L. G. Kovács, “Primitive subgroups of wreath products in product action,”
  *Proceedings of the London Mathematical Society* (3) 58 (1989), 306--322.
  [DOI](https://doi.org/10.1112/plms/s3-58.2.306).

These sources locate the monolithic, chief-factor, and product-action
machinery.  The manuscript claims only the CMP-specific lift and
three-obstruction synthesis, not those general frameworks.

6. M. W. Liebeck, C. E. Praeger, and J. Saxl, “Transitive subgroups of
   primitive permutation groups,” *Journal of Algebra* 234 (2000), 291–361.
   [DOI](https://doi.org/10.1006/jabr.2000.8547). Corollary 3(iv) says that
   its product-action alternative has an almost-simple primitive component
   with a core-free transitive subgroup. In the manuscript the constructed
   action has \(k\geq2\), socle \(S^k\), component \(X\) on \(X/H\), and
   socle point stabilizer \((H\cap S)^k\), which is nontrivial and not
   subdirect. Thus it is exactly the product-action case of that corollary.
   Primary PDF SHA-256:

       ae0b23d751420b3840d3421d07bbc0fff891dec9bd814e31c0665a0507d9f00f

7. M. W. Liebeck, C. E. Praeger, and J. Saxl, *The Maximal Factorizations of
   the Finite Simple Groups and Their Automorphism Groups*, Memoirs AMS 86
   (1990), no. 432. [DOI](https://doi.org/10.1090/memo/0432),
   [primary publisher preview, p. 9](https://books.google.com/books?id=9WrUCQAAQBAJ&pg=PA9&vq=Theorem+D).
   Theorem D applies to
   \(L=A_n\trianglelefteq G\leq\operatorname{Aut}(L)\) with \(G=AB\) and
   neither factor containing \(L\). Its generic conclusion has
   \(A_{n-k}\leq A\leq S_{n-k}\times S_k\), \(1\leq k\leq5\), with \(B\)
   \(k\)-homogeneous; Remark 2 lists the exceptional degrees \(6,8,10\).
   The manuscript takes \(n\geq13\), \(A\) equal to a 6-set stabilizer, and
   \(B\) equal to a hypothetical core-free transitive factor, so all
   hypotheses match and the generic conclusion gives the required
   contradiction. Its classical tables are restated by Xia--Li below.
8. C. H. Li and B. Xia, *Factorizations of Almost Simple Groups with a
   Solvable Factor, and Cayley Graphs of Solvable Groups*, Memoirs AMS 279
   (2022), no. 1375, [DOI](https://doi.org/10.1090/memo/1375),
   [arXiv:1408.0350](https://arxiv.org/abs/1408.0350). Theorem 2.15 and
   Appendix Tables A.1--A.7 restate the LPS maximal-factorization
   list for almost-simple groups with classical socle, subject to the
   correction in item 9. PDF SHA-256:
   `4ef16aa4308f8c487a06e9c8e84ece77247d0e763146f0215d8e109e443e3a93`.
9. N. Gill, M. Giudici, and P. Spiga, “A generalization of Szep's conjecture
   for almost simple groups,” *Vietnam Journal of Mathematics* 52 (2024),
   325--359. [DOI](https://doi.org/10.1007/s10013-023-00635-1). Section 2
   supplies two omitted maximal factorizations for
   \(\operatorname{P}\Omega_8^+(4)\) and
   \(\operatorname{P}\Omega_8^+(16)\); neither affects the manuscript's
   central-node parabolic argument. PDF SHA-256:
   `152124653e92f7671426e07fccd43d548f960991de7c165b36d57aece3db54d4`.
10. C. Hering, M. W. Liebeck, and J. Saxl, “The factorizations of the finite
   exceptional groups of Lie type,” *Journal of Algebra* 106 (1987),
   517--527. [DOI](https://doi.org/10.1016/0021-8693(87)90013-5).
   Theorems 1--2 are exhaustive for exceptional simple groups and their
   automorphism groups. PDF SHA-256:
   `abdc30c6272a8e5bd14024c4bf39ee7ea57063e5e8e6d306084639fd3e89e357`.
11. M. Giudici, “Factorisations of sporadic simple groups,” *Journal of
    Algebra* 304 (2006), 311--323.
    [DOI](https://doi.org/10.1016/j.jalgebra.2006.04.019). Theorem 1.1 and
    Tables 1--2 treat simple sporadic groups; Theorem 1.2 and Table 3 treat
    the genuinely new outer cases; Theorem 1.3 and Table 4 list exact
    factorizations. The factor-free argument uses the complete lists in
    Tables 1--3, not the exact-only list in Table 4. PDF SHA-256:
   `cd2d8cb213c038193db9c0ba14b3d9042448a1861552014436c2be1900aea826`.
12. J. H. Conway, R. T. Curtis, S. P. Norton, R. A. Parker, and
    R. A. Wilson, *Atlas of Finite Groups*, Oxford, 1985. Its maximal-subgroup
    lists are used only to select sporadic maximal subgroups absent from
    Giudici's factorization tables. The eight published-only assertions are
    pinned to the official online ATLAS “Maximal subgroups” sections for
    [He and He.2](https://brauer.maths.qmul.ac.uk/Atlas/v3/spor/He/#maxes),
    [Ru](https://brauer.maths.qmul.ac.uk/Atlas/v3/spor/Ru/#maxes),
    [Suz and Suz.2](https://brauer.maths.qmul.ac.uk/Atlas/v3/spor/Suz/#maxes),
    [Fi22 and Fi22.2](https://brauer.maths.qmul.ac.uk/Atlas/v3/spor/F22/#maxes),
    and [Co1](https://brauer.maths.qmul.ac.uk/Atlas/v3/spor/Co1/#maxes).
13. M. W. Liebeck, C. E. Praeger, and J. Saxl, “Regular subgroups of
    primitive permutation groups,” *Memoirs of the American Mathematical
    Society* 203 (2010), no. 952.
    [DOI](https://doi.org/10.1090/S0065-9266-09-00569-9),
    [author-hosted PDF](https://www.ma.imperial.ac.uk/~mwl/REGFINAL.PDF).
    Lemmas 2.1--2.2 and Corollary 2.3 supply the
    \(\operatorname{PSp}_4(2^f)\) involution-class input.  Section 10,
    case (10.1), is **not** used to infer maximality of an
    \(O_4^+\)-normalizer in an arbitrary outer coordinate group. PDF
    SHA-256:
    `00a76f52b998f4017127c5c4e5e971b36501475092f402cf7bff3e84f222c03b`.

14. J. N. Bray, D. F. Holt, and C. M. Roney-Dougal, *The Maximal Subgroups
    of the Low-Dimensional Finite Classical Groups*, London Mathematical
    Society Lecture Note Series 407, Cambridge University Press, 2013.
    [DOI](https://doi.org/10.1017/CBO9781139192576),
    [publisher Chapter 8 locator](https://www.cambridge.org/core/books/abs/maximal-subgroups-of-the-lowdimensional-finite-classical-groups/tables/E93516E412E7226B7535F385BED059C1),
    [Chapter 8 DOI](https://doi.org/10.1017/CBO9781139192576.010).
    Table 8.14 is the exact maximal-subgroup source for the prime-degree
    subfield subgroup \(\operatorname{Sp}_4(q_0)<\operatorname{Sp}_4(q)\).
    The same row is independently stated in item 15, and the scope of Table
    8.14 is described in item 16.
15. T. C. Burness, “On base sizes for actions of finite classical groups,”
    *Journal of the London Mathematical Society* 75 (2007), 545--562.
    [DOI](https://doi.org/10.1112/jlms/jdm033),
    [author PDF](https://seis.bristol.ac.uk/~tb13602/docs/baselms.pdf).
    Proposition 4.2 and Table 3 record the
    \(\operatorname{Sp}_4(q_0)\) row with \(q=q_0^r\), \(r\) prime. PDF SHA-256:
    `dcf25d06cf433dfa32734d6ceb7289f8913d34e8ba2360a89c0a520302bd31bf`.
16. S. Harper, “Totally deranged elements of almost simple groups and
    invariable generating sets,” *Journal of the London Mathematical
    Society* 109(6) (2024), e12935.
    [DOI](https://doi.org/10.1112/jlms.12935),
    [open author manuscript](https://research-repository.st-andrews.ac.uk/handle/10023/29976).
    The setup before Lemma 2.1 and Theorem 4(a) records
    \(\rho^2=\varphi\), while Lemma 2.1 gives
    \(\operatorname{Aut}(\operatorname{Sp}_4(2^f))=\langle S,\rho\rangle\);
    Section 3.5 identifies BHRD Table 8.14 as the
    complete maximal-subgroup source. PDF SHA-256:
    `b741f7dfecd2dc78d37a7f2a9d5a5bb928eceb94cde290193980a1ee6d3ff522`.
17. P. B. Kleidman and M. W. Liebeck, *The Subgroup Structure of the
    Finite Classical Groups*, London Mathematical Society Lecture Note
    Series 129, Cambridge University Press, 1990.
    [DOI](https://doi.org/10.1017/CBO9780511629235). Chapters 3--4 are the
    standard reference for the geometric-subgroup maximality statements
    used in the classical-group argument.
18. L. L. Scott, “Representations in characteristic (p),” in *The Santa
    Cruz Conference on Finite Groups*, Proceedings of Symposia in Pure
    Mathematics 37, American Mathematical Society, 1980, 319--331.
    [DOI](https://doi.org/10.1090/pspum/037/604599). The lemma on page 328
    supplies the direct product of disjoint full diagonal strips used in the
    product-action lifting theorem.

## Additional exact-factorization sources

19. C. H. Li, L. Wang, and B. Xia, “The Exact Factorizations of Almost Simple
    Groups,” *Journal of the London Mathematical Society* 108 (2023),
    1417--1447, [arXiv:2012.09551 v6](https://arxiv.org/abs/2012.09551).
    v6 PDF SHA-256:
    `991992d864f8e44cd652a9f4386989b659986253edfef780c7b65c600bfd88f9`.
20. T. C. Burness and C. H. Li, “On solvable factors of almost simple groups,”
    [author-hosted PDF](https://seis.bristol.ac.uk/~tb13602/docs/BL_factorisations_final.pdf).
    PDF SHA-256:
    `7fae2925a45f86e4804a39577b85967ce50fb3c02454937824e7f46b958f63bd`.

21. V. S. Monakhov and I. L. Sokhor, “On Indices of Maximal Chains in
    Finite Groups,” *Results in Mathematics* 80 (2025), article 155,
    [DOI](https://doi.org/10.1007/s00025-025-02468-5). The publisher abstract
    concerns monotone index sequences in maximal chains and structural
    consequences such as supersolvability. It does not classify exact
    complements or nonabelian composition factors and is cited only to mark
    the boundary with recent maximal-subgroup-index work. The publisher
    abstract and metadata were inspected on 2026-08-31; the subscription
    article was not used as a proof input.

## Non-proof orientation sources

Recent workshop reports and slides on regular subgroups of primitive groups
were checked for status orientation. They are not used as classification
inputs in the proof:

- H. Huang, [“Regular subgroups of primitive groups” (2025
  slides)](https://hongyihuang328.github.io/talks/Kunming_251112.pdf).
- [Oberwolfach Report 16/2025](https://oa.tib.eu/renate/server/api/core/bitstreams/bcbd7e3c-e1cc-43a8-9a00-46c39314f494/content).

The manuscript's universal steps use the published exhaustive inputs above;
the slides and bounded GAP scans are not used to extrapolate an infinite
family statement.
