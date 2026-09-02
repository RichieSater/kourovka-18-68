Read("gap/factor_free_tom.g");;

FFAssert := function(condition, message)
    if not condition then
        Error(Concatenation("factor-free test failed: ", message));
    fi;
end;

# Positive control: in A5, an A4 maximal (class 8) has a core-free regular
# factor C5.  This ensures that the containment/intersection orientation is
# not silently making every result factor-free.
tom := TableOfMarks("A5");;
rows := FFCorefreeTransitiveFactorsTom(tom, 8);;
FFAssert(Length(rows) > 0, "A5/A4 positive control was not detected");
FFAssert(ForAny(rows,
              row -> row.factor_order = 5
                     and row.intersection_order = 1),
       "A5 = A4 C5 exact factorization was not detected");

# Negative control used in the proof: the S3 maximal (class 6) is
# factor-free.
cert := FFCertificateTom("A5", 6);;
FFAssert(cert.maximal_order = 6 and cert.index = 10,
       "A5 negative-control class changed");
FFAssert(cert.factor_free, "A5/S3 should be factor-free");

# Outer almost-simple socle detection and one row used in the proof.
cert := FFCertificateTom("A6.2^2", 49);;
FFAssert(cert.socle_order = 360, "failed to detect the A6 socle");
FFAssert(cert.maximal_order = 32 and cert.index = 45,
       "A6.2^2 pinned maximal changed");
FFAssert(cert.socle_intersection_order = 8,
       "A6.2^2 socle intersection changed");
FFAssert(cert.factor_free, "A6.2^2 proof row should be factor-free");

Print("FACTOR-FREE TOM TESTS PASSED\n");
QUIT_GAP(0);
