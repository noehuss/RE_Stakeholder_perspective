from offering_strategy import OnePriceScheme, TwoPricesScheme
import pandas as pd
from data.data_creation import scenario_generator
import matplotlib.pyplot as plt

df_scenario = scenario_generator()

P_nom = 500
nb_hours = 24

OnePrice = OnePriceScheme(T=nb_hours, scenarios=df_scenario[0:200], Pnom=P_nom)
OnePrice.solve_model()
profit_one_price = OnePrice.get_profit_distribution()
OnePrice.model.p_DA.pprint()

TwoPrice = TwoPricesScheme(T=nb_hours, scenarios=df_scenario[0:200], Pnom=P_nom)
TwoPrice.solve_model()
profit_two_price = TwoPrice.get_profit_distribution()
TwoPrice.model.p_DA.pprint()

# Plot one price and two price comulative distribution profit
plt.hist(cumulative=True, x=profit_one_price[0], density=True, bins=100, alpha=0.5, label='One price')
plt.hist(cumulative=True, x=profit_two_price[0], density=True, bins=100, alpha=0.5, label='Two prices')
plt.legend()
plt.show()