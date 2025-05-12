import numpy as np
import pandas as pd
from data.data_creation import scenario_generator
from offering_strategy import OnePriceScheme, TwoPricesScheme, OfferingStrategy
import matplotlib.pyplot as plt
import param
from ex_post_analysis import out_sample_analysis

Pnom = 500
nb_hours = 24

average_expected_profit_df_64_1, p_DA_df_64_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 64)
average_expected_profit_df_32_1, p_DA_df_32_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 32)
average_expected_profit_df_16_1, p_DA_df_16_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 16)
average_expected_profit_df_10_1, p_DA_df_10_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 10)
average_expected_profit_df_8_1, p_DA_df_8_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 8)
average_expected_profit_df_4_1, p_DA_df_4_1 = out_sample_analysis(OnePriceScheme, Pnom, nb_hours, 4)


average_expected_profit_df_64, p_DA_df_64 = out_sample_analysis(TwoPricesScheme, Pnom, nb_hours, 32)
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
x_til = [400, 200, 160, 100, 50, 25]

plt.plot(x_til, average_in_one, color=param.colors[1], label='In sample', marker='o')
plt.plot(x_til, average_out_one, color=param.colors[2], label='Out sample', marker='^')
plt.xlabel('Number of in-sample scenarios')
plt.ylabel('Average profit')
plt.legend()
plt.show()

plt.plot(x_til, average_in_two, color=param.colors[1], label='In sample', marker='o')
plt.plot(x_til, average_out_two, color=param.colors[2], label='Out sample', marker='^')
plt.xlabel('Number of in-sample scenarios')
plt.ylabel('Average profit')
plt.legend()
plt.show()

