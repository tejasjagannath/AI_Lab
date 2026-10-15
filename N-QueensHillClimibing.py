import random

def compute_heuristic(state):
    """Calculates the number of attacking queen pairs."""
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            # Same row conflict
            if state[i] == state[j]:
                conflicts += 1
            # Diagonal conflict
            elif abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_best_neighbor(state):
    """Finds the neighbor with the minimum number of conflicts."""
    current_conflicts = compute_heuristic(state)
    best_state = list(state)
    min_conflicts = current_conflicts
    
    n = len(state)
    for col in range(n):
        for row in range(n):
            if row != state[col]:
                neighbor = list(state)
                neighbor[col] = row
                neighbor_conflicts = compute_heuristic(neighbor)
                
                if neighbor_conflicts < min_conflicts:
                    min_conflicts = neighbor_conflicts
                    best_state = neighbor
                    
    return best_state, min_conflicts

def hill_climbing_4_queens_verbose():
    """Solves 4-Queens while tracking and printing all intermediate evaluations."""
    restart_count = 0
    
    while True:
        # Generate and display a new random initial state
        current_state = [random.randint(0, 3) for _ in range(4)]
        h_val = compute_heuristic(current_state)
        
        print(f"--- Attempt #{restart_count + 1} (Random Restart Initial State) ---")
        print(f"State: {current_state} | Conflicts (h): {h_val}")
        
        while True:
            neighbor, neighbor_conflicts = get_best_neighbor(current_state)
            current_conflicts = compute_heuristic(current_state)
            
            # If no neighbor is strictly better, we hit a peak or local plateau
            if neighbor_conflicts >= current_conflicts:
                if current_conflicts == 0:
                    print(f"-> Global Optimum Found!\n")
                    return current_state, restart_count
                else:
                    print(f"-> Stuck in Local Optimum at {current_state} (h={current_conflicts}). Restarting...\n")
                    break # Local optimum reached; break to trigger a restart
            
            current_state = neighbor
            print(f"   Step to neighbor: {current_state} | Conflicts (h): {neighbor_conflicts}")
            
        restart_count += 1

def print_board(state):
    """Visualizes the board configuration."""
    for row in range(4):
        line = ""
        for col in range(4):
            if state[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)


solution, total_restarts = hill_climbing_4_queens_verbose()

print("====================================")
print(f"**FINAL SOLUTION STATE**")
print("====================================")
print(f"State configuration: {solution}")
print(f"Total Random Restarts needed: {total_restarts}\n")
print_board(solution)
