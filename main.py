import random, json

from sim.simpleBoatController import SimpleBoatController
from ast.mcts.mctsController import MCTSController

def main():
    env = SimpleBoatController()
    j = 0
    crash = False
    while not crash:  # Force crash. Might want to find statistics for brute force
        i = 0
        env.reset_state()
        while not env.is_endstate():
            env.execute_action(random.random())
            i += 1
        crash = env.collision_happened
        j += 1
    print("Ended in carsh? ", env.collision_happened)
    print("Nr of states:   ", i, " ", j)
    env.plot_routes()

if __name__ == "__main__":
    main()
