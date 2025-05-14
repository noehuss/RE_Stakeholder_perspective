import numpy as np
import pandas as pd
from data.generation_scen_task1 import scenario_generator
from task1_offering_strategy import OnePriceScheme, TwoPricesScheme, OfferingStrategy
import matplotlib.pyplot as plt
import param
# setting font size
plt.rcParams.update({'font.size': param.fontsize})

def out_sample_analysis(offering_strategy:OfferingStrategy, Pnom, nb_hours, nb_split) -> pd.DataFrame | pd.DataFrame:
  scenario_df = scenario_generator()

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
        # Calculation of profit under the OnePrice scheme
        price = np.multiply(row["Price"], np.add(np.multiply(1.25, row["System condition"]),np.multiply(0.85, np.subtract(1, row["System condition"]))))
        out_sample.loc[i, "Imbalance cost"] = sum(np.multiply(row["Imbalance"], price))
    else:
      for i, row in out_sample.iterrows():
        # Calculation of profit under the TwoPrice scheme
        deficit = np.multiply(row["System condition"], np.subtract(row["Imbalance up"], np.multiply(1.25, row["Imbalance down"])))
        excess = np.multiply(np.subtract(1, row["System condition"]), np.subtract(np.multiply(0.85, row["Imbalance up"]), row["Imbalance down"]))
        imbalance_cost = np.multiply(row["Price"], np.add(deficit, excess)) 
        out_sample.loc[i, "Imbalance cost"] = sum(imbalance_cost)
    
    out_sample["Profit"] = out_sample["DA profit"] + out_sample["Imbalance cost"]

    average_expected_profit[key] = {
      "out_sample" : out_sample["Profit"].mean()/1000, #k€
      "in_sample" : model.get_average_profit()    
    }
    key += 1

  return pd.DataFrame(average_expected_profit).transpose(), p_DA_df

