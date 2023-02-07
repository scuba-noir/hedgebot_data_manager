import pandas as pd
import numpy as np
import math as m

import warnings
warnings.filterwarnings("ignore")

def Simulate_Three_Statements(assumptions_data_dict, prev_yr_data_dict):

    income_statement_df = Simulate_Income_Statement(assumptions_data_dict)

  
    cash_flow_df, assets_df, liabilities_df = Simulate_Cash_Flow_Statement(assumptions_data_dict, prev_yr_data_dict, income_statement_df)


    financial_indices_df = Simulate_Financial_Indices(assumptions_data_dict, income_statement_df, cash_flow_df, assets_df, liabilities_df)


    return income_statement_df, cash_flow_df, assets_df, liabilities_df, financial_indices_df

def Simulate_Income_Statement(assumptions_data_dict):

    sugar_NY = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Sugar') & (assumptions_data_dict['Data_group'] == 'Price Assumptions')].values[0]
    sugar_production = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Sugar production') & (assumptions_data_dict['Data_group'] == 'Final Volume Forecasts')].values[0]
    usdbrl =assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Exchange rate') & (assumptions_data_dict['Data_group'] == 'Price Assumptions')].values[0]
    hydrous_esalq = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Hydrous') & (assumptions_data_dict['Data_group'] == 'Price Assumptions')].values[0]
    hydrous_production = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Hydrous production') & (assumptions_data_dict['Data_group'] == 'Final Volume Forecasts')].values[0]
    anhydrous_esalq = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Anhydrous') & (assumptions_data_dict['Data_group'] == 'Price Assumptions')].values[0]
    anhydrous_production = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Anhydrous production') & (assumptions_data_dict['Data_group'] == 'Final Volume Forecasts')].values[0]
    energy_px = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Energy') & (assumptions_data_dict['Data_group'] == 'Price Assumptions')].values[0]
    energy_production =assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Energy production') & (assumptions_data_dict['Data_group'] == 'Final Volume Forecasts')].values[0]
    lease_cost_BRL = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Lease cost') & (assumptions_data_dict['Units'] == 'BRL/ha')].values[0]
    leased_area = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Leased area') & (assumptions_data_dict['Units'] == 'ha')].values[0]
    third_party_cane_mt = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Third party cane') & (assumptions_data_dict['Units'] == '000 mt')].values[0]
    third_party_cane_cost_BRLperMT = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Third party cane cost') & (assumptions_data_dict['Units'] == 'BRL/mt of cane')].values[0]
    inputs_BRLperMT = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Inputs') & (assumptions_data_dict['Data_group'] == 'Production Cost Assumptions')].values[0]
    cane_crushed = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Cane crushed') & (assumptions_data_dict['Data_group'] == 'Final Volume Forecasts')].values[0]
    fuel_BRLperMT = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Fuel') & (assumptions_data_dict['Data_group'] == 'Production Cost Assumptions')].values[0]
    freights_perMT = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Freights') & (assumptions_data_dict['Data_group'] == 'Production Cost Assumptions')].values[0]
    labor_cost_perMT = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Labor cost') & (assumptions_data_dict['Data_group'] == 'Production Cost Assumptions')].values[0]
    industrial_cost_perMT = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Industrial cost') & (assumptions_data_dict['Data_group'] == 'Production Cost Assumptions')].values[0]
    depreciation_cost_perMT = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Depreciation') & (assumptions_data_dict['Data_group'] == 'Production Cost Assumptions')].values[0]
    planting_cost_perHa = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Planting cost') & (assumptions_data_dict['Data_group'] == 'Production Cost Assumptions')].values[0]
    planted_area = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Planting area') & (assumptions_data_dict['Data_group'] == 'Own Cane Assumptions')].values[0]
    sales_expenses_perMT = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Sales expenses') & (assumptions_data_dict['Data_group'] == 'SGA Assumptions')].values[0]
    administrative_cost_perMT = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Administrative expenses') & (assumptions_data_dict['Data_group'] == 'SGA Assumptions')].values[0]
    other_SGA_cost_perMT = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Other SG&A') & (assumptions_data_dict['Data_group'] == 'SGA Assumptions')].values[0]
    income_tax_rate = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Income tax rate') & (assumptions_data_dict['Data_group'] == 'Balance Sheet Assumptions')].values[0]
    financial_expenses = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Total financial expenses') & (assumptions_data_dict['Data_group'] == 'Indebtness Assumptions')].values[0]

    sugar_revenues_USD = (sugar_NY * sugar_production * 22.0462) 
    #print('Sugar Production Stuff:'
    #+ '/n' + 'Sugar Price: ' + str(sugar_NY) +
    #'/n' + 'Sugar Production: ' + str(sugar_production) +
    #'/n' + 'Sugar Revenues USD: ' + str(sugar_revenues_USD))
    sugar_revenues_BRL = (sugar_revenues_USD * usdbrl) 
    #print('Sugar Revenues BRL: ' + str(sugar_revenues_BRL))
    hydrous_revenues_BRL = (hydrous_esalq * hydrous_production) 
    anhydrous_revenues_BRL = (anhydrous_esalq * anhydrous_production * 1000) 
    energy_revenues_BRL = (energy_px * energy_production) / 1000
    total_revenues_BRL = (sugar_revenues_BRL + hydrous_revenues_BRL + anhydrous_revenues_BRL + energy_revenues_BRL)
    
    lease_cost = -1 * lease_cost_BRL * leased_area / 1000
    third_party_cane_cost = -1 * third_party_cane_mt * third_party_cane_cost_BRLperMT
    input_cost = -1 * inputs_BRLperMT * cane_crushed
    fuel_cost = -1 * fuel_BRLperMT * cane_crushed
    freight_cost = -1 * freights_perMT * cane_crushed
    labor_cost = -1 * labor_cost_perMT * cane_crushed
    industrial_cost = -1 * industrial_cost_perMT * cane_crushed
    depreciation = -1 * depreciation_cost_perMT * cane_crushed
    planting_cost = -1 * planting_cost_perHa * planted_area / 1000
    total_COGS = lease_cost + third_party_cane_cost + input_cost + fuel_cost + freight_cost + labor_cost + industrial_cost + depreciation + planting_cost
    
    gross_profit = total_revenues_BRL + total_COGS

    sales_expenses = -1 * sales_expenses_perMT * cane_crushed     
    administrative_expenses = -1 * administrative_cost_perMT * cane_crushed      
    other_SGA = -1 * other_SGA_cost_perMT * cane_crushed   
    total_SGA = sales_expenses + administrative_expenses + other_SGA
    
    ebit = gross_profit + total_SGA
            
    profit_before_tax = ebit + (-1*financial_expenses)
    
    if (profit_before_tax > 0):
        
        income_tax = -1 * profit_before_tax * income_tax_rate
    
    else:
        
        income_tax = 0
        
    net_income = profit_before_tax + income_tax
    
    final_df = pd.DataFrame([[sugar_revenues_USD, sugar_revenues_BRL, hydrous_revenues_BRL, anhydrous_revenues_BRL, energy_revenues_BRL, total_revenues_BRL,
                            lease_cost, third_party_cane_cost, input_cost, fuel_cost, freight_cost, labor_cost,
                            industrial_cost, depreciation, planting_cost, total_COGS, gross_profit, sales_expenses, administrative_expenses, 
                            other_SGA, total_SGA, ebit, profit_before_tax, income_tax, net_income, financial_expenses]], 
                    
                        columns = ['Sugar Revenues USD','Sugar Revenues BRL','Hydrous Revenues BRL','Anhydrous Revenues BRL',
                                'Energy Revenues BRL','Total Revenues BRL','Lease Cost BRL','Third Party Cane Cost BRL','Input Cost BRL','Fuel Cost BRL',
                                'Freight Cost BRL','Labor Cost BRL','Industrial Cost BRL','Depreciation BRL','Planting Cost BRL','Total COGS BRL',
                                'Gross Profit BRL','Sales Expenses BRL','Adminstrative Expenses BRL','Other SG&A BRL','Total SG&A BRL','EBIT','Profit Before Tax BRL',
                                'Income Tax BRL','Net Income BRL', 'Financial Expenses BRL'
                                ]
                    )
    
    return final_df

