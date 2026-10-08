import heapq

GOAL = (1, 2, 3,
        8, 0, 4,
        7, 6, 5)

def manhattan(state):
    """Sum of each tile's row and column distance from its goal position."""
    total = 0
    for index, tile in enumerate(state):
        if tile == 0:                      # the blank is not counted
            continue
        goal_index = GOAL.index(tile)
        row, col = divmod(index, 3)
        goal_row, goal_col = divmod(goal_index, 3)
        total += abs(row - goal_row) + abs(col - goal_col)
    return total

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

def a_star(start):
    open_heap = [(manhattan(start), start)]  # entries are (f, state)
    came_from = {}                           # state -> the state we came from
    g = {start: 0}                           # cost from start to each state
    closed = set()                           # states already expanded

    while open_heap:
        f, current = heapq.heappop(open_heap)  # lowest f comes out first

        if current == GOAL:
            return reconstruct_path(came_from, current)
        if current in closed:
            continue
        closed.add(current)

        for neighbor in neighbors(current):
            new_g = g[current] + 1             # each move costs 1
            if neighbor not in g or new_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = new_g
                f = new_g + manhattan(neighbor)
                heapq.heappush(open_heap, (f, neighbor))

    return None  # no solution

def print_board(state):
    for row in range(3):
        print(" ".join(str(t) if t else "_" for t in state[row * 3:row * 3 + 3]))
    print()

if __name__ == "__main__":
    start = (2, 8, 3,
             1, 6, 4,
             0, 7, 5)

    path = a_star(start)
    if path is None:
        print("No solution found.")
    else:
        print(f"Solved in {len(path) - 1} moves\n")
        for state in path:
            print_board(state)