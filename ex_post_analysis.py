import numpy as np
import pandas as pd
from data.data_creation import scenario_generator
from offering_strategy import OnePriceScheme, TwoPricesScheme
import matplotlib.pyplot as plt

Pnom = 500
nb_hours = 24
scenario_df = scenario_generator()

scheme = "two"
scenario_df = scenario_df.sample(frac=1).reset_index(drop=True)

average_expected_profit = {}
p_DA_df = pd.DataFrame()
key = 1
for in_sample in np.array_split(scenario_df, 8):
  assert len(in_sample) == len(scenario_df) / 8
  in_sample = pd.DataFrame(in_sample)
  if scheme == "one":
    model = OnePriceScheme(nb_hours, in_sample, Pnom=Pnom)
  else:
    model = TwoPricesScheme(nb_hours, in_sample, Pnom=Pnom)
  p_DA = model.get_p_DA()
  out_sample = scenario_df.drop(index=in_sample.index)
  p_DA_df[f"p_DA_{key}"] = p_DA
  # Profit day ahead
  out_sample["DA profit"] = out_sample["Price"].map(lambda x: sum(np.multiply(x, p_DA)))

  # Cost imbalance
  def calc_imbalance(x):
    return np.subtract(np.multiply(x, Pnom), p_DA)
  out_sample["Imbalance"] = out_sample["Wind"].map(lambda x: calc_imbalance(x))
  out_sample["Imbalance up"] = out_sample["Imbalance"].map(lambda y: list(map(lambda x: max(x,0),y))) #Two prices
  out_sample["Imbalance down"] = out_sample["Imbalance"].map(lambda y: list(map(lambda x: -min(x,0),y))) #Two prices

  if scheme == "one":
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
  profit_one_price = model.get_profit_distribution()
  # plt.hist(cumulative=True, x=profit_one_price["Expected profit"], density=True, bins=100, alpha=0.5, label='in sample')
  # plt.hist(cumulative=True, x=out_sample["Profit"], density=True, bins=100, alpha=0.5, label='out sample')
  # plt.legend()
  # plt.show()

  key += 1

average_expected_profit_df = pd.DataFrame(average_expected_profit).transpose()

print(average_expected_profit_df)
print(average_expected_profit_df.describe())
print(p_DA_df)
print(p_DA_df.transpose().describe())
average_expected_profit_df.plot()
plt.show()
