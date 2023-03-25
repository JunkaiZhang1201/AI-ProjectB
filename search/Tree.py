class TreeNode:
    # initialize the root node with initial board
    def __init__(self, board, action):
        self.board = board
        self.action = action
        self.children = []
        self.parent = None

    # append child node with their board and action
    def make_child(self, board, action):
        child_node = TreeNode(board, action)
        self.children.append(child_node)

    # get the path from goal node to initial board by actions
    def track_back(self):
        current_node = self 
        path = []
        while current_node is not None:
            path += current_node.action
            current_node = current_node.parent
        return path[::-1]

