from pyomo.environ import *
import pandas as pd
import matplotlib.pyplot as plt
from pyomo.contrib.iis import write_iis
import numpy as np
import param


class OptimalReserveCapacity():
    def __init__(T, scenarios:list[list[float]]):
        self.model = ConcreteModel()
        self.T = T
        self.scenarios = scenarios
        self.nb_scenarios = len(scenarios)

    def indexes():
        self.model.scenarios = RangeSet(0, self.nb_scenarios-1)
        self.model.hours = RangeSet(0, self.T-1) # 1 to T
        
        
    def parameters():
        self.model.F_up = Param(self.modeel.scenarios, )

    def variables():
        self.model.c_up = Var(bounds=())


    def constraints():

    def objective_function():

    def solve_model():


class CVaR(OptimalReserveCapacity):
    def __init__():
        super.__init__()
    
    def indexes():
        super.indexes()
    
    def parameters():
        super.parameters()
    
    def variables():
        super.variables()


class AlsoX(OptimalReserveCapacity):
    def __init__():
        super.__init__()
    
    def indexes():
        super.indexes()
    
    def variables(self):
        super().variables()
        
    
    
        