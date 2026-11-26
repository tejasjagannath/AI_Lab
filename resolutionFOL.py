from dataclasses import dataclass
from typing import List, Dict, Set



class Term:
    pass


@dataclass(frozen=True)
class Var(Term):
    name: str

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Func(Term):
    name: str
    args: List[Term]

    def __str__(self):
        return (
            f"{self.name}({', '.join(map(str, self.args))})"
            if self.args
            else self.name
        )


class Formula:
    pass


@dataclass(frozen=True)
class Pred(Formula):
    name: str
    args: List[Term]

    def __str__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"


@dataclass(frozen=True)
class Not(Formula):
    f: Formula

    def __str__(self):
        return f"¬{self.f}"


@dataclass(frozen=True)
class And(Formula):
    left: Formula
    right: Formula

    def __str__(self):
        return f"({self.left} ∧ {self.right})"


@dataclass(frozen=True)
class Or(Formula):
    left: Formula
    right: Formula

    def __str__(self):
        return f"({self.left} ∨ {self.right})"


@dataclass(frozen=True)
class Implies(Formula):
    left: Formula
    right: Formula

    def __str__(self):
        return f"({self.left} ⇒ {self.right})"


@dataclass(frozen=True)
class Iff(Formula):
    left: Formula
    right: Formula

    def __str__(self):
        return f"({self.left} ⇔ {self.right})"


@dataclass(frozen=True)
class ForAll(Formula):
    var: str
    f: Formula

    def __str__(self):
        return f"∀{self.var} {self.f}"


@dataclass(frozen=True)
class Exists(Formula):
    var: str
    f: Formula

    def __str__(self):
        return f"∃{self.var} {self.f}"



def substitute_term(term: Term, mapping: Dict[str, Term]) -> Term:
    if isinstance(term, Var):
        return mapping.get(term.name, term)
    if isinstance(term, Func):
        return Func(term.name, [substitute_term(a, mapping) for a in term.args])
    return term


def substitute(f: Formula, mapping: Dict[str, Term]) -> Formula:
    if isinstance(f, Pred):
        return Pred(f.name, [substitute_term(a, mapping) for a in f.args])
    if isinstance(f, Not):
        return Not(substitute(f.f, mapping))
    if isinstance(f, And):
        return And(substitute(f.left, mapping), substitute(f.right, mapping))
    if isinstance(f, Or):
        return Or(substitute(f.left, mapping), substitute(f.right, mapping))
    if isinstance(f, ForAll):
        new_map = {k: v for k, v in mapping.items() if k != f.var}
        return ForAll(f.var, substitute(f.f, new_map))
    if isinstance(f, Exists):
        new_map = {k: v for k, v in mapping.items() if k != f.var}
        return Exists(f.var, substitute(f.f, new_map))
    return f


def eliminate_implications(f: Formula) -> Formula:
    if isinstance(f, Iff):
        a, b = eliminate_implications(f.left), eliminate_implications(f.right)
        return And(Or(Not(a), b), Or(Not(b), a))
    if isinstance(f, Implies):
        a, b = eliminate_implications(f.left), eliminate_implications(f.right)
        return Or(Not(a), b)
    if isinstance(f, Not):
        return Not(eliminate_implications(f.f))
    if isinstance(f, And):
        return And(
            eliminate_implications(f.left), eliminate_implications(f.right)
        )
    if isinstance(f, Or):
        return Or(
            eliminate_implications(f.left), eliminate_implications(f.right)
        )
    if isinstance(f, ForAll):
        return ForAll(f.var, eliminate_implications(f.f))
    if isinstance(f, Exists):
        return Exists(f.var, eliminate_implications(f.f))
    return f



def move_not_inwards(f: Formula) -> Formula:
    if isinstance(f, Not):
        inner = f.f
        if isinstance(inner, Not):
            return move_not_inwards(inner.f)
        if isinstance(inner, And):
            return Or(
                move_not_inwards(Not(inner.left)),
                move_not_inwards(Not(inner.right)),
            )
        if isinstance(inner, Or):
            return And(
                move_not_inwards(Not(inner.left)),
                move_not_inwards(Not(inner.right)),
            )
        if isinstance(inner, ForAll):
            return Exists(inner.var, move_not_inwards(Not(inner.f)))
        if isinstance(inner, Exists):
            return ForAll(inner.var, move_not_inwards(Not(inner.f)))
        return Not(move_not_inwards(inner))
    if isinstance(f, And):
        return And(move_not_inwards(f.left), move_not_inwards(f.right))
    if isinstance(f, Or):
        return Or(move_not_inwards(f.left), move_not_inwards(f.right))
    if isinstance(f, ForAll):
        return ForAll(f.var, move_not_inwards(f.f))
    if isinstance(f, Exists):
        return Exists(f.var, move_not_inwards(f.f))
    return f


