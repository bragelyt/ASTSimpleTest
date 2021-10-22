import math, json

class TreeNode:

    def __init__(self, state):
        self.state = state
        self.times_visited = 1  # TODO: Safe way out, but double check
        self.children_visits = {}
        self.children_evaluations = {}
        self.children = []  # Probably just use children_visit.keys()
        with open("parameters.json") as f:
            params = json.load(f)  # Pass out to main?
        self.exploration_coefficient = params["exploration_coefficient"]
    
    def visit_node(self):
        self.times_visited += 1
    
    def add_child(self, childNode):
        self.children_visits[childNode] = 1
        self.children_evaluations[childNode] = 0
    
    def visit_child(self, childNode):
        self.children_visits[childNode] += 1
    
    def evaluate_child(self, child, evaluation):
        self.children_evaluations[child] = (evaluation - self.children_evaluations[child])/self.children_visits[child]

    def backpropegate(self, reward, targetNode):
        if self == targetNode:
            pass
        else:  # TODO: Unsusre if this is correct. Must find out how policy works
            self.totalEvaluation += reward
            self.times_visited += 1
            if self.parrent is not None:
                self.parrent.backpropegate(reward + self.reward, targetNode)  # TODO: Do we want to return this? Don't see why, but i'm partialy blind.

    def UCTselect(self):
        maxValue = -math.inf
        bestChild = None
        for child in self.children_visits:
            x = self.children_evaluations[child] + self.exploration_coefficient*math.sqrt(math.log(self.times_visited)/self.children_visits[child])
            if x > maxValue:
                bestChild = child
                maxValue = x
        return bestChild


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