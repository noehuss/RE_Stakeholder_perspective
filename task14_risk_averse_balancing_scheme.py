from task1_offering_strategy import OnePriceSchemeRisk, TwoPricesSchemeRisk, OfferingStrategyRisk
import pandas as pd
from data.generation_scen_task1 import scenario_generator, max_profit_per_scenario_distribution_TP, max_profit_per_scenario_distribution_OP
import matplotlib.pyplot as plt
import param
import numpy as  np
from matplotlib.gridspec import GridSpec
# setting font size
plt.rcParams.update({'font.size': param.fontsize})

df_scenario = scenario_generator()

P_nom = 500
nb_hours = 24
alpha = 0.9

def risk_averse(Scheme:OfferingStrategyRisk)-> pd.DataFrame|dict|dict:
    df = pd.DataFrame(columns=['beta', 'exp profit', 'CVaR', 'VaR'])
    profit_distributions = {}
    VaRs = {}
    for row, beta in enumerate(np.linspace(0,1,3)):
        PriceScheme = Scheme(T=nb_hours, scenarios=df_scenario[0:200], Pnom=P_nom, beta=beta, alpha=alpha)
        df.loc[row, 'beta'] = beta
        df.loc[row, 'exp profit'] = PriceScheme.get_expected_profit()/1000
        df.loc[row, 'CVaR'] = PriceScheme.get_CVaR()/1000
        df.loc[row, 'VaR'] = PriceScheme.get_VaR()/1000
        profit_distributions[beta] = PriceScheme.get_profit_distribution(plot=False)
        VaRs[beta] = PriceScheme.get_VaR()
    return df, profit_distributions, VaRs


df_one_price, profit_distribution_one_price, VaRs_one_price = risk_averse(OnePriceSchemeRisk)
df_two_price, profit_distribution_two_price, VaRs_two_price = risk_averse(TwoPricesSchemeRisk)

fig, (ax1, ax2) = plt.subplots(1,2)

ax1.plot(df_one_price['CVaR'], df_one_price['exp profit'], marker='.', linestyle="--", color=param.colors[0])
ax2.plot(df_two_price['CVaR'], df_two_price['exp profit'], marker='.', linestyle="--", color=param.colors[1])
ax1.set(xlabel='CVaR (k€)', ylabel='Expected profit (k€)', title='One-price scheme')
ax2.set(xlabel='CVaR (k€)', ylabel='Expected profit (k€)', title='Two-price Scheme')
ax1.grid(linestyle='--', linewidth=0.4)
ax2.grid(linestyle='--', linewidth=0.4)


for i, row in df_one_price.iterrows():
    bbox = dict(boxstyle='round', fc=param.colors[0], ec=param.colors[0], alpha=0.5)
    ax1.annotate(f'{row['beta']:.1f}', (row['CVaR'], row['exp profit']), fontsize=16, bbox=bbox)
for i, row in df_two_price.iterrows():
    bbox = dict(boxstyle='round', fc=param.colors[1], ec=param.colors[1], alpha=0.5)
    ax2.annotate(f'{row['beta']:.1f}', (row['CVaR'], row['exp profit']), fontsize=16, bbox=bbox)
plt.show()    


# One-price profit volatility
fig, (ax1, ax2) = plt.subplots(1, 2, width_ratios=[4,1], sharey=True)
max_profit_distribution = max_profit_per_scenario_distribution_OP(df_scenario=df_scenario[0:200], pnom=P_nom)
ax1.hist(cumulative=True, x= max_profit_distribution, density=True,bins=100, color=param.colors[-1], alpha=0.2, label='Maximum profit')
first_decile = np.percentile(max_profit_distribution, (1-alpha)*100)
print(first_decile)
ax2.hist(cumulative=True, x=[profit for profit in max_profit_distribution if profit <= first_decile], density=True,bins=100, color=param.colors[-1], alpha=0.2, label='Maximum profit')

for i, (beta, item) in enumerate(profit_distribution_one_price.items()):
    # Plot one price and two price comulative distribution profit
    ax1.hist(cumulative=True, x=item["Expected profit"], density=True, histtype="step", bins=100, alpha=1, label=f'$\\beta$={beta:.1f}', color=param.colors[i])
    bins = 10
    item = item[pd.qcut(item['Expected profit'], bins,  labels=range(bins)).eq(0)]
    list = item["Expected profit"] #k€
    ax2.hist(cumulative=True, x=list, density=True, histtype="step", bins=10, color=param.colors[i])

ax1.set(xlabel='Expected profit (k€)', ylabel='Probability')
ax2.set(xlabel='Expected profit (k€)')
ax1.grid(linestyle='--', linewidth=0.4)
ax2.grid(linestyle='--', linewidth=0.4)
ax1.legend()
plt.show()


# Two-price profit volatility
fig, (ax1, ax2) = plt.subplots(1, 2, width_ratios=[4,1], sharey=True)
max_profit_distribution = max_profit_per_scenario_distribution_TP(df_scenario=df_scenario[0:200], pnom=P_nom)
ax1.hist(cumulative=True, x= max_profit_distribution, density=True,bins=100, color=param.colors[-1], alpha=0.2, label='Maximum profit')
first_decile = np.percentile(max_profit_distribution, (1-alpha)*100)
print(first_decile)
ax2.hist(cumulative=True, x=[profit for profit in max_profit_distribution if profit <= first_decile], density=True,bins=100, color=param.colors[-1], alpha=0.2, label='Maximum profit')

for i, (beta, item) in enumerate(profit_distribution_two_price.items()):
    # Plot one price and two price comulative distribution profit
    ax1.hist(cumulative=True, x=item["Expected profit"], density=True, histtype="step", bins=100, alpha=1, label=f'$\\beta$={beta:.1f}', color=param.colors[i])
    bins = 10
    item = item[pd.qcut(item['Expected profit'], bins,  labels=range(bins)).eq(0)]
    list = item["Expected profit"] #k€
    ax2.hist(cumulative=True, x=list, density=True, histtype="step", bins=10, color=param.colors[i])


ax1.set(xlabel='Expected profit (k€)', ylabel='Probability')
ax2.set(xlabel='Expected profit (k€)')
ax1.grid(linestyle='--', linewidth=0.4)
ax2.grid(linestyle='--', linewidth=0.4)
ax1.legend()
plt.show()


print(VaRs_two_price)
print(VaRs_one_price)
print(df_one_price)
print(df_two_price)

