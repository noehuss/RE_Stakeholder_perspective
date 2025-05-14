from pyomo.environ import *
import pandas as pd
import matplotlib.pyplot as plt
from pyomo.contrib.iis import write_iis
import numpy as np
import param
import time
# setting font size
plt.rcParams.update({'font.size': param.fontsize})

# This file contains all models used in step 1: 
# - OnePriceScheme
# - OnePriceSchemeRisk
# - TwoPrice
# - TwoPriceSchemeRisk

class OfferingStrategy():
    def __init__(self, T:int,  scenarios:pd.DataFrame, Pnom:int):
        self.model = ConcreteModel()
        self.T = T
        self.scenarios = scenarios
        self.Pnom = Pnom
        self.nb_scenarios = len(scenarios)
        start = time.time()
        self.solve_model()
        self.execution_time = time.time() - start 

    def indexes(self):
        self.model.hours = RangeSet(0, self.T-1) # 1 to T
        self.model.scenarios = Set(initialize=self.scenarios.index)

    def parameters(self):
        self.model.price = Param(self.model.scenarios, self.model.hours, within=Reals, initialize= lambda model, s, h: self.scenarios.loc[s,"Price"][h], name="price")
        self.model.wind = Param(self.model.scenarios, self.model.hours, within=Reals, initialize= lambda model, s, h: self.scenarios.loc[s,"Wind"][h], name="cf")
        self.model.sys_condition = Param(self.model.scenarios, self.model.hours, within=Reals, initialize= lambda model, s, h: self.scenarios.loc[s, "System condition"][h])

    def variables(self):
        self.model.p_DA = Var(self.model.hours, bounds = (0, self.Pnom), name="pDA")
        self.model.delta = Var(self.model.scenarios, self.model.hours, domain = Reals, name="Delta")
    
    def constraints(self):
        def rule_imbalance(model, s, h):
            return model.delta[(s,h)] == model.wind[(s,h)]*self.Pnom - model.p_DA[h]
        self.model.imbalance = Constraint (self.model.scenarios, self.model.hours, rule = rule_imbalance) 

    def _profit(self, s:int, t:int):
        pass

    def objective_function(self):
        self.model.objective = Objective(expr = (1/self.nb_scenarios)*sum(sum( self._profit(s,t)
                                                         for s in self.model.scenarios ) for t in self.model.hours), 
                                        sense=maximize)
        
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

    def get_profit_distribution(self, plot:bool=False, color:str=None) -> pd.DataFrame:
        profit = pd.DataFrame(index=self.model.scenarios, columns=["Expected profit"])
        for s in self.model.scenarios:
            hourly_profit = []
            for t in self.model.hours:
                hourly_profit.append(value(self._profit(s,t)))
            profit.loc[s, "Expected profit"] = sum(hourly_profit)/1000 #k€

        if plot:
            plt.hist(cumulative=True, x=profit["Expected profit"], density=True, bins=100, alpha=0.5, label='Profit distribution', color=color)
            plt.axvline(self.get_average_profit(), color=color, linestyle='--', label=f'Expected profit: {self.get_average_profit():.0f} k€')
            plt.xlabel("Profit (k€)")
            plt.ylabel("Probability")
            plt.grid(linestyle='--', linewidth=0.4)
            plt.legend()
            plt.show()
        return profit
    
    def get_average_profit(self):
        return value(self.model.objective)/1000 #k€

    def get_p_DA(self):
        return [value(self.model.p_DA[t]) for t in self.model.hours]
    
    def system_condition_distribution(self):
        sys_cond = [np.mean([value(self.model.sys_condition[(s, t)]) for s in self.model.scenarios]) for t in self.model.hours]
        full_bid = np.multiply(1.25, sys_cond)
        zero_bid = np.multiply(0.85, np.subtract(1, sys_cond))
        diff_bid = np.subtract(full_bid, zero_bid)

        p_DA = self.get_p_DA()
        print(p_DA)
        time = [t for t in self.model.hours]
        print(time)
        fig, ax1 = plt.subplots()

        ax2 = ax1.twinx()
        ax1.step(x=time, y=p_DA, color=param.colors[1], where='post')
        ax2.step(x=time, y=diff_bid, color=param.colors[2], where='post')
        ax1.set_xlabel('Hours')
        ax1.set_ylabel('Production offered', color=param.colors[1])
        ax2.set_ylabel('System status ', color=param.colors[2])
        ax1.set_ylim((-10,510))
        ax2.set_ylim((-1,1))
        ax2.axhline(0, color=param.colors[2], linestyle='--')
        plt.show()

