import random

import game
from game_simulator import Simulator

def freq(board):
    # Count frequencies of 2**0, 2**1, ... 2**11
    power_freq = []
    target_value = 1
    while target_value <= 2048:
        value_count = sum([1 if x == target_value else 0 for row in board for x in row])
        power_freq.append(value_count)
        target_value *= 2

    # Reverse so higher values are higher priority
    return tuple(reversed(power_freq))

def random_actor(board):
    moves = game.get_moves(board)
    moves = list(reversed(sorted(moves, key=freq)))
    return moves[0]

if __name__ == "__main__":
    sim = Simulator.from_argv(random_actor)
    sim.run()

