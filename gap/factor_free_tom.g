#############################################################################
##
##  factor_free_tom.g
##
##  Exact Table-of-Marks test for a maximal subgroup H of an almost-simple
##  group X to have no core-free transitive subgroup in X/H.
##
#############################################################################

if LoadPackage("tomlib") <> true then
    Error("factor-free: the GAP package TomLib is required");
fi;


FFSocleClassTom := function(tom)
    local orders, lengths, normal, leastOrder, candidates;

    if tom = fail or not IsTableOfMarks(tom) then
        Error("factor-free: no table of marks was supplied");
    fi;
    orders := OrdersTom(tom);
    lengths := LengthsTom(tom);
    if not IsList(orders) or not IsList(lengths)
       or Length(orders) <> Length(lengths) then
        Error("factor-free: subgroup-order or class-length data are missing");
    fi;
    normal := Filtered([1 .. Length(orders)],
                       i -> lengths[i] = 1 and orders[i] > 1);
    if Length(normal) = 0 then
        Error("factor-free: the group has no nontrivial normal subgroup");
    fi;
    leastOrder := Minimum(List(normal, i -> orders[i]));
    candidates := Filtered(normal, i -> orders[i] = leastOrder);
    if Length(candidates) <> 1 then
        Error("factor-free: a unique least nontrivial normal class was not found");
    fi;
    return candidates[1];
end;


FFClassContainsClassTom := function(tom, overgroup, subgroup)
    local contained;

    contained := SubsTom(tom);
    if not IsList(contained) or Length(contained) < overgroup
       or not IsList(contained[overgroup]) then
        Error("factor-free: subgroup-containment data are missing");
    fi;
    return subgroup in contained[overgroup];
end;


# Return all certificates X = H C with C core-free.  For each certificate,
# an intersection class I is recorded with |H||C| = |X||I| and with positive
# multiplicity in IntersectionsTom(tom,h,c).  Thus an empty return value is an
# exhaustive negative result relative to the complete table of marks.
FFCorefreeTransitiveFactorsTom := function(tom, h)
    local orders, maximals, socle, groupOrder, rows, c, intersections, i;

    orders := OrdersTom(tom);
    maximals := MaximalSubgroupsTom(tom);
    if not IsList(maximals) or Length(maximals) < 1
       or not IsList(maximals[1]) then
        Error("factor-free: maximal-subgroup data are missing");
    fi;
    if not h in maximals[1] then
        Error("factor-free: the requested class is not maximal");
    fi;
    socle := FFSocleClassTom(tom);
    if FFClassContainsClassTom(tom, h, socle) then
        Error("factor-free: the requested maximal subgroup is not core-free");
    fi;
    groupOrder := orders[Length(orders)];
    rows := [];

    for c in [1 .. Length(orders) - 1] do
        if not FFClassContainsClassTom(tom, c, socle)
           and (orders[h] * orders[c]) mod groupOrder = 0 then
            intersections := IntersectionsTom(tom, h, c);
            if not IsList(intersections) then
                Error("factor-free: intersection data are missing");
            fi;
            for i in [1 .. Length(intersections)] do
                if IsBound(intersections[i]) and intersections[i] > 0
                   and orders[h] * orders[c]
                       = groupOrder * orders[i] then
                    Add(rows, rec(
                        factor_class := c,
                        intersection_class := i,
                        factor_order := orders[c],
                        intersection_order := orders[i],
                        multiplicity := intersections[i]
                    ));
                fi;
            od;
        fi;
    od;
    return rows;
end;


FFCertificateTom := function(name, h)
    local tom, orders, socle, rows;

    if not IsString(name) or not IsPosInt(h) then
        Error("factor-free: expected a TomLib name and a positive class position");
    fi;
    tom := TableOfMarks(name);
    if tom = fail then
        Error(Concatenation("factor-free: no TomLib table named ", name));
    fi;
    orders := OrdersTom(tom);
    if h > Length(orders) then
        Error("factor-free: class position is outside the table");
    fi;
    socle := FFSocleClassTom(tom);
    rows := FFCorefreeTransitiveFactorsTom(tom, h);
    return rec(
        table_name := name,
        group_order := orders[Length(orders)],
        socle_class := socle,
        socle_order := orders[socle],
        maximal_class := h,
        maximal_order := orders[h],
        socle_intersection_order := orders[h] * orders[socle]
                                    / orders[Length(orders)],
        index := orders[Length(orders)] / orders[h],
        corefree_factor_rows := rows,
        factor_free := Length(rows) = 0
    );
end;
