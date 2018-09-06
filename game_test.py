import unittest

import game


class GameTest(unittest.TestCase):
    def test_board_getset(self):
        board_size = 4
        board = [[2 for _ in range(board_size)] for _ in range(board_size)]  # board is filled with 2's

        idx = board_size - 1

        self.assertEqual([2, 2, 2, 2], game.get_board_row(board, idx))
        game.set_board_row(board, idx, [2, 2, 4, 4])
        self.assertEqual([2, 2, 4, 4], game.get_board_row(board, idx))

        self.assertEqual([2, 2, 2, 4], game.get_board_col(board, idx))
        game.set_board_col(board, idx, [4, 4, 8, 8])
        self.assertEqual([4, 4, 8, 8], game.get_board_col(board, idx))

        self.assertEqual([2, 2, 4, 8], game.get_board_row(board, idx))

    def test_merge_row(self):
        before = [0, 2, 2, 4, 2, 0, 16, 8, 8, 16]
        after = [0, 4, 0, 4, 2, 0, 16, 16, 0, 16]
        game.board_size = len(before)
        self.assertEqual(after, game.merge_row(before))

    def test_squish_row(self):
        before = [2, 0, 4, 2, 0, 0, 16]
        after = [2, 4, 2, 16, 0, 0, 0]
        game.board_size = len(before)
        self.assertEqual(after, game.squish_row(before))
