import random
import json
import os
from colorama import Fore, Style, init

init()

SCORES_FILE = "scores.json"

def color_symbol(symbol):
    if symbol == "X":
        return Fore.GREEN + "X" + Style.RESET_ALL
    elif symbol == "O":
        return Fore.YELLOW + "O" + Style.RESET_ALL
    else:
        return symbol

def print_board(board):
    print()
    for row in board:
        print(" | ".join(color_symbol(cell) for cell in row))
        print("-" * 9)

def show_guide():
    print("\nBoard Guide (use these numbers to place your move):")
    print("1 | 2 | 3")
    print("4 | 5 | 6")
    print("---------")
    print("7 | 8 | 9")

def check_win(board, player):
    # check rows + columns + diagonals for a win
    for i in range(3):
        if all(cell == player for cell in board[i]): # row
            return True
        if all(board[j][i] == player for j in range(3)): # column
            return True
        
        # diagonals

    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False
    
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_move(player):
    while True:
        try:
            move = int(input(f"{player}'s move (1-9): "))
            if move < 1 or move > 9:
                print("Invalid move. Choose a number from 1 to 9.")
            else:
                return move
        except ValueError:
            print("Invalid move. Please enter a number.")

def cpu_move_easy(board):
    empty = [(r,c) for r in range(3) for c in range(3) if board[r][c] == " "]
    return random.choice(empty) if empty else None

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as file:
            scores = json.load(file)
            scores = {k.upper() if k.lower() in ['x', 'o'] else k: v for k,v in scores.items()}
            return scores
    return {"X": 0, "O": 0, "Draws": 0, "mode": "pvp"}

def save_scores(scores):
    with open(SCORES_FILE, "w") as file:
        json.dump(scores, file)


def show_scores(scores):
    print("\nScoreboard:")
    print(f"Player X Wins: {scores['X']}")
    print(f"Player O Wins: {scores['O']}")
    print(f"{'CPU' if scores['mode'] == 'cpu' else 'Player O'} Wins: {scores['O']}")
    print(f"Draws: {scores['Draws']}")

def play_game(mode, scores, player_symbol):
    board = [[" " for _ in range(3)] for _ in range(3)]
    moves_map = {
        1: (0,0), 2: (0,1), 3: (0,2),
        4: (1,0), 5: (1,1), 6: (1,2),
        7: (2,0), 8: (2,1), 9: (2,2),
    }

    cpu_symbol = "O" if player_symbol == "X" else "X"
    print_board(board)

    current_player = "X"
    while True:
        if current_player == player_symbol or mode == "pvp":
            move = get_move(f"Player {current_player}")
            row, col = moves_map[move]
            if board[row][col] != " ":
                print("That spot is already taken. Try again.")
                continue
            board[row][col] = current_player
        else:
            print("CPU is thinking...")
            row, col = cpu_move_easy(board)
            board[row][col] = current_player

        print_board(board)

        if check_win(board, current_player):
            winner = "CPU" if mode == "cpu" and current_player == cpu_symbol else f"Player {current_player}"
            print(f"{winner} wins!")
            scores[current_player] += 1
            break
        if check_draw(board):
            print("It's a draw.")
            scores["Draws"] += 1
            break

        current_player = "O" if current_player == "X" else "X"

def main():
    scores = load_scores()

    while True:
        print("\nChoose Game Mode:")
        print("1. Player vs. Player")
        print("2. Player vs. CPU")
        choice = input("Enter 1 or 2: ").strip()

        if choice == "1":
            mode = "pvp"
        elif choice == "2":
            mode = "cpu"
        else:
            print("Invalid choice. Try again.")
            continue

        while True:
            symbol = input("Do you want to be X or O? ").strip().upper()
            print(f"DEBUG: You entered '{symbol}'")
            if symbol in ["X", "O"]:
                break
            print("Invalid choice. Choose X or O.")

        scores["mode"] = mode
        show_guide()
        play_game(mode, scores, player_symbol=symbol)
        show_scores(scores)
        save_scores(scores)
        
        again = input("\nPlay again? (Y/N): ").strip().lower()
        if again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()