def Simulate_Cash_Flow_Statement(assumptions_data_dict, financial_performance_df, income_statement_df):

    total_revenues = income_statement_df['Total Revenues BRL'].values[0]     
    net_income = income_statement_df['Net Income BRL'].values[0]
    depreciation = income_statement_df['Depreciation BRL'].values[0]
    
    accounts_receivable_days = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Accounts receivable') & (assumptions_data_dict['Data_group'] == 'Balance Sheet Assumptions')].values[0]
    inventory_days = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Inventories') & (assumptions_data_dict['Data_group'] == 'Balance Sheet Assumptions')].values[0]
    other_current_assets_pct = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Other current assets') & (assumptions_data_dict['Data_group'] == 'Balance Sheet Assumptions')].values[0]
    other_nonc_assets_pct = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Other non current assets') & (assumptions_data_dict['Data_group'] == 'Balance Sheet Assumptions')].values[0]
    st_accounts_payable_days = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Short term accounts payable') & (assumptions_data_dict['Data_group'] == 'Balance Sheet Assumptions')].values[0]
    total_COGS = income_statement_df['Total COGS BRL'].values[0]
    other_current_liabilities_pct = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Other current liabilities') & (assumptions_data_dict['Data_group'] == 'Balance Sheet Assumptions')].values[0]
    other_non_current_liabilities_pct = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Other non current liabilities') & (assumptions_data_dict['Data_group'] == 'Balance Sheet Assumptions')].values[0]
    # write_offs = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Write-offs') & (assumptions_data_dict['Data_group'] == 'Cash Flow Statement Forecasts')].values[0]
    write_offs = 0

    st_debt = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Total debt, short term') & (assumptions_data_dict['Data_group'] == 'Indebtness Assumptions')].values[0]
    lt_debt = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Total debt, long term') & (assumptions_data_dict['Data_group'] == 'Indebtness Assumptions')].values[0]
    initial_cash = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Initial cash') & (assumptions_data_dict['Data_group'] == 'Balance Sheet Assumptions')].values[0]
    capex = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'CAPEX') & (assumptions_data_dict['Data_group'] == 'Cash Flow Statement Forecasts')].values[0]

    prev_FY_accounts_receivable = financial_performance_df['Value'].loc[(financial_performance_df['Variable_name_eng'] == 'Accounts receivable') & (financial_performance_df['Data_group'] == 'Asset Sheet Forecasts')].values[0]
    prev_FY_inventories = financial_performance_df['Value'].loc[(financial_performance_df['Variable_name_eng'] == 'Inventories') & (financial_performance_df['Data_group'] == 'Asset Sheet Forecasts')].values[0]
    prev_FY_other_current_assets = financial_performance_df['Value'].loc[(financial_performance_df['Variable_name_eng'] == 'Other current assets') & (financial_performance_df['Data_group'] == 'Asset Sheet Forecasts')].values[0]
    prev_FY_other_non_current_assets = financial_performance_df['Value'].loc[(financial_performance_df['Variable_name_eng'] == 'Other non current assets') & (financial_performance_df['Data_group'] == 'Asset Sheet Forecasts')].values[0]
    prev_FY_st_accounts_payable = financial_performance_df['Value'].loc[(financial_performance_df['Variable_name_eng'] == 'Short term accounts payable') & (financial_performance_df['Data_group'] == 'Liabilities Sheet Forecasts')].values[0]
    prev_FY_other_current_liabilities = financial_performance_df['Value'].loc[(financial_performance_df['Variable_name_eng'] == 'Other current liabilities') & (financial_performance_df['Data_group'] == 'Liabilities Sheet Forecasts')].values[0]
    prev_FY_other_non_current_liabilities =financial_performance_df['Value'].loc[(financial_performance_df['Variable_name_eng'] == 'Other non current liabilities') & (financial_performance_df['Data_group'] == 'Liabilities Sheet Forecasts')].values[0]
    prev_FY_st_debt = financial_performance_df['Value'].loc[(financial_performance_df['Variable_name_eng'] == 'Short term debt') & (financial_performance_df['Data_group'] == 'Liabilities Sheet Forecasts')].values[0]
    prev_FY_lt_debt = financial_performance_df['Value'].loc[(financial_performance_df['Variable_name_eng'] == 'Long term debt') & (financial_performance_df['Data_group'] == 'Liabilities Sheet Forecasts')].values[0]
    
    accounts_receivable = total_revenues / 365 * accounts_receivable_days
    inventories = total_revenues / 365 * inventory_days
    other_current_assets = total_revenues * other_current_assets_pct
    other_non_current_assets = total_revenues * other_nonc_assets_pct
    
    st_accounts_payable = -1 * st_accounts_payable_days * total_COGS / 365 
    other_current_liabilities = -1 * other_current_liabilities_pct * total_COGS
    other_non_current_liabilities = -1 * other_non_current_liabilities_pct * total_COGS
    
    working_capital_variation = (prev_FY_accounts_receivable + prev_FY_inventories + prev_FY_other_current_assets + prev_FY_other_non_current_assets - prev_FY_st_accounts_payable - prev_FY_other_current_liabilities - prev_FY_other_non_current_liabilities) - (accounts_receivable + inventories + other_current_assets + other_non_current_assets - st_accounts_payable - other_current_liabilities - other_non_current_liabilities)    
    cash_flow_from_operations = net_income + depreciation + working_capital_variation     
    cash_flow_from_investment_activities = -1 * capex     
    debt_amortization = -1 * prev_FY_st_debt       
    new_debt = (st_debt + lt_debt) - (prev_FY_st_debt + prev_FY_lt_debt) - debt_amortization   
    cash_flow_from_financing = debt_amortization + new_debt    
    change_in_cash = cash_flow_from_operations + capex + cash_flow_from_financing    
    ending_cash = initial_cash + change_in_cash
    
    assets_df = Simulate_Asset_Sheet(assumptions_data_dict, accounts_receivable, inventories, other_current_assets, other_non_current_assets, ending_cash)
    
    liabilities_df = Simulate_Liabilities_Sheet(assumptions_data_dict, financial_performance_df, net_income, st_accounts_payable, other_current_liabilities, other_non_current_liabilities, st_debt, lt_debt)
    
    final_df = pd.DataFrame([[net_income, depreciation, working_capital_variation, cash_flow_from_operations, capex, write_offs, 
                cash_flow_from_investment_activities, debt_amortization, new_debt, cash_flow_from_financing, change_in_cash, initial_cash, ending_cash]],
                columns = ['Net income (000 R$)','Depreciation (000 R$)','Working capital variation (000 R$)','Cash flow from operations (000 R$)','CAPEX (000 R$)','Write-offs (000 R$)',
                'Cash flow from investment activities (000 R$)','Debt amortization (000 R$)','New debt (000 R$)','Cash flow from financing activities (000 R$)','Change in cash (000 R$)','Initial cash (000 R$)','Ending cash (000 R$)'])
    

    return final_df, assets_df, liabilities_df

