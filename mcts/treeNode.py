import math, json

class TreeNode:

    def __init__(self, state):
        self.state = state
        self.timesVisited = 1  # Initiates only after visit so should be one
        self.childrenVisits = {}
        self.childrenEvaluations = {}
        with open("parameters.json") as f:
            params = json.load(f)  # Pass out to main?
        self.explorationCoefficient = params["exploration_coefficient"]
    
    def visit_node(self):
        self.timesVisited += 1
    
    def add_child(self, childNode):
        self.childrenVisits[childNode] = 0
        self.childrenEvaluations[childNode] = 0
    
    def visit_child(self, childNode):
        self.childrenVisits[childNode] += 1
    
    def evaluate_child(self, child, evaluation):
        self.childrenEvaluations[child] = self.childrenEvaluations[child] + (evaluation - self.childrenEvaluations[child])/self.childrenVisits[child]

    def backpropegate(self, reward, targetNode):
        if self == targetNode:
            pass
        else:  # TODO: Unsusre if this is correct. Must find out how policy works
            self.totalEvaluation += reward
            self.timesVisited += 1
            if self.parrent is not None:
                self.parrent.backpropegate(reward + self.reward, targetNode)  # TODO: Do we want to return this? Don't see why, but i'm partialy blind.

    def UCTselect(self):  # Tree policy. "Bandit based Monte-Carlo Planning", Kocsis and Szepervari (2006)
        maxValue = -math.inf
        bestChild = None
        for child in self.childrenVisits:
            x = self.childrenEvaluations[child] + self.explorationCoefficient*(math.sqrt(math.log(self.timesVisited)/(1+self.childrenVisits[child])))
            if x > maxValue:
                bestChild = child
                maxValue = x
        return bestChild