import random

import game
from game_simulator import Simulator

def random_actor(board):
    return random.choice(game.get_moves(board))

if __name__ == "__main__":
    sim = Simulator.from_argv(random_actor)
    sim.run()
