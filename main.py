from sim.simpleBoatController import SimpleBoatController
from mcts.mctsController import MCTSController
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,8)

def main():
    MCTS = MCTSController()
    bestState, bestReward = MCTS.loop()
    SBC = SimpleBoatController(bestState)
    SBC.plot()


if __name__ == "__main__":
    main()
