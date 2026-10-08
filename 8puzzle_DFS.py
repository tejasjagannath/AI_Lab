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

def reconstruct_path(came_from, current):
    """Follow parent links back to the start, then reverse the list."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def dfs(start):
    stack = [start]          # states waiting to be explored (last in, first out)
    came_from = {}           # state -> the state we came from
    visited = {start}        # states already added, so none is explored twice

    while stack:
        current = stack.pop()            # take the most recently added state

        if current == GOAL:
            return reconstruct_path(came_from, current)

        for neighbor in neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)

    return None  # no solution

def print_board(state):
    for row in range(3):
        print(" ".join(str(t) if t else "_" for t in state[row * 3:row * 3 + 3]))
    print()

if __name__ == "__main__":
    start = (2, 8, 3,
             1, 6, 4,
             0, 7, 5)

    path = dfs(start)
    if path is None:
        print("No solution found.")
    else:
        print(f"Solved in {len(path) - 1} moves\n")
        for state in path:
            print_board(state)