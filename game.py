import queue
import random

board_size = 4


def get_board_col(board, index):
    return board[index]


def get_board_row(board, index):
    row = []
    for i in range(board_size):
        row.append(board[i][index])
    return row


def set_board_col(board, index, new_col):
    board[index] = new_col


def set_board_row(board, index, new_row):
    for i in range(board_size):
        board[i][index] = new_row[i]


def print_board(board):
    for y in range(board_size):
        print("+----" * board_size, end="+\n")
        for x in range(board_size):
            print('|', end='')
            if board[x][y] == 0:
                print("    ", end='')
            else:
                print("%04s" % str(board[x][y]), end='')
        print('|')
    print("+----" * board_size, end="+\n")


def add_cell(board):
    open_cells = []
    for x in range(board_size):
        for y in range(board_size):
            if board[x][y] == 0:
                open_cells.append((x, y))

    if len(open_cells) == 0:  # No free space available
        return

    (x, y) = random.choice(open_cells)
    board[x][y] = 2 if random.random() > .1 else 4


def new_board():
    board = [[0 for _ in range(board_size)] for _ in range(board_size)]
    add_cell(board)
    add_cell(board)
    return board


def squish_row(row):
    empty_cells = queue.Queue()
    for i in range(board_size):
        if row[i] == 0:
            empty_cells.put(i)
        elif not empty_cells.empty():
            row[empty_cells.get()] = row[i]
            row[i] = 0
            empty_cells.put(i)
    return row


def merge_row(row):
    for i in range(board_size - 1):
        if row[i] == row[i + 1]:
            row[i] <<= 1
            row[i + 1] = 0
    return row


def move_row(row):
    return squish_row(merge_row(squish_row(row)))


def push_board_left(board):
    left_board = [x[:] for x in board]
    for rowIdx in range(board_size):
        set_board_row(left_board, rowIdx, move_row(get_board_row(left_board, rowIdx)))
    return left_board


def push_board_right(board):
    right_board = [x[:] for x in board]
    for rowIdx in range(board_size):
        set_board_row(right_board, rowIdx, move_row(get_board_row(right_board, rowIdx)[::-1])[::-1])
    return right_board


def push_board_up(board):
    up_board = [x[:] for x in board]
    for colIdx in range(board_size):
        set_board_col(up_board, colIdx, move_row(get_board_col(up_board, colIdx)))
    return up_board


def push_board_down(board):
    down_board = [x[:] for x in board]
    for colIdx in range(board_size):
        set_board_col(down_board, colIdx, move_row(get_board_col(down_board, colIdx)[::-1])[::-1])
    return down_board


def is_board_won(board):
    for row in board:
        for cell in row:
            if cell == 2048:
                return True
    return False


def is_board_lost(board):
    return len(get_moves(board)) == 0


def get_moves(board):
    moves = []

    left_board = push_board_left(board)
    right_board = push_board_right(board)
    up_board = push_board_up(board)
    down_board = push_board_down(board)

    if left_board != board:
        moves.append(left_board)

    if right_board != board:
        moves.append(right_board)

    if up_board != board:
        moves.append(up_board)

    if down_board != board:
        moves.append(down_board)

    return moves
