# Problem 18.68 solution and review plan

**Current stage:** All four internal rounds are complete. The hard-final
source-workspace candidate `3a39b3d2ec29aab0d0a156aff93d35dc330f567d` passed Referee 4 with
the recommendation **circulate for external specialist review**. The
graph-outer symplectic defect `R186-PR1-01` is answered by a uniform
prime-degree subfield action. External specialist review remains pending.
The reports preserve their original source-workspace commit hashes. Version
1.0.2 of this standalone repository contains the reviewed final tree.

## Milestones

| Milestone | Status | Required focus | Artifact |
|---|---|---|---|
| Initial solution | complete | Full composition-factor theorem under complemented maximals | `reviews/00-initial-solution.md`; `915e4c4` |
| Revision 1 | complete | Answer every item in `reviews/01-pre-revision-referee.md`, especially the graph-outer \(\operatorname{PSp}_4(2^f)\) screen; recheck complement convention and quotient/section/extension behavior | `reviews/01-revision.md`; `580255e809726fd224b75382220f7197612d81c2` |
| Referee 1 | complete | Independent structural and minimality audit | `reviews/01-referee.md`; pass |
| Revision 2 | complete | Classification completeness, source scope, low parameters, and outer automorphisms | `reviews/02-revision.md`; `3bcf19c6ee90042bc392aaac508c559541fae272` |
| Referee 2 | complete | Independent extension and classification-source audit | `reviews/02-referee.md`; pass |
| Revision 3 | complete | Complement certificates, finite scans, mutation controls, and reproducibility | `reviews/03-revision.md`; `c815d3ba8cc9cf587aa738135b9bac4cb50ccfd1` |
| Referee 3 | complete | Fresh-clone witness/completeness/mutation audit | `reviews/03-referee.md`; pass |
| Revision 4 | complete | Arbitrary composition-factor synthesis, status/disclosure cleanup, and release candidate | `reviews/04-revision.md`; `3a39b3d2ec29aab0d0a156aff93d35dc330f567d` |
| Referee 4 | complete | Hard-final theorem/source/certificate pass | `reviews/04-referee.md`; circulate for external specialist review |

## Initial-solution instructions

The candidate must fix the exact meaning of complement, prove how the ambient
property reaches arbitrary composition factors, and not infer the answer from
the stronger Hall-maximal hypothesis. It must reproduce the known simple list
\(L_2(7),L_2(11),L_5(2)\), handle split and nonsplit extensions, and give
explicit complement or non-complement evidence for every finite certificate.

## Four review rounds

1. **Structural:** attack quotient inheritance, Frattini reductions, direct
   products, and every primitive/monolithic transition.
2. **Extension/classification:** independently check cohomology claims,
   complement existence versus conjugacy, and all simple-family sources.
3. **Computation:** require exhaustive candidate-complement coverage or a
   mathematically complete nonexistence certificate; rerun in isolation.
4. **Hard final:** verify that the conclusion controls every nonabelian
   composition factor rather than only the socle of a minimal example.

No milestone may move to `complete` from a split-extension scan alone.

The complete draft at candidate commit
`915e4c4487aa5ed4fcd753b51ea07916a9aaf3ea` is frozen for the first referee
pass. Its claimed proof status is internal; external specialist review remains
outstanding.

The full initial-candidate pass is preserved at
[`reviews/01-pre-revision-referee.md`](reviews/01-pre-revision-referee.md).
It reviewed the exact frozen commit, issued a **major revision** verdict, and
is deliberately non-milestone because the repository protocol requires
Revision 1 before formal Referee 1.  The report found no counterexample to the
main theorem, but it exhibited \(X=S_4(4).4\) as a counterexample to the
manuscript's assertion that
\(N_X(\Omega_4^+(4))\) is maximal and supplements the socle.  External
circulation is deferred until a new frozen candidate answers the report and
passes a fresh full review.

The prepared repair takes
\(V=\operatorname{Sp}_4(2^{f/r})\) for a prime \(r\mid f\).  Its class is
fixed by the exceptional graph-field generator, and
\(N_X(V)\) is maximal and supplements the socle for every coordinate group.
The exact response and new audit ledger are
[`reviews/01-revision.md`](reviews/01-revision.md) and
[`notes/07-classification-containment-ledger.md`](notes/07-classification-containment-ledger.md).
