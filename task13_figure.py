import numpy as np
import pandas as pd
from data.generation_scen_task1 import scenario_generator
from task1_offering_strategy import OnePriceScheme, TwoPricesScheme, OfferingStrategy
import matplotlib.pyplot as plt
import param
from task13_ex_post_analysis import out_sample_analysis
# setting font size
plt.rcParams.update({'font.size': param.fontsize+4})

Pnom = 500
nb_hours = 24

# Comparison of the expected profits in- and out-of-sample
for offering_strategy in [OnePriceScheme, TwoPricesScheme]:
    average_expected_profit_df_8, p_DA_df_8 = out_sample_analysis(offering_strategy, Pnom, nb_hours, 8)
    average_expected_profit_df_4, p_DA_df_4 = out_sample_analysis(offering_strategy, Pnom, nb_hours, 4)

    print(average_expected_profit_df_8)
    print(average_expected_profit_df_8.describe())
    print(p_DA_df_8)
    print(p_DA_df_8.transpose().describe())
    p_DA_df_8.transpose().describe().to_csv('results.csv')
    plt.plot(average_expected_profit_df_8['in_sample'], color=param.colors[1], label='In sample', marker='o')
    plt.plot(average_expected_profit_df_8['out_sample'], color=param.colors[2], label='Out sample', marker='^')
    plt.axhline(average_expected_profit_df_8['in_sample'].mean(), color=param.colors[1], linestyle='--', label=f'Mean In sample: {average_expected_profit_df_8['in_sample'].mean():.2f} k€')
    plt.axhline(average_expected_profit_df_8['out_sample'].mean(), color=param.colors[2], linestyle=':', label=f'Mean Out sample: {average_expected_profit_df_8['out_sample'].mean():.2f} k€')
    plt.grid(linestyle='--', linewidth=0.4)
    plt.ylabel('Expected profit (k€)')
    plt.legend()
    plt.show()

    # print(average_expected_profit_df_4)
    # print(average_expected_profit_df_4.describe())
    # print(p_DA_df_4)
    # print(p_DA_df_4.transpose().describe())
    # plt.plot(average_expected_profit_df_4['in_sample'], color=param.colors[1], label='In sample', marker='o')
    # plt.plot(average_expected_profit_df_4['out_sample'], color=param.colors[2], label='Out sample', marker='^')
    # plt.axhline(average_expected_profit_df_4['in_sample'].mean(), color=param.colors[1], linestyle='--', label=f'Mean In sample {average_expected_profit_df_4['in_sample'].mean()}')
    # plt.axhline(average_expected_profit_df_4['out_sample'].mean(), color=param.colors[2], linestyle=':', label=f'Mean Out sample {average_expected_profit_df_4['out_sample'].mean()}')
    # plt.grid(linestyle='--', linewidth=0.4)
    # plt.legend()
    # plt.show()


# Comparison of the expected profit regarding the number of in-sample scenarios

average_expected_profit_df_64_1, p_DA_df_64_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 64)
average_expected_profit_df_32_1, p_DA_df_32_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 32)
average_expected_profit_df_16_1, p_DA_df_16_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 16)
average_expected_profit_df_10_1, p_DA_df_10_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 10)
average_expected_profit_df_8_1, p_DA_df_8_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 8)
average_expected_profit_df_4_1, p_DA_df_4_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 4)


average_expected_profit_df_64, p_DA_df_64 = out_sample_analysis(TwoPricesScheme, Pnom, nb_hours, 64)
average_expected_profit_df_32, p_DA_df_32 = out_sample_analysis(TwoPricesScheme, Pnom, nb_hours, 32)
average_expected_profit_df_16, p_DA_df_16 = out_sample_analysis(TwoPricesScheme, Pnom, nb_hours, 16)
average_expected_profit_df_10, p_DA_df_10 = out_sample_analysis(TwoPricesScheme, Pnom, nb_hours, 10)
average_expected_profit_df_8, p_DA_df_8 = out_sample_analysis(TwoPricesScheme, Pnom, nb_hours, 8)
average_expected_profit_df_4, p_DA_df_4 = out_sample_analysis(TwoPricesScheme, Pnom, nb_hours, 4)

average_in_one = [average_expected_profit_df_64_1['in_sample'].mean(),
                  average_expected_profit_df_32_1['in_sample'].mean(), 
                  average_expected_profit_df_16_1['in_sample'].mean(), 
                  average_expected_profit_df_10_1['in_sample'].mean(),
                  average_expected_profit_df_8_1['in_sample'].mean(),
                  average_expected_profit_df_4_1['in_sample'].mean()]

average_in_two = [average_expected_profit_df_64['in_sample'].mean(),
                  average_expected_profit_df_32['in_sample'].mean(), 
                  average_expected_profit_df_16['in_sample'].mean(), 
                  average_expected_profit_df_10['in_sample'].mean(),
                  average_expected_profit_df_8['in_sample'].mean(),
                  average_expected_profit_df_4['in_sample'].mean()]

average_out_one =[average_expected_profit_df_64_1['out_sample'].mean(),
                  average_expected_profit_df_32_1['out_sample'].mean(), 
                  average_expected_profit_df_16_1['out_sample'].mean(), 
                  average_expected_profit_df_10_1['out_sample'].mean(),
                  average_expected_profit_df_8_1['out_sample'].mean(),
                  average_expected_profit_df_4_1['out_sample'].mean()]

average_out_two = [average_expected_profit_df_64['out_sample'].mean(),
                   average_expected_profit_df_32['out_sample'].mean(), 
                  average_expected_profit_df_16['out_sample'].mean(), 
                  average_expected_profit_df_10['out_sample'].mean(),
                  average_expected_profit_df_8['out_sample'].mean(),
                  average_expected_profit_df_4['out_sample'].mean()]

x = [4,8,10,16,32, 64]
x_til = [25, 50, 100, 160, 200, 400]

plt.plot(x_til, average_in_one, color=param.colors[1], label='In sample', marker='o')
plt.plot(x_til, average_out_one, color=param.colors[2], label='Out sample', marker='^')
plt.xlabel('Number of in-sample scenarios')
plt.ylabel('Average profit (k€)')
plt.grid(linestyle='--', linewidth=0.4)
plt.legend()
plt.show()

plt.plot(x_til, average_in_two, color=param.colors[1], label='In sample', marker='o')
plt.plot(x_til, average_out_two, color=param.colors[2], label='Out sample', marker='^')
plt.xlabel('Number of in-sample scenarios')
plt.ylabel('Average profit (k€)')
plt.grid(linestyle='--', linewidth=0.4)
plt.legend()
plt.show()

