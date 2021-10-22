import math, json, copy

import matplotlib.pyplot as plt

class SimpleBoatController:

    def __init__(self, state = None) -> None:
        with open("parameters.json") as f:
            params = json.load(f)
        self.steplength = params["steplength"]
        self.crash_distance_threshold = params["crash_distance_threshold"]
        self.action_range = params["action_range"]
        self.reset_state()
        if state is not None:
            self.fast_forward(state)
    
    def execute_action(self, action: float):  # Action should be in range [0,1]
        p = self.get_transition_probability(action)
        totalRange = self.action_range[1] - self.action_range[0]
        scaledAction = totalRange*action + self.action_range[0]
        self.steerable_angle += scaledAction*math.pi/100
        self.next_state()
        self.action_trace.append(action)
        self.is_endstate()
        e = self.collision_happened  # TODO: crashed?
        d = self.closest_boat_distance
        return(p, e, d)

    def next_state(self):
        self.steerable_pos[0] += math.sin(self.steerable_angle)*self.steplength
        self.steerable_pos[1] += math.cos(self.steerable_angle)*self.steplength
        self.straight_pos[0] += self.steplength
        self.update_closest_distance()

    def is_endstate(self):
        if self.sim_in_endstate != True:
            if self.get_current_distance() < self.crash_distance_threshold:
                self.collision_happened = True
                self.sim_in_endstate = True
            elif self.straight_pos[0] > 100:
                self.sim_in_endstate = True
        return self.sim_in_endstate
    
    def get_current_distance(self):  # TODO: Run after next_state and store value?
        return self.boat_distance(self.steerable_pos, self.straight_pos)

    def boat_distance(self, pos1, pos2):
        return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

    def update_closest_distance(self):
        distance = self.get_current_distance()
        if distance < self.closest_boat_distance:
            self.closest_boat_distance = distance
    
    def reset_state(self):  
        self.straight_pos = [0,50]
        self.steerable_pos = [30,0]
        self.steerable_angle = 0
        self.action_trace = []
        self.collision_happened = False
        self.sim_in_endstate = False
        self.closest_boat_distance = self.get_current_distance()

    def fast_forward(self, state):
        for action in state:
            self.execute_action(action)

    def get_transition_probability(self, action):
        if len(self.action_trace) == 0:
            return 1
        else:
            return abs(action - self.action_trace[-1])  # TODO: Check if this is correct

    def get_sim_state(self):
        return self.action_trace

    def plot_routes(self):
        steerable_pos_trace, straight_pos_trace = self.get_position_trace()
        cdt = self.crash_distance_threshold
        colors = {8*cdt: "gray", 4*cdt: "yellow", 2*cdt: "red", cdt: "black"}
        for i in range(len(steerable_pos_trace)):
            steerable_pos = steerable_pos_trace[i]
            straight_pos = straight_pos_trace[i]
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

    def get_position_trace(self):  # Prev pos is not stored, so sim is reset, and fast forwarded through
        action_trace = self.action_trace
        self.reset_state()
        steerable_state = []
        straight_state = []
        for action in action_trace:
            steerable_state.append(copy.copy(self.steerable_pos))
            straight_state.append(copy.copy(self.straight_pos))
            self.execute_action(action)
        steerable_state.append(copy.copy(self.steerable_pos))
        straight_state.append(copy.copy(self.straight_pos))
        return steerable_state, straight_state
