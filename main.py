from sim.simpleBoatController import SimpleBoatController
from ast.mcts.mctsController import MCTSController

def main():
    for i in range(50):  # Running 50 separate searches of size 50 000 each I got a crash 42/50 times. Might want to tune exploration biases? 
        MCTS = MCTSController(2.0)
        bestState = MCTS.loop()
    SBC = SimpleBoatController(bestState)
    SBC.plot()

if __name__ == "__main__":
    main()
