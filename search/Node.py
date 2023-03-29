class Node:
    def __init__(self, board, num_step, action, parent, heuristic):
        self.board = board
        self.num_step = num_step
        self.action = action
        self.parent = parent

        h_value = heuristic(board)
        self.eval = h_value + num_step
        if parent is not None:
            if parent.action is not None:
                for pre_act in parent.action:
                    self.action.insert(0, pre_act)

    def __lt__(self, other):
        return self.eval < other.eval

    def __le__(self, other):
        return self.eval <= other.eval

    def __gt__(self, other):
        return self.eval > other.eval

    def __ge__(self, other):
        return self.eval >= other.eval

    def __eq__(self, other):
        return self.eval == other.eval

    def __ne__(self, other):
        return self.eval != other.eval


