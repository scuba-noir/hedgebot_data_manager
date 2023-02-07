
import numpy as np
import pandas as pd

from . import create_assumptions_dict, simulate_statements
from . import models

def custom_append(dict_1, dict_2, counter):
    print(dict_1)
    if counter == 0:
        dict_1.update(dict_2)
    else:
        for keys in dict_2.keys():
            print(dict_2[keys])
            dict_1[keys].append(dict_2[keys])

def main(initial_simulation_variables, prev_year_financial_df, mc_meta_data_1):

    initial_simulation_variables_2 = initial_simulation_variables
    market_var_list = ['Sugar','Hydrous','Anhydrous','Energy','Exchange rate','Domestic interest rate','Foreign interest rate','Inflation','Crude oil','Fertilizers']
    mc_market_var_list = ['sugar_1', 'hydrous', 'anhydrous', 'energy', 'usdbrl', 'brent', 'fert']
    translation_market_var_list = ['NY No.11','Hydrous Ethanol','Anhydrous Ethanol','Energy Prices','USDBRL','Brent Crude','Fertilizer Costs']    
    driver_values = initial_simulation_variables_2.loc[initial_simulation_variables_2['Variable_name_eng'].isin(market_var_list)]

    max_date = mc_meta_data_1['simulation_date'].max()
    mc_meta_data_1 = mc_meta_data_1.loc[(mc_meta_data_1['simulation_date'] == max_date) & (mc_meta_data_1['end_date'] == pd.to_datetime('2024-03-31', dayfirst=False))]
    driver_values['Value'].loc[(driver_values['Variable_name_eng'] == 'Domestic interest rate')].values[0] * 100,
    temp_values = {
        'Anhydrous Ethanol':[],
        'Hydrous Ethanol':[],
        'NY No.11':[],
        'USDBRL':[],
        'Brent Crude':[],
        'Energy Prices':[],
        'Fertilizer Costs':[],
    }
    ls_name = ['Anhydrous Ethanol',
        'Hydrous Ethanol',
        'NY No.11',
        'USDBRL',
        'Fertilizer Costs',
        'Brent Crude',
        'Energy Prices'
        ]
    counter = 0

    mc_meta_data = mc_meta_data_1.loc[mc_meta_data_1['reference'].isin(mc_market_var_list)]
    
    for row, values in mc_meta_data.iterrows():
        temp_sim = []
        label_index = mc_market_var_list.index(values.reference)
        mean = values.mean_returned
        std = values.std_returned
        factor_name = translation_market_var_list[label_index]
        sim_data = np.random.normal(mean, std, 10000).tolist()
        temp_values[factor_name].append([
            sim_data  
        ])

    temp_selic = driver_values['Value'].loc[(driver_values['Variable_name_eng'] == 'Domestic interest rate')].values[0]
    temp_inflation = driver_values['Value'].loc[(driver_values['Variable_name_eng'] == 'Inflation')].values[0]
    temp_foreign_coupon = driver_values['Value'].loc[(driver_values['Variable_name_eng'] == 'Foreign interest rate')].values[0]

    final_value_dict = {
            "simulation_number":1,
            "sugar_price":1,
            "hydrous_price":1,
            "anhydrous_price":1,
            "energy_price":1,
            "fx_rate":1,
            "selic_rate":1,
            "foreign_debt_rate":1,
            "inflation_rate":1,
            "crude_price":1,
            "fertilizer_price":1,
            "sugar_revenues":1,
            "hydrous_revenues":1,
            "anhydrous_revenues":1,
            "energy_revenues":1,
            "input_costs":1,
            "fuel_costs":1,
            "freight_costs":1,
            "labor_costs":1,
            "indutrial_costs":1,
            "depreciation":1,
            "planting_costs":1,
            "lease_costs":1,
            "gross_profit":1,
            "sga_costs":1,
            "ebit":1,
            "financial_costs":1,
            "ebt":1,
            "tax":1,
            "net_income":1,
            "gross_margin":1,
            "ebitda_margin":1,
            "net_margin":1,
            "net_debt_to_ebitda":1,
            "net_debt_to_mt_cane": 1,
            "indebtness":1,
            "short_term_debt":1,
            "current_ratio":1
    }


    for i in range(0,10000):

        print(final_value_dict)

        sugar_price = temp_values['NY No.11'][0][0][i]
        hydrous_price = temp_values['Hydrous Ethanol'][0][0][i]
        anhydrous_price = temp_values['Anhydrous Ethanol'][0][0][i]
        energy_price = temp_values['Energy Prices'][0][0][i]
        fx_rate = temp_values['USDBRL'][0][0][i]
        selic_rate = temp_selic
        foreign_debt_rate =temp_foreign_coupon
        inflation_rate = temp_inflation
        crude_price = temp_values['Brent Crude'][0][0][i]
        fertilizer_price=temp_values['Fertilizer Costs'][0][0][i]


        new_drivers_ls = [sugar_price, hydrous_price, anhydrous_price, energy_price, fx_rate, selic_rate, foreign_debt_rate, inflation_rate, crude_price, fertilizer_price]

        new_drivers_dict = {
            'Sugar':sugar_price, 
            'Hydrous':hydrous_price,
            'Anhydrous':anhydrous_price, 
            'Energy':energy_price, 
            'Exchange rate':fx_rate, 
            'Domestic interest rate':selic_rate, 
            'Foreign interest rate':foreign_debt_rate, 
            'Inflation':inflation_rate, 
            'Crude oil':crude_price, 
            'Fertilizers':fertilizer_price}

        forecast_chg = create_assumptions_dict.main(new_drivers_dict, new_drivers_ls, prev_year_financial_df, initial_simulation_variables)
        temp_income_statement_df, temp_cash_flow_df, temp_assets_df, temp_liabilities_df, temp_financial_indices_df = simulate_statements.Simulate_Three_Statements(forecast_chg, prev_year_financial_df)
        income_statement_final_df = pd.DataFrame(temp_income_statement_df)
        cash_flow_final_df = pd.DataFrame(temp_cash_flow_df)
        assets_final_df = pd.DataFrame(temp_assets_df)
        liabilities_final_df = pd.DataFrame(temp_liabilities_df)
        financial_indices_final_df = pd.DataFrame(temp_financial_indices_df)

        final_df = simulate_statements.aggregate_fin_sim_results(income_statement_final_df, cash_flow_final_df, assets_final_df, liabilities_final_df, financial_indices_final_df)
        final_df['Mean Returned'] = pd.to_numeric(final_df['Mean Returned'].astype(str).str.replace(',',''), errors='coerce').fillna(0).astype(int)

        temp_dict = {
            "simulation_number":i,
            "sugar_price":sugar_price,
            "hydrous_price":hydrous_price,
            "anhydrous_price":anhydrous_price,
            "energy_price":energy_price,
            "fx_rate":fx_rate,
            "selic_rate":selic_rate,
            "foreign_debt_rate":foreign_debt_rate,
            "inflation_rate":inflation_rate,
            "crude_price":crude_price,
            "fertilizer_price":fertilizer_price,
            "sugar_revenues":final_df['Mean Returned'].loc[final_df['Account'] == 'Sugar Revenues BRL'].values[0],
            "hydrous_revenues":final_df['Mean Returned'].loc[final_df['Account'] == 'Hydrous Revenues BRL'].values[0],
            "anhydrous_revenues":final_df['Mean Returned'].loc[final_df['Account'] == 'Anhydrous Revenues BRL'].values[0],
            "energy_revenues":final_df['Mean Returned'].loc[final_df['Account'] == 'Energy Revenues BRL'].values[0],
            "input_costs":final_df['Mean Returned'].loc[final_df['Account'] == 'Input Cost BRL'].values[0],
            "fuel_costs":final_df['Mean Returned'].loc[final_df['Account'] == 'Fuel Cost BRL'].values[0],
            "freight_costs":final_df['Mean Returned'].loc[final_df['Account'] == 'Freight Cost BRL'].values[0],
            "labor_costs":final_df['Mean Returned'].loc[final_df['Account'] == 'Labor Cost BRL'].values[0],
            "indutrial_costs":final_df['Mean Returned'].loc[final_df['Account'] == 'Industrial Cost BRL'].values[0],
            "depreciation":final_df['Mean Returned'].loc[final_df['Account'] == 'Depreciation BRL'].values[0],
            "planting_costs":final_df['Mean Returned'].loc[final_df['Account'] == 'Planting Cost BRL'].values[0],
            "lease_costs":final_df['Mean Returned'].loc[final_df['Account'] == 'Lease Cost BRL'].values[0],
            "gross_profit":final_df['Mean Returned'].loc[final_df['Account'] == 'Gross Profit BRL'].values[0],
            "sga_costs":final_df['Mean Returned'].loc[final_df['Account'] == 'Total SG&A BRL'].values[0],
            "ebit":final_df['Mean Returned'].loc[final_df['Account'] == 'EBIT'].values[0],
            "financial_costs":final_df['Mean Returned'].loc[final_df['Account'] == 'Financial Expenses BRL'].values[0],
            "ebt":final_df['Mean Returned'].loc[final_df['Account'] == 'Profit Before Tax BRL'].values[0],
            "tax":final_df['Mean Returned'].loc[final_df['Account'] == 'Income Tax BRL'].values[0],
            "net_income":final_df['Mean Returned'].loc[final_df['Account'] == 'Net Income BRL'].values[0],
            "gross_margin":final_df['Mean Returned'].loc[final_df['Account'] == 'Gross Margin'].values[0],
            "ebitda_margin":final_df['Mean Returned'].loc[final_df['Account'] == 'EBITDA Margin'].values[0],
            "net_margin":final_df['Mean Returned'].loc[final_df['Account'] == 'Net Margin'].values[0],
            "net_debt_to_ebitda":final_df['Mean Returned'].loc[final_df['Account'] == 'Net Debt / EBITDA'].values[0],
            "net_debt_to_mt_cane": final_df['Mean Returned'].loc[final_df['Account'] == 'Net Debt / MT of Cane'].values[0],
            "indebtness":final_df['Mean Returned'].loc[final_df['Account'] == 'Indebtness'].values[0],
            "short_term_debt":final_df['Mean Returned'].loc[final_df['Account'] == 'Short Term Debt Percent'].values[0],
            "current_ratio":final_df['Mean Returned'].loc[final_df['Account'] == 'Current Ratio'].values[0]
        }

        print(temp_dict)

        final_value_dict = custom_append(final_value_dict, temp_dict, i)
    
    return final_value_dict
