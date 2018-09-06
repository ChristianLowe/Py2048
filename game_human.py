
# This file is a human-playable version of 2048.
# Controls: W/A/S/D for up/down/left/right, followed by the enter key

from game import *


def main():
    board = new_board()

    while True:
        print_board(board)

        if is_board_lost(board):
            print("No moves left. Game over.")
            return

        if is_board_won(board):
            print("Congrats! You win!")
            return

        key = input()

        left_board = push_board_left(board)
        right_board = push_board_right(board)
        up_board = push_board_up(board)
        down_board = push_board_down(board)

        if key == "a" and board != left_board:
            board = left_board
            add_cell(board)
        if key == "d" and board != right_board:
            board = right_board
            add_cell(board)
        if key == "w" and board != up_board:
            board = up_board
            add_cell(board)
        if key == "s" and board != down_board:
            board = down_board
            add_cell(board)


if __name__ == "__main__":
    main()

