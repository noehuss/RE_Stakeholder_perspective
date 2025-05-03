import random as rd
import numpy as np
import pandas as pd

minutes =  [i for i in range(0,60)]

loads = [ [rd.randint(220,600)] for i in range(300)]


for k in range(1):
    for i in range(1,60):
        random = rd.randint(max(220-loads[k][i-1],-35),min(600-loads[k][i-1],35))
        loads[k].append(loads[k][i-1]+random)

print(len(loads))
print(len(loads[0]))
print(loads[0])

