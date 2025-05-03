import random as rd
import numpy as np
import pandas as pd

minutes =  [i for i in range(0,60)]

loads = [ [rd.randint(220,600)] for i in range(300)]

print(minutes)

for i in range(1,59):
    for k in range(300):
        print(max(220-loads[k][i-1],-35))
        print(min(600-loads[k][i-1],35))
        random = rd.randint(max(220-loads[k][i-1],-35),min(600-loads[k][i-1],35))
        loads[k].append(random)

print(len(loads))
print(len(loads[1]))
print(loads[1])

