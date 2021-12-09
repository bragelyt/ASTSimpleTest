import random, math, json

from datetime import date, datetime, time
from typing import Dict, List
from typing_extensions import runtime
from IPython.core.pylabtools import figsize

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn

from mcts.treeNode import TreeNode
from sim.simInterface import SimInterface
from sim.simpleBoatController import SimpleBoatController

class MCTSController:

    def __init__(self, verbose = True) -> None:  # Currently using this one
        self.verbose = verbose
        self.simIntefrace = SimInterface()
        self.endStates = []
        self.crashStates = []
        self.bestState = None
        self.bestReward = -math.inf
        with open("parameters.json") as f:
            params = json.load(f)  # Pass out to main?
        self.k = params["expansion_coefficient"]
        self.a = params["expansion_exponentioal"]
        self.MCT : Dict[tuple, TreeNode] = {}

    def loop(self, numberOfLoops):  # Exploration to, creation and rollout form a leaf node in the Monte Carlo Tree
        timeStart = datetime.now()
        deltaTime = datetime.now()
        Gs = []
        its = []
        itTimes = []
        runTimes = []
        firstIt = None
        for i in range(numberOfLoops):
            self.currentNode = None
            if (self.verbose and i%1000 == 0):
                itTimes.append((datetime.now() - deltaTime).total_seconds())
                runTimes.append((datetime.now() - timeStart).total_seconds())
                deltaTime = datetime.now()
                its.append(i)
                print(i)
            self.simIntefrace.reset_sim()
            G = self.simulate()
            if G > self.bestReward:
                if G > 0 and firstIt is None:
                    firstIt = i
                self.bestState = self.simIntefrace.get_state()
                self.bestReward = G
                if self.verbose:
                    print(f'Score {round(G, 2)} found at iteration {i}')
            Gs.append(G)
            runTime = datetime.now() - timeStart
        with open('crashStates.json', 'w') as f:
            json.dump(self.crashStates, f, ensure_ascii=False, indent=4)
        if self.verbose:
            self.plotRunTime(its, itTimes, runTimes)
            self.stats(Gs, runTime)
        return self.bestState, self.bestReward, firstIt, self.crashStates
    
    def simulate(self):  # Three polict, expansion, rollout and backprop of a leaf node
        state = self.simIntefrace.get_state()
        if tuple(state) not in list(self.MCT.keys()):
            simNode = TreeNode(state)
            self.MCT[tuple(state)] = simNode
            return self.rollout()  # return self.multipleRollouts(50)  # return self.rollout()
        node = self.MCT[tuple(state)]
        node.visit_node()
        if len(node.childrenVisits) < self.k*node.timesVisited**self.a:
            seedAction = random.random()
            newBornState = state + [seedAction]
            node.add_child(newBornState)
        nextNode = node.UCTselect()  # TODO: OBS, returns state, not just action. Might want to change
        chosenSeed = nextNode[-1]
        reward = self.simIntefrace.step(chosenSeed)
        terminal = self.simIntefrace.is_terminal()  # TODO: Swapped back
        e = self.simIntefrace.is_failure_episode()
        # self.currentNode = nextNode
        if terminal:  # If tree is big enough to have an endstate in it we cant rollout.
            self.endStates.append(state)
            if e:
                self.crashStates.append(tuple(state))
            return reward
        # self.currentNode = nextNode
        totalReward = reward + self.simulate()
        node.visit_child(nextNode)
        node.evaluate_child(nextNode, totalReward)
        return totalReward
    
    def rollout(self) -> float:  # Rollout from a leafnode to a terminal state. Returns ecumulated reward
        actionSeed = random.random()
        reward = self.simIntefrace.step(actionSeed)
        terminal = self.simIntefrace.is_terminal()
        e = self.simIntefrace.is_failure_episode()
        if terminal:
            state = self.simIntefrace.get_state()
            self.endStates.append(state)
            if e:
                self.crashStates.append(tuple(state))
            return reward
        return reward + self.rollout()
    
    def multipleRollouts(self, rolloutAmount):  # TODO: Not very effective. Might want to look into returning avg instead? Or just scrap
        bestReward = -math.inf
        state = self.simIntefrace.get_state()
        bestActionTrace = None
        for i in range(rolloutAmount):
            reward = self.rollout()
            if reward > bestReward:
                bestActionTrace = self.simIntefrace.get_state()
                bestReward = reward
            self.simIntefrace.set_state(state)
        self.simIntefrace.set_state(bestActionTrace)
        return bestReward
    
    def plotRunTime(self, its, itTimes, runTimes):
        plt.rcParams["figure.figsize"] = (5,4)
        ticks = []
        for i in range(len(its)):
            if i%5 == 0:
                ticks.append(its[i])
        plt.xticks(ticks)

        plt.plot(its, runTimes)
        plt.xlabel("Iterations")
        plt.ylabel("Runtime (sec)")
        plt.show()

        bins = []
        for itt in its:
            bins.append(itt+500)
            
        plt.xticks(ticks)
        plt.hist(x=its[1:], weights=itTimes[1:], bins= bins, edgecolor='black',color='white')
        plt.xlabel("Iterations")
        plt.ylabel("Runtime (sec)")
        plt.show()

    def stats(self, Gs, runTime):
        # plt.rcParams["figure.figsize"] = (7.5,7)
        print("-"*35)
        root = list(self.MCT.values())[0]
        ranks = [[root]]
        # lastState = [[0]]
        rank = 0
        while len(ranks[rank]) > 0:
            ranks.append([])
            # lastState.append([])
            for node in ranks[rank]:
                for childNodeState in node.childrenVisits.keys():
                    if tuple(childNodeState) in self.MCT.keys():
                        child = self.MCT[tuple(childNodeState)]
                        ranks[rank+1].append(child)
                    # lastState[rank+1].append(child.state[rank])
            rank += 1
        tot = 0
        for i, rankList in enumerate(ranks[:-1]):
            tot += len(rankList)
            print(f'At depth {i:2} there are {len(rankList):3} nodes')
        print(f'Total nodes:',tot)
        print("-"*35)
        print(f'Runtime         | {runTime}')
        print(f'{"Best reward found":<25} | {round(self.bestReward, 2):4}')
        print(f'{"Nr of crash states found":<25} | {len(self.crashStates):}')
        print(f'{"Unique crash states found":<25} | {len(set(self.crashStates))}')
        childrenCounter = []
        totalChildren = 0
        for node in self.MCT.values():
            totalChildren += len(node.childrenVisits)
            childrenCounter.append(len(node.childrenVisits))
        print(f'Average nr of children in tree: {round(totalChildren/len(self.MCT),3)}')
        print(f'{"Best action trace":<25} | {self.bestState}')
        printSim = SimInterface()
        printSim.set_state(self.bestState)
        printSim.plot()
        sn.countplot(x=childrenCounter)
        plt.show()
        index = range(len(Gs))
        plt.xlabel("Iterations")
        plt.ylabel("Reward")
        plt.plot(index, Gs)
        plt.show()