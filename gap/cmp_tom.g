#############################################################################
##
##  cmp_tom.g
##
##  Exact Table-of-Marks test for the property that every maximal subgroup
##  has a complement.  This file contains no bounded subgroup enumeration:
##  it uses the complete subgroup-class and intersection data encoded by a
##  table of marks.
##
#############################################################################

if LoadPackage("tomlib") <> true then
    Error("CMP: the GAP package TomLib is required");
fi;


CMPPackageVersion := function(name)
    local info;

    info := PackageInfo(name);
    if info = fail or Length(info) = 0 or not IsBound(info[1].Version) then
        return "unavailable";
    fi;
    return info[1].Version;
end;


CMPJoinIntegers := function(values, separator)
    return JoinStringsWithSeparator(List(values, String), separator);
end;


CMPValidateTableOfMarks := function(tom)
    local orders, names, maximal, groupOrder, marks;

    if tom = fail or not IsTableOfMarks(tom) then
        Error("CMP: no table of marks was supplied");
    fi;

    orders := OrdersTom(tom);
    # ClassNamesTom is only cosmetic and can fail on tables having very many
    # classes of one structural type.  Position labels are total, stable, and
    # are the actual identifiers used by all table-of-marks operations.
    names := List([1 .. Length(orders)],
                  i -> Concatenation("class-", String(i)));
    maximal := MaximalSubgroupsTom(tom);

    if not IsList(orders) or Length(orders) = 0 then
        Error("CMP: OrdersTom returned no subgroup classes");
    fi;
    if orders[1] <> 1 then
        Error("CMP: class 1 is not the trivial subgroup class");
    fi;
    if maximal = fail or not IsList(maximal) or Length(maximal) < 1
       or not IsList(maximal[1]) then
        Error("CMP: maximal-subgroup data are unavailable");
    fi;
    if ForAny(maximal[1],
              m -> not IsPosInt(m) or m > Length(orders)) then
        Error("CMP: invalid maximal-subgroup class position");
    fi;
    groupOrder := orders[Length(orders)];
    marks := MarksTom(tom);
    if not IsList(marks) or Length(marks) <> Length(orders)
       or not IsList(marks[1]) or Length(marks[1]) < 1
       or marks[1][1] <> groupOrder then
        Error("CMP: the final class is not certified as the full group");
    fi;
    if ForAny(orders, order -> groupOrder mod order <> 0) then
        Error("CMP: a subgroup-class order does not divide the group order");
    fi;

    return rec(
        orders := orders,
        names := names,
        maximal_classes := maximal[1],
        group_order := groupOrder
    );
end;


# For subgroup classes m and c, IntersectionsTom(tom,m,c)[1] is the
# multiplicity with which the trivial subgroup class occurs among all
# intersections of a conjugate of class m with a conjugate of class c.
CMPTrivialIntersectionMultiplicity := function(tom, m, c)
    local intersections;

    intersections := IntersectionsTom(tom, m, c);
    if not IsList(intersections) or Length(intersections) < 1 then
        Error("CMP: IntersectionsTom returned incomplete data");
    fi;
    if not IsInt(intersections[1]) or intersections[1] < 0 then
        Error("CMP: invalid trivial-intersection multiplicity");
    fi;
    return intersections[1];
end;


# Return the orders of the factors in one deterministic chief series, from
# the top factor down.  Conjugacy-class length one is exactly normality.  At
# each stage, a contained normal class of largest proper order is maximal in
# the relevant interval of the normal-subgroup lattice.
CMPChiefFactorOrdersByTom := function(tom)
    local data, lengths, subs, normalClasses, current, below, next, result;

    data := CMPValidateTableOfMarks(tom);
    lengths := LengthsTom(tom);
    subs := SubsTom(tom);
    if not IsList(lengths) or Length(lengths) <> Length(data.orders)
       or not IsList(subs) or Length(subs) <> Length(data.orders) then
        Error("CMP: normal-subgroup lattice data are unavailable");
    fi;

    normalClasses := Filtered([1 .. Length(lengths)],
                              i -> lengths[i] = 1);
    current := Length(data.orders);
    result := [];
    while current <> 1 do
        below := Filtered(normalClasses,
                          i -> i <> current and i in subs[current]);
        if Length(below) = 0 then
            Error("CMP: failed to descend the normal-subgroup lattice");
        fi;
        SortBy(below, i -> [data.orders[i], i]);
        next := below[Length(below)];
        if data.orders[current] mod data.orders[next] <> 0 then
            Error("CMP: invalid chief-factor order ratio");
        fi;
        Add(result, data.orders[current] / data.orders[next]);
        current := next;
    od;
    return result;
