# Simple test for using MCTS for finding failure stats in simulator

Based on the work done by Lee, Ritchie et al. in "Adaptive Stress Testing: Finding Likely Failure Events with Reinforcement Learning". Used as a proof of concept before doing adaptive stresstesting of more advanced agents and simulators.

Simulator is dumb boat going in straight line, while disturbance is steerable boat trying to crash in to the streerable boat. The boats opperate in a 100x100 world with a steplength of 5.

The MCTS has no knowledge of the workings of the sim-world, and can only pass in a random action-seed and is returned a set of variables to estimate the reward of the cvrrent state of the sim-world.

## MCTS

The monte carlo tree search is quite simple, where one loop searches down through the tree, finds a leaf node and does a single rollout from that node. This project is based on pseudocode on page 13 in Lee, Ritchie et al., "Adaptive Stress Testing: Finding Likely Failure Events with Reinforcement Learning"

## TODOs

* Check if doing multiple rollouts might enhance search speed. Right now the tree is expanded with one node (almost) every simulation, and the search time through the tree drastically increases after a fiew thousand nodes are created. By doing multiple rollouts (which does not add nodes to the tree) the estimated rewards of the existing nodes should be stronger.
* Greedy Grafting: Go through tree gready and find the two nodes with the highest drop in Q. Try to remove this node from the tree, and connecting it back up together, leaving the tree one node shorter. Would need to re-evaluate everything in that path. Do multiple rollouts from new leafnode trying to find a better endstate.
* Evolutionary search through best results: By useing the state, which is a list of seed-actions, as chromosomes in a evolutionary maximation problem some final optimation might be done to further the score of the results. A obvious drawback of MCTS on a continous action space is that small tweaks later on in the search is hard as progressive widening and the tree structure of the search space hinders tweaking in early states. Might not be a problem as a lot of early states has been searched through, but i feel that there might be some potential here.
* Probably a bad idea, but one migt want to assumne that states following each other are not higly correlated and that nodes could be collapsed, removing an action resulting in a new set of states after the removal. This might speed up the search time, but probably not as most scores needs to be recalculated.

## Results and effectivity of the model

Useing 

### Figures
----

![Image of a generated, most likely crash path](figs/crashPath.png?raw=true "Crash Path")

An example of a generated, most likely crash path. Steerable boat starts at x=17, y=0. Connected dots are positions in same time step, colors indicate distances between boats.

----

![Image of a route with random seed actions](figs/randomPath.png?raw=true "Random path")

An example of a random path withouhg useing MCTS. Through testing over 500,000 random paths was generated of which none resulted in a crash.

----

![Reward over time](figs/scoreOverTime.png?raw=true "Reward over time")

An example of the score of each simulation as it develops over time. First crash is found after 717 simulations.
