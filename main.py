import random, json

from sim.simpleBoatController import SimpleBoatController
from ast.mcts.mctsController import MCTSController

def main():
    env = SimpleBoatController()
    i = 0
    while not env.is_endstate():
        env.execute_action(random.random())
        i += 1
    print("Ended in carsh? ", env.collision_happened)
    print("Nr of states:   ", i)
    env.plot_routes()

if __name__ == "__main__":
    main()
