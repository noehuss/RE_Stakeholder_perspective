from offering_strategy import TwoPricesScheme
import pandas as pd
from data_creation import scenario_generator
from pyomo.environ import *

df_scenario = scenario_generator()

test = TwoPricesScheme(24, scenarios=df_scenario[0:200], Pnom=500)
test.solve_model()
test.get_profit_distribution()
test.model.p_DA.pprint()