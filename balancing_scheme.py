from offering_strategy import OnePriceScheme, TwoPriceScheme
import pandas as pd
from data.data_creation import scenario_generator
import matplotlib.pyplot as plt
import param

df_scenario = scenario_generator()

P_nom = 500
nb_hours = 24

OnePrice = OnePriceScheme(T=nb_hours, scenarios=df_scenario[0:200], Pnom=P_nom)
profit_one_price = OnePrice.get_profit_distribution(plot=False, color=param.colors[1])
#OnePrice.system_condition_distribution()
OP_Average_profit = OnePrice.get_average_profit()

TwoPrice = TwoPriceScheme(T=nb_hours, scenarios=df_scenario[0:200], Pnom=P_nom)
profit_two_price = TwoPrice.get_profit_distribution(plot=False, color=param.colors[2])
TP_Average_profit = TwoPrice.get_average_profit()

# Plot one price and two price comulative distribution profit
# plt.hist(cumulative=True, x=profit_one_price["Expected profit"], density=True, bins=100, alpha=0.5, label='One-price', color=param.colors[1])
# plt.hist(cumulative=True, x=profit_two_price["Expected profit"], density=True, bins=100, alpha=0.5, label='Two-price', color=param.colors[2])
# plt.axvline(OP_Average_profit, color=param.colors[1], linestyle='--')
# plt.axvline(TP_Average_profit, color=param.colors[2], linestyle='--')
# plt.legend()
# plt.show()

#OnePrice.model.p_DA.pprint()
print(f"One-price expected profit: {OP_Average_profit}")
print(OnePrice.execution_time)
print("------------------------------------------------")
#TwoPrice.model.p_DA.pprint()
print(f"Two-price expected profit: {TP_Average_profit}")
print(TwoPrice.execution_time)