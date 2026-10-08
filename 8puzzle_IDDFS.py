GOAL = (1, 2, 3,
        8, 0, 4,
        7, 6, 5)

def neighbors(state):
    """All states reachable by sliding one tile into the blank."""
    blank = state.index(0)
    row, col = divmod(blank, 3)
    result = []
    for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + d_row, col + d_col
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank = new_row * 3 + new_col
            tiles = list(state)
            tiles[blank], tiles[new_blank] = tiles[new_blank], tiles[blank]
            result.append(tuple(tiles))
    return result

def depth_limited_search(state, limit, path, on_path):
    """
    Depth-first search that stops at 'limit' moves.
    path holds the moves so far; on_path holds the states in that path,
    so the search never walks back into a state it is already using.
    Returns the list of states to the goal, or None if not found.
    """
    if state == GOAL:
        return list(path)
    if limit == 0:
        return None

    for neighbor in neighbors(state):
        if neighbor not in on_path:
            path.append(neighbor)
            on_path.add(neighbor)

            result = depth_limited_search(neighbor, limit - 1, path, on_path)
            if result is not None:
                return result

            # Undo the move before trying the next neighbor (backtrack)
            on_path.remove(neighbor)
            path.pop()

    return None

def iddfs(start, max_depth=31):
    for limit in range(max_depth + 1):
        path = [start]
        result = depth_limited_search(start, limit, path, {start})
        if result is not None:
            return result
    return None  # no solution within max_depth

def print_board(state):
    for row in range(3):
        print(" ".join(str(t) if t else "_" for t in state[row * 3:row * 3 + 3]))
    print()

if __name__ == "__main__":
    start = (2, 8, 3,
             1, 6, 4,
             0, 7, 5)

    path = iddfs(start)
    if path is None:
        print("No solution found.")
    else:
        print(f"Solved in {len(path) - 1} moves\n")
        for state in path:
            print_board(state)