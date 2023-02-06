from lib2to3.pgen2 import driver
from external_python_scripts import aws_database_connector as aws


import pandas as pd
import numpy as np
import datetime

def get_current_mc_mean():

    forecast_source_data = aws.return_source_forecast_data()
    forecast_mc_date = aws.return_market_forecast_data()

    temp_df = forecast_mc_date.loc[forecast_mc_date['Forecast_date'] == forecast_mc_date['Forecast_date'].max()]
    temp_df = temp_df.loc[temp_df['Date_published'] == temp_df['Date_published'].max()]
    sugar_df = temp_df.loc[temp_df['Variable'] == 'NY No.11']
    
    sugar_price = sugar_df['Mean_returned']
    hydrous_price = temp_df['Mean_returned'].loc[temp_df['Variable'] == 'Hydrous Ethanol']
    anhydrous_price = temp_df['Mean_returned'].loc[temp_df['Variable'] == 'Anhydrous Ethanol']
    energy_price = temp_df['Mean_returned'].loc[temp_df['Variable'] == 'Energy Prices']
    fx_rate = temp_df['Mean_returned'].loc[temp_df['Variable'] == 'USDBRL']
    crude_price = temp_df['Mean_returned'].loc[temp_df['Variable'] == 'Brent Crude']
    fertilizer_price = temp_df['Mean_returned'].loc[temp_df['Variable'] == 'Fertilizer Costs']

    #print(forecast_source_data)
    column_ls = list(forecast_source_data['Description'].drop_duplicates())

    inflation_rate = forecast_source_data.loc[forecast_source_data['Description'] == column_ls[1]]
    inflation_rate = inflation_rate.loc[inflation_rate['Forecast_period'] == inflation_rate['Forecast_period'].max()]
    inflation_rate = inflation_rate['Forecasted_value'].loc[inflation_rate['Date_published'] == inflation_rate['Date_published'].max()].values[0]

    selic_rate = forecast_source_data.loc[forecast_source_data['Description'] == column_ls[4]]
    selic_rate = selic_rate.loc[selic_rate['Forecast_period'] == selic_rate['Forecast_period'].max()]
    selic_rate = selic_rate['Forecasted_value'].loc[selic_rate['Date_published'] == selic_rate['Date_published'].max()].values[0]

    foreign_debt_rate = forecast_source_data.loc[forecast_source_data['Description'] == column_ls[3]]
    foreign_debt_rate = foreign_debt_rate.loc[foreign_debt_rate['Forecast_period'] == foreign_debt_rate['Forecast_period'].max()]
    foreign_debt_rate = foreign_debt_rate['Forecasted_value'].loc[foreign_debt_rate['Date_published'] == foreign_debt_rate['Date_published'].max()].values[0]

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

    return new_drivers_dict, new_drivers_ls

def main(new_drivers_dict, new_drivers_ls):

    forecast_baseline = aws.return_forecast_assumptions(0)
    temp_baseline = forecast_baseline.loc[forecast_baseline['Season'] == "2022/23"]

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
    temp_prev_season_df = forecast_baseline.loc[forecast_baseline['Season'] == '2021/22']
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

