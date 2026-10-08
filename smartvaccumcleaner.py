from itertools import product

LOCATIONS = ("A", "B")
STATUSES = ("Clean", "Dirty")

def all_states():
    """All 8 combinations: vacuum location x status of room A x status of room B."""
    return [(loc, a, b) for loc, a, b in product(LOCATIONS, STATUSES, STATUSES)]

def result(state, action):
    """Return the new state after the vacuum performs an action."""
    loc, a, b = state
    if action == "Suck":
        if loc == "A":
            a = "Clean"
        else:
            b = "Clean"
    elif action == "Left":
        loc = "A"
    elif action == "Right":
        loc = "B"
    return (loc, a, b)

def is_goal(state):
    """The goal is reached when both rooms are clean."""
    _, a, b = state
    return a == "Clean" and b == "Clean"

def agent_action(state):
    """Simple reflex agent: clean if the current room is dirty, otherwise move."""
    loc, a, b = state
    current_status = a if loc == "A" else b
    if current_status == "Dirty":
        return "Suck"
    return "Right" if loc == "A" else "Left"

def run(state, max_steps=20):
    print(f"Start: {state}")
    steps = 0
    while not is_goal(state) and steps < max_steps:
        action = agent_action(state)
        state = result(state, action)
        steps += 1
        print(f"Step {steps}: {action:<5} -> {state}")
    if is_goal(state):
        print(f"\nBoth rooms are clean after {steps} step(s).")
    else:
        print("\nStopped before finishing.")

if __name__ == "__main__":
    print("All 8 possible states:")
    for i, s in enumerate(all_states(), start=1):
        print(f"  {i}. {s}")

    print()
    run(("A", "Dirty", "Dirty"))