X, O, EMPTY = "X", "O", " "

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]

def winner(board):
    """Return 'X' or 'O' if someone has three in a line, otherwise None."""
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None

def empty_cells(board):
    return [i for i in range(9) if board[i] == EMPTY]

def minimax(board, player, ai):
    """
    Score the board from the AI's point of view, assuming both sides
    play perfectly from here on.
        +1 = AI wins, -1 = human wins, 0 = draw
    """
    human = O if ai == X else X

    # Base cases: the game is over
    if winner(board) == ai:
        return 1
    if winner(board) == human:
        return -1
    if not empty_cells(board):
        return 0

    next_player = human if player == ai else ai
    scores = []

    # Try every empty square, score the result, then undo the move
    for i in empty_cells(board):
        board[i] = player
        scores.append(minimax(board, next_player, ai))
        board[i] = EMPTY

    # The AI picks the highest score, the human picks the lowest
    return max(scores) if player == ai else min(scores)

def best_move(board, ai):
    """Check every empty square with minimax and return the best one."""
    human = O if ai == X else X
    best_score = float("-inf")
    best = None

    for i in empty_cells(board):
        board[i] = ai
        score = minimax(board, human, ai)
        board[i] = EMPTY

        if score > best_score:
            best_score = score
            best = i
    return best

def print_board(board):
    cells = [str(i + 1) if board[i] == EMPTY else board[i] for i in range(9)]
    for r in range(3):
        print(" " + " | ".join(cells[r * 3:r * 3 + 3]))
        if r < 2:
            print("---+---+---")
    print()

def play():
    human, ai = X, O
    board = [EMPTY] * 9
    print("You are X. The AI is O. Enter a number from 1 to 9 to place your mark.\n")
    print_board(board)

    while True:
        # Human turn
        while True:
            choice = input("Your move (1-9): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= 9 and board[int(choice) - 1] == EMPTY:
                board[int(choice) - 1] = human
                break
            print("That square is taken or invalid. Try again.")
        print_board(board)

        if winner(board) == human:
            print("You win!")
            break
        if not empty_cells(board):
            print("It's a draw.")
            break

        # AI turn
        print("AI is thinking...")
        move = best_move(board, ai)
        board[move] = ai
        print(f"AI plays square {move + 1}.\n")
        print_board(board)

        if winner(board) == ai:
            print("The AI wins!")
            break
        if not empty_cells(board):
            print("It's a draw.")
            break

if __name__ == "__main__":
    play()