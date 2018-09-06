import random
import sys

import game


def main():
    n = 5000

    won = 0
    lost = 0

    for i in range(n):
        print("\rGame #%d" % (i + 1), end='')
        sys.stdout.flush()

        board = game.new_board()

        while True:
            board = random.choice(game.get_moves(board))
            game.add_cell(board)

            if game.is_board_won(board):
                won += 1
                break

            if game.is_board_lost(board):
                lost += 1
                break

    print("\n\nWin: %d, Lost: %d, Percent: %.1f" % (won, lost, (won / lost) * 100))


if __name__ == "__main__":
    main()