def standardize_variables(
    f: Formula, used: Set[str] = None, mapping: Dict[str, Term] = None
) -> Formula:
    if used is None:
        used = set()
    if mapping is None:
        mapping = {}

    if isinstance(f, Pred):
        return substitute(f, mapping)
    if isinstance(f, Not):
        return Not(standardize_variables(f.f, used, mapping))
    if isinstance(f, And):
        return And(
            standardize_variables(f.left, used, mapping),
            standardize_variables(f.right, used, mapping),
        )
    if isinstance(f, Or):
        return Or(
            standardize_variables(f.left, used, mapping),
            standardize_variables(f.right, used, mapping),
        )
    if isinstance(f, (ForAll, Exists)):
        new_var = f.var
        while new_var in used:
            new_var += "_1"
        used.add(new_var)
        new_mapping = {**mapping, f.var: Var(new_var)}
        sub_f = standardize_variables(f.f, used, new_mapping)
        return (
            ForAll(new_var, sub_f)
            if isinstance(f, ForAll)
            else Exists(new_var, sub_f)
        )
    return f


def skolemize(
    f: Formula, univ_vars: List[str] = None, counter: List[int] = None
) -> Formula:
    if univ_vars is None:
        univ_vars = []
    if counter is None:
        counter = [1]

    if isinstance(f, ForAll):
        return ForAll(f.var, skolemize(f.f, univ_vars + [f.var], counter))
    if isinstance(f, Exists):
        idx = counter[0]
        counter[0] += 1
        if not univ_vars:
            skolem_term = Func(f"G{idx}", [])  
        else:
            skolem_term = Func(
                f"H{idx}", [Var(v) for v in univ_vars]
            )  
        replaced = substitute(f.f, {f.var: skolem_term})
        return skolemize(replaced, univ_vars, counter)
    if isinstance(f, And):
        return And(
            skolemize(f.left, univ_vars, counter),
            skolemize(f.right, univ_vars, counter),
        )
    if isinstance(f, Or):
        return Or(
            skolemize(f.left, univ_vars, counter),
            skolemize(f.right, univ_vars, counter),
        )
    if isinstance(f, Not):
        return Not(skolemize(f.f, univ_vars, counter))
    return f


def drop_universals(f: Formula) -> Formula:
    if isinstance(f, ForAll):
        return drop_universals(f.f)
    if isinstance(f, And):
        return And(drop_universals(f.left), drop_universals(f.right))
    if isinstance(f, Or):
        return Or(drop_universals(f.left), drop_universals(f.right))
    if isinstance(f, Not):
        return Not(drop_universals(f.f))
    return f


def distribute_or_over_and(f: Formula) -> Formula:
    if isinstance(f, And):
        return And(
            distribute_or_over_and(f.left), distribute_or_over_and(f.right)
        )
    if isinstance(f, Or):
        a = distribute_or_over_and(f.left)
        b = distribute_or_over_and(f.right)
        if isinstance(a, And):
            return And(
                distribute_or_over_and(Or(a.left, b)),
                distribute_or_over_and(Or(a.right, b)),
            )
        if isinstance(b, And):
            return And(
                distribute_or_over_and(Or(a, b.left)),
                distribute_or_over_and(Or(a, b.right)),
            )
        return Or(a, b)
    return f


def convert_to_cnf(statement: Formula) -> Formula:
    s1 = eliminate_implications(statement)
    s2 = move_not_inwards(s1)
    s3 = standardize_variables(s2)
    s4 = skolemize(s3)
    s5 = drop_universals(s4)
    s6 = distribute_or_over_and(s5)
    return s6



if __name__ == "__main__":

    formula = ForAll(
        "x",
        Implies(
            Pred("Person", [Var("x")]),
            Exists(
                "y",
                And(
                    Pred("Heart", [Var("y")]),
                    Pred("Has", [Var("x"), Var("y")]),
                ),
            ),
        ),
    )

    print("Original:", formula)
    cnf = convert_to_cnf(formula)
    print("CNF:     ", cnf)
