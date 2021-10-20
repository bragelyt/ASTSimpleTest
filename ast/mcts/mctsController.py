import random, math, json
from typing import Dict, List
from ast.mcts import treeNode

from ast.mcts.treeNode import TreeNode
from sim.simpleBoatController import SimpleBoatController

class MCTSController:

    def __init__(self, root: TreeNode, ExplorationBias: float) -> None:  # Currently using this one
        self.mainSim = SimpleBoatController()
        # self.rootNode = root
        # self.currentNode = root
        # self.currentLeafNode = root
        self.endStates = []
        self.bestState = None
        self.bestReward = -math.inf
        self.ExplorationBiasCoefficient = ExplorationBias
        with open("parameters.json") as f:
            params = json.load(f)  # Pass out to main?
        self.collision_reward = params["collision_reward"]
        self.MCT : Dict[List, TreeNode] = {}
        self.k = 0.2
        self.a = 0.5

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
    
    def loop(self):
        self.mainSim.reset_state()
        G = self.simulate()
        if G > self.bestReward:
            self.bestState = self.mainSim.get_sim_state()
            self.bestReward = G
    
    def simulate(self):
        state = self.mainSim.get_sim_state()
        if state not in self.MCT.keys():
            simNode = treeNode(state)
            self.MCT[state] = simNode
            rolloutSim = SimpleBoatController(state)
            return self.rollout(rolloutSim)
        node = self.MCT[state]
        node.visit_node()
        if len(node.children_visits) < self.k*node.times_visited**self.a:
            seedAction = random.random()
            newBornNode = treeNode(state + [seedAction])
            node.add_child(newBornNode)
        nextNode = node.UCTselect()  # TODO: OBS, returns state, not just action. Might want to change
        chosenSeed = nextNode.state[-1]
        terminal = self.mainSim.is_endstate()  # TODO: Stil think this is the wrong way around, (this and next line)
        p, e, d = self.mainSim.execute_action(chosenSeed)
        reward = self.get_reward(p,e,d, terminal)  # TODO: Think this could be moved out to node level. Might even be returned from execute_action
        if terminal:
            self.endStates.append(state)
            return reward
        totalReward = reward + self.simulate()
        node.visit_child(nextNode)
        node.evaluate_child(nextNode, totalReward)
        return totalReward
        
        
    def rollout(self, simulator) -> float:
        actionSeed = random.random()
        terminal = simulator.is_endstate()  # TODO: Stil think this is the wrong way around, (this and next line)
        p, e, d = simulator.execute_action(actionSeed)
        reward = self.get_reward(p,e,d, terminal)
        if terminal:
            return reward
        return reward + self.rollout(simulator)
    
    def get_reward(self, p,e,d, terminal):
        if terminal:
            if e:
                return self.collision_reward
            else:
                return -d
        else:
            return math.log(p)

