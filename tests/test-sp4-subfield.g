#############################################################################
## Regression certificate for the corrected q=4 graph-outer subfield action.
## Pinned environment: GAP 4.15.1, AtlasRep 2.1.11.
#############################################################################

SP4Require := function(condition, message)
    if not condition then
        Error(Concatenation("Sp4 subfield regression: ", message));
    fi;
end;

SP4V2 := function(number)
    local value, exponent;
    SP4Require(IsPosInt(number), "valuation input must be positive");
    value := number;
    exponent := 0;
    while value mod 2 = 0 do
        value := value / 2;
        exponent := exponent + 1;
    od;
    return exponent;
end;

SP4Require(GAPInfo.Version = "4.15.1", "expected GAP 4.15.1");
SP4Require(LoadPackage("atlasrep") = true, "AtlasRep is unavailable");
SP4Require(PackageInfo("atlasrep")[1].Version = "2.1.11",
           "expected AtlasRep 2.1.11");

G := AtlasGroup("S4(4).4", IsPermGroup, true);;
SP4Require(G <> fail, "AtlasGroup(S4(4).4) is unavailable");
S := DerivedSubgroup(G);;
maximals := MaximalSubgroupClassReps(G);;
SP4Require(IsList(maximals), "maximal-subgroup representatives are unavailable");
M := First(maximals,
           subgroup -> Size(subgroup) = 2880
                       and Size(Intersection(subgroup, S)) = 720);;
SP4Require(M <> fail, "the subfield-normalizer maximal class was not found");

V := Intersection(M, S);;
H := Normalizer(G, V);;
SP4Require(H = M, "the selected maximal subgroup is not N_X(V)");
SP4Require(Normalizer(S, V) = V, "V is not self-normalizing in S");
SP4Require(Size(G) = 3916800, "unexpected automorphism-group order");
SP4Require(Size(S) = 979200, "unexpected socle order");
SP4Require(Size(H) = 2880, "unexpected normalizer order");
SP4Require(Size(V) = 720, "unexpected subfield-subgroup order");
SP4Require(Index(G, H) = 1360, "unexpected corrected degree");
SP4Require(ClosureGroup(H, S) = G, "normalizer does not supplement the socle");
SP4Require(SP4V2(Index(G, H)) = 4, "unexpected degree 2-valuation");
SP4Require(SP4V2(Index(G, S)) = 2, "unexpected outer 2-valuation");

classesS := Filtered(ConjugacyClasses(S),
                     class -> Order(Representative(class)) = 2);;
classesV := Filtered(ConjugacyClasses(V),
                     class -> Order(Representative(class)) = 2);;
coverage := List(classesS,
                 classS -> ForAny(classesV,
                     classV -> IsConjugate(S,
                         Representative(classS), Representative(classV))));;
SP4Require(Length(classesS) = 3, "socle does not have three involution classes");
SP4Require(ForAll(coverage, value -> value = true),
           "the subfield subgroup misses an involution class");

Print("SP4 SUBFIELD REGRESSION PASSED: |X:H|=1360, ",
      "|H|=2880, |H intersect S|=720, involution coverage=", coverage,
      "\n");
QUIT_GAP(0);
