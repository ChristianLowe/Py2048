import multiprocessing as mp
import random
import sys

import game


def simulate(n):
    if n == 0: yield 0, 0
    won = 0
    lost = 0

    for i in range(n):
        board = game.new_board()

        while True:
            board = random.choice(game.get_moves(board))
            game.add_cell(board)

            if game.is_board_won(board):
                yield 1, 0
                break

            if game.is_board_lost(board):
                yield 0, 1
                break


def simulate_batched(n, batch_size=50):
    whole_batches = n // batch_size

    for batch_idx in range(whole_batches):
        won, lost = map(sum, zip(*simulate(batch_size)))
        yield won, lost

    won, lost = map(sum, zip(*simulate(n % batch_size)))
    yield won, lost


def simulate_mp_worker(n, q, batch_size):
    for result in simulate_batched(n, batch_size):
        q.put(result)


def simulate_mp(n, p, batch_size):
    won = 0
    lost = 0

    children = []
    q = mp.Queue()

    for p_idx in range(p):
        work_here = n // p + (1 if p_idx < n % p else 0)
        proc = mp.Process(target=simulate_mp_worker, args=(work_here, q, batch_size))
        proc.start()
        children.append(p)

    while mp.active_children():
        try:
            yield q.get(timeout=3)
        except:
            # safe to ignore
            pass


def main(argv):
    won = 0
    lost = 0

    simulation = simulate_batched(argv.n, argv.b) \
            if argv.p == 1 else simulate_mp(argv.n, argv.p, argv.b)

    for won_here, lost_here in simulation:
        won += won_here
        lost += lost_here
        print("\rGame #%d: %d:%d" % (won + lost, won, lost), end='')
        sys.stdout.flush()

    print("\n\nWin: %d, Lost: %d, Percent: %.1f" % (won, lost, (won / lost) * 100))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='how many simulations to run', default=5000)
    parser.add_argument('-p', type=int, help='parallelism for multiprocessing', default=1)
    parser.add_argument('-b', type=int, help='how large each batch should be', default=50)
    main(parser.parse_args())
