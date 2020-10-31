import multiprocessing as mp
import sys

import game


class Simulator:
    def __init__(self, actor, total_cases, parallelism, batch_size):
        self.actor = actor
        self.total_cases = total_cases
        self.parallelism = parallelism
        self.batch_size = batch_size


    @staticmethod
    def from_argv(actor):
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('-n', type=int, help='how many simulations to run', default=5000)
        parser.add_argument('-p', type=int, help='parallelism for multiprocessing', default=1)
        parser.add_argument('-b', type=int, help='how large each batch should be', default=50)
        argv = parser.parse_args()
        return Simulator(actor, argv.n, argv.p, argv.b)


    def simulate(self, n):
        if n == 0: yield 0, 0, 0
        won = 0
        lost = 0

        for i in range(n):
            board = game.new_board()

            moves_deep = 0
            while True:
                board = self.actor(board)
                moves_deep += 1
                game.add_cell(board)

                if game.is_board_won(board):
                    yield 1, 0, moves_deep
                    break

                if game.is_board_lost(board):
                    yield 0, 1, moves_deep
                    break


    def simulate_batched(self, n):
        whole_batches = n // self.batch_size

        for batch_idx in range(whole_batches):
            yield tuple(map(sum, zip(*self.simulate(self.batch_size))))

        yield tuple(map(sum, zip(*self.simulate(n % self.batch_size))))


    def simulate_mp_worker(self, n, q):
        for result in self.simulate_batched(n):
            q.put(result)


    def simulate_mp(self, n):
        won = 0
        lost = 0

        p = self.parallelism
        children = []
        q = mp.Queue()

        for p_idx in range(p):
            work_here = n // p + (1 if p_idx < n % p else 0)
            proc = mp.Process(target=self.simulate_mp_worker, args=(work_here, q))
            proc.start()
            children.append(p)

        while mp.active_children():
            try:
                yield q.get(timeout=3)
            except:
                # safe to ignore
                pass


    def run(self):
        won = 0
        lost = 0
        moves_played = 0

        simulation = self.simulate_batched(self.total_cases) \
                if self.parallelism <= 1 else self.simulate_mp(self.total_cases)

        for won_here, lost_here, moves_deep in simulation:
            won += won_here
            lost += lost_here
            moves_played += moves_deep
            expected_moves = 0 if won + lost == 0 else moves_played / (won + lost)
            print("\rGame #%d: %d:%d    E[moves]: %.1f" % (won + lost, won, lost, expected_moves), end='')
            sys.stdout.flush()

        print("\n\nWin: %d, Lost: %d, Percent Won: %.1f    E[moves]: %.1f" % (won, lost, (won / lost) * 100, moves_played / (won + lost)))

