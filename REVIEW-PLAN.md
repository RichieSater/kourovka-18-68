# Problem 18.68 solution and review plan

**Current stage:** complete candidate solution and internal adversarial audit;
independent referee rounds not started.

## Milestones

| Milestone | Status | Required focus | Artifact |
|---|---|---|---|
| Initial solution | complete internally | Full composition-factor theorem under complemented maximals | `paper/kourovka-18-68.tex` |
| Revision 1 | not started | Complement convention and quotient/section/extension behavior | `reviews/01-revision.md` |
| Referee 1 | not started | Independent structural and minimality audit | `reviews/01-referee.md` |
| Revision 2 | not started | Primitive, monolithic, nonsplit, and cohomological cases | `reviews/02-revision.md` |
| Referee 2 | not started | Independent extension and classification-source audit | `reviews/02-referee.md` |
| Revision 3 | not started | Complement certificates, finite scans, and reproducibility | `reviews/03-revision.md` |
| Referee 3 | not started | Fresh-clone witness/completeness/mutation audit | `reviews/03-referee.md` |
| Revision 4 | not started | Arbitrary composition-factor synthesis and release candidate | `reviews/04-revision.md` |
| Referee 4 | not started | Hard-final theorem/source/certificate pass | `reviews/04-referee.md` |

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
