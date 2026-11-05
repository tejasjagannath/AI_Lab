FAILURE = "FAILURE"
NIL = []


def is_variable(t):
    return isinstance(t, str) and t[:1].islower()


def is_constant(t):
    return isinstance(t, str) and t[:1].isupper()


def is_compound(t):
    return isinstance(t, tuple)


def occurs_in(var, term):
    if term == var:
        return True
    if is_compound(term):
        return any(occurs_in(var, arg) for arg in term[1:])
    return False


def apply_subst(term, subst):
    for replacement, var in subst:
        if term == var:
            term = replacement
        elif is_compound(term):
            term = (term[0],) + tuple(apply_subst(a, [(replacement, var)])
                                      for a in term[1:])
    return term


def unify(psi1, psi2):
    if is_variable(psi1) or is_constant(psi1) or \
       is_variable(psi2) or is_constant(psi2):
        if psi1 == psi2:
            return NIL
        if is_variable(psi1):
            if occurs_in(psi1, psi2):
                return FAILURE
            return [(psi2, psi1)]
        if is_variable(psi2):
            if occurs_in(psi2, psi1):
                return FAILURE
            return [(psi1, psi2)]
        return FAILURE

    if psi1[0] != psi2[0]:
        return FAILURE

    if len(psi1) != len(psi2):
        return FAILURE

    subst = list(NIL)

    args1, args2 = list(psi1[1:]), list(psi2[1:])
    for i in range(len(args1)):
        s = unify(args1[i], args2[i])

        if s == FAILURE:
            return FAILURE

        if s != NIL:
            for j in range(i + 1, len(args1)):
                args1[j] = apply_subst(args1[j], s)
                args2[j] = apply_subst(args2[j], s)
            subst = s + subst

    return subst


def show_term(t):
    if is_compound(t):
        return f"{t[0]}({', '.join(show_term(a) for a in t[1:])})"
    return t


def show_result(r):
    if r == FAILURE:
        return "FAILURE"
    if r == NIL:
        return "NIL (already identical)"
    return "{" + ", ".join(f"{show_term(rep)}/{var}" for rep, var in r) + "}"


if __name__ == "__main__":
    tests = [
        (("Knows", "John", "x"), ("Knows", "John", "Jane")),
        (("Knows", "John", "x"), ("Knows", "y", ("Mother", "y"))),
        (("Knows", "John", "x"), ("Knows", "y", "Bill")),
        (("P", "x", "x"), ("P", "A", "B")),
        (("P", "x"), ("P", ("f", "x"))),
        (("P", "A"), ("Q", "A")),
        (("P", "A"), ("P", "A", "B")),
        (("P", "A", "B"), ("P", "A", "B")),
        (("P", "x", "y", "z"), ("P", "y", "z", "A")),
    ]
    for a, b in tests:
        print(f"Unify({show_term(a)}, {show_term(b)})")
        print("   ->", show_result(unify(a, b)), "\n")