from offering_strategy import OnePriceSchemeRisk, TwoPricesSchemeRisk, OfferingStrategyRisk
import pandas as pd
from data.data_creation import scenario_generator
import matplotlib.pyplot as plt
import param
import numpy as  np

df_scenario = scenario_generator()

P_nom = 500
nb_hours = 24


def risk_averse(Scheme:OfferingStrategyRisk)->pd.DataFrame|dict:
    df = pd.DataFrame(columns=['beta', 'exp profit', 'CVaR'])
    profit_distributions = {}
    for row, beta in enumerate(np.linspace(0,1,10)):
        PriceScheme = Scheme(T=nb_hours, scenarios=df_scenario[0:200], Pnom=P_nom, beta=beta, alpha=0.9)
        df.loc[row, 'beta'] = beta
        df.loc[row, 'exp profit'] = PriceScheme.get_expected_profit()/1000
        df.loc[row, 'CVaR'] = PriceScheme.get_CVaR()/1000
        profit_distributions[beta] = PriceScheme.get_profit_distribution(plot=False)
    return df, profit_distributions


df_one_price, profit_distribution_one_price = risk_averse(OnePriceSchemeRisk)
df_two_price, profit_distribution_two_price = risk_averse(TwoPricesSchemeRisk)

fig, (ax1, ax2) = plt.subplots(1,2)

ax1.plot(df_one_price['CVaR'], df_one_price['exp profit'], marker='.', linestyle="--", color=param.colors[1])
ax2.plot(df_two_price['CVaR'], df_two_price['exp profit'], marker='.', linestyle="--", color=param.colors[2])

ax1.set(xlabel='CVaR (k€)', ylabel='Expected profit (k€)', title='One price scheme')
ax2.set(xlabel='CVaR (k€)', ylabel='Expected profit (k€)', title='Two price Scheme')

ax1.grid(linestyle='--', linewidth=0.4)
ax2.grid(linestyle='--', linewidth=0.4)
plt.show()    


for beta, item in profit_distribution_two_price.items():
    # Plot one price and two price comulative distribution profit
    plt.hist(cumulative=True, x=item["Expected profit"], density=True, bins=100, alpha=0.5, label=f'$beta$={beta}')
plt.legend()
plt.show()




