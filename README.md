# Simple test for using MCTS for finding failure stats in simulator

Based on the work done by Lee, Ritchie et al. in "Adaptive Stress Testing: Finding Likely Failure Events with Reinforcement Learning"

Simulator is dumb boat going in straight line, while disturbance is steerable boat.

Goal for MCTS is to crash the steerable boat into a boat goint straight. The boats opperate in a 100x100 world with a steplength of 5.

## MCTS

The monte carlo tree search is quite simple, where one loop searches down through the tree, finds a leaf node and does a single rollout from that node. Based on pseudocode on page 13 in Lee, Ritchie et al., "Adaptive Stress Testing: Finding Likely Failure Events with Reinforcement Learning"

## TODOs

* Check if doing multiple rollouts might
* Probably a bad idea, but one migt want to assumne that states are not correlated and that nodes could be collapsed, removing an action resulting in a new set of states after the removal. This might speed up the search time, but probably not as most scores needs to be recalculated.
* Greedy Grafting: Go through tree gready and find the two nodes with the highest drop in Q. Try to remove this node from the tree, and connecting it back up together, leaving the tree one node shorter. Would need to re-evaluate everything in that path. Do multiple rollouts from new leafnode trying to find a better endstate.
