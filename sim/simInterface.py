import json

from typing import List, Tuple

from sim.simpleBoatController import SimpleBoatController


class SimInterface:

    def __init__(self) -> None:  # Initiates simulation at state zero
        self.simWorld = SimpleBoatController()
        with open("parameters.json") as f:
            params = json.load(f)
        action_range = params["action_range"]
        self.totalRange = action_range[1] - action_range[0]
        self.minAction = action_range[0]
        self.actionTrace : List(float) = []
        self.sim_in_endstate : bool = False

    def step(self, actionSeed) -> Tuple:  # return (p, e, d)
        action = actionSeed * self.totalRange + self.minAction
        p, e, d = self.simWorld.execute_action(action)
        self.actionTrace.append(actionSeed)
        self.sim_in_endstate = self.simWorld.is_endstate()
        return(p, e, d)

    def is_terminal(self) -> bool:
        return self.sim_in_endstate
   
    def get_state(self) -> List:
        return(self.actionTrace)
    
    def set_state(self, state : Tuple) -> None:  # return (p, e, d)?
        self.reset_sim()
        state = list(state)
        for actionSeed in state:
            self.step(actionSeed)

    def reset_sim(self) -> None:
        self.actionTrace = []
        self.simWorld.reset_sim()

    def plot(self) -> None:
        self.simWorld.plot()

    # def _rewertToSeed(self, action) -> float:
    #     actionSeed = (action- self.minAction)/self.totalRange
    #     return actionSeed