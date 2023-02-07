from lib2to3.pgen2 import driver


import pandas as pd
import numpy as np
import datetime

def main(new_drivers_dict, new_drivers_ls, prev_season_df, current_season_df):

    forecast_baseline = prev_season_df
    temp_baseline = current_season_df

    drivers_to_change = [
        ('Sugar','Price Assumptions'),
        ('Hydrous', 'Price Assumptions'),
        ('Anhydrous', 'Price Assumptions'),
        ('Energy','Price Assumptions'),
        ('Exchange rate', 'Price Assumptions'),
        ('Domestic interest rate','Price Assumptions'),
        ('Foreign interest rate','Price Assumptions'),
        ('Inflation', 'Price Assumptions'),
        ('Crude oil','Price Assumptions'),
        ('Fertilizers', 'Price Assumptions'),
    ]

    forecast_chg = temp_baseline
    prev_season_values  = []
    temp_prev_season_df = forecast_baseline
    for i in range(0,len(drivers_to_change)):
        index = forecast_chg['Value'].loc[(forecast_chg['Variable_name_eng'].isin(drivers_to_change[i])) & (forecast_chg['Data_group'].isin(drivers_to_change[i]))].index.values[0]
        print(i)
        forecast_chg.at[index, 'Value'] = new_drivers_ls[i]
        prev_season_values.append(temp_prev_season_df['Value'].loc[(temp_prev_season_df['Variable_name_eng'].isin(drivers_to_change[i])) & (temp_prev_season_df['Data_group'].isin(drivers_to_change[i]))].values[0])

    prev_season_values_df = pd.DataFrame([prev_season_values], columns = ['Sugar', 'Hydrous', 'Anhydrous', 'Energy','Exchange Rate','Domestic interest rate','Foreign interest rate','Inflation','Crude oil','Fertilizers'])
    forecast_chg['Most_recent_company_forecast'].loc[:] = 0
    forecast_chg['Date_published'].loc[:] = datetime.datetime.today().strftime("%Y-%m-%d")
    #forecast_baseline = pd.concat([forecast_baseline, forecast_chg])
   
    """
    driven variables:
    Inputs - > (Percentage Chg. b/w Fertilizer Costs)
    Fuel - > (Percentage Chg. b/w Brent Cost)
    Freights - > (Percentage Chg. b/w Brent Cost)
    Labor Cost -> (Multiplied by Inflation Rate)
    Industrial Cost -> (Multiplied by Inflation Rate)
    Planting Cost -> (Percentage Chg. b/w Fertilizer Costs)
    Financial expenses
    """

    #Input Costs
    #new_fert = new_drivers_dict['Fertilizers'].values[0]
    #prev_fert = prev_season_values_df['Fertilizers'].values[0]
    """Temp Fix (Must Change)"""
    chg_fert = 1.30
    prev_input_costs = temp_prev_season_df['Value'].loc[(temp_prev_season_df['Variable_name_eng'] == 'Inputs') & (temp_prev_season_df['Data_group'] == 'Production Cost Assumptions')].values[0]
    new_input_costs = prev_input_costs * chg_fert

    #Fuel Costs
    try:
        new_fuel = new_drivers_dict['Crude oil'].values[0]
    except:
        new_fuel = new_drivers_dict['Crude oil']
    prev_fuel = prev_season_values_df['Crude oil'].values[0]
    prev_fuel_costs = temp_prev_season_df['Value'].loc[(temp_prev_season_df['Variable_name_eng'] == 'Fuel') & (temp_prev_season_df['Data_group'] == 'Production Cost Assumptions')].values[0]
    new_fuel_costs = prev_fuel_costs * (new_fuel / prev_fuel)

    #Freight Costs
    prev_freight_costs = temp_prev_season_df['Value'].loc[(temp_prev_season_df['Variable_name_eng'] == 'Freights') & (temp_prev_season_df['Data_group'] == 'Production Cost Assumptions')].values[0]
    new_freight_costs = prev_freight_costs * (new_fuel / prev_fuel)

    #Labor Costs
    inflation_rate = new_drivers_dict['Inflation'] / 100
    prev_labor_costs = temp_prev_season_df['Value'].loc[(temp_prev_season_df['Variable_name_eng'] == 'Labor cost') & (temp_prev_season_df['Data_group'] == 'Production Cost Assumptions')].values[0]
    new_labor_costs = prev_labor_costs * (1+inflation_rate)

    #Industrial Costs
    prev_industrial_costs = temp_prev_season_df['Value'].loc[(temp_prev_season_df['Variable_name_eng'] == 'Industrial cost') & (temp_prev_season_df['Data_group'] == 'Production Cost Assumptions')].values[0]
    new_industrial_costs = prev_industrial_costs * (1+inflation_rate)

    #Planting costs
    prev_planting_costs = temp_prev_season_df['Value'].loc[(temp_prev_season_df['Variable_name_eng'] == 'Planting cost') & (temp_prev_season_df['Data_group'] == 'Production Cost Assumptions')].values[0]
    new_planting_costs = prev_planting_costs * (chg_fert)

    #Financial costs
    try:
        new_fx = new_drivers_dict['Exchange rate'].values[0]
    except:
        new_fx = new_drivers_dict['Exchange rate']
    new_foreign_ir = new_drivers_dict['Foreign interest rate'] / 100
    total_usd_debt = temp_baseline['Value'].loc[(temp_baseline['Variable_name_eng'] == 'US$ debt, total') & (temp_baseline['Units'] == '000 USD')].values[0]
    avg_coupon_usd = temp_baseline['Value'].loc[(temp_baseline['Variable_name_eng'] == 'Average cost (coupon), USD debt') & (temp_baseline['Units'] == 'Libor +, p.a.')].values[0]
    total_brl_st_debt =  temp_baseline['Value'].loc[(temp_baseline['Variable_name_eng'] == 'R$ debt, short term') & (temp_baseline['Data_group'] == 'Indebtness Assumptions')].values[0]
    total_brl_lt_debt = temp_baseline['Value'].loc[(temp_baseline['Variable_name_eng'] == 'R$ debt, long term') & (temp_baseline['Data_group'] == 'Indebtness Assumptions')].values[0]
    total_brl_debt = total_brl_st_debt + total_brl_lt_debt
    avg_coupon_brl = temp_baseline['Value'].loc[(temp_baseline['Variable_name_eng'] == 'Average cost (coupon), USD debt') & (temp_baseline['Units'] == 'CDI +, p.a.')].values[0]
    new_domestic_ir = new_drivers_dict['Domestic interest rate'] / 100
    new_financial_costs = (total_usd_debt*(avg_coupon_usd+new_foreign_ir)*new_fx) + (total_brl_debt*(avg_coupon_brl+new_domestic_ir))

    driven_variables = [
        ('Inputs','Production Cost Assumptions'),
        ('Fuel', 'Production Cost Assumptions'),
        ('Freights', 'Production Cost Assumptions'),
        ('Labor cost', 'Production Cost Assumptions'),
        ('Industrial cost', 'Production Cost Assumptions'),
        ('Planting cost', 'Production Cost Assumptions'),
        ('Total financial expenses', 'Indebtness Assumptions')
    ]

    new_driven_costs_ls = [new_input_costs, new_fuel_costs, new_freight_costs, new_labor_costs, new_industrial_costs, new_planting_costs, new_financial_costs]


    for i in range(0,len(driven_variables)):
        try:
            index = forecast_chg['Value'].loc[(forecast_chg['Variable_name_eng'].isin(driven_variables[i])) & (forecast_chg['Data_group'].isin(driven_variables[i]))].index.values[0]
        except:
            index = forecast_chg['Value'].loc[(forecast_chg['Variable_name_eng'].isin(driven_variables[i])) & (forecast_chg['Data_group'].isin(driven_variables[i]))].index.values
        try:
            forecast_chg.at[index, 'Value'] = new_driven_costs_ls[i]
        except:
            print(driven_variables[i])


    return forecast_chg