def Simulate_Asset_Sheet(assumptions_data_dict, accounts_receivable, inventories, other_current_assets, other_non_current_assets, ending_cash):
    
    cash = ending_cash
    ppe = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'PP&E') & (assumptions_data_dict['Data_group'] == 'Asset Sheet Forecasts')].values[0]
    total_current_assets = cash + accounts_receivable + inventories + other_current_assets
    total_non_current_assets = ppe + other_non_current_assets
    total_assets = total_current_assets + total_non_current_assets
    
    final_df = pd.DataFrame([[cash, accounts_receivable, inventories, other_current_assets, total_current_assets, ppe, other_non_current_assets, total_non_current_assets, total_assets]],
                            columns = ['Cash (000 R$)','Accounts receivable (000 R$)','Inventories (000 R$)','Other current assets (000 R$)','Total current assets (000 R$)','PP&E (000 R$)','Other non current assets (000 R$)','Total non current assets (000 R$)','Total assets (000 R$)'])
    return final_df

def Simulate_Liabilities_Sheet(assumptions_data_dict, financial_performance_df, net_income, st_accounts_payable, other_current_liabilities, other_non_current_liabilities, st_debt, lt_debt):

        total_current_liabilities = st_accounts_payable + st_debt + other_current_liabilities
        total_non_current_liabilities = lt_debt + other_non_current_liabilities
        total_liabilities = total_current_liabilities + total_non_current_liabilities
        issued_capital = assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Issued capital') & (assumptions_data_dict['Data_group'] == 'Balance Sheet Assumptions')].values[0]
        retained_earnings = net_income + assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Retained earnings') & (assumptions_data_dict['Data_group'] == 'Liabilities Sheet Forecasts')].values[0]
        total_equity = issued_capital + retained_earnings
        liabilities_plus_equity = total_liabilities + total_equity
        
        final_df = pd.DataFrame([[st_accounts_payable, st_debt, other_current_liabilities, total_current_liabilities, lt_debt, other_non_current_liabilities, total_non_current_liabilities, total_liabilities, issued_capital, retained_earnings, total_equity, liabilities_plus_equity]],
                                columns = ['Short term accounts payable (000 R$)','Short term debt (000 R$)','Other current liabilities (000 R$)', 'Total current liabilities (000 R$)', 'Long term debt (000 R$)', 'Other non current liabilities (000 R$)','Total non current liabilities (000 R$)','Total liabilities (000 R$)','Issued capital (000 R$)','Retained earnings (000 R$)','Total equity (000 R$)','Liabilities + equity (000 R$)']
                                )
        
        return final_df

