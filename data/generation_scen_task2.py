import random as rd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_scenarios() -> list[list[float]]:
    rd.seed(0)
    minutes =  [i for i in range(0,60)]
    loads = [ [rd.randint(220,600)] for i in range(300)]
    for k in range(300):
        for i in range(1,60):
            random = rd.randint(max(220-loads[k][i-1],-35),min(600-loads[k][i-1],35))
            loads[k].append(loads[k][i-1]+random)
    return loads

def plot_distrib(loads_list):
    distrib = []
    for loads in loads_list:
        distrib += loads
    #print(distrib)
    #calculate deciles of data
    decile = np.percentile(distrib, np.arange(0, 100, 10))

    plt.axvline(264, color = 'red', linestyle = '--', label = 'ALSO-X')
    plt.axvline(244.8833, color = 'blue', linestyle = '--', label = 'CVaR')
    plt.axvline(decile[1], color = 'orange', linestyle = '--', label = 'First decile')
    plt.hist(distrib, bins=50, density=True)
    plt.xlabel('Load (MW)')
    plt.ylabel('Probability density')
    plt.legend()
    plt.show()

#plot_distrib(generate_scenarios()[:100])
