from offering_strategy import OnePriceScheme
import pandas as pd
from data_creation import scenario_generator

df_scenario = scenario_generator()

test = OnePriceScheme(24, scenarios=df_scenario[0:200], Pnom=200)
test.solve_model()
test.model.p_DA.pprint()
print(test.get_profit_distribution())