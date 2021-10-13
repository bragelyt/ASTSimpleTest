from ast.mcts.treeNode import TreeNode
from sim.simpleBoatController import SimpleBoatController

class MCTSController:

    def __init__(self) -> None:
        self.mainSim = SimpleBoatController()

    
    def rollout(self) -> float:
        accReward = 0.0
        rolloutSim = SimpleBoatController(state = self.mainSim.get_sim_state())
        return accReward
