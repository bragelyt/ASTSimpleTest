

class TreeNode:

    def __init__(self, parrent, state_path):
        self.times_visited = 0
        self.children = []
        self.parrent = parrent
        self.state_path = state_path
    
    def visit_node(self):
        pass

    