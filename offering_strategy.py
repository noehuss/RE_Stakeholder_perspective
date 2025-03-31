from pyomo.environ import *
import pandas as pd

class OfferingStrategy():
    def __init__(self, T:int,  scenarios:pd.DataFrame, Pnom:int):
        self.model = ConcreteModel()
        self.T = T
        self.scenarios = scenarios
        self.Pnom = Pnom
        self.nb_scenarios = len(scenarios)

    def indexes(self):
        self.model.hours = RangeSet(self.T) # 1 to T
        self.model.scenarios = RangeSet(self.nb_scenarios)

    def parameters(self):
        self.model.price = Param(self.model.scenarios, self.model.hours, initialize= lambda model, s, h: self.scenarios.loc[s, "Price"][h-1])
        self.model.wind = Param(self.model.scenarios, self.model.hours, initialize= lambda model, s, h: self.scenarios.loc[s, "Wind"][h-1])
        self.model.sys_condition = Param(self.model.scenarios, self.model.hours, initialize= lambda model, s, h: self.scenarios.loc[s, "System condition"][h-1])

    def variables(self):
        self.model.p_DA = Var(self.model.hours, bounds = (0, self.Pnom))
        self.model.delta_up = Var(self.model.scenarios, self.model.hours, domain = NonNegativeReals)
        self.model.delta_down = Var(self.model.scenarios, self.model.hours, domain = NonNegativeReals)
        self.model.delta = Var(self.model.scenarios, self.model.hours, domain = Reals)
    
    def constraints(self):
        def equality_delta (model, s , h):
            return model.delta[(s,h)] == model.delta_up[(s,h)] - model.delta_down[(s,h)]
        self.model.def_delta = Constraint (self.model.scenarios, self.model.hours, rule = equality_delta)
        def rule_imbalance(model, s, h):
            return model.delta[(s,h)] == model.wind[(s,h)]*self.Pnom - model.p_DA[h]
        self.model.imbalance = Constraint (self.model.scenarios, self.model.hours, rule = rule_imbalance) 

    def objective_function(self):
        pass

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
    

class OnePriceScheme(OfferingStrategy):
    def objective_function(self):
        self.model.objective = Objective(expr = sum(sum(self.model.price[(s,t)]*self.model.p_DA[(s,t)]
                                                        +self.model.price[(s,t)]*
                                                        (0.85*self.model.delta_up[(s,t)]
                                                        -1.25*self.model.delta_down[(s,t)])
                                                        ) for s in self.model.scenarios for t in self.model.hours), 
                                        sense=maximize)

# class TwoPricesScheme(OfferingStrategy):
#         def objective_function(self):
#             self.model.objective = Objective(expr = sum(sum(self.model.price[(s,t)]*self.model.p_DA[(s,t)]
#                                                         +self.model.price[(s,t)]*
#                                                         (0.85*self.model.delta_up[(s,t)]
#                                                         -1.25*self.model.delta_down[(s,t)])
#                                                         ) for s in self.model.scenarios for t in self.model.hours), 
#                                         sense=maximize)