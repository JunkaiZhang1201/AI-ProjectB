# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]


# count the total power of one color in board.
def count_blue_power(board):
    total = 0
    value_list = list(board.values())

    for i in range(len(value_list)):
        if value_list[i][0] == 'b':
            total += value_list[i][1]

    return total


def count_red_power(board):
    total = 0
    value_list = list(board.values())

    for i in range(len(value_list)):
        if value_list[i][0] == 'r':
            total += value_list[i][1]

    return total


# count the total num of one color
def count_blue_num(board):
    total = 0
    value_list = list(board.values())

    for i in range(len(value_list)):
        if value_list[i][0] == 'b':
            total += 1

    return total

def count_red_num(board):
    total = 0
    value_list = list(board.values())

    for i in range(len(value_list)):
        if value_list[i][0] == 'r':
            total += 1

    return total

def update_board(board, target, chess_col):

    # update a exist chess
    if target in board:
        chess_cur = board.get(target)
        cur_pow = chess_cur[1]

        # when current location has a power 6 chess
        if cur_pow == 6:
            del board[target]
        else:
            next_pow = cur_pow + 1
            board[target] = (chess_col, next_pow)

    # create a new chess
    else:
        board[target] = (chess_col, 1)

# board is a dictionary in form of {(1,1):('r',1),(1,2):('b',2)}
# action is a tuple in form of (1,1,0,1)
def spread(board, action):
    chess_r = action[0]
    chess_q = action[1]
    direction_r = action[2]
    direction_q = action[3]
    status = board.get(chess_r, chess_q)
    chess_col = status[0]
    chess_pow = status[1]

    for i in chess_pow:
        target_r = chess_r + direction_r

        # when hit the board edge
        if target_r < 0:
            target_r = 6
        elif target_r > 6:
            target_r = 0

        target_q = chess_q + direction_q

        # when hit the board edge
        if target_q < 0:
            target_q = 6
        elif target_q > 6:
            target_q = 0

        target = (target_r, target_q)
        update_board(board, target, chess_col)




