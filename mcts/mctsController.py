import random, math, json

from datetime import datetime
from typing import Dict, List
from IPython.core.pylabtools import figsize

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn

from mcts.treeNode import TreeNode
from sim.simpleBoatController import SimpleBoatController

class MCTSController:

    def __init__(self) -> None:  # Currently using this one
        self.sim = SimpleBoatController()
        self.endStates = []
        self.crashStates = []
        self.bestState = None
        self.bestReward = -math.inf
        with open("parameters.json") as f:
            params = json.load(f)  # Pass out to main?
        self.collision_reward = params["collision_reward"]
        self.k = params["expansion_coefficient"]
        self.a = params["expansion_exponentioal"]
        self.MCT : Dict[List, TreeNode] = {}

    def loop(self, numberOfLoops):  # Exploration to, creation and rollout form a leaf node in the Monte Carlo Tree
        timeStart = datetime.now()
        Gs = []
        index = []
        for i in range(numberOfLoops):
            if (i%1000 == 0):
                print(i)
            self.sim.reset_sim()
            G = self.simulate()
            if G > self.bestReward:
                self.bestState = self.sim.get_state()
                self.bestReward = G
                print(f'Score {round(G, 2)} found at iteration {i}')
            Gs.append(G)
            index.append(i)
        print(f'{"Number of iterations":<25} | {i+1:4}')
        print(f'{"Number of nodes in tree":<25} | {len(self.MCT):4}')
        print(f'{"Best reward found":<25} | {round(self.bestReward, 2):4}')
        print(f'{"Runtime":<25} | {datetime.now() -timeStart}')
        print(f'{"Best action trace":<25} | {self.bestState[:-1]}')
        print(f'{"Nr of crash states found":<25} | {len(self.crashStates)}')
        print(f'{"Nr of unique crash states":<25} | {len(self.crashStates)}')
        with open('crashStates.json', 'w') as f:
            json.dump(self.crashStates, f, ensure_ascii=False, indent=4)
        self.MCTStats()
        plt.plot(index, Gs)
        plt.show()
        return self.bestState, self.bestReward
    
    def simulate(self):  # Three polict, expansion, rollout and backprop of a leaf node
        state = self.sim.get_state()
        if tuple(state) not in list(self.MCT.keys()):
            simNode = TreeNode(state)
            self.MCT[tuple(state)] = simNode
            return self.rollout()  # return self.multipleRollouts(50)  # return self.rollout()
        node = self.MCT[tuple(state)]
        node.visit_node()
        if len(node.childrenVisits) < self.k*node.timesVisited**self.a:
            seedAction = random.random()
            newBornState = state + [seedAction]
            newBornNode = TreeNode(newBornState)
            node.add_child(newBornNode)
        nextNode = node.UCTselect()  # TODO: OBS, returns state, not just action. Might want to change
        chosenSeed = nextNode.state[-1]
        terminal = self.sim.is_endstate()  # TODO: Probably swap back
        p, e, d = self.sim.execute_action(chosenSeed)
        reward = self.reward(p, e, d, terminal)  # TODO: Might be returned from execute_action
        if terminal:  # If tree is big enough to have an endstate in it we cant rollout.
            self.endStates.append(state)  # TODO: Get som stats on how often this happened. Does it happen to same nodes multiple times?
            if e:
                self.crashStates.append(tuple(state))
            return reward
        totalReward = reward + self.simulate()
        node.visit_child(nextNode)
        node.evaluate_child(nextNode, totalReward)
        return totalReward
    
    def multipleRollouts(self, rolloutAmount):  # TODO: Not working correctly. Idea is to rollout x times and return best rollout.
        bestReward = -math.inf
        state = self.sim.get_state()
        bestActionTrace = None
        for i in range(rolloutAmount):
            reward = self.rollout()
            if reward > bestReward:
                bestActionTrace = self.sim.get_state()
                bestReward = reward
            self.sim.reset_sim(state)
        self.sim.reset_sim(bestActionTrace)
        return bestReward

    def rollout(self) -> float:  # Rollout from a leafnode to a terminal state. Returns ecumulated reward
        actionSeed = random.random()
        terminal = self.sim.is_endstate()
        p, e, d = self.sim.execute_action(actionSeed)
        reward = self.reward(p, e, d, terminal)
        if terminal:
            state = self.sim.get_state()
            self.endStates.append(state)
            if e:
                self.crashStates.append(tuple(state))
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
    
    def MCTStats(self):
        childrenCounter = []
        totalChildren = 0
        for state, node in self.MCT.items():
            totalChildren += len(node.childrenVisits)
            childrenCounter.append(len(node.childrenVisits))
        print(totalChildren/len(self.MCT))
        sn.countplot(x=childrenCounter)
        plt.show()

    def rankMCTNodes(self):
        root = self.MCT.values()[0]
        ranks = [[root]]
        rank = 0
        while len(ranks[rank]) > 0:
            ranks.append([])
            for node in ranks[rank]:
                for child in node.childrenVisits.keys():
                    ranks[rank+1].append(child)
            rank += 1
        for rankList in ranks:
            print(len(rankList))