def Simulate_Financial_Indices(assumptions_data_dict, income_statement_df, cash_flow_df, assets_df, liabilities_df):

    gross_margin = income_statement_df['Gross Profit BRL'].values[0] / income_statement_df['Total Revenues BRL'].values[0]
    ebitda = income_statement_df['EBIT'].values[0]  + income_statement_df['Depreciation BRL'].values[0]
    ebitda_margin = ebitda / income_statement_df['Total Revenues BRL'].values[0]
    net_margin = income_statement_df['Net Income BRL'].values[0] / income_statement_df['Total Revenues BRL'].values[0]
    net_debt_brl = liabilities_df['Total liabilities (000 R$)'].values[0] - assets_df['Cash (000 R$)'].values[0]
    net_debt_ebitda = net_debt_brl / ebitda
    net_debt_mt_cane = net_debt_brl / assumptions_data_dict['Value'].loc[(assumptions_data_dict['Variable_name_eng'] == 'Cane crushed') & (assumptions_data_dict['Data_group'] == 'Final Volume Forecasts')].values[0]
    indebtness = net_debt_brl / assets_df['Total assets (000 R$)'].values[0]
    st_debt_percent = liabilities_df['Short term debt (000 R$)'].values[0] / liabilities_df['Total liabilities (000 R$)'].values[0]
    current_ratio = assets_df['Total current assets (000 R$)'].values[0] / liabilities_df['Total current liabilities (000 R$)'].values[0]

    final_df = pd.DataFrame([[gross_margin, ebitda, ebitda_margin, net_margin, net_debt_brl, net_debt_ebitda, net_debt_mt_cane, indebtness, st_debt_percent, current_ratio]], 
            columns = ['Gross Margin', 'EBITDA', 'EBITDA Margin', 'Net Margin','Net Debt', 'Net Debt / EBITDA', 'Net Debt / MT of Cane','Indebtness','Short Term Debt Percent','Current Ratio'])

    return final_df

