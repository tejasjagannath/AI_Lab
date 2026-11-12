import copy
from itertools import count

# Counter to generate unique standardized variable names
_var_counter = count(1)

class Expr:
    """Represents a First-Order Logic atomic sentence, e.g., Criminal(West)."""
    def __init__(self, op, args=()):
        self.op = op
        self.args = tuple(args)

    def __repr__(self):
        if not self.args:
            return str(self.op)
        return f"{self.op}({', '.join(map(str, self.args))})"

    def __eq__(self, other):
        return isinstance(other, Expr) and self.op == other.op and self.args == other.args

    def __hash__(self):
        return hash((self.op, self.args))

class Clause:
    """Represents a definite clause: (p1 ^ p2 ^ ... ^ pn) => q."""
    def __init__(self, premises, conclusion):
        self.premises = tuple(premises)
        self.conclusion = conclusion

    def __repr__(self):
        if not self.premises:
            return repr(self.conclusion)
        prem_str = " ^ ".join(map(repr, self.premises))
        return f"({prem_str}) => {self.conclusion}"

def is_variable(x):
    """Variables are strings starting with a lowercase letter (e.g., 'x', 'y')."""
    return isinstance(x, str) and x[0].islower()

def standardize_variables(clause):
    """Replaces all variables in a clause with fresh, unique variable names."""
    mapping = {}
    
    def rename(term):
        if isinstance(term, Expr):
            return Expr(term.op, [rename(arg) for arg in term.args])
        elif is_variable(term):
            if term not in mapping:
                mapping[term] = f"{term}_{next(_var_counter)}"
            return mapping[term]
        return term

    new_premises = [rename(p) for p in clause.premises]
    new_conclusion = rename(clause.conclusion)
    return Clause(new_premises, new_conclusion)

def subst(theta, x):
    """Applies substitution dictionary `theta` to expression `x`."""
    if isinstance(x, Expr):
        return Expr(x.op, [subst(theta, arg) for arg in x.args])
    elif is_variable(x):
        while x in theta:
            x = theta[x]
        return x
    return x

def occur_check(var, x, theta):
    """Prevents infinite loops when unifying a variable with an expression containing it."""
    if var == x:
        return True
    elif is_variable(x) and x in theta:
        return occur_check(var, theta[x], theta)
    elif isinstance(x, Expr):
        return any(occur_check(var, arg, theta) for arg in x.args)
    return False

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif is_variable(x) and x in theta:
        return unify(var, theta[x], theta)
    elif occur_check(var, x, theta):
        return None
    else:
        new_theta = theta.copy()
        new_theta[var] = x
        return new_theta

def unify(x, y, theta=None):
    """Unifies two atomic sentences or terms, returning a substitution dict or None (fail)."""
    if theta is None:
        theta = {}
    if theta is None:
        return None
    elif x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    elif isinstance(x, Expr) and isinstance(y, Expr):
        if x.op != y.op or len(x.args) != len(y.args):
            return None
        for a, b in zip(x.args, y.args):
            theta = unify(a, b, theta)
            if theta is None:
                return None
        return theta
    return None

def match_premises(premises, facts, theta):
    """Recursively finds all substitutions `theta` that satisfy all `premises` against known `facts`."""
    if not premises:
        yield theta
        return

    first, rest = premises[0], premises[1:]
    for fact in facts:
        new_theta = unify(first, fact, theta)
        if new_theta is not None:
            yield from match_premises(rest, facts, new_theta)

def is_renaming(x, y):
    """Checks if atomic sentence `x` already unifies/renames to an existing sentence `y`."""
    theta = unify(x, y, {})
    if theta is None:
        return False
    # Ensure it's a pure variable renaming (no variable bound to a constant/compound term)
    return all(is_variable(val) for val in theta.values())

def fol_fc_ask(kb_facts, kb_rules, alpha):
    """
    Implementation of FOL-FC-ASK from the image.
    - kb_facts: list of atomic Expr objects
    - kb_rules: list of Clause objects (implications)
    - alpha: query Expr
    """
    kb = list(kb_facts)

    # Check if query is already trivially satisfied by initial facts
    for fact in kb:
        phi = unify(fact, alpha, {})
        if phi is not None:
            return phi

    while True:
        new = []
        for rule in kb_rules:
            std_rule = standardize_variables(rule)
            
            # Find all theta such that SUBST(theta, p1 ^ ... ^ pn) = SUBST(theta, p1' ^ ... ^ pn')
            for theta in match_premises(std_rule.premises, kb, {}):
                q_prime = subst(theta, std_rule.conclusion)
                
                # If q' does not unify (rename) with some sentence already in KB or new
                already_exists = any(is_renaming(q_prime, s) for s in kb + new)
                if not already_exists:
                    new.append(q_prime)
                    phi = unify(q_prime, alpha, {})
                    if phi is not None:
                        return phi
        
        if not new:
            return False
        kb.extend(new)


# ==========================================
# Example Usage: The Classic "Colonel West" Problem
# ==========================================
if __name__ == "__main__":
    # Facts (Atomic sentences in KB)
    facts = [
        Expr("American", ["West"]),
        Expr("Missile", ["M1"]),
        Expr("Owns", ["Nono", "M1"]),
        Expr("Enemy", ["Nono", "America"]),
    ]

    # Rules (Definite clauses in KB)
    rules = [
        # Missile(x) ^ Owns(Nono, x) => Sells(West, x, Nono)
        Clause(
            [Expr("Missile", ["x"]), Expr("Owns", ["Nono", "x"])],
            Expr("Sells", ["West", "x", "Nono"])
        ),
        # Missile(x) => Weapon(x)
        Clause(
            [Expr("Missile", ["x"])],
            Expr("Weapon", ["x"])
        ),
        # Enemy(x, America) => Hostile(x)
        Clause(
            [Expr("Enemy", ["x", "America"])],
            Expr("Hostile", ["x"])
        ),
        # American(x) ^ Weapon(y) ^ Sells(x, y, z) ^ Hostile(z) => Criminal(x)
        Clause(
            [
                Expr("American", ["x"]),
                Expr("Weapon", ["y"]),
                Expr("Sells", ["x", "y", "z"]),
                Expr("Hostile", ["z"])
            ],
            Expr("Criminal", ["x"])
        ),
    ]

    # Query: Is West a criminal? -> Criminal(West) or Criminal(who)
    query = Expr("Criminal", ["who"])
    
    result = fol_fc_ask(facts, rules, query)
    print("Query:", query)
    print("Result substitution:", result)
