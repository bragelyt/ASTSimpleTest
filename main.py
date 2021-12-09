from datetime import datetime
from sim.simInterface import SimInterface
from sim.simpleBoatController import SimpleBoatController
from mcts.mctsController import MCTSController
import matplotlib.pyplot as plt
import random

def singleAST():
    MCTS = MCTSController(verbose = True)
    MCTS.loop(20100)

def loopAST(nrOfSearches, searchDepth):
    pos = []
    neg = []
    its = []
    timeStart = datetime.now()
    crashStates = []
    for i in range(nrOfSearches):
        print(i)
        MCTS = MCTSController(verbose = False)
        s, r, i, cs = MCTS.loop(searchDepth)
        crashStates += cs
        if r < 0:
            neg.append(r)
        else:
            pos.append(r)
            its.append(i)
    runTime = datetime.now() - timeStart
    print(len(pos))
    print(len(neg))
    print(pos)
    print(neg)
    print(its)
    print(sum(its) / len(its))
    print(runTime)
    print(f'{"Nr of crash states found":<25} | {len(crashStates):}')
    print(f'{"Unique crash states found":<25} | {len(set(crashStates))}')

def randomPath(verbose = True):
    SBC = SimInterface()
    reward = 0
    while not SBC.sim_in_endstate:
        reward += SBC.step(random.random())
    if verbose:
        SBC.plot()
    return SBC.is_failure_episode(), reward, SBC.simWorld.closest_boat_distance

def loopRandomPaths(nrOfSimulations):    
    hits = 0
    rewards = []
    distances = []
    timeStart = datetime.now()
    for i in range(nrOfSimulations):
        failure, reward, distance = randomPath(verbose = False)
        rewards.append(reward)
        distances.append(distance)
        if failure:
            hits+=1
        if (i+1)%10000 == 0:
            print(hits, "collisions in",i+1,"random routes")
    runTime = datetime.now() - timeStart
    print(runTime)
    print(max(rewards))
    print(min(rewards))
    print(sum(rewards) / len(rewards))
    print(max(distances))
    print(min(distances))
    print(sum(distances) / len(distances))


    # Run single AST search and plot path, reward over time and tree statistics.
# singleAST()

    # Run multiple, separate AST searches. Some statistics are printed
loopAST(nrOfSearches=1000, searchDepth=6000)

    # Baseline search.
# loopRandomPaths(nrOfSimulations= 10**6)