def simulate_large_scale(simulation_date, mc_data, forecast_data):

    forecast_source_data = forecast_data
    mc_forecast_df = mc_data
    mc_forecast_df = mc_forecast_df.loc[mc_forecast_df['Date_published'] == simulation_date]
    mc_forecast_df['Forecast_date'] = pd.to_datetime(mc_forecast_df['Forecast_date'], format = "%Y-%m-%d")
    mc_forecast_df = mc_forecast_df.loc[mc_forecast_df['Forecast_date'] == mc_forecast_df['Forecast_date'].max()]

    sugar_price = mc_forecast_df.loc[mc_forecast_df['Variable'] == 'NY No.11']
    sugar_mu = sugar_price['Mean_returned'].values[0]
    sugar_std = sugar_price['Std'].values[0]
    sugar_price = np.random.normal(sugar_mu, sugar_std, 1000)

    hydrous_price = mc_forecast_df.loc[mc_forecast_df['Variable'] == 'Hydrous Ethanol']
    hydrous_mu = hydrous_price['Mean_returned'].values[0]
    hydrous_std = hydrous_price['Std'].values[0]
    hydrous_price = np.random.normal(hydrous_mu, hydrous_std, 1000)

    anhydrous_price = mc_forecast_df.loc[mc_forecast_df['Variable'] == 'Anhydrous Ethanol']
    anhydrous_mu = anhydrous_price['Mean_returned'].values[0]
    anhydrous_std = anhydrous_price['Std'].values[0]
    anhydrous_price = np.random.normal(anhydrous_mu, anhydrous_std, 1000)

    energy_price = mc_forecast_df.loc[mc_forecast_df['Variable'] == 'Energy Prices']
    energy_mu = energy_price['Mean_returned'].values[0]
    energy_std = energy_price['Std'].values[0]
    energy_price = np.random.normal(energy_mu, energy_std, 1000)

    fx_rate = mc_forecast_df.loc[mc_forecast_df['Variable'] == 'USDBRL']
    fx_mu = fx_rate['Mean_returned'].values[0]
    fx_std = fx_rate['Std'].values[0]
    fx_rate = np.random.normal(fx_mu, fx_std, 1000)

    crude_price = mc_forecast_df.loc[mc_forecast_df['Variable'] == 'Brent Crude']
    crude_mu = crude_price['Mean_returned'].values[0]
    crude_std = crude_price['Std'].values[0]
    crude_price = np.random.normal(crude_mu, crude_std, 1000)

    fertilizer_price = mc_forecast_df.loc[mc_forecast_df['Variable'] == 'Fertilizer Costs']
    fert_mu = fertilizer_price['Mean_returned'].values[0]
    fert_std = fertilizer_price['Std'].values[0]
    #fertilizer_price = np.random.normal(fert_mu, fert_std, 1000).mean()
    fertilizer_price = np.random.normal(fert_mu, fert_std, 1000)

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

    market_mc_data = pd.DataFrame({'NY No.11':list(sugar_price), 'Hydrous Ethanol':list(hydrous_price), 'Anhydrous Ethanol':list(anhydrous_price), 'Energy Prices':list(energy_price), 'USDBRL':list(fx_rate), 'Brent Crude':list(crude_price), 'Fertilizer Costs':list(fertilizer_price)})

    for i in range(0,1):
        
        new_drivers_ls = [sugar_price[i], hydrous_price[i], anhydrous_price[i], energy_price[i], fx_rate[i], selic_rate, foreign_debt_rate, inflation_rate, crude_price[i], fertilizer_price[i]]

        new_drivers_dict = {
            'Sugar':sugar_price[i], 
            'Hydrous':hydrous_price[i],
            'Anhydrous':anhydrous_price[i], 
            'Energy':energy_price[i], 
            'Exchange rate':fx_rate[i], 
            'Domestic interest rate':selic_rate, 
            'Foreign interest rate':foreign_debt_rate, 
            'Inflation':inflation_rate, 
            'Crude oil':crude_price[i], 
            'Fertilizers':fertilizer_price[i]
        }

        forecast_chg = create_assumptions_dict.main(new_drivers_dict, new_drivers_ls)

        prev_year_financial_df = aws.return_forecast_assumptions(0)
        prev_year_financial_df = prev_year_financial_df.loc[prev_year_financial_df['Season'] == '2023/24']

        temp_income_statement_df, temp_cash_flow_df, temp_assets_df, temp_liabilities_df, temp_financial_indices_df = Simulate_Three_Statements(forecast_chg, prev_year_financial_df)

        if i == 0:

            income_statement_final_df = pd.DataFrame(temp_income_statement_df)
            cash_flow_final_df = pd.DataFrame(temp_cash_flow_df)
            assets_final_df = pd.DataFrame(temp_assets_df)
            liabilities_final_df = pd.DataFrame(temp_liabilities_df)
            financial_indices_final_df = pd.DataFrame(temp_financial_indices_df)

        else:

            income_statement_final_df = pd.concat([income_statement_final_df, temp_income_statement_df])
            cash_flow_final_df = pd.concat([cash_flow_final_df, temp_cash_flow_df])
            assets_final_df = pd.concat([assets_final_df, temp_assets_df])
            liabilities_final_df = pd.concat([liabilities_final_df, temp_liabilities_df])
            financial_indices_final_df = pd.concat([financial_indices_final_df, temp_financial_indices_df])

    return income_statement_final_df, cash_flow_final_df, assets_final_df, liabilities_final_df, financial_indices_final_df, market_mc_data

