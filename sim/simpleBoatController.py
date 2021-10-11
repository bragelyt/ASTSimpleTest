import math
import matplotlib.pyplot as plt

class SimpleBoatController:

    def __init__(self) -> None:
        self.steerable_pos = [30,0]
        self.straight_pos = [0,50]
        self.prev_steerable_state = [[], []]
        self.prev_straight_state = [[], []]
        self.angle = 0
        self.steplength = 1
        self.crash_distance_threshold = 2
        self.collision_happened = False
    
    def execute_action(self, action: int = 0):
        if action != 0:
            self.angle += action*math.pi/100
        self.next_state()

    def next_state(self):
        self.add_to_prev_state()
        self.steerable_pos[0] += math.sin(self.angle)*self.steplength
        self.steerable_pos[1] += math.cos(self.angle)*self.steplength
        self.straight_pos[0] += self.steplength

    def is_endstate(self):
        # print(math.sqrt((self.straight_pos[0]-self.steerable_pos[0])**2 + (self.straight_pos[1]-self.steerable_pos[1])**2))
        if self.boat_distance(self.steerable_pos, self.straight_pos) < self.crash_distance_threshold:
            self.collision_happened = True
            self.add_to_prev_state()
            return True
        elif self.straight_pos[0] == 100:
            self.add_to_prev_state()
            return True
        return False
    
    def boat_distance(self, pos1, pos2):
        return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

    def update_closest_distance(self):
        # TODO: Update shortest distance for reward.
        pass

    def get_reward(self):
        # If state is terminal and was crash -> R_E
        # If terminal but no crash -> -d
        # Otherwise -> log(p(x|s))
        pass

    def add_to_prev_state(self):
        self.prev_steerable_state[0].append(self.steerable_pos[0])
        self.prev_steerable_state[1].append(self.steerable_pos[1])
        self.prev_straight_state[0].append(self.straight_pos[0])
        self.prev_straight_state[1].append(self.straight_pos[1])

    def plot_routes(self):
        colors = {20: "gray", 10: "yellow", 5: "red", 2: "black"}
        for i in range(len(self.prev_steerable_state[0])):
            steerable_pos = [self.prev_steerable_state[0][i], self.prev_steerable_state[1][i]]
            straight_pos = [self.prev_straight_state[0][i], self.prev_straight_state[1][i]]
            distance = self.boat_distance(steerable_pos, straight_pos)
            color = "blue"
            for key, _color in colors.items():
                if distance > key:
                    color = _color
                    break
            plt.scatter(steerable_pos[0], steerable_pos[1], c = color)
            plt.scatter(straight_pos[0], straight_pos[1], c = color)
        # plt.scatter(self.prev_steerable_state[0],self.prev_steerable_state[1], c="red")
        # plt.scatter(self.prev_straight_state[0],self.prev_straight_state[1])
        plt.ylim(0, 100)
        plt.xlim(0, 100)
        plt.show()