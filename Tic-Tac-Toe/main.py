import os
import sys
import random
import time

def clear_screen():
    """Clears the terminal screen for a clean UI redrawing."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_board(board):
    """Displays the 3x3 Tic-Tac-Toe grid with current positions."""
    print("\n   TIC-TAC-TOE   ")
    print("  -------------")
    print(f"   {board[0]} | {board[1]} | {board[2]} ")
    print("  -----------")
    print(f"   {board[3]} | {board[4]} | {board[5]} ")
    print("  -----------")
    print(f"   {board[6]} | {board[7]} | {board[8]} ")
    print("  -------------\n")

def check_win(board, player):
    """Checks if the specified player ('X' or 'O') has achieved 3 in a row."""
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Vertical
        [0, 4, 8], [2, 4, 6]             # Diagonal
    ]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

def check_tie(board):
    """Checks if the grid is full with no remaining empty positions."""
    return all(space in ['X', 'O'] for space in board)

def get_empty_positions(board):
    """Returns a list of available board index positions."""
    return [i for i, space in enumerate(board) if space not in ['X', 'O']]


def minimax(board, depth, is_maximizing, computer_symbol, human_symbol):
    """
    Minimax algorithm for the unbeatable Hard mode.
    Evaluates all possible future game states.
    """
    if check_win(board, computer_symbol):
        return 10 - depth
    if check_win(board, human_symbol):
        return depth - 10
    if check_tie(board):
        return 0

    empty_spots = get_empty_positions(board)

    if is_maximizing:
        best_score = -1000
        for spot in empty_spots:
            board[spot] = computer_symbol
            score = minimax(board, depth + 1, False, computer_symbol, human_symbol)
            board[spot] = str(spot + 1)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for spot in empty_spots:
            board[spot] = human_symbol
            score = minimax(board, depth + 1, True, computer_symbol, human_symbol)
            board[spot] = str(spot + 1)
            best_score = min(score, best_score)
        return best_score


def get_computer_move(board, computer_symbol, human_symbol, difficulty):
    """
    Determines computer move based on chosen difficulty level:
    1. Easy: Purely random moves.
    2. Medium: Smart blocking & immediate win checks, otherwise random.
    3. Hard: Unbeatable Minimax recursive evaluation algorithm.
    """
    empty_spots = get_empty_positions(board)

    if difficulty == '1':
        return random.choice(empty_spots)

    elif difficulty == '2':
        for spot in empty_spots:
            board_copy = board.copy()
            board_copy[spot] = computer_symbol
            if check_win(board_copy, computer_symbol):
                return spot

        for spot in empty_spots:
            board_copy = board.copy()
            board_copy[spot] = human_symbol
            if check_win(board_copy, human_symbol):
                return spot

        if 4 in empty_spots:
            return 4
        return random.choice(empty_spots)

    elif difficulty == '3':
        best_score = -1000
        best_move = empty_spots[0]

        for spot in empty_spots:
            board[spot] = computer_symbol
            score = minimax(board, 0, False, computer_symbol, human_symbol)
            board[spot] = str(spot + 1)

            if score > best_score:
                best_score = score
                best_move = spot

        return best_move


def get_human_move(board, player_symbol):
    """Prompts human player for position input (1-9)."""
    while True:
        try:
            choice = input(f"Player '{player_symbol}', choose a position (1-9): ").strip()
            if choice.lower() in ['q', 'quit', 'exit']:
                print("\nGame exited. Thanks for playing! 👋")
                sys.exit()

            position = int(choice) - 1
            if position < 0 or position > 8:
                print("⚠️ Invalid number! Please enter a number between 1 and 9.")
            elif board[position] in ['X', 'O']:
                print("⚠️ Position already taken! Choose an open spot.")
            else:
                return position
        except ValueError:
            print("⚠️ Invalid input! Please enter a number from 1 to 9.")


def select_difficulty():
    """Prompts user to select computer difficulty level."""
    while True:
        print("\nSelect Computer Difficulty Level:")
        print("1. Easy   (Computer picks random moves)")
        print("2. Medium (Computer blocks and looks for instant wins)")
        print("3. Hard   (Unbeatable Minimax AI)")

        choice = input("\nEnter level (1, 2, or 3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("⚠️ Invalid choice! Please select 1, 2, or 3.")



def main():
    while True:
        clear_screen()
        print("=" * 45)
        print("    🎮 WELCOME TO PYTHON TIC-TAC-TOE 🎮    ")
        print("=" * 45)
        print("Select Game Mode:")
        print("1. Play against Computer 🤖")
        print("2. Two Players 👥")

        mode_choice = input("\nEnter choice (1 or 2): ").strip()
        while mode_choice not in ['1', '2']:
            mode_choice = input("⚠️ Invalid choice! Enter 1 or 2: ").strip()

        vs_computer = (mode_choice == '1')
        difficulty = None

        if vs_computer:
            difficulty = select_difficulty()

        board = [str(i) for i in range(1, 10)]
        human_symbol = 'X'
        computer_symbol = 'O'
        current_player = 'X'
        game_over = False

        clear_screen()
        draw_board(board)

        while not game_over:
            if current_player == human_symbol:
                move_idx = get_human_move(board, current_player)
            else:
                if vs_computer:
                    print("🤖 Computer is calculating best move...")
                    time.sleep(0.6)  # Realistic delay effect
                    move_idx = get_computer_move(board, computer_symbol, human_symbol, difficulty)
                else:
                    move_idx = get_human_move(board, current_player)

            board[move_idx] = current_player
            clear_screen()
            draw_board(board)

            if check_win(board, current_player):
                if vs_computer and current_player == computer_symbol:
                    print("🤖 COMPUTER WINS! Better luck next time! 💻\n")
                else:
                    print(f"🎉 CONGRATULATIONS! Player '{current_player}' wins! 🎉\n")
                game_over = True
            elif check_tie(board):
                print("🤝 IT'S A TIE! Great game!\n")
                game_over = True
            else:
                current_player = 'O' if current_player == 'X' else 'X'

        play_again = input("Do you want to play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("\nThanks for playing! Goodbye! 👋")
            break

if __name__ == '__main__':
    main()