def aggregate_fin_sim_results(income_statement_final_df, cash_flow_final_df, assets_final_df, liabilities_final_df, financial_indices_final_df):

    final_df = []
    account_ls = []
    mu_ls = []
    std_ls = []
    columns_ls = income_statement_final_df.columns.to_list()
    for i in range(0,len(columns_ls)):
        account_ls.append(columns_ls[i])
        mu_ls.append(income_statement_final_df[columns_ls[i]].mean())
        std_ls.append(income_statement_final_df[columns_ls[i]].std())

    
    column_ls_2 = cash_flow_final_df.columns.to_list()
    for z in range(0,len(column_ls_2)):
        account_ls.append(column_ls_2[z])
        mu_ls.append(cash_flow_final_df[column_ls_2[z]].mean())
        std_ls.append(cash_flow_final_df[column_ls_2[z]].std())

    column_ls_3 = assets_final_df.columns.to_list()
    for t in range(0,len(column_ls_3)):
        account_ls.append(column_ls_3[t])
        mu_ls.append(assets_final_df[column_ls_3[t]].mean())
        std_ls.append(assets_final_df[column_ls_3[t]].std())

    column_ls_4 = liabilities_final_df.columns.to_list()
    for x in range(0,len(column_ls_4)):
        account_ls.append(column_ls_4[x])
        mu_ls.append(liabilities_final_df[column_ls_4[x]].mean())
        std_ls.append(liabilities_final_df[column_ls_4[x]].std())

    column_ls_5 = financial_indices_final_df.columns.to_list()
    for w in range(0,len(column_ls_5)):
        account_ls.append(column_ls_5[w])
        mu_ls.append(financial_indices_final_df[column_ls_5[w]].mean())
        std_ls.append(financial_indices_final_df[column_ls_5[w]].std())

    final_ls = []
    final_df = pd.DataFrame(account_ls, columns = ['Account'])
    final_df['Mean Returned'] = mu_ls
    final_df['STD Returned'] = std_ls

    return final_df

