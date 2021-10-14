from ast.mcts.treeNode import TreeNode
from sim.simpleBoatController import SimpleBoatController

class MCTSController:

    def __init__(self, root: TreeNode, ExplorationBias: float) -> None:
        self.mainSim = SimpleBoatController()
        self.rootNode = root
        self.currentNode = root
        self.currentLeafNode = root
        self.ExplorationBiasCoefficient = ExplorationBias
        
        # self.HashTable = {}
        # self.History = []

    def __init__(
        self,
        root: TreeNode,
        ExplorationBias: float
    ):
       # self.simWorld = SimWorld(root.state)
        self.rootNode = root
        self.currentNode = root
        self.currentLeafNode = root
        self.ExplorationBiasCoefficient = ExplorationBias
        self.HashTable = {}
        self.History = []
    
    def rollout(self) -> float:
        accReward = 0.0
        rolloutSim = SimpleBoatController(state = self.mainSim.get_sim_state())
        return accReward