end;


CMPMaximalCertificateByTom := function(tom, m)
    local data, maxOrder, index, candidates, candidateRows, c,
          multiplicity, witness;

    data := CMPValidateTableOfMarks(tom);
    maxOrder := data.orders[m];
    if data.group_order mod maxOrder <> 0 then
        Error("CMP: maximal-subgroup order does not divide the group order");
    fi;
    index := data.group_order / maxOrder;

    # A complement must have exactly the index as its order.  Since a table
    # of marks contains every conjugacy class of subgroups, this candidate
    # list is exhaustive relative to the supplied table.
    candidates := Filtered([1 .. Length(data.orders)],
                           c -> data.orders[c] = index);
    candidateRows := [];
    witness := fail;

    for c in candidates do
        multiplicity := CMPTrivialIntersectionMultiplicity(tom, m, c);
        Add(candidateRows, rec(
            class := c,
            label := data.names[c],
            order := data.orders[c],
            trivial_intersection_multiplicity := multiplicity
        ));
        if witness = fail and multiplicity > 0 then
            witness := c;
        fi;
    od;

    return rec(
        maximal_class := m,
        maximal_label := data.names[m],
        maximal_order := maxOrder,
        index := index,
        candidates := candidateRows,
        complemented := witness <> fail,
        witness_class := witness
    );
end;


CMPTableOfMarksCertificateFromTable := function(tom, name)
    local data, rows, m, row, failures, lengths, normalClasses,
          nonabelianSimple, cmpValue, solvable, chiefFactorOrders;

    if not IsString(name) then
        Error("CMP: a certificate name must be a string");
    fi;
    data := CMPValidateTableOfMarks(tom);
    lengths := LengthsTom(tom);
    if not IsList(lengths) or Length(lengths) <> Length(data.orders) then
        Error("CMP: subgroup conjugacy-class lengths are unavailable");
    fi;
    normalClasses := Filtered([1 .. Length(lengths)],
                              i -> lengths[i] = 1);
    nonabelianSimple := data.group_order > 1
                        and normalClasses = [1, Length(data.orders)]
                        and not IsAbelianTom(tom);

    rows := [];
    failures := [];
    for m in data.maximal_classes do
        row := CMPMaximalCertificateByTom(tom, m);
        Add(rows, row);
        if not row.complemented then
            Add(failures, row.maximal_class);
        fi;
    od;
    cmpValue := Length(failures) = 0;

    # Normal-lattice calculations on some large negative tables are costly
    # and irrelevant to a countercertificate already supplied by one failed
    # maximal class.  Compute chief data exactly for every positive table and
    # mark it as deliberately unavailable (fail/empty) for negative tables.
    if cmpValue then
        solvable := IsSolvableTom(tom);
        chiefFactorOrders := CMPChiefFactorOrdersByTom(tom);
    else
        solvable := fail;
        chiefFactorOrders := [];
    fi;

    return rec(
        table_name := name,
        group_order := data.group_order,
        subgroup_class_count := Length(data.orders),
        maximal_class_count := Length(data.maximal_classes),
        normal_class_count := Length(normalClasses),
        nonabelian_simple := nonabelianSimple,
        solvable := solvable,
        chief_factor_orders := chiefFactorOrders,
        maximal_rows := rows,
        cmp := cmpValue,
        failed_maximal_classes := failures,
        gap_version := GAPInfo.Version,
        tomlib_version := CMPPackageVersion("tomlib")
    );
end;


CMPTableOfMarksCertificate := function(name)
    local tom;

    if not IsString(name) then
        Error("CMP: a TomLib table name must be a string");
    fi;
    tom := TableOfMarks(name);
    if tom = fail then
        Error(Concatenation("CMP: TomLib has no table named ", name));
    fi;
    return CMPTableOfMarksCertificateFromTable(tom, name);
end;


CMPFormatCandidateRows := function(rows)
    if Length(rows) = 0 then
        return "none";
    fi;
    return JoinStringsWithSeparator(
        List(rows,
             row -> Concatenation(
                 String(row.class), ":",
                 String(row.trivial_intersection_multiplicity))),
        ","
    );
end;
