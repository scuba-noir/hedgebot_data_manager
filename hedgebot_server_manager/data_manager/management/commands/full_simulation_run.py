
import numpy as np
import pandas as pd

from external_python_scripts import create_assumptions_dict
from external_python_scripts import aws_database_connector as aws
from external_python_scripts import simulate_statements
from sugar_app.models import current_financial_simulations


def main():

    initial_simulation_variables = aws.return_forecast_assumptions('2023/24')
    initial_simulation_variables_2 = initial_simulation_variables.loc[initial_simulation_variables['Most_recent_company_forecast'] == 1]
    market_var_list = ['Sugar','Hydrous','Anhydrous','Energy','Exchange rate','Domestic interest rate','Foreign interest rate','Inflation','Crude oil','Fertilizers']
    driver_values = initial_simulation_variables_2.loc[initial_simulation_variables_2['Variable_name_eng'].isin(market_var_list)]

    mc_meta_data_1 = aws.return_mc_meta_vars()
    max_date = mc_meta_data_1['date_published'].max()
    mc_meta_data_1 = mc_meta_data_1.loc[(mc_meta_data_1['date_published'] == max_date) & (mc_meta_data_1['forecast_date'] == pd.to_datetime('2023-03-24', dayfirst=False))]
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

    mc_meta_data = mc_meta_data_1.loc[mc_meta_data_1['variable_name'].isin(ls_name)]
    
    for row, values in mc_meta_data.iterrows():
        temp_sim = []
        mean = values.mean_returned
        std = values.std_returned
        factor_name = values.variable_name
        sim_data = np.random.normal(mean, std, 10000).tolist()
        temp_values[factor_name].append([
            sim_data  
        ])

    temp_selic = driver_values['Value'].loc[(driver_values['Variable_name_eng'] == 'Domestic interest rate')].values[0]
    temp_inflation = driver_values['Value'].loc[(driver_values['Variable_name_eng'] == 'Inflation')].values[0]
    temp_foreign_coupon = driver_values['Value'].loc[(driver_values['Variable_name_eng'] == 'Foreign interest rate')].values[0]

    for i in range(0,10000):
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

        forecast_chg = create_assumptions_dict.main(new_drivers_dict, new_drivers_ls)
        prev_year_financial_df = aws.return_forecast_assumptions(0)
        prev_year_financial_df = prev_year_financial_df.loc[prev_year_financial_df['Season'] == '2021/22']
        temp_income_statement_df, temp_cash_flow_df, temp_assets_df, temp_liabilities_df, temp_financial_indices_df = simulate_statements.Simulate_Three_Statements(forecast_chg, prev_year_financial_df)
        income_statement_final_df = pd.DataFrame(temp_income_statement_df)
        cash_flow_final_df = pd.DataFrame(temp_cash_flow_df)
        assets_final_df = pd.DataFrame(temp_assets_df)
        liabilities_final_df = pd.DataFrame(temp_liabilities_df)
        financial_indices_final_df = pd.DataFrame(temp_financial_indices_df)

        final_df = simulate_statements.aggregate_fin_sim_results(income_statement_final_df, cash_flow_final_df, assets_final_df, liabilities_final_df, financial_indices_final_df)

