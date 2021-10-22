import random, math, json
from typing import Dict, List
from ast.mcts import treeNode

from ast.mcts.treeNode import TreeNode
from sim.simpleBoatController import SimpleBoatController

class MCTSController:

    def __init__(self, explorationBias: float) -> None:  # Currently using this one
        self.mainSim = SimpleBoatController()
        # self.rootNode = root
        # self.currentNode = root
        # self.currentLeafNode = root
        self.endStates = []
        self.bestState = None
        self.bestReward = -math.inf
        self.explorationBiasCoefficient = explorationBias
        with open("parameters.json") as f:
            params = json.load(f)  # Pass out to main?
        self.collision_reward = params["collision_reward"]
        self.MCT : Dict[List, TreeNode] = {}
        self.k = 0.2
        self.a = 0.5

    def loop(self):
        for i in range(25000):
            if i%250 == 0:
                print(i)
            self.mainSim.reset_state()
            G = self.simulate()
            if G > self.bestReward:
                self.bestState = self.mainSim.get_sim_state()
                self.bestReward = G
        return self.bestState
    
    def simulate(self):
        state = self.mainSim.get_sim_state()
        if tuple(state) not in list(self.MCT.keys()):
            simNode = TreeNode(state)
            self.MCT[tuple(state)] = simNode
            return self.rollout()
        node = self.MCT[tuple(state)]
        node.visit_node()
        if len(node.children_visits) < self.k*node.times_visited**self.a:
            print(len(node.children_visits), self.k*node.times_visited**self.a)
            seedAction = random.random()
            newBornState = state + [seedAction]
            newBornNode = TreeNode(newBornState)
            node.add_child(newBornNode)
        nextNode = node.UCTselect()  # TODO: OBS, returns state, not just action. Might want to change
        chosenSeed = nextNode.state[-1]
        p, e, d = self.mainSim.execute_action(chosenSeed)
        terminal = self.mainSim.is_endstate()  # TODO: Stil think this is the wrong way around, (this and next line)
        reward = self.get_reward(p,e,d, terminal)  # TODO: Think this could be moved out to node level. Might even be returned from execute_action
        if terminal:
            self.endStates.append(state)
            return reward
        totalReward = reward + self.simulate()
        node.visit_child(nextNode)
        node.evaluate_child(nextNode, totalReward)
        return totalReward
        
        
    def rollout(self) -> float:
        actionSeed = random.random()
        p, e, d = self.mainSim.execute_action(actionSeed)
        terminal = self.mainSim.is_endstate()  # TODO: Stil think this is the wrong way around, (this and next line)
        reward = self.get_reward(p,e,d, terminal)
        # print(simulator.get_sim_state())
        if terminal:
            return reward
        return reward + self.rollout()
    
    def get_reward(self, p,e,d, terminal):
        if terminal:
            if e:
                return self.collision_reward
            else:
                return -d
        else:
            return math.log(p)

    def list_to_string(self, list):
        return 