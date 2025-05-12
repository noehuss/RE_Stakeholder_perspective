import numpy as np
import pandas as pd
from data.data_creation import scenario_generator
from offering_strategy import OnePriceScheme, TwoPricesScheme, OfferingStrategy
import matplotlib.pyplot as plt
import param

def out_sample_analysis(offering_strategy:OfferingStrategy, Pnom, nb_hours, nb_split) -> pd.DataFrame | pd.DataFrame:
  scenario_df = scenario_generator()
  scenario_df = scenario_df.sample(frac=1).reset_index(drop=True)

  average_expected_profit = {}
  p_DA_df = pd.DataFrame()
  key = 1
  for in_sample in np.array_split(scenario_df, nb_split):
    assert len(in_sample) == len(scenario_df) / nb_split
    in_sample = pd.DataFrame(in_sample)
    model = offering_strategy(nb_hours, in_sample, Pnom)
    p_DA = model.get_p_DA()
    out_sample = scenario_df.drop(index=in_sample.index)
    p_DA_df[f"p_DA_{key}"] = p_DA
    # Profit day ahead
    out_sample["DA profit"] = out_sample["Price"].map(lambda x: sum(np.multiply(x, p_DA)))

    # Cost imbalance
    def calc_imbalance(x):
      return np.subtract(np.multiply(x, model.Pnom), p_DA)
    out_sample["Imbalance"] = out_sample["Wind"].map(lambda x: calc_imbalance(x))
    out_sample["Imbalance up"] = out_sample["Imbalance"].map(lambda y: list(map(lambda x: max(x,0),y))) #Two prices
    out_sample["Imbalance down"] = out_sample["Imbalance"].map(lambda y: list(map(lambda x: -min(x,0),y))) #Two prices

    if type(model) is OnePriceScheme:
      for i, row in out_sample.iterrows():
        price = np.multiply(row["Price"], np.add(np.multiply(1.25, row["System condition"]),np.multiply(0.85, np.subtract(1, row["System condition"]))))
        out_sample.loc[i, "Imbalance cost"] = sum(np.multiply(row["Imbalance"], price))
    else:
      for i, row in out_sample.iterrows():
        deficit = np.multiply(row["System condition"], np.subtract(row["Imbalance up"], np.multiply(1.25, row["Imbalance down"])))
        excess = np.multiply(np.subtract(1, row["System condition"]), np.subtract(np.multiply(0.85, row["Imbalance up"]), row["Imbalance down"]))
        imbalance_cost = np.multiply(row["Price"], np.add(deficit, excess)) 
        out_sample.loc[i, "Imbalance cost"] = sum(imbalance_cost)
    
    out_sample["Profit"] = out_sample["DA profit"] + out_sample["Imbalance cost"]

    average_expected_profit[key] = {
      "out_sample" : out_sample["Profit"].mean(),
      "in_sample" : model.get_average_profit()    
    }
    # profit_one_price = model.get_profit_distribution()
    # plt.hist(cumulative=True, x=profit_one_price["Expected profit"], density=True, bins=100, alpha=0.5, label='in sample')
    # plt.hist(cumulative=True, x=out_sample["Profit"], density=True, bins=100, alpha=0.5, label='out sample')
    # plt.legend()
    # plt.show()
    key += 1

  return pd.DataFrame(average_expected_profit).transpose(), p_DA_df

Pnom = 500
nb_hours = 24
offering_strategy = TwoPricesScheme

average_expected_profit_df_8, p_DA_df_8 = out_sample_analysis(offering_strategy, Pnom, nb_hours, 8)
average_expected_profit_df_4, p_DA_df_4 = out_sample_analysis(offering_strategy, Pnom, nb_hours, 4)

print(average_expected_profit_df_8)
print(average_expected_profit_df_8.describe())
print(p_DA_df_8)
print(p_DA_df_8.transpose().describe())
plt.plot(average_expected_profit_df_8['in_sample'], color=param.colors[1], label='In sample', marker='o')
plt.plot(average_expected_profit_df_8['out_sample'], color=param.colors[2], label='Out sample', marker='^')
plt.axhline(average_expected_profit_df_8['in_sample'].mean(), color=param.colors[1], linestyle='--', label='Mean In sample')
plt.axhline(average_expected_profit_df_8['out_sample'].mean(), color=param.colors[2], linestyle=':', label='Mean Out sample')
plt.legend()
plt.show()
