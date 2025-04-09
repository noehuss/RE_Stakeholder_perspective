from offering_strategy import OnePriceScheme, TwoPricesScheme
import pandas as pd
from data.data_creation import scenario_generator
import matplotlib.pyplot as plt

df_scenario = scenario_generator()

P_nom = 500
nb_hours = 24

OnePrice = OnePriceScheme(T=nb_hours, scenarios=df_scenario[0:200], Pnom=P_nom)
profit_one_price = OnePrice.get_profit_distribution()
OnePrice.model.p_DA.pprint()
OP_Average_profit = OnePrice.get_average_profit()


TwoPrice = TwoPricesScheme(T=nb_hours, scenarios=df_scenario[0:200], Pnom=P_nom)
profit_two_price = TwoPrice.get_profit_distribution()
TwoPrice.model.p_DA.pprint()
TP_Average_profit = TwoPrice.get_average_profit()

# Plot one price and two price comulative distribution profit
plt.hist(cumulative=True, x=profit_one_price["Expected profit"], density=True, bins=100, alpha=0.5, label='One price')
plt.hist(cumulative=True, x=profit_two_price["Expected profit"], density=True, bins=100, alpha=0.5, label='Two prices')
plt.axvline(OP_Average_profit, color='blue', linestyle='--')
plt.axvline(TP_Average_profit, color='orange', linestyle='--')
plt.legend()
plt.show()