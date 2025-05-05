from offering_strategy import OnePriceSchemeRisk, TwoPriceSchemeRisk, OfferingStrategyRisk
import pandas as pd
from data.data_creation import scenario_generator
import matplotlib.pyplot as plt
import param
import numpy as  np

df_scenario = scenario_generator()

P_nom = 500
nb_hours = 24
alpha = 0.9

def risk_averse(Scheme:OfferingStrategyRisk)->pd.DataFrame|dict:
    df = pd.DataFrame(columns=['beta', 'exp profit', 'CVaR', 'VaR'])
    profit_distributions = {}
    VaRs = {}
    for row, beta in enumerate(np.linspace(0,1,6)):
        PriceScheme = Scheme(T=nb_hours, scenarios=df_scenario[0:100], Pnom=P_nom, beta=beta, alpha=alpha)
        df.loc[row, 'beta'] = beta
        df.loc[row, 'exp profit'] = PriceScheme.get_expected_profit()/1000
        df.loc[row, 'CVaR'] = PriceScheme.get_CVaR()/1000
        df.loc[row, 'VaR'] = PriceScheme.get_VaR()/1000
        profit_distributions[beta] = PriceScheme.get_profit_distribution(plot=False)
        VaRs[beta] = PriceScheme.get_VaR()
    return df, profit_distributions, VaRs


df_one_price, profit_distribution_one_price, VaRs_one_price = risk_averse(OnePriceSchemeRisk)
df_two_price, profit_distribution_two_price, VaRs_two_price = risk_averse(TwoPriceSchemeRisk)

fig, (ax1, ax2) = plt.subplots(1,2)

ax1.plot(df_one_price['CVaR'], df_one_price['exp profit'], marker='.', linestyle="--", color=param.colors[1])
ax2.plot(df_two_price['CVaR'], df_two_price['exp profit'], marker='.', linestyle="--", color=param.colors[2])

ax1.set(xlabel='CVaR (k€)', ylabel='Expected profit (k€)', title='One price scheme')
ax2.set(xlabel='CVaR (k€)', ylabel='Expected profit (k€)', title='Two prices Scheme')

ax1.grid(linestyle='--', linewidth=0.4)
ax2.grid(linestyle='--', linewidth=0.4)
plt.show()    


fig, (ax1, ax2) = plt.subplots(1,2, sharex=True)
for i, (beta, item) in enumerate(profit_distribution_one_price.items()):
    # Plot one price and two price comulative distribution profit
    #plt.hist(cumulative=True, x=item["Expected profit"], density=True, histtype="step", bins=500, alpha=1, label=f'$beta$={beta}')
    #plt.axhline(VaRs_two_price[beta], linestyle='--')
    bins=10
    #item = item[pd.qcut(item['Expected profit'], bins,  labels=range(bins), duplicates='drop').eq(0)]
    list = item["Expected profit"]/1000 #k€
    bplot = ax1.boxplot(list, positions=[i+1], patch_artist=False, tick_labels=[f"{beta:.1f}"], showmeans=True)
ax1.set(ylabel='Expected profit (k€)', title='One price scheme')


for i, (beta, item) in enumerate(profit_distribution_two_price.items()):
    # Plot one price and two price comulative distribution profit
    #plt.hist(cumulative=True, x=item["Expected profit"], density=True, histtype="step", bins=500, alpha=1, label=f'$beta$={beta}')
    #plt.axhline(VaRs_two_price[beta], linestyle='--')
    bins=10
    #item = item[pd.qcut(item['Expected profit'], bins,  labels=range(bins), duplicates='drop').eq(0)]
    list = item["Expected profit"]/1000 #k€
    bplot = ax2.boxplot(list, positions=[i+1], patch_artist=False, tick_labels=[f"{beta:.1f}"], showmeans=True)
ax2.set(xlabel='$\\beta$', ylabel='Expected profit (k€)', title='Two prices scheme')




#plt.axvline(1-alpha, linestyle='--', color='black')
#plt.legend()
plt.show()

print(VaRs_two_price)
print(VaRs_one_price)
print(df_one_price)
print(df_two_price)