class OfferingStrategyRisk(OfferingStrategy):
    def __init__(self, T, scenarios, Pnom, beta, alpha):
        self.beta = beta
        self.alpha = alpha
        super().__init__(T, scenarios, Pnom)
        print(self)

    def variables(self):
        super().variables()
        self.model.VaR = Var(domain = Reals, name = 'VaR')
        self.model.eta = Var(self.model.scenarios, domain = NonNegativeReals, name = 'eta')

    def constraints(self):
        super().constraints()
        def inequality_eta (model, s):
            return model.eta[s] >= model.VaR - sum(self._profit(s,t) for t in model.hours)
        self.model.constraint_eta = Constraint(self.model.scenarios, rule = inequality_eta)

    def objective_function(self):
        self.model.objective = Objective(expr = ((1-self.beta)*(1/self.nb_scenarios)*sum(sum( self._profit(s,t)
                                                for t in self.model.hours) for s in self.model.scenarios)+
                                                self.beta*(self.model.VaR-(1/(1-self.alpha))*(1/self.nb_scenarios)*sum(self.model.eta[s] for s in self.model.scenarios))), 
                                        sense=maximize)

    def get_expected_profit(self):
        return value((1/self.nb_scenarios)*sum(sum( self._profit(s,t) for s in self.model.scenarios) for t in self.model.hours))

    def get_CVaR(self):
        if self.beta > 0:
            return value(self.model.VaR-(1/(1-self.alpha))*(1/self.nb_scenarios)*sum(self.model.eta[s] for s in self.model.scenarios))
        else:
            profit_list = [value(sum(self._profit(s,t) for t in self.model.hours))  for s in self.model.scenarios]
            first_decile = np.percentile(profit_list, (1-self.alpha)*100)
            return np.mean([profit for profit in profit_list if profit <= first_decile])
    
    def get_VaR(self):
        return value(self.model.VaR)

class OnePriceScheme(OfferingStrategy):
    def _profit(self, s:int, t:int):
        return self.model.price[(s,t)]*(self.model.p_DA[(t)]+self.model.delta[(s,t)]*
                                                        (0.85*(1-self.model.sys_condition[(s,t)])
                                                        +1.25*self.model.sys_condition[(s,t)]))

class OnePriceSchemeRisk(OfferingStrategyRisk):
    def _profit(self, s:int, t:int):
        return self.model.price[(s,t)]*(self.model.p_DA[(t)]+self.model.delta[(s,t)]*
                                                        (0.85*(1-self.model.sys_condition[(s,t)])
                                                        +1.25*self.model.sys_condition[(s,t)]))

class TwoPricesScheme(OfferingStrategy):
    def variables(self):
        super().variables()
        self.model.delta_up = Var(self.model.scenarios, self.model.hours, domain = NonNegativeReals, name="DeltaUp")
        self.model.delta_down = Var(self.model.scenarios, self.model.hours, domain = NonNegativeReals, name="DeltaDown")

    def constraints(self):
        super().constraints()
        def equality_delta (model, s , h):
            return model.delta[(s,h)] == model.delta_up[(s,h)] - model.delta_down[(s,h)]
        self.model.def_delta = Constraint(self.model.scenarios, self.model.hours, rule = equality_delta)

    def _profit(self, s:int , t:int):
        return self.model.price[(s,t)]*(self.model.p_DA[(t)]+
                                        (self.model.sys_condition[(s,t)]*(self.model.delta_up[(s,t)]-1.25*self.model.delta_down[(s,t)])
                                        +(1-self.model.sys_condition[(s,t)])*(0.85*self.model.delta_up[(s,t)]-self.model.delta_down[(s,t)]))) 

class TwoPricesSchemeRisk(OfferingStrategyRisk):
    def variables(self):
        super().variables()
        self.model.delta_up = Var(self.model.scenarios, self.model.hours, domain = NonNegativeReals, name="DeltaUp")
        self.model.delta_down = Var(self.model.scenarios, self.model.hours, domain = NonNegativeReals, name="DeltaDown")

    def constraints(self):
        super().constraints()
        def equality_delta (model, s , h):
            return model.delta[(s,h)] == model.delta_up[(s,h)] - model.delta_down[(s,h)]
        self.model.def_delta = Constraint (self.model.scenarios, self.model.hours, rule = equality_delta)

    def _profit(self, s:int , t:int):
        return self.model.price[(s,t)]*(self.model.p_DA[(t)]+
                                        (self.model.sys_condition[(s,t)]*(self.model.delta_up[(s,t)]-1.25*self.model.delta_down[(s,t)])
                                        +(1-self.model.sys_condition[(s,t)])*(0.85*self.model.delta_up[(s,t)]-self.model.delta_down[(s,t)]))) 