from sim.simpleBoatController import SimpleBoatController
from ast.mcts.mctsController import MCTSController

def main():
    MCTS = MCTSController(2.0)
    bestState = MCTS.loop()
    SBC = SimpleBoatController(bestState)
    SBC.plot()

if __name__ == "__main__":
    main()
