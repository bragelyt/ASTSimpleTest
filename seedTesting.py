import gym.utils.seeding as seeding

import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt

seeds = []
maxBytes = 4

for i in range(109):
    newSeed = seeding.create_seed(max_bytes=maxBytes) 
    print(f'Seed:   {newSeed}')
    scaledSeed = newSeed/2**(maxBytes*8)
    seeds.append(scaledSeed)

sn.histplot(data=seeds, bins=40)
print(max(seeds))

plt.show()