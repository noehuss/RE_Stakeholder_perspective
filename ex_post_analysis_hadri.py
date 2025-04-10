from data.data_creation import scenario_generator
from offering_strategy import OnePriceScheme, TwoPricesScheme
from sklearn import model_selection
import numpy as np

#Parameters
df_scenario = scenario_generator()
P_nom = 500
nb_hours = 24



def ex_post_CV(scenario):
    #We create a cross-validation model
    CV = model_selection.KFold(n_splits = 8, shuffle = True)

    # Store in and out profit
    profit_in_sample = np.empty(8)
    profit_out_of_sample = np.empty(8)

    #An index to compute the values in the table
    index=0

    for train_index, test_index in CV.split(scenario):
        #We select the train (in) and test (out) scenarios
        scenario_train = scenario.iloc[train_index, :].copy()
        scenario_test = scenario.iloc[test_index, :].copy()
        
        #We call our price scheme, and obtain the average profit on the trained data. We add the average profit in the table
        OnePrice = OnePriceScheme(T=nb_hours, scenarios = scenario_train, Pnom=P_nom)
        avg_profit_train = OnePrice.get_average_profit()
        profit_in_sample[index] = avg_profit_train

        #We select the offer, our bid p_DA, the production we bid on the market. From this, we calculate the expected profit for the out_of sample scenarios
        p_DA = OnePrice.get_p_DA()
        print(p_DA)
        print('-----------------------------------------------------------------')

        # We initialize randomly 3 new columns 
        scenario_test['Imbalance'] = None
        scenario_test['Profit'] = None
        scenario_test['Daily Profit'] = np.nan

        for i, row in scenario_test.iterrows():
            # Imbalance and profit calculation
            imbalance = [row['Wind'][j]*P_nom - p_DA[j] for j in range (nb_hours)]
            profit = [row['Price'][j]*(p_DA[j] + imbalance[j]*(1.25*row['System condition'][j] + 0.85*(1-row['System condition'][j])))
                                                                            for j in range (nb_hours)]
            
            scenario_test.at[i, 'Imbalance'] = imbalance
            scenario_test.at[i, 'Profit'] = profit
            scenario_test.at[i, 'Daily Profit'] = sum(profit)
            
        avg_profit_test = scenario_test['Daily Profit'].mean()
        profit_out_of_sample[index] = avg_profit_test

        index += 1
    

    return profit_in_sample, profit_out_of_sample
    
profit_in, profit_out = ex_post_CV(df_scenario)
print(f'Profit in sample: {profit_in}')
print(f'Profit out of sample: {profit_out}')
print(profit_in.mean())
print(profit_out.mean())



