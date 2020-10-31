import random

import game
from game_simulator import Simulator

def actor(board):
    up_board = game.push_board_up(board)
    left_board = game.push_board_left(board)
    right_board = game.push_board_right(board)
    down_board = game.push_board_down(board)

    # If possible, keep a piece in the upper left
    if board != up_board and up_board[0][0] != 0:
        return up_board

    if board != left_board and left_board[0][0] != 0:
        return left_board

    if board != right_board and right_board[0][0] != 0:
        return right_board

    if board != down_board and down_board[0][0] != 0:
        return down_board

    # Can't keep piece in upper left, try to keep our pattern
    if board != up_board:
        return up_board

    if board != left_board:
        return left_board

    if board != right_board:
        return right_board

    if board != down_board:
        return down_board

    raise Exception('No possible move')

if __name__ == "__main__":
    sim = Simulator.from_argv(actor)
    sim.run()

