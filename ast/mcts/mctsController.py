import random, math, json
from typing import Dict, List


import matplotlib.pyplot as plt
import numpy as np

from ast.mcts.treeNode import TreeNode
from sim.simpleBoatController import SimpleBoatController

class MCTSController:

    def __init__(self, explorationBias: float) -> None:  # Currently using this one
        self.mainSim = SimpleBoatController()
        self.endStates = []
        self.bestState = None
        self.bestReward = -math.inf
        self.explorationBiasCoefficient = explorationBias
        with open("parameters.json") as f:
            params = json.load(f)  # Pass out to main?
        self.collision_reward = params["collision_reward"]
        self.k = params["bandit_coefficient"]
        self.a = params["bandit_exponentioal"]
        self.MCT : Dict[List, TreeNode] = {}

    def loop(self):  # Exploration to, creation and rollout form a leaf node in the Monte Carlo Tree
        Gs = []
        index = []
        for i in range(10000):
            if i%1000 == 0:
                print(i)
            self.mainSim.reset_sim()
            G = self.simulate()
            if G >= self.bestReward:
                self.bestState = self.mainSim.get_state()
                self.bestReward = G
                print(G)
            Gs.append(G)
            index.append(i)
        print(f'{"Number of nodes in tree":<25} | {len(self.MCT):4}')
        print(f'{"Best reward found":<25} | {round(self.bestReward,1):4}')
        print(len(Gs))
        plt.plot(index, Gs)
        plt.show()
        return self.bestState
    
    def simulate(self):  # Three polict, expansion, rollout and backprop of a leaf node
        state = self.mainSim.get_state()
        if tuple(state) not in list(self.MCT.keys()):
            simNode = TreeNode(state)
            self.MCT[tuple(state)] = simNode
            return self.rollout()
        node = self.MCT[tuple(state)]
        node.visit_node()
        if len(node.childrenVisits) < self.k*node.timesVisited**self.a:
            seedAction = random.random()
            newBornState = state + [seedAction]
            newBornNode = TreeNode(newBornState)
            node.add_child(newBornNode)
        nextNode = node.UCTselect()  # TODO: OBS, returns state, not just action. Might want to change
        chosenSeed = nextNode.state[-1]
        p, e, d = self.mainSim.execute_action(chosenSeed)
        terminal = self.mainSim.is_endstate()
        reward = self.reward(p, e, d, terminal)  # TODO: Might be returned from execute_action
        if terminal:  # If tree is big enough to have an endstate in it we cant rollout.
            self.endStates.append(state)  # TODO: Get som stats on how often this happened. Does it happen to same nodes multiple times?
            return reward
        totalReward = reward + self.simulate()
        node.visit_child(nextNode)
        node.evaluate_child(nextNode, totalReward)
        return totalReward
        
    def rollout(self) -> float:  # Rollout from a leafnode to a terminal state. Returns ecumulated reward
        actionSeed = random.random()
        p, e, d = self.mainSim.execute_action(actionSeed)
        terminal = self.mainSim.is_endstate()
        reward = self.reward(p, e, d, terminal)
        # print(simulator.get_sim_state())
        if terminal:
            return reward
        return reward + self.rollout()
    
    def reward(self, # Reward function.
        p,  # Transition probability
        e,  # An episode accured (e.g. boats crashed or NMAC)
        d,  # Closest distance between the boats throughout the simulation
        terminal):  # Simulation has terminated
        if terminal:
            if e:
                return self.collision_reward
            else:
                return -d
        else:
            return math.log(p)