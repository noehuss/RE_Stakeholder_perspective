from pyomo.environ import *
import pandas as pd
import matplotlib.pyplot as plt
from pyomo.contrib.iis import write_iis
import numpy as np
import param
import data.generation_scen_task2 as g
# setting font size
plt.rcParams.update({'font.size': param.fontsize})

class OptimalReserveCapacity():
    def __init__(self, scenarios:list[list[float]],T=24, P=0.9):
        """
        scenarios: list[list[float]] \n
        T: number of hours, default: T=24 \n
        P: P requirement, default: P90, P=0.9 \n
        """
        self.model = ConcreteModel()
        self.T = T
        self.scenarios = scenarios
        self.nb_scenarios = len(scenarios)
        self.P = P

    def indexes(self):
        self.model.scenarios = RangeSet(0, self.nb_scenarios-1)
        self.model.hours = RangeSet(0, self.T-1) # 1 to T
        
    def parameters(self):
        self.model.F_up = Param(self.model.scenarios, self.model.hours, initialize= lambda model, s, h: self.scenarios[s][h], name="F_up" )

    def variables(self):
        self.model.c_up = Var(within=NonNegativeReals)

    def constraints(self):
        pass 

    def objective_function(self):
        self.model.objective = Objective(expr = self.model.c_up, sense = maximize)

    def solve_model(self):
        self.indexes()
        self.parameters()
        self.variables()
        self.constraints()
        self.objective_function()
        # Dual
        self.model.dual = Suffix(direction=Suffix.IMPORT)
        # Create a solver
        solver = SolverFactory("gurobi", solver_io="python")  # Make sure Gurobi is installed and properly configured
        # Solve the model
        solution = solver.solve(self.model, tee=True)
        #self.model.write("model.lp")

    def return_c_up(self):
        return value(self.model.c_up)
    

class CVaR(OptimalReserveCapacity):    
    def variables(self):
        super().variables()
        self.model.y = Var(self.model.scenarios, self.model.hours, bounds=(0,1))
        self.model.beta = Var(within = NegativeReals)
        self.model.zeta = Var(self.model.scenarios, self.model.hours, within = Reals)
        
    def constraints(self):
        def rule_c_up(model, s, h):
            return model.c_up - model.F_up[s,h] <= model.zeta[s,h]  
        self.model.constraint_c_up = Constraint(self.model.scenarios, self.model.hours, rule = rule_c_up)      
        
        def rule_zeta(model, s,h):
            return model.beta <= model.zeta[s,h]
        self.model.constraint_zeta = Constraint(self.model.scenarios, self.model.hours, rule = rule_zeta) 
        
        def rule(model):
            return (sum(sum(model.zeta[s,h] for s in self.model.scenarios) for h in self.model.hours))/(self.T*self.nb_scenarios)<=self.model.beta*self.P
        self.model.constraint = Constraint(rule = rule)


class AlsoX(OptimalReserveCapacity):
    def __init__(self, scenarios, T=24, P=0.9):
        super().__init__(scenarios, T, P)
        self.M = 1000
        self.q = (1-self.P)*self.nb_scenarios*self.T

    def variables(self):
        super().variables()
        self.model.y = Var(self.model.scenarios, self.model.hours, within = Binary)
        
    def constraints(self):
        def rule_c_up(model, s, h):
                return model.c_up - model.F_up[s,h] <= self.model.y[s, h]*self.M
        self.model.constraint_c_up = Constraint(self.model.scenarios, self.model.hours, rule=rule_c_up) 
        
        def rule_q(model):
            return  sum(sum(self.model.y[s,h]for s in self.model.scenarios) for h in self.model.hours)<= self.q
        self.model.constraint_q = Constraint(rule=rule_q)


def plot_freq_overbid(c_up, scenarios):
    freq = []
    for scenario in scenarios:
        count_overbid = sum([1 for i in scenario if i < c_up])
        freq.append(100*count_overbid/len(scenario))
    ax = plt.subplot()
    ax.hist(freq, density=False, bins=61, color=param.colors[0], align='mid')
    print(sorted(freq))
    ax.axvline(10, linestyle='--', color=param.colors[1], label='P90 requirement (10%)')
    ax.axvline(np.mean(freq), linestyle='--', color=param.colors[2], label=f'mean = {np.mean(freq):.2f} %')
    ax.set(xlabel='Frequency of overbid (%)', ylabel='Count of scenarios')
    bbox = dict(boxstyle='round', fc=param.colors[2], ec=param.colors[2], alpha=0.5)
    ax.text(0.95, 0.07, f'Bid: {c_up:.2f} kW', fontsize=16, bbox=bbox,
            transform=ax.transAxes, horizontalalignment='right')
    ax.grid(linestyle='--', linewidth=0.4)
    ax.legend()
    plt.show()



scenarios = g.generate_scenarios()        

alsoX = AlsoX(scenarios=scenarios[:100])
alsoX.solve_model()

cvar = CVaR(scenarios=scenarios[:100])
cvar.solve_model()

print(alsoX.return_c_up())        
print(cvar.return_c_up())

plot_freq_overbid(alsoX.return_c_up(), scenarios[:100])
plot_freq_overbid(alsoX.return_c_up(), scenarios[100:300])
plot_freq_overbid(cvar.return_c_up(), scenarios[:100])
plot_freq_overbid(cvar.return_c_up(), scenarios[100:300])