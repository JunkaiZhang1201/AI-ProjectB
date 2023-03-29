# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from search.utils import render_board
from copy import deepcopy
from search.Node import Node


def search(input):
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
    result = A_star(input, heuristic)
    return result

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    '''return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]'''


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
    target_r = action[0]
    target_q = action[1]
    direction_r = action[2]
    direction_q = action[3]
    status = board.get((target_r, target_q))
    chess_col = status[0]
    chess_pow = status[1]

    del board[(target_r, target_q)]

    for i in range(chess_pow):
        target_r = target_r + direction_r

        # when hit the board edge
        if target_r < 0:
            target_r = 6
        elif target_r > 6:
            target_r = 0

        target_q = target_q + direction_q

        # when hit the board edge
        if target_q < 0:
            target_q = 6
        elif target_q > 6:
            target_q = 0

        target = (target_r, target_q)
        update_board(board, target, chess_col)

    return board


# get D coordinate of a chess
# which is a tuple in form of (1,1)
def count_D(chess) -> int:
    if chess[0] + chess[1] == 0 or chess[0] + chess[1] == 7:
        return 0
    elif chess[0] + chess[1] == 1 or chess[0] + chess[1] == 8:
        return 1
    elif chess[0] + chess[1] == 2 or chess[0] + chess[1] == 9:
        return 2
    elif chess[0] + chess[1] == 3 or chess[0] + chess[1] == 10:
        return 3
    elif chess[0] + chess[1] == 4 or chess[0] + chess[1] == 11:
        return 4
    elif chess[0] + chess[1] == 5 or chess[0] + chess[1] == 12:
        return 5
    else:
        return 6


# get the line list using the greedy algorithm
# the element in the list which is returned has a form like 'r1'
def record_line(board, my_dict, my_list) -> list:
    copy_dict = my_dict
    copy_board = board
    max_value = max(my_dict.values())

    if max_value <= 0:
        return list(set(my_list))
    else:
        for key, value in my_dict.items():
            if value == max_value:
                my_list.append(key)

                # decrease the sum of each axis if a blue chess is on the longest line
                # and delete this chess on board
                for chess in copy_board:
                    if copy_board[chess][0] == 'b':
                        if ('r' + f"{chess[0]}" == key) or \
                                ('q' + f"{chess[1]}" == key) or \
                                ('D' + f"{count_D(chess)}" == key):
                            copy_dict['r' + f"{chess[0]}"] -= 1
                            copy_dict['q' + f"{chess[1]}"] -= 1
                            copy_dict['D' + f"{count_D(chess)}"] -= 1

                return record_line(copy_board, copy_dict, my_list)


def heuristic(board) -> int:
    if count_blue_num(board) == 0:
        return 0
    else:
        record_list = []
        # dic which used to record the coordinates of (lines for) blue chess.
        findline_dict = {'r0': 0, 'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0, 'r5': 0, 'r6': 0,
                         'q0': 0, 'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'q5': 0, 'q6': 0,
                         'D0': 0, 'D1': 0, 'D2': 0, 'D3': 0, 'D4': 0, 'D5': 0, 'D6': 0}

        # count each line's chess num
        for chess in board:
            chess_val = board[chess]
            if chess_val[0] == 'b':
                findline_dict['r' + f"{chess[0]}"] += 1
                findline_dict['q' + f"{chess[1]}"] += 1
                findline_dict['D' + f"{count_D(chess)}"] += 1

        line_list = record_line(board, findline_dict, record_list)
        line_num = len(line_list)

        # if a red chess is on the line that in the minimum line list
        for chess in board:
            chess_val = board[chess]
            if chess_val[0] == 'r':
                if ('r' + f"{chess[0]}") in line_list or \
                        ('q' + f"{chess[1]}") in line_list or \
                        ('D' + f"{count_D(chess)}") in line_list:
                    return line_num

        # if no red chess is on the line that in the minimum line list
        return 1 + line_num


# build a heap
import heapq


# make a node for heap
# def make_q_node(board, num_step, action, parent):
#     h_value = heuristic(board)
#     eval = h_value + num_step
#     node = (eval, board, num_step, action, parent)
#     if parent is not None:
#         if parent[3] is not None:
#             for pre_act in parent[3]:
#                 node[3].insert(0, node[4][3][pre_act])
#     return node


# check if goal
def goal_test(node):
    if count_blue_num(node.board) == 0:
        return 1
    else:
        return 0


# spread a node to six directions
def find_child(node, child_list, heuristic):
    cur_board = node.board
    cur_cost = node.num_step
    action_list = []

    for key, value in cur_board.items():
        if value[0] == 'r':
            direction = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, -1)]
            for d in direction:
                action = (key[0], key[1], d[0], d[1])
                action_list.append(action)

    for act in action_list:
        next_board = deepcopy(node.board)
        child_board = spread(next_board, act)
        child_node = Node(child_board, cur_cost + 1, [act], node, heuristic)
        child_list.append(child_node)


# A*
def A_star(board, heuristic):
    start_node = Node(board, 0, [], None, heuristic)
    h = []
    heapq.heappush(h, start_node)

    while True:
        node = heapq.heappop(h)
        if goal_test(node) == 1:
            return node.num_step
        else:
            child = []
            find_child(node, child, heuristic)
            for i in child:
                heapq.heappush(h, i)



