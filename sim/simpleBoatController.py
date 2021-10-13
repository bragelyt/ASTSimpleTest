import math, json, copy

import matplotlib.pyplot as plt

class SimpleBoatController:

    def __init__(self, state = None) -> None:
        with open("parameters.json") as f:
            params = json.load(f)
        self.steplength = params["steplength"]
        self.crash_distance_threshold = params["crash_distance_threshold"]
        self.actionRange = params["actionSpan"]
        self.state = state
        self.reset_state()
    
    def execute_action(self, action: int):  # Action should be in range [0,1]
        totalRange = self.actionRange[1]- self.actionRange[0]
        scaledAction = totalRange*action + self.actionRange[0]
        self.steerable_angle += scaledAction*math.pi/100
        self.action_trace.append(action)
        self.next_state()

    def next_state(self):
        self.steerable_pos[0] += math.sin(self.steerable_angle)*self.steplength
        self.steerable_pos[1] += math.cos(self.steerable_angle)*self.steplength
        self.straight_pos[0] += self.steplength

    def is_endstate(self):
        if self.sim_in_endstate != True:
            if self.boat_distance(self.steerable_pos, self.straight_pos) < self.crash_distance_threshold:
                self.collision_happened = True
                self.sim_in_endstate = True
            elif self.straight_pos[0] > 100:
                self.sim_in_endstate = True
        return self.sim_in_endstate
    
    def boat_distance(self, pos1, pos2):
        return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

    def update_closest_distance(self):
        # TODO: Update shortest distance for reward.
        pass

    def get_reward(self):
        # If state is terminal and was crash -> R_E  # Crash reward (a lot)
        # If terminal but no crash -> -d  # TODO: Closest position throughout?
        # Otherwise -> log(p(x|s))  # TODO: Prob of disturbance given current state (Implement difference from last action)
        pass
    
    def reset_state(self):  
        if self.state is not None:  # If rollout sim, resetting wil only reset to rollout point
            self.straight_pos = self.state["straight_pos"]   # All theese should go. Take in actions and fast forward from start
            self.steerable_pos = self.state["steerable_pos"]
            self.steerable_angle = self.state["steerable_angle"]
            self.action_trace = self.state["action_trace"]
            # self.prev_steerable_state = self.state["prev_steerable_state"]
            # self.prev_straight_state = self.state["prev_straight_state"]
            # self.prev_action = self.state["prev_action"]
        else:  # If main sim, resetting wil completly rolle back simulation to start anew.
            self.straight_pos = [0,50]
            self.steerable_pos = [30,0]
            self.steerable_angle = 0
            self.action_trace = []
            # self.prev_steerable_state = [[], []]  # x, y, action
            # self.prev_straight_state = [[], []]
            # self.prev_action = None
        self.collision_happened = False
        self.sim_in_endstate = False

    def transition_probability(self, action):
        if self.action_trace == None:
            self.transition_probability = 1
        else:
            self.transition_probability = abs(action - self.action_trace[-1])  # TODO: Check if this is correct

    def get_sim_state(self):
        return self.action_trace
    
    def get_position_trace(self):  # Prev pos is not stored, so sim is reset, and fast forwarded through
        action_trace = self.action_trace
        self.reset_state()
        steerable_state = [[],[]]
        straight_state = [[], []]
        for action in action_trace:
            steerable_state[0].append(self.steerable_pos[0])
            steerable_state[1].append(self.steerable_pos[1])
            straight_state[0].append(self.straight_pos[0])
            straight_state[1].append(self.straight_pos[1])
            self.execute_action(action)
        return steerable_state, straight_state

    def plot_routes(self):
        steerable_pos_trace, straight_pos_trace = self.get_position_trace()
        cdt = self.crash_distance_threshold
        colors = {8*cdt: "gray", 4*cdt: "yellow", 2*cdt: "red", cdt: "black"}
        for i in range(len(steerable_pos_trace[0])):
            steerable_pos = [steerable_pos_trace[0][i], steerable_pos_trace[1][i]]
            straight_pos = [straight_pos_trace[0][i], straight_pos_trace[1][i]]
            distance = self.boat_distance(steerable_pos, straight_pos)
            color = "blue"
            for key, _color in colors.items():
                if distance > key:
                    color = _color
                    break
            plt.plot([steerable_pos[0], straight_pos[0]], [steerable_pos[1], straight_pos[1]], c = "#F0F0F0", zorder=0)
            plt.scatter(steerable_pos[0], steerable_pos[1], c = color, zorder=10)
            plt.scatter(straight_pos[0], straight_pos[1], c = color, zorder=10)
        plt.ylim(0, 100)
        plt.xlim(0, 100)
        plt.show()
