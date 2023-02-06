# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 17:46:55 2021

@author: ChristopherTHOMPSON
"""

import pandas as pd
import datetime as datetime
import numpy as np
import math

class sugar_Mill():
    
    def __init__(self, identifier, attribute_matrix, financial_performance_df, assumptions_df, initial_portfolio, target_price_sugar, start_date):
        self.identifier = identifier
        self.attribute_matrix = attribute_matrix
        self.financial_performance_df = financial_performance_df
        self.assumptions_df = assumptions_df
        self.weighted_price, self.unhedged_volumes, self.hedged_volumes, self.fixed_revenues = self.portfolio_Organizer(initial_portfolio)
        self.target_price_sugar = target_price_sugar
        self.current_price_mar = 0 
        self.current_price_may = 0
        self.current_price_jul = 0
        self.current_price_oct = 0
        self.current_price_mar2 = 0
        self.record_book = self.initiate_Records(start_date, self.weighted_price, self.unhedged_volumes, self.hedged_volumes, self.fixed_revenues, self.target_price_sugar, self.current_price_mar, self.current_price_may, self.current_price_jul, self.current_price_oct, self.current_price_mar2)
        #self.update_Records = self.update_Records(self.record_book, start_date, self.weighted_price, self.unhedged_volumes, self.hedged_volumes, self.fixed_revenues)
        self.hedge_attempts = 0
        
    def initiate_Records(self, start_date, weighted_price, unhedged_volumes, hedged_volumes, fixed_revenues, target_price, current_price_mar, current_price_may, current_price_jul, current_price_oct, current_price_mar2):
        unhedged_volumes_mar1 = unhedged_volumes[0]
        unhedged_volumes_may = unhedged_volumes[1]
        unhedged_volumes_jul = unhedged_volumes[2]
        unhedged_volumes_oct = unhedged_volumes[3]
        unhedged_volumes_mar2 = unhedged_volumes[4]
        x = pd.DataFrame([[self.identifier, start_date, weighted_price, unhedged_volumes_mar1, unhedged_volumes_may, unhedged_volumes_jul, unhedged_volumes_oct, unhedged_volumes_mar2, hedged_volumes, fixed_revenues, 0, 0, 0, 0, 0, target_price, current_price_mar, current_price_may, current_price_jul, current_price_oct, current_price_mar2, self.attribute_matrix[0], self.attribute_matrix[1], self.attribute_matrix[2], self.attribute_matrix[3], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], columns = ['Identity','Date', 'Weighted Average Price','Unhedged Volumes Mar 1','Unhedged Volumes May','Unhedged Volumes Jul','Unhedged Volumes Oct', 'Unhedged Volumes Mar 2','Hedged Volumes','Fixed Revenues', 'Hedge Boolean', 'Hedge Boolean B','Hedge Boolean C','Hedge Boolean D', 'Hedge Boolean E','Target Price','Current Price Mar','Current Price May','Current Price Jul','Current Price Oct','Current Price Mar 2', 'Attribute A', 'Attribute B','Attribute C','Attribute D', 'ST_A','ST_B','ST_C','ST_D','ST_E','MT_A','MT_B','MT_C','MT_D','MT_E', 'Mar1 VaR','May VaR','Jul VaR','Oct VaR','Mar2 VaR'])
        return x
    
    def update_Records(self, start_date, weighted_price, unhedged_volumes, hedged_volumes, fixed_revenues, hedge_boolean, hedge_boolean_b, hedge_boolean_c, hedge_boolean_d, hedge_boolean_e, current_price_mar, current_price_may, current_price_jul, current_price_oct, current_price_mar2, ST_a, ST_b, ST_c, ST_d, ST_e, MT_a, MT_b, MT_c, MT_d, MT_e, mar1_VaR, may_VaR, jul_VaR, oct_VaR, mar2_VaR):
        unhedged_volumes_mar1 = self.unhedged_volumes[0]
        unhedged_volumes_may = self.unhedged_volumes[1]
        unhedged_volumes_jul = self.unhedged_volumes[2]
        unhedged_volumes_oct = self.unhedged_volumes[3]
        unhedged_volumes_mar2 = self.unhedged_volumes[4]
        
        """
        print('---------')
        print('Mill Identifier: ' + str(self.identifier))
        print('Date: ' + str(start_date))
        print('Weighted Price: ' + str(weighted_price))
        print('Unhedged Volumes: ' + str(unhedged_volumes))
        print('Hedged Volumes: ' + str(hedged_volumes))
        print('Fixed Revenues: ' + str(fixed_revenues))
        print('---------')
        """
        self.record_book = self.record_book.append(pd.DataFrame([[self.identifier, start_date, weighted_price, unhedged_volumes_mar1, unhedged_volumes_may, unhedged_volumes_jul, unhedged_volumes_oct, unhedged_volumes_mar2, hedged_volumes, fixed_revenues, hedge_boolean, hedge_boolean_b, hedge_boolean_c, hedge_boolean_d, hedge_boolean_e, self.target_price_sugar, current_price_mar, current_price_may, current_price_jul, current_price_oct, current_price_mar2, self.attribute_matrix[0], self.attribute_matrix[1], self.attribute_matrix[2], self.attribute_matrix[3],  ST_a, ST_b, ST_c, ST_d, ST_e, MT_a, MT_b, MT_c, MT_d, MT_e, mar1_VaR, may_VaR, jul_VaR, oct_VaR, mar2_VaR]], columns = self.record_book.columns))
        
    def hedge_Decision(self, last_date, prev_values, ST_pred_y, MT_pred_y, fundamental_indicator, price_data, expirations):
        
        mar_expiry = expirations[0]
        may_expiry = expirations[1]
        jul_expiry = expirations[2]
        oct_expiry = expirations[3]
        mar_2_expiry = expirations[4]
                
        length_mar = (mar_expiry - last_date).days
        length_may = (may_expiry - last_date).days
        length_jul = (jul_expiry - last_date).days
        length_oct = (oct_expiry - last_date).days
        length_mar_2 = (mar_2_expiry - last_date).days
        
        time_till_expiry = [length_mar, length_may, length_jul, length_oct, length_mar_2]
        
        #mar1_VaR, may_VaR, jul_VaR, oct_VaR, mar2_VaR = self.calc_VaR(price_data, time_till_expiry, last_date)
        
        try:
            ST_a = ST_pred_y[0]
        except:
            ST_a = 0
        try:
            ST_b = ST_pred_y[1]
        except:
            ST_b = 0
        try:
            ST_c = ST_pred_y[2]
        except:
            ST_c = 0
        try:
            ST_d = ST_pred_y[3]
        except:
            ST_d = 0
        try:
            ST_e = ST_pred_y[4]
        except:
            ST_e = 0
            
        try:
            MT_a = MT_pred_y[0]
        except:
            MT_a = 0
        try:
            MT_b = MT_pred_y[1]
        except:
            MT_b = 0
        try:
            MT_c = MT_pred_y[2]
        except:
            MT_c = 0
        try:
            MT_d = MT_pred_y[3]
        except:
            MT_d = 0
        try:
            MT_e = MT_pred_y[4]
        except:
            MT_e = 0
         
            
        difference = len(time_till_expiry) - len(ST_pred_y)
        prev_values = list(prev_values)
        for i in range(0,difference):
            time_till_expiry.pop(0)
            prev_values.pop(0)
        
        check_st = 0
        check_mt = 0
        check_f = 0
        check_roll = 0
        
        if (self.attribute_matrix[0] == 1):
            check_st = False
        else:
            check_st = 0
        
        if (self.attribute_matrix[1] == 1):
            check_mt = False
        else:
            check_mt = 0
            
        if (self.attribute_matrix[2] == 1):
            check_f = False
        else:
            check_f = 0
            
        if (self.attribute_matrix[3] == 1):
            check_roll = False
        else:
            check_roll = 0
        
        contract_checks = np.zeros((len(ST_pred_y), 4))
        contract_checks = pd.DataFrame(contract_checks)
        
        for i in range(0,contract_checks.shape[0]):
            contract_checks.iat[i,0] = check_st
            contract_checks.iat[i,1] = check_mt
            contract_checks.iat[i,2] = check_f
            contract_checks.iat[i,3] = check_roll
            
        for z in range(0, contract_checks.shape[0]):
            
            if (prev_values[z] > self.target_price_sugar):
                try:
                    if ((check_st == False) and (ST_pred_y[z] < 0) and (prev_values[z] > self.target_price_sugar)):
                    
                        contract_checks.iat[z,1] = True
                except:
                    print(ST_pred_y[z])
                    print(prev_values[z])
                    print(check_st)
                    print(self.target_price_sugar)
                    
                if ((check_mt == False) and (MT_pred_y[z] < 0) and (prev_values[z] > self.target_price_sugar)):
                    
                    contract_checks.iat[z,1] = True
                    
                if ((check_f == False) and (fundamental_indicator[z] < self.target_price_sugar) and (prev_values[z] > self.target_price_sugar)):
                    
                    contract_checks.iat[z,2] = True
                    
                if((check_roll == False) and (time_till_expiry[z] > 15)):
                    
                    contract_checks.iat[z,3] = False
                    
            elif(prev_values[z] < self.target_price_sugar):
                
                if ((check_roll == False) and (time_till_expiry[z] <= 15) and (ST_pred_y[z] < 0)):
                    
                    contract_checks.iat[z,3] = True
                    
                elif ((check_roll == False) and (time_till_expiry[z] <= 10)):
                    
                    contract_checks.iat[z,3] = True

        
        final_checks = np.zeros(len(contract_checks))
        final_checks = pd.DataFrame(final_checks)

        for q in range(0, contract_checks.shape[0]):
            
            if (contract_checks.iat[q,3] == True):
                final_checks[q] = True
                
            elif (any(contract_checks.loc[q,:])):
                final_checks[q] = True  
                
            else:
                final_checks[q] = False
                
        hedge_boolean = 0
        hedge_boolean_b = 0
        hedge_boolean_c = 0
        hedge_boolean_d = 0
        hedge_boolean_e = 0

        for zz in range(0, final_checks.shape[0]):
            
            if (any(final_checks[zz])):
                
                self.hedge_Sugar(prev_values, last_date, zz, time_till_expiry)
                
                if (zz == 0):
                    hedge_boolean = 1
                elif(zz == 1):
                    hedge_boolean_b = 1
                elif(zz == 2):
                    hedge_boolean_c = 1
                elif(zz == 3):
                    hedge_boolean_d = 1
                elif (zz == 4):
                    hedge_boolean_e = 1
                    
        if (hedge_boolean == 1 or hedge_boolean_b == 1 or hedge_boolean_c == 1 or hedge_boolean_d == 1 or hedge_boolean_e == 1):
            self.hedge_attempts = self.hedge_attempts + 1
            
        for zzz in range(0, 5 - len(prev_values)):
            prev_values.insert(0,0)
            
        curr_price_mar = prev_values[0]
        curr_price_may = prev_values[1]
        curr_price_jul = prev_values[2]
        curr_price_oct = prev_values[3]
        curr_price_mar2 = prev_values[4]
        mar1_VaR = 0
        may_VaR = 0
        jul_VaR = 0 
        oct_VaR =  0
        mar2_VaR = 0
            
        self.update_Records(last_date, self.weighted_price, self.unhedged_volumes, self.hedged_volumes, self.fixed_revenues, hedge_boolean, hedge_boolean_b, hedge_boolean_c, hedge_boolean_d, hedge_boolean_e, curr_price_mar, curr_price_may, curr_price_jul, curr_price_oct, curr_price_mar2, ST_a, ST_b, ST_c, ST_d, ST_e, MT_a, MT_b, MT_c, MT_d, MT_e, mar1_VaR, may_VaR, jul_VaR, oct_VaR, mar2_VaR)

    def hedge_Sugar(self, prices, last_date, zz, time_till_expiry):
        """
        print('-----------')
        print('Start Hedge')
        print('Contract No: ' + str(zz + 1) + ' -> Out of -> ' + str(len(prices)))
        print('Prices All: ' + str(prices))
        print('Prev Date: ' + str(last_date))
        print('Mill No: ' + str(self.identifier))
        """
        
        available_volumes = self.unhedged_volumes.copy()
        contracts_remaining = len(prices)
        additional_vols = 0
        i_ls = []
        
        if contracts_remaining < 5:
            for i in range (0,(len(self.unhedged_volumes) - contracts_remaining)):
                i_ls.append(i)
                additional_vols = additional_vols + available_volumes.pop((0))

        temp_len = len(i_ls.copy())
        for i in range(0,temp_len):
            x = i_ls.pop()
            self.unhedged_volumes[x] = 0
            
        
        current_contract_unhedge_volumes = self.unhedged_volumes[zz + (len(self.unhedged_volumes) - contracts_remaining)]
        total_volumes = additional_vols + current_contract_unhedge_volumes
        
        """
        print('Unhedged Volumes Ls: ' + str(self.unhedged_volumes))
        print('Total Volumes: ' + str(total_volumes))
        print('Current Contract Volumes: ' + str(current_contract_unhedge_volumes))
        print('ZZ: ' + str(zz))
        print('Length A: ' + str(len(self.unhedged_volumes)))
        print('Contracts Remaining: ' + str(contracts_remaining))
        print('Additional Volumes: ' + str(additional_vols))
        """
        
        if (total_volumes > 0):
            """
            print('-----------')
            print('Start Hedge')
            print('Contract No: ' + str(zz + 1) + ' -> Out of -> ' + str(len(prices)))
            print('Prices All: ' + str(prices))
            print('Prev Date: ' + str(last_date))
            print('Mill No: ' + str(self.identifier))
            print('Original Unhedged List:  ' + str(orig_unhedged))
            """
            
            try:
                remaining_time_season = float(time_till_expiry[zz + (len(self.unhedged_volumes) - contracts_remaining)] / 7.0)
            except:
                print(zz)
                print(len(self.unhedged_volumes))
                print(contracts_remaining)
                print(time_till_expiry)
                remaining_time_season = time_till_expiry[0]
            try:
                initial_success_rate = self.hedge_attempts / float((last_date - today).days / 7.0)
                if (initial_success_rate <= 0):
                    raise ValueError
            except:
                initial_success_rate = 0.75
            
            if (remaining_time_season > 0):
                attempts_future = remaining_time_season * (initial_success_rate)
                rand_n = np.random.randint(80,150)
                rand_n = rand_n / 100
                volumes_to_hedge = (total_volumes / attempts_future) * rand_n
                                
                if (volumes_to_hedge > total_volumes):
                    volumes_to_hedge = total_volumes
                elif (volumes_to_hedge < 0):
                    print('Negative Volumes to Hedge')
                    volumes_to_hedge = 0
                
                remaining_volumes = total_volumes - volumes_to_hedge
                self.fixed_revenues = self.fixed_revenues + (volumes_to_hedge * prices[zz] * (2204.26/100))
                self.hedged_volumes = self.hedged_volumes + (volumes_to_hedge)
                self.unhedged_volumes[zz + (len(self.unhedged_volumes) - contracts_remaining)] = remaining_volumes
                self.weighted_price = self.fixed_revenues / self.hedged_volumes * (100/2204.62)

        
    def portfolio_Organizer(self, initial_portfolio):
        
        fixed_volumes = initial_portfolio['Fixed'].sum()
        unfixed_volumes = []
        unfixed_volumes.append(initial_portfolio['To Sell'].loc[initial_portfolio['Contract'] == 'H22'].sum())
        unfixed_volumes.append(initial_portfolio['To Sell'].loc[initial_portfolio['Contract'] == 'K22'].sum())
        unfixed_volumes.append(initial_portfolio['To Sell'].loc[initial_portfolio['Contract'] == 'N22'].sum())                     
        unfixed_volumes.append(initial_portfolio['To Sell'].loc[initial_portfolio['Contract'] == 'V22'].sum())
        if (initial_portfolio['To Sell'].loc[initial_portfolio['Contract'] == 'H23'].sum() > 0):
            unfixed_volumes.append(initial_portfolio['To Sell'].loc[initial_portfolio['Contract'] == 'H23'].sum())
        else:
            unfixed_volumes.append(0)
            
        average_price = 0
        revenues = 0
        volumes = 0
        
        for i in range(0,initial_portfolio['Fixed'].shape[0]):
            
            if (initial_portfolio['Fixed'].iat[i] > 0):
                
                if (initial_portfolio['Average Price (2)'].iat[i] > 0):
                    
                    revenues = revenues + initial_portfolio['Fixed'].iat[i] * initial_portfolio['Average Price (2)'].iat[i] * (2204.62/100)
                    volumes = volumes + initial_portfolio['Fixed'].iat[i]
                    
                else:
                    revenues = revenues + initial_portfolio['Fixed'].iat[i] * initial_portfolio['Average Price'].iat[i] * (2204.62/100)
                    volumes = volumes + initial_portfolio['Fixed'].iat[i]
        
        fixed_volumes = volumes
        average_price = revenues / volumes * (100/2204.62)
        
        return 0, unfixed_volumes, 0, 0
        return average_price, unfixed_volumes, fixed_volumes, revenues
        
    def run_Full_Sim(self, i):
        
        i = 0
        
    def simulate_IS(self, assumptions_ls):
        
        sugar_NY = assumptions_ls[0]
        sugar_production = assumptions_ls[1]
        USDBRL = assumptions_ls[2]
        hydrous_esalq = assumptions_ls[3]
        hydrous_production = assumptions_ls[4]
        anhydrous_esalq = assumptions_ls[5]
        anhydrous_production = assumptions_ls[6]
        energy_px = assumptions_ls[7]
        energy_production = assumptions_ls[8]
        lease_cost_BRL = assumptions_ls[9]
        leased_area = assumptions_ls[10]
        third_party_cane_mt = assumptions_ls[11]
        third_party_cane_cost_BRLperMT = assumptions_ls[12]
        inputs_BRLperMT = assumptions_ls[13]
        cane_crushed = assumptions_ls[14]
        fuel_BRLperMT = assumptions_ls[15]
        freights_perMT = assumptions_ls[16]
        labor_cost_perMT = assumptions_ls[17]
        industrial_cost_perMT = assumptions_ls[18]
        depreciation_cost_perMT = assumptions_ls[19]
        planting_cost_perHa = assumptions_ls[20]
        planted_area = assumptions_ls[21]
        sales_expenses_perMT = assumptions_ls[22]
        administrative_cost_perMT = assumptions_ls[23]
        other_SGA_cost_perMT = assumptions_ls[24]
        income_tax_rate = assumptions_ls[25]
        financial_expenses = assumptions_ls[26]
        
        sugar_revenues_USD = sugar_NY * sugar_production * 22.0462
        sugar_revenues_BRL = sugar_revenues_USD * USDBRL
        hydrous_revenues_BRL = hydrous_esalq * hydrous_production
        anhydrous_revenues_BRL = anhydrous_esalq * anhydrous_production
        energy_revenues_BRL = energy_px * energy_production / 1000
        total_revenues_BRL = sugar_revenues_BRL + hydrous_revenues_BRL + anhydrous_revenues_BRL + energy_revenues_BRL
        
        lease_cost = -1 * lease_cost_BRL * leased_area / 1000
        third_party_cane_cost = third_party_cane_mt * third_party_cane_cost_BRLperMT
        input_cost = -1 * inputs_BRLperMT * cane_crushed
        fuel_cost = -1 * fuel_BRLperMT * cane_crushed
        freight_cost = -1 * freights_perMT * cane_crushed
        labor_cost = -1 * labor_cost_perMT * cane_crushed
        industrial_cost = -1 * industrial_cost_perMT * cane_crushed
        depreciation = -1 * depreciation_cost_perMT * cane_crushed
        planting_cost = -1 * planting_cost_perHa * planted_area
        total_COGS = lease_cost + third_party_cane_cost + input_cost + fuel_cost + freight_cost + labor_cost + industrial_cost + depreciation + planting_cost
        
        gross_profit = total_revenues_BRL + total_COGS
    
        sales_expenses = -1 * sales_expenses_perMT * cane_crushed     
        administrative_expenses = -1 * administrative_cost_perMT * cane_crushed      
        other_SGA = -1 * other_SGA_cost_perMT * cane_crushed   
        total_SGA = sales_expenses + administrative_expenses + other_SGA
        
        EBIT = gross_profit + total_SGA
                
        profit_before_tax = EBIT + financial_expenses
        
        if (profit_before_tax > 0):
            
            income_tax = -1 * profit_before_tax * income_tax_rate
        
        else:
            
            income_tax = 0
            
        net_income = profit_before_tax + income_tax
        
        final_df = pd.DataFrame([sugar_revenues_USD, sugar_revenues_BRL, hydrous_revenues_BRL, anhydrous_revenues_BRL, energy_revenues_BRL, total_revenues_BRL,
                                 lease_cost, third_party_cane_cost, input_cost, fuel_cost, freight_cost, labor_cost,
                                 industrial_cost, depreciation, planting_cost, total_COGS, gross_profit, sales_expenses, administrative_expenses, 
                                 other_SGA, total_SGA, EBIT, profit_before_tax, income_tax, net_income], 
                           
                            columns = ['Sugar Revenues USD','Sugar Revenues BRL','Hydrous Revenues BRL','Anhydrous Revenues BRL',
                                     'Energy Revenues BRL','Total Revenues BRL','Lease Cost BRL','Third Party Cane Cost BRL','Input Cost BRL','Fuel Cost BRL',
                                     'Freight Cost BRL','Labor Cost BRL','Industrial Cost BRL','Depreciation BRL','Planting Cost BRL','Total COGS BRL',
                                     'Gross Profit BRL','Sales Expenses BRL','Adminstrative Expenses BRL','Other SG&A BRL','Total SG&A BRL','EBIT','Profit Before Tax BRL',
                                     'Net Income BRL'
                                     ]
                        )
        
        return final_df
        
        
    def simulate_CF(self, income_statement_df, assumptions_df, financial_performance_df):
        
        total_revenues = income_statement_df['Total Revenues BRL'].values[0]     
        net_income = income_statement_df['Net Income BRL'].values[0]
        depreciation = income_statement_df['Depreciation BRL'].values[0]
        
        accounts_receivable_days = assumptions_df['Accounts receivable (days)'].values[0]
        inventory_days = assumptions_df['Inventories (days)'].values[0]
        other_current_assets_pct = assumptions_df['Other current assets (% of revenues)'].values[0]
        other_nonc_assets_pct = assumptions_df['Other non current assets (% of revenues)'].values[0]
        st_accounts_payable_days = assumptions_df['Short term accounts payable (days)'].values[0]
        total_COGS = income_statement_df['Total COGS BRL'].values[0]
        other_current_liabilities_pct = assumptions_df['Other current liabilities (% of COGS)'].values[0]
        other_non_current_liabilities_pct = assumptions_df['Other non current liabilities (% of COGS)'].values[0]
        write_offs = assumptions_df['Write-offs (000 R$)'].values[0]
        st_debt = assumptions_df['Total debt, short term (000 R$)'].values[0]
        lt_debt = assumptions_df['Total debt, long term (000 R$)'].values[0]
        initial_cash = assumptions_df['Initial cash (000 R$)'].values[0]
        
        prev_FY_accounts_receivable = financial_performance_df['Accounts receivable (000 R$)'].values[0]
        prev_FY_inventories = financial_performance_df['Inventories (000 R$)'].values[0]
        prev_FY_other_current_assets = financial_performance_df['Other Current Assets (000 R$)'].values[0]
        prev_FY_other_non_current_assets = financial_performance_df['Other non current assets (000 R$)'].values[0]
        prev_FY_st_accounts_payable = financial_performance_df['Short term accounts payable (000 R$)'].values[0]
        prev_FY_other_current_liabilities = financial_performance_df['Other current liabilities (000 R$)'].values[0]
        prev_FY_other_non_current_liabilities = financial_performance_df['Other non current liabilities (000 R$)'].values[0]
        prev_FY_st_debt = financial_performance_df['Short term debt (000 R$)'].values[0]
        prev_FY_lt_debt = financial_performance_df['Long term debt (000 R$)'].values[0]
        
        accounts_receivable = total_revenues / 365 * accounts_receivable_days
        inventories = total_revenues / 365 * inventory_days
        other_current_assets = total_revenues * other_current_assets_pct
        other_non_current_assets = total_revenues * other_nonc_assets_pct
        
        st_accounts_payable = -1 * st_accounts_payable_days * total_COGS / 365 
        other_current_liabilities = -1 * other_current_liabilities_pct * total_COGS
        other_non_current_liabilities = -1 * other_non_current_liabilities_pct * total_COGS
        
        working_capital_variation = (prev_FY_accounts_receivable + prev_FY_inventories + prev_FY_other_current_assets + prev_FY_other_non_current_assets - prev_FY_st_accounts_payable - prev_FY_other_current_liabilities - prev_FY_other_non_current_liabilities) - (accounts_receivable + inventories + other_current_assets + other_non_current_assets - st_accounts_payable - other_current_liabilities - other_non_current_liabilities)    
        cash_flow_from_operations = net_income + depreciation + working_capital_variation     
        capex = get_CAPEX('Total (Domestic Currency)')     
        cash_flow_from_investment_activities = -1 * capex + write_offs      
        debt_amortization = -1 * prev_FY_st_debt       
        new_debt = (st_debt + lt_debt) - (prev_FY_st_debt + prev_FY_lt_debt) - debt_amortization   
        cash_flow_from_financing = debt_amortization + new_debt    
        change_in_cash = cash_flow_from_operations + capex + cash_flow_from_financing    
        ending_cash = initial_cash + change_in_cash
        
        assets_df = self.simulate_Assets(accounts_receivable, inventories, other_current_assets, other_non_current_assets, ending_cash)
        
        liabilities_df = self.simulate_Liabilities(assumptions_df, financial_performance_df, net_income, st_accounts_payable, other_current_liabilities, other_non_current_liabilities, st_debt, lt_debt, other_current_liabilities)
        
        final_df = pd.DataFrame([net_income, depreciation, working_capital_variation, cash_flow_from_operations, capex, write_offs, cash_flow_from_investment_activities, debt_amortization, new_debt, cash_flow_from_financing, change_in_cash, ending_cash],
                    columns = ['Net income (000 R$)','Depreciation (000 R$)','Working capital variation (000 R$)','Cash flow from operations (000 R$)','CAPEX (000 R$)','Write-offs (000 R$)','Cash flow from investment activities (000 R$)','Debt amortization (000 R$)','New debt (000 R$)','Cash flow from financing activities (000 R$)','Change in cash (000 R$)','Initial cash (000 R$)','Ending cash (000 R$)'])
        
        """
        Net income (000 R$)
        Depreciation (000 R$)
        Working capital variation (000 R$)
        Cash flow from operations (000 R$)
        CAPEX (000 R$)
        Write-offs (000 R$)
        Cash flow from investment activities (000 R$)
        Debt amortization (000 R$)
        New debt (000 R$)
        Cash flow from financing activities (000 R$)
        Change in cash (000 R$)
        Initial cash (000 R$)
        Ending cash (000 R$)
        """        
        
        return final_df, assets_df, liabilities_df
        
    def simulate_Assets(self, accounts_receivable, inventories, other_current_assets, other_non_current_assets, ending_cash):
        
        cash = ending_cash
        ppe = self.get_CAPEX('PP&E')
        total_current_assets = cash + accounts_receivable + inventories + other_current_assets
        total_non_current_assets = ppe + other_non_current_assets
        total_assets = total_current_assets + total_non_current_assets
        
        final_df = pd.DataFrame([cash, accounts_receivable, inventories, other_current_assets, total_current_assets, ppe, other_non_current_assets, total_non_current_assets, total_assets],
                                columns = ['Cash (000 R$)','Accounts receivable (000 R$)','Inventories (000 R$)','Other current assets (000 R$)','Total current assets (000 R$)','PP&E (000 R$)','Other non current assets (000 R$)','Total non current assets (000 R$)','Total assets (000 R$)'])
        return final_df
        
    def simulate_Liabilities(self, assumptions_df, financial_performance_df, net_income, st_accounts_payable, other_current_liabilities, other_non_current_liabilities, st_debt, lt_debt):
        
        total_current_liabilities = st_accounts_payable, st_debt, other_current_liabilities
        total_non_current_liabilities = lt_debt, other_non_current_liabilities
        total_liabilities = total_current_liabilities + total_non_current_liabilities
        issued_capital = assumptions_df['Issued capital (000 R$)'].values[0]
        retained_earnings = net_income + financial_performance_df['Retained earnings (000 R$)'].values[0]
        total_equity = issued_capital + retained_earnings
        liabilities_plus_equity = total_liabilities + total_equity
        
        final_df = pd.DataFrame([st_accounts_payable, st_debt, other_current_liabilities, total_current_liabilities, lt_debt, other_non_current_liabilities, total_non_current_liabilities, total_liabilities, issued_capital, retained_earnings, total_equity, liabilities_plus_equity],
                                columns = ['Short term accounts payable (000 R$)','Short term debt (000 R$)','Other current liabilities (000 R$)', 'Total current liabilities (000 R$)', 'Long term debt (000 R$)', 'Other non current liabilities (000 R$)','Total non current liabilities (000 R$)','Total liabilities (000 R$)','Issued capital (000 R$)','Retained earnings (000 R$)','Total equity (000 R$)','Liabilities + equity (000 R$)']
                                )
        
        return final_df

    def simulate_Financial_Indices(self, liabilities_df, assets_df, balance_sheet_df, income_statement_df):
        
        i = 3
        
        """
        Gross margin (%)
        EBITDA (000 R$)
        EBITDA margin (%)
        Net income (%)
        Net debt (000 R$)
        Net debt/EBITDA
        Net debt/mt of cane
        Indebtedness
        Short term debt (% of total)
        Current ratio
        """
        
    def get_CAPEX(self, requested_var):
        
        if(requested_var == 'Total (Domestic Currency)'):
            var_return = 83700
        elif(requested_var == 'PP&E'):
            var_return = 324920
        
        return var_return
    
    def calc_VaR(self, price_data, time_till_expiry, last_date):
        
        unhedged_volumes_mar1 = self.unhedged_volumes[0]
        unhedged_volumes_may = self.unhedged_volumes[1]
        unhedged_volumes_jul = self.unhedged_volumes[2]
        unhedged_volumes_oct = self.unhedged_volumes[3]
        unhedged_volumes_mar2 = self.unhedged_volumes[4]
        
        date = pd.to_datetime(last_date)
        
        mar1_VaR = 0
        may_VaR = 0
        jul_VaR = 0
        oct_VaR = 0
        mar2_VaR = 0
        
        if (unhedged_volumes_mar1 > 0):
            
            temp_prices = price_data.filter(like = 'SBMAR1')
            temp_time_left = time_till_expiry[0]
            temp_date_i = last_date - datetime.timedelta(days = temp_time_left)
            temp_prices = temp_prices.loc[(temp_prices.index >= temp_date_i) & (temp_prices.index <= last_date)]
            temp_prices_pct_chg = temp_prices.pct_change()
            mean1 = temp_prices_pct_chg.mean()
            sigma1 = temp_prices_pct_chg.std()/100
            forward_sim = pd.DataFrame(np.random.normal(mean1, (sigma1), size = (1000, int(temp_time_left/7))))
            temp_px = temp_prices.max().values[0]
            
            for i in range(0,forward_sim.shape[1]):
                temp_forward = forward_sim[:][i]
                delta = temp_forward.quantile(q = 0.95)
                temp_px = temp_px * (1 - abs(delta))
            
            mar1_VaR = unhedged_volumes_mar1 * (temp_prices.max().values[0] - temp_px) * (2204.26/100)
            
        if (unhedged_volumes_may > 0):
            
            temp_prices = price_data.filter(like = 'SBMAY1')
            temp_time_left = time_till_expiry[1]
            temp_date_i = last_date - datetime.timedelta(days = temp_time_left)
            temp_prices = temp_prices.loc[(temp_prices.index >= temp_date_i) & (temp_prices.index <= last_date)]
            temp_prices_pct_chg = temp_prices.pct_change()
            mean1 = temp_prices_pct_chg.mean()
            sigma1 = temp_prices_pct_chg.std()/100
            forward_sim = pd.DataFrame(np.random.normal(mean1, (sigma1), size = (1000, int(temp_time_left/7))))
            temp_px = temp_prices.max().values[0]
            
            for i in range(0,forward_sim.shape[1]):
                temp_forward = forward_sim[:][i]
                delta = temp_forward.quantile(q = 0.95)
                temp_px = temp_px * (1 - abs(delta))
            
            may_VaR = unhedged_volumes_may * (temp_prices.max().values[0] - temp_px) * (2204.26/100)
        
        if (unhedged_volumes_jul > 0):
            
            temp_prices = price_data.filter(like = 'SBJUL1')
            temp_time_left = time_till_expiry[2]
            temp_date_i = last_date - datetime.timedelta(days = temp_time_left)
            temp_prices = temp_prices.loc[(temp_prices.index >= temp_date_i) & (temp_prices.index <= last_date)]
            temp_prices_pct_chg = temp_prices.pct_change()
            mean1 = temp_prices_pct_chg.mean()
            sigma1 = temp_prices_pct_chg.std()/100
            forward_sim = pd.DataFrame(np.random.normal(mean1, (sigma1), size = (1000, int(temp_time_left/7))))
            temp_px = temp_prices.max().values[0]
            
            for i in range(0,forward_sim.shape[1]):
                temp_forward = forward_sim[:][i]
                delta = temp_forward.quantile(q = 0.95)
                temp_px = temp_px * (1 - abs(delta))
            
            jul_VaR = unhedged_volumes_jul * (temp_prices.max().values[0] - temp_px) * (2204.26/100)
            
        if (unhedged_volumes_oct > 0):
            
            temp_prices = price_data.filter(like = 'SBOCT1')
            temp_time_left = time_till_expiry[3]
            temp_date_i = last_date - datetime.timedelta(days = temp_time_left)
            temp_prices = temp_prices.loc[(temp_prices.index >= temp_date_i) & (temp_prices.index <= last_date)]
            temp_prices_pct_chg = temp_prices.pct_change()
            mean1 = temp_prices_pct_chg.mean()
            sigma1 = temp_prices_pct_chg.std()/100
            forward_sim = pd.DataFrame(np.random.normal(mean1, (sigma1), size = (1000, int(temp_time_left/7))))
            temp_px = temp_prices.max().values[0]
            
            for i in range(0,forward_sim.shape[1]):
                temp_forward = forward_sim[:][i]
                delta = temp_forward.quantile(q = 0.95)
                temp_px = temp_px * (1 - abs(delta))
            
            oct_VaR = unhedged_volumes_jul * (temp_prices.max().values[0] - temp_px) * (2204.26/100)
            
        if (unhedged_volumes_mar2 > 0):
            
            temp_prices = price_data.filter(like = 'SBMAR2')
            temp_time_left = time_till_expiry[4]
            temp_date_i = last_date - datetime.timedelta(days = temp_time_left)
            temp_prices = temp_prices.loc[(temp_prices.index >= temp_date_i) & (temp_prices.index <= last_date)]
            temp_prices_pct_chg = temp_prices.pct_change()
            mean1 = temp_prices_pct_chg.mean()
            sigma1 = temp_prices_pct_chg.std()/100
            forward_sim = pd.DataFrame(np.random.normal(mean1, (sigma1), size = (1000, int(temp_time_left/7))))
            temp_px = temp_prices.max().values[0]
            
            for i in range(0,forward_sim.shape[1]):
                temp_forward = forward_sim[:][i]
                delta = temp_forward.quantile(q = 0.95)
                temp_px = temp_px * (1 - abs(delta))
            
            mar2_VaR = unhedged_volumes_mar2 * (temp_prices.max().values[0] - temp_px) * (2204.26/100)

            return mar1_VaR, may_VaR, jul_VaR, oct_VaR, mar2_VaR
        
            
            
        