def main(date_ls, date_boolean):

    if date_boolean == False:
        simulation_dates = ['2022-09-01']
    else:
        simulation_dates = date_ls
    final_df = []
    for q in range(0,len(simulation_dates)):
        income_statement_final_df, cash_flow_final_df, assets_final_df, liabilities_final_df, financial_indices_final_df = simulate_large_scale(simulation_dates[q])
        account_ls = []
        mu_ls = []
        std_ls = []
        columns_ls = income_statement_final_df.columns.to_list()
        for i in range(0,len(columns_ls)):
            account_ls.append(columns_ls[i])
            mu_ls.append(income_statement_final_df[columns_ls[i]].mean())
            std_ls.append(income_statement_final_df[columns_ls[i]].std())

        
        column_ls_2 = cash_flow_final_df.columns.to_list()
        for z in range(0,len(column_ls_2)):
            account_ls.append(column_ls_2[z])
            mu_ls.append(cash_flow_final_df[column_ls_2[z]].mean())
            std_ls.append(cash_flow_final_df[column_ls_2[z]].std())

        column_ls_3 = assets_final_df.columns.to_list()
        for t in range(0,len(column_ls_3)):
            account_ls.append(column_ls_3[t])
            mu_ls.append(assets_final_df[column_ls_3[t]].mean())
            std_ls.append(assets_final_df[column_ls_3[t]].std())

        column_ls_4 = liabilities_final_df.columns.to_list()
        for x in range(0,len(column_ls_4)):
            account_ls.append(column_ls_4[x])
            mu_ls.append(liabilities_final_df[column_ls_4[x]].mean())
            std_ls.append(liabilities_final_df[column_ls_4[x]].std())

        column_ls_5 = financial_indices_final_df.columns.to_list()
        for w in range(0,len(column_ls_5)):
            account_ls.append(column_ls_5[w])
            mu_ls.append(financial_indices_final_df[column_ls_5[w]].mean())
            std_ls.append(financial_indices_final_df[column_ls_5[w]].std())

        final_ls = []


        if q == 0:
            final_df = pd.DataFrame(account_ls, columns = ['Account'])
            final_df['Mean Returned'] = mu_ls
            final_df['STD Returned'] = std_ls
            final_df['Simulation Date'] = simulation_dates[q]
        else:
            temp_df = pd.DataFrame(account_ls, columns = ['Account'])
            temp_df['Mean Returned'] = mu_ls
            temp_df['STD Returned'] = std_ls        
            temp_df['Simulation Date'] = simulation_dates[q]
            final_df = pd.concat([final_df, temp_df])

    return(final_df)
