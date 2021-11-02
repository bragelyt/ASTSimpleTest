# %%
from sim.simpleBoatController import SimpleBoatController
from mcts.mctsController import MCTSController
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,8)
import random

def main():
    MCTS = MCTSController()
    bestState, bestReward = MCTS.loop(4000)
    SBC = SimpleBoatController(bestState)
    SBC.plot()
    print(SBC.collision_happened)

def randomPath(verbose = True):
    SBC = SimpleBoatController()
    while not SBC.sim_in_endstate:
        SBC.execute_action(random.random())
    if verbose:
        SBC.plot()
    return SBC.collision_happened

# %%
main()

# # %%
# randomPath()


# # %%
# hits = 0
# for i in range(10000):
#     if randomPath(False):
#         hits+=1
# print(hits, "collisions in 10,000 random routes")