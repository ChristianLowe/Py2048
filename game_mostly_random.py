import random

import game
from game_simulator import Simulator

def essentially_lost(board):
    if game.is_board_lost(board):
        return True

    zeroes = sum([1 if x == 0 else 0 for row in board for x in row])
    return zeroes < 3

def random_actor(board):
    moves = game.get_moves(board)
    
    if great_moves := [ m for m in moves if game.is_board_won(m) ]:
        return random.choice(great_moves)

    if decent_moves := [ m for m in moves if not essentially_lost(m) ]:
        return random.choice(decent_moves)

    return random.choice(moves)

if __name__ == "__main__":
    sim = Simulator.from_argv(random_actor)
    sim.run()
