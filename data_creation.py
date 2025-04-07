import numpy as np
import random as random
import pandas as pd
import ast 

def scenario_generator() -> pd.DataFrame:
    wind_condition = pd.read_csv("data/WindForecast_20250301-20250321.csv", sep=';')

    wind_condition['DateTime'] = pd.to_datetime(wind_condition['DateTime'], format='%d/%m/%Y %H:%M')
    wind_condition['DateTime'] = pd.to_datetime(wind_condition['DateTime'], format='%d/%m/%Y %H:%M')
    wind_condition['Measured & upscaled [MW]'] = wind_condition['Measured & upscaled [MW]'].astype(str)
    wind_condition['Measured & upscaled [MW]'] = wind_condition['Measured & upscaled [MW]'].str.replace(',', '.', regex=False)
    wind_condition['Measured & upscaled [MW]'] = wind_condition['Measured & upscaled [MW]'].str.replace(r'[^0-9.]', '', regex=True)
    wind_condition['Measured & upscaled [MW]'] = pd.to_numeric(wind_condition['Measured & upscaled [MW]'], errors='coerce')

    wind_condition['Monitored Capacity [MW]'] = wind_condition['Monitored Capacity [MW]'].astype(str)
    wind_condition['Monitored Capacity [MW]'] = wind_condition['Monitored Capacity [MW]'].str.replace(',', '.', regex=False)
    wind_condition['Monitored Capacity [MW]'] = wind_condition['Monitored Capacity [MW]'].str.replace(r'[^0-9.]', '', regex=True)
    wind_condition['Monitored Capacity [MW]'] = pd.to_numeric(wind_condition['Monitored Capacity [MW]'], errors='coerce')

    wind_condition['Capacity_factor']=wind_condition['Measured & upscaled [MW]']/wind_condition['Monitored Capacity [MW]'] 
    wind_condition['Hour'] = wind_condition['DateTime'].dt.strftime('%d/%m/%Y %H:00')
    wind_condition['Date'] = wind_condition['DateTime'].dt.date
    
    df_mean = wind_condition.groupby(['Date', 'Hour'])['Capacity_factor'].mean().reset_index()
    daily_values = [df_mean[df_mean['Date'] == day]['Capacity_factor'].tolist() 
                    for day in df_mean['Date'].unique()]

    real_time=[]
    for i in range(0,4):
        scenario_i=[]
        for j in range (0,24):
            scenario_i.append(np.random.binomial(1,0.5))
        real_time.append(scenario_i)

    price_1 = [
        128.2, 120.38, 117.09, 112.15, 109.75, 111.89, 117.11, 135.81, 138.82, 137.77,
        125.08, 112.1, 102.21, 97.27, 99.39, 97.8, 125.41, 145, 158.55, 150.78,
        133.41, 125.42, 122.03, 119.92
    ]

    price_2 = [
        102.61, 57.86, 30.22, 21.37, 19.06, 19.05, 43.56, 90.69, 103.11, 89,
        33.71, 11.22, 7.4, 3.14, 2.85, 19, 54.16, 99.69, 136.58, 117.23,
        80.9, 61.1, 35.12, 25.41
    ]

    price_3 = [
        28.31, 27.04, 25.8, 20.11, 14.94, 20.11, 41.81, 58.7, 70.1, 44.59,  
        20.1, 4.29, 2.43, 1.67, 10.81, 34.89, 70.65, 129.19, 163.66, 102.7,  
        88.19, 79.94, 69.01, 40.3
    ]

    price_4 = [
        65.55, 54.39, 32.29, 20.11, 20.1, 42.51, 52.96, 65.9, 62.85, 61.23,  
        25.3, 13.26, 4, 4.04, 10.11, 30.07, 32.66, 74.91, 64.54, 42.3,  
        29.85, 25.33, 25.52, 20.1
    ]

    price_5 = [
        4, 4, 4, 4, 9.8, 4, 16.04, 43.93, 39.29, 12.6, 0.34, -0.67, -0.7, -0.78,  
        0.01, 3.97, 13.23, 60.4, 60.41, 43.5, 34.76, 33.55, 31.31, 31.16
    ]

    price_6 = [
        30.3, 29.53, 35.47, 39.26, 47.4, 65.97, 93.16, 139.44, 108.51, 78.7,  
        50.47, 4.02, 0.08, 0.02, 13.16, 63.61, 99.2, 129.7, 165.36, 149.11,  
        125.64, 106.63, 101.47, 91.11
    ]

    price_7 = [
        90.27, 90.27, 91.38, 91.69, 98.13, 115.16, 135.67, 147.7, 122.23, 83,  
        65.3, 31.51, 13.08, 8.08, 37.05, 90.15, 126.99, 149.92, 216.65, 178.68,  
        148.7, 132.4, 119.11, 111.83
    ]

    price_8 = [
        124.97, 113.94, 117.22, 116.76, 118.42, 121.3, 127.82, 120.6, 98.05, 72.54,  
        18.05, 2.07, -0.33, -0.1, 2.76, 53.53, 100.87, 145.58, 174.04, 140.03,  
        111.21, 100.01, 99.24, 97.9
    ]

    price_9 = [
        95.19, 94.81, 94.44, 96.51, 98.67, 101.51, 100, 93, 59.02, 24.41,  
        21.32, 3.95, 1.29, 3.95, 11.03, 28.01, 68.99, 107.86, 134.15, 132.71,  
        114.54, 107.87, 104.56, 103.64
    ]

    price_10 = [
        95.84, 94.92, 96.7, 96.86, 89.98, 101.13, 148.63, 159.87, 134.08, 98.92,  
        84.44, 77.92, 76.06, 77.36, 83.96, 97.54, 127.59, 148.1, 175.06, 160.4,  
        142.28, 126.68, 106.87, 97.93
    ]

    price_11 = [
        104.39, 101.79, 99.72, 100.48, 102.51, 110.88, 148.14, 153.09, 146.54, 128.53,  
        102, 97.48, 96.45, 98.39, 102.35, 112.84, 132.9, 172.03, 205.15, 181.06,  
        149.49, 133.05, 121.27, 107.36
    ]

    price_12 = [
        101.74, 100.11, 97.82, 97.43, 101.85, 110.37, 144.57, 161.75, 148.49, 125.02,  
        102.64, 99.73, 98.11, 99.95, 101.69, 117.81, 140.35, 159.04, 199.9, 179.58,  
        148.09, 132.26, 120.02, 109.91
    ]

    price_13 = [
        108.49, 102.22, 98.96, 96.69, 98.33, 105.87, 132.7, 160.74, 160.99, 154.8,  
        123.84, 110.75, 110.08, 108.28, 107.6, 110.02, 121.56, 142.95, 166.09, 173.42,  
        148.99, 135.69, 123.41, 111.53
    ]



    price_14 = [
        109.19, 106.08, 105.97, 103.89, 105.37, 114.08, 143.05, 155.29, 155.08, 132.11,  
        112.01, 106.37, 104.49, 104.58, 105.38, 109.42, 124.93, 146.56, 155.47, 151.02,  
        130.1, 111.46, 114, 105.15
    ]

    price_15 = [
        112.16, 103.15, 96, 89.89, 86.89, 90.55, 97, 99.38, 98.73, 86.36,  
        72.35, 67.12, 57.28, 47.96, 54.46, 70.76, 84.2, 121.87, 130.26, 132.91,  
        121.41, 108.46, 104.98, 95.21
    ]

    price_16 = [
        89.97, 85.75, 79.57, 78.15, 78.55, 29.41, 30.14, 30.7, 30.5, 28.73, 
        24.06, 2.9, 1.01, 0.19, 2.67, 30.81, 59.97, 94.68, 83.61, 45.54, 
        31.49, 31.1, 30.69, 30.44
    ]

    price_17 = [
        30.66, 40.11, 77.6, 80.9, 85.84, 103.33, 135.26, 152.96, 135.32, 100.77, 
        68.2, 50.53, 31.14, 27.92, 50.12, 70.02, 98.59, 143.14, 177.42, 170.09, 
        141.58, 113.55, 106.46, 93.49
    ]

    price_18 = [
        92.18, 89.96, 89.71, 67.1, 69.44, 102.28, 128.02, 136.73, 106.56, 
        68.46, 27.24, 1.79, -0.2, -0.28, 17.36, 38.6, 96.03, 141.1, 171.17, 
        167.77, 142.51, 117.77, 107.46, 100.5
    ]

    price_19 = [
        204.12, 101.46, 97.67, 98.58, 101.74, 110.71, 153.27, 140.98, 99.91, 76.08, 
        38.9, 6.7, 3.13, 3.41, 30.98, 62.63, 120.26, 154.93, 279.34, 251.99, 163.48, 
        136.61, 124.83, 117.5
    ]

    price_20 = [
        107.45, 102.55, 101.34, 102.15, 106.74, 122.73, 158.29, 147.93, 108.19, 73.39, 
        28.86, 3.96, -0.56, -0.16, 27.42, 40.28, 109.8, 147.64, 248.27, 220.53, 176.9, 
        138.38, 124.58, 111.27
    ]

    day_ahead = [
        price_1, price_2, price_3, price_4, price_5, price_6, price_7, price_8, price_9, 
        price_10, price_11, price_12, price_13, price_14, price_15, price_16, price_17, price_18, 
        price_19, price_20
    ]

    # scenario= []
    # for i in daily_values:
    #     for j in day_ahead:
    #         for k in real_time:
    #             scenario.append(i + j + k)

    # df_scenario = pd.DataFrame(scenario)

    # df_scenario.to_csv("data/scenario.csv")

    df_scenario = pd.DataFrame(columns=["Wind", "Price", "System condition"])
    row = 0
    for i in daily_values:
        for j in day_ahead:
            for k in real_time:
                df_scenario.loc[row, "Wind"] = i
                df_scenario.loc[row, "Price"] = j
                df_scenario.loc[row, "System condition"] = k
                row += 1

    return df_scenario
