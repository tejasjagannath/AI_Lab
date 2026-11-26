import math


def alpha_beta_search(state, game):
    best_score, beta, best_path = -math.inf, math.inf, []

    for a in game.actions(state):
        v, path = min_value(game.result(state, a), best_score, beta, game)
        if v > best_score:
            best_score, best_path = v, [f"{state} --({a})--> {path}"]

    print(f"\nOptimal Action : {best_path[0].split('(')[1].split(')')[0]}")
    print(f"Optimal Utility: {best_score}")
    print(f"Optimal Path   : {best_path[0]}")
    return best_path[0]


def max_value(state, alpha, beta, game):
    if game.terminal_test(state):
        u = game.utility(state)
        print(f"Leaf {state} = {u}")
        return u, str(state)

    v, best_path = -math.inf, ""
    for i, a in enumerate(game.actions(state)):
        child_v, child_path = min_value(game.result(state, a), alpha, beta, game)
        if child_v > v:
            v, best_path = child_v, f"{state} --({a})--> {child_path}"
        if v >= beta:
            print(f"Pruned at MAX {state} (v={v} >= β={beta}), skipped {game.actions(state)[i+1:]}")
            return v, best_path
        alpha = max(alpha, v)
    return v, best_path


def min_value(state, alpha, beta, game):
    if game.terminal_test(state):
        u = game.utility(state)
        print(f"Leaf {state} = {u}")
        return u, str(state)

    v, best_path = math.inf, ""
    for i, a in enumerate(game.actions(state)):
        child_v, child_path = max_value(game.result(state, a), alpha, beta, game)
        if child_v < v:
            v, best_path = child_v, f"{state} --({a})--> {child_path}"
        if v <= alpha:
            print(f"Pruned at MIN {state} (v={v} <= α={alpha}), skipped {game.actions(state)[i+1:]}")
            return v, best_path
        beta = min(beta, v)
    return v, best_path


# --- Example Game Tree ---
class TreeGame:
    transitions = {
        "A": {"a1": "B", "a2": "C", "a3": "D"},
        "B": {"b1": "B1", "b2": "B2", "b3": "B3"},
        "C": {"c1": "C1", "c2": "C2", "c3": "C3"},
        "D": {"d1": "D1", "d2": "D2", "d3": "D3"},
    }
    utilities = {"B1": 3, "B2": 12, "B3": 8, "C1": 2, "C2": 4, "C3": 6, "D1": 14, "D2": 5, "D3": 2}

    actions = lambda self, s: list(self.transitions.get(s, {}).keys())
    result = lambda self, s, a: self.transitions[s][a]
    terminal_test = lambda self, s: s in self.utilities
    utility = lambda self, s: self.utilities[s]


if __name__ == "__main__":
    alpha_beta_search("A", TreeGame())
