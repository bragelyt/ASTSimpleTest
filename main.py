from sim.simpleBoatController import SimpleBoatController
import math
import random

def main():
    env = SimpleBoatController()
    actions= [-1, 0, 1]
    i = 0
    while not env.is_endstate():
        env.execute_action(random.choice(actions))
        i += 1
    print("Ended in carsh? ", env.collision_happened)
    print("Nr of states:   ", i)
    env.plot_routes()

if __name__ == "__main__":
    main()
