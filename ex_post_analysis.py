import numpy as np
import pandas as pd
from data.data_creation import scenario_generator
from offering_strategy import OnePriceScheme, TwoPricesScheme

Pnom = 500
nb_hours = 24
scenario_df = scenario_generator()

scenario_df = scenario_df.sample(frac=1).reset_index(drop=True)

for in_sample in np.array_split(scenario_df, 8):
  assert len(in_sample) == len(scenario_df) / 8
  in_sample = pd.DataFrame(in_sample)
  one_price = OnePriceScheme(nb_hours, in_sample, Pnom=Pnom)
  p_DA = one_price.get_p_DA()
  
  out_sample = scenario_df.drop(index=in_sample.index)
  # Profit day ahead
  out_sample["DA profit"] = out_sample["Price"].map(lambda x: np.multiply(x, p_DA))

  # Cost imbalance
  def calc_imbalance(x):
    return np.subtract(np.multiply(x, Pnom), p_DA)
  out_sample["Imbalance"] = out_sample["Wind"].map(lambda x: calc_imbalance(x))
  out_sample["Imbalance up"] = out_sample["Imbalance"].map(lambda y: list(map(lambda x: max(x,0),y)))
  out_sample["Imbalance down"] = out_sample["Imbalance"].map(lambda y: list(map(lambda x: -min(x,0),y)))
  
  df_costs = pd.DataFrame(columns=["Imbalance cost"])
  for i, row in out_sample.iterrows():
    price = np.multiply(row["Price"], np.add(np.multiply(1.25, row["System condition"]),np.multiply(0.85, np.subtract(1, row["System condition"]))))
    print(np.multiply(row["Imbalance"], price))
    df_costs.loc[i, "Imbalance cost"] = list(np.multiply(row["Imbalance"], price))
  print(df_costs["Imbalance cost"])
  break