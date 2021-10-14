

class TreeNode:

    def __init__(self, parrent, state_path, reward):
        self.times_visited = 0
        self.totalEvaluation = 0  # Accumulated  evaluation of this node
        self.reward = reward
        self.children = {}
        self.parrent = parrent
        self.state_path = state_path
    
    def visit_node(self):
        # TODO: Visiting might be handled in backprop?
        pass
    
    def backpropegate(self, reward, targetNode):
        if self == targetNode:
            pass
        else:  # TODO: Unsusre if this is correct. Must find out how policy works
            self.totalEvaluation += reward
            self.times_visited += 1
            if self.parrent is not None:
                self.parrent.backpropegate(reward + self.reward, targetNode)  # TODO: Do we want to return this? Don't see why, but i'm partialy blind.

 
'''
    def getExpectedResult(self, action: int) -> float:
        #print(self.children[action].totalEvaluation, self.numTakenAction[action])
        return self.children[action].totalEvaluation / self.numTakenAction[action]

    def addChild(self, action: int, child) -> None:
        if action in self.children.keys():
            raise Exception("duplicate child is illigal (no twins!)")
        self.children[action] = child
        child.parent = self
        return child
        
    def getExplorationBias(self, action: int) -> float:
        return  math.sqrt(math.log(self.numTimesVisited) / (self.numTakenAction[action] + 1))

    def addActionTaken(self, action: int):
        self.numTakenAction[action] += 1
'''