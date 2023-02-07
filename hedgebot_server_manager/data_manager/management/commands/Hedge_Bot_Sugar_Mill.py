# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 04:20:40 2021

@author: ChristopherTHOMPSON
"""

"""
Order of operations:
    1. Hedging attribute matrix
    2. Random Walk
    3. Cost Regression
    4. Distribution of results
"""

import pandas as pd
import datetime as datetime
import numpy as np
import Sugar_Mill as Sugar_Mill
import V2_Price_Indicators as V2_Price_Indicators
import math as m
import pdblp

class HedgeBot_SM_Simulater:

    march_expiry = False
    may_expiry = False
    jul_expiry = False
    oct_expiry = False
    mar_2_expiry = False
    sugar_futures_data = False
    start_date = False
    end_data = False
    initial_portfolio = False
    financial_performance_hist = False
    seasonal_assumptions = False
    attribute_matrices = [
                [1,0,0,0],
                [1,1,0,0],
                [1,1,1,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,1,0,0],
                [1,0,1,0],
                [1,0,0,1],
                [1,1,0,1],
                [1,1,1,1],
                [0,1,1,1],
                [0,0,1,1],
                [0,1,0,1],
                [1,0,1,1],
                ]

    def __init__(self, expirations, start_date, end_date) -> None:

        self.march_expiry = expirations['march_expiry']
        self.may_expiry = expirations['may_expiry']
        self.jul_expiry = expirations['jul_expiry']
        self.oct_expiry = expirations['oct_expiry']
        self.mar_2_expiry = expirations['mar_2_expiry']
        self.start_date = start_date
        self.end_data = end_date

        self.initialize_sugar_futures_data()
        self.initialize_company_data()

    def initialize_company_data(self):

        return 0

    def initialize_sugar_futures_data(self):
        
        initial_data_date = self.start_date - datetime.datetime(self.start_date.year - 5, self.start_date.month, self.start_date.day)
        initial_data_date = initial_data_date.strftime("%yyyy%mm%dd")
        end_data_date = self.start_date.strftime("%yyyy%mm%dd")

        con = pdblp.BCon(debug=False, port=8194, timeout=100000)
        con.start()
        
        tickers = ['SBMAR1 Comdty','SBMAY1 Comdty','SBJUL1 Comdty','SBOCT1 Comdty','SBMAR2 Comdty']
        fields = ['PX_LAST','PR244','VL137','VL151','VL158','VL165','PR243']
        
        sugar_futures_data = con.bdh(tickers, fields, initial_data_date,end_data_date, longdata=False)
        
        import_columns = ['SBMAR1 Comdty - PR244',	'SBMAR1 Comdty - PR243',	'SBMAR1 Comdty - PX_LAST',	'SBMAR1 Comdty - VL137',	'SBMAR1 Comdty - VL151',	'SBMAR1 Comdty - VL158',	'SBMAR1 Comdty - VL165',	'SBMAY1 Comdty - PR244',	'SBMAY1 Comdty - PR243',	'SBMAY1 Comdty - PX_LAST',	'SBMAY1 Comdty - VL137',	'SBMAY1 Comdty - VL151',	'SBMAY1 Comdty - VL158',	'SBMAY1 Comdty - VL165',	'SBJUL1 Comdty - PR244',	'SBJUL1 Comdty - PR243',	'SBJUL1 Comdty - PX_LAST',	'SBJUL1 Comdty - VL137',	'SBJUL1 Comdty - VL151',	'SBJUL1 Comdty - VL158',	'SBJUL1 Comdty - VL165',	'SBOCT1 Comdty - PR244',	'SBOCT1 Comdty - PR243',	'SBOCT1 Comdty - PX_LAST',	'SBOCT1 Comdty - VL137',	'SBOCT1 Comdty - VL151',	'SBOCT1 Comdty - VL158',	'SBOCT1 Comdty - VL165',	'SBMAR2 Comdty - PR244',	'SBMAR2 Comdty - PR243',	'SBMAR2 Comdty - PX_LAST',	'SBMAR2 Comdty - VL137',	'SBMAR2 Comdty - VL151',	'SBMAR2 Comdty - VL158',	'SBMAR2 Comdty - VL165']
        data_columns = ['SBMAR1 Comdty - PR244 - Total Put Open Interest',	'SBMAR1 Comdty - Total Call Open Interest',	'SBMAR1 Comdty - PX_LAST - Last Price',	'SBMAR1 Comdty - VL137 - 30D Implied Volatility',	'SBMAR1 Comdty - VL151 - 60D Implied Volatility',	'SBMAR1 Comdty - VL158 - 3M Implied Volatility',	'SBMAR1 Comdty - VL165 - 6M Implied Volatility',	'SBMAY1 Comdty - PR244 - Total Put Open Interest',	'SBMAY1 Comdty - Total Call Open Interest',	'SBMAY1 Comdty - PX_LAST - Last Price',	'SBMAY1 Comdty - VL137 - 30D Implied Volatility',	'SBMAY1 Comdty - VL151 - 60D Implied Volatility',	'SBMAY1 Comdty - VL158 - 3M Implied Volatility',	'SBMAY1 Comdty - VL165 - 6M Implied Volatility',	'SBJUL1 Comdty - PR244 - Total Put Open Interest',	'SBJUL1 Comdty - Total Call Open Interest',	'SBJUL1 Comdty - PX_LAST - Last Price',	'SBJUL1 Comdty - VL137 - 30D Implied Volatility',	'SBJUL1 Comdty - VL151 - 60D Implied Volatility',	'SBJUL1 Comdty - VL158 - 3M Implied Volatility',	'SBJUL1 Comdty - VL165 - 6M Implied Volatility',	'SBOCT1 Comdty - PR244 - Total Put Open Interest',	'SBOCT1 Comdty - Total Call Open Interest',	'SBOCT1 Comdty - PX_LAST - Last Price',	'SBOCT1 Comdty - VL137 - 30D Implied Volatility',	'SBOCT1 Comdty - VL151 - 60D Implied Volatility',	'SBOCT1 Comdty - VL158 - 3M Implied Volatility',	'SBOCT1 Comdty - VL165 - 6M Implied Volatility',	'SBMAR2 Comdty - PR244 - Total Put Open Interest',	'SBMAR2 Comdty - Total Call Open Interest',	'SBMAR2 Comdty - PX_LAST - Last Price',	'SBMAR2 Comdty - VL137 - 30D Implied Volatility',	'SBMAR2 Comdty - VL151 - 60D Implied Volatility',	'SBMAR2 Comdty - VL158 - 3M Implied Volatility',	'SBMAR2 Comdty - VL165 - 6M Implied Volatility']
        columns = []
        for col in sugar_futures_data.columns:
            temp_str = str(col[0]) + ' - ' + str(col[1])
            try:
                index =import_columns.index(temp_str)
            except:
                continue
            columns.append(data_columns[index])
        
        sugar_futures_data.columns = columns
        sugar_futures_data['Date'] = sugar_futures_data.index
        
        temp_index = pd.to_datetime(sugar_futures_data['Date'])
        sugar_futures_data.index = temp_index
        sugar_futures_data = sugar_futures_data.resample('W-FRI', closed = 'left').last()
        sugar_futures_data = sugar_futures_data.dropna()
        self.sugar_futures_data = sugar_futures_data

    def create_random_walks(self):
            
        sugar_futures_data = self.sugar_futures_data.copy()
        temp_index = pd.to_datetime(sugar_futures_data['Date'])
        sugar_futures_data.index = temp_index
        data_df = sugar_futures_data.resample('W-FRI', closed = 'left').last()
        
        length_mar = (self.march_expiry - self.start_date).days
        length_may = (self.may_expiry - self.start_date).days
        length_jul = (self.jul_expiry - self.start_date).days
        length_oct = (self.oct_expiry - self.start_date).days
        length_mar_2 = (self.mar_2_expiry - self.start_date).days
        
        data_df = data_df.drop(['Date'], axis = 1)
        temp_index = data_df.index
        data_df = data_df.reset_index()
        data_df = data_df.drop(['Date'], axis = 1)
        
        data_df = np.log1p(data_df.pct_change())

        data_df.index = temp_index
        data_df = data_df.dropna()
        
        means = np.array([data_df.mean()/100]).transpose()
        sigmas = np.array([data_df.std()/100]).transpose()
        
        scenarios = []
        forward_period = int(length_mar_2 / 7)

        for i in range(0,1000):
            
            scenarios.append(np.array(np.random.normal(means,np.sqrt(sigmas), size = (means.shape[0], forward_period))))

        #scenarios = random walk for futures data
        return scenarios
                
    def initiate_Mills(self, num_mills, start_date):
        
        initial_portfolio = pd.read_excel("C:\\Users\\ChristopherTHOMPSON\\Desktop\\AnacondaWorkspace\\220408_SaoDomingos_HedgeBot_Proposal.xlsx", sheet_name = 'Sao Domingos Current Fixations')
        financial_performance_df = pd.read_excel("C:\\Users\\ChristopherTHOMPSON\\Desktop\AnacondaWorkspace\\Sugar_Mill_Class_Test_Variables_SD.xlsx", sheet_name = 'Financial Performance')
        assumptions_df = pd.read_excel("C:\\Users\\ChristopherTHOMPSON\\Desktop\\AnacondaWorkspace\\Sugar_Mill_Class_Test_Variables_SD.xlsx", sheet_name = 'Assumptions')
        
        mills = []
        for i in range(0,num_mills):
            #Need assumptions first
            rand_int = np.random.randint(0,len(self.attribute_matrices) - 1)
            temp_mill = Sugar_Mill.sugar_Mill(i, self.attribute_matrices[rand_int], financial_performance_df, assumptions_df, initial_portfolio, 18.15, start_date)
            mills.append(temp_mill)
    
        return mills

    def run_Simulation(self):
        
        fundamental_indicator = [
            17.32,
            17.82,
            18.4,
            17.4,
            17.22]
                
        scenarios = self.create_random_walks(self.sugar_futures_data)
        mills = self.initiate_Mills(num_mills = 100, start_date = self.start_date)
        
        length_mar = int((self.march_expiry - self.start_date).days / 7)
        length_may = int((self.may_expiry - self.start_date).days / 7)
        length_jul = int((self.jul_expiry - self.start_date).days / 7)
        length_oct = int((self.oct_expiry - self.start_date).days / 7)
        length_mar_2 = int((self.mar_2_expiry - self.start_date).days / 7)

        MT_regressor = False
        ST_regressor = False
        zompy = 0
        columns_ls = ['Date', 'Weighted Average Price','Unhedged Volumes Mar 1','Unhedged Volumes May','Unhedged Volumes Jul','Unhedged Volumes Oct', 'Unhedged Volumes Mar','Hedged Volumes','Fixed Revenues', 'Hedge Boolean', 'Target Price','Current Price Mar','Current Price May','Current Price Jul','Current Price Oct','Current Price Mar 2', 'Attribute A', 'Attribute B','Attribute C','Attribute D']
        
        record_book = pd.DataFrame([np.zeros(len(columns_ls))], columns = columns_ls)
        data_f_n_ls = []
        final_ls = []
        
        for i in range(0, len(mills)):
            print('Mill No. ' + str(i))
            
            final_ls = []
            stepped_data = []
            stepped_data = self.sugar_futures_data.copy()
            stepped_data = stepped_data.drop(['Date'], axis = 1)
                    
            ST_pred_y = 0
            MT_pred_y = 0
            temp_ls_1 = []
            
            for q in range(0, length_mar_2):
                
                try:
                    stepped_data = stepped_data.drop(['Date'], axis = 1)
                except:
                    zompy = 1
                
                if ((q <= length_mar) and (q <= length_may) and (q <= length_jul) and (q <= length_oct) and (q <= length_mar_2)):
                    tickers = ['SBMAR1 Comdty', 'SBMAY1 Comdty', 'SBJUL1 Comdty', 'SBOCT1 Comdty', 'SBMAR2 Comdty']

                elif ((q > length_mar) and (q <= length_may) and (q <= length_jul) and (q <= length_oct) and (q <= length_mar_2)):
                    tickers = ['SBMAY1 Comdty', 'SBJUL1 Comdty', 'SBOCT1 Comdty', 'SBMAR2 Comdty']
                    
                elif ((q > length_mar) and (q > length_may) and (q <= length_jul) and (q <= length_oct) and (q <= length_mar_2)):
                    tickers = ['SBJUL1 Comdty', 'SBOCT1 Comdty', 'SBMAR2 Comdty']

                elif ((q > length_mar) and (q > length_may) and (q > length_jul) and (q <= length_oct) and (q <= length_mar_2)):
                    tickers = ['SBOCT1 Comdty', 'SBMAR2 Comdty']
                    
                elif ((q > length_mar) and (q > length_may) and (q > length_jul) and (q > length_oct) and (q <= length_mar_2)):
                    tickers = ['SBMAR2 Comdty']
                    
                elif ((q > length_mar) and (q > length_may) and (q > length_jul) and (q > length_oct) and (q > length_mar_2)):
                    tickers = []
                
                random_int = np.random.randint(0,len(scenarios) - 1)
                data_f_n = scenarios[random_int].T
                temp_ls_1.append(list(data_f_n[q]))

            prev_data = stepped_data.loc[stepped_data.index == max(stepped_data.index)].values
            
            tickers = ['SBMAR1 Comdty', 'SBMAY1 Comdty', 'SBJUL1 Comdty', 'SBOCT1 Comdty', 'SBMAR2 Comdty']
            
            for q_i in range(0,len(temp_ls_1)):
                data_f_n_ls.append([x+1 for x in temp_ls_1[q_i]])
            

            for q_i in range(0,len(data_f_n_ls)):
                if(q_i == 0):
                    final_ls.append(list(*[a*b for a, b in zip(data_f_n_ls[q_i], prev_data)]))
                else:
                    final_ls.append(list([a*b for a, b in zip(data_f_n_ls[q_i], final_ls[q_i - 1])]))

            last_date = self.start_date + datetime.timedelta(days = 7)
            added_dates = []
            for q_z in range(0,len(final_ls)):
                try:
                    if (q_z == 0):
                        added_dates.append(last_date)
                    else:
                        added_dates.append(added_dates[q_z-1] + datetime.timedelta(days = 7))
                except:
                    return added_dates, final_ls
                
            temp_columns = stepped_data.columns
            stepped_data = stepped_data.reset_index()
            temp_df_df = pd.DataFrame((final_ls), columns = temp_columns)
            temp_df_df['Date'] = added_dates
            stepped_data = pd.concat((stepped_data,temp_df_df))
            stepped_data.index = stepped_data['Date']
            stepped_data = stepped_data.drop(['Date'], axis = 1)
            price_data = stepped_data.filter(like = 'PX_LAST')            
            previous_prices = stepped_data.filter(like = 'PX_LAST')
            previous_prices = previous_prices.loc[(previous_prices.index >= self.start_date) & (previous_prices.index <= self.mar_2_expiry)]
                    
            if ((MT_regressor == False) or (ST_regressor == False)):
                MT_pred_y, MT_regressor, ST_pred_y, ST_regressor = V2_Price_Indicators.run_MT_ST_Indicators(tickers, stepped_data, False, ST_regressor, MT_regressor)
            else:
                MT_pred_y, MT_regressor, ST_pred_y, ST_regressor = V2_Price_Indicators.run_MT_ST_Indicators(tickers, stepped_data, True, ST_regressor, MT_regressor)
            
            mill_temp = mills[i]
            
            for x_zz in range(0,len(ST_pred_y)):
                ST_pred_y[x_zz] = ST_pred_y[x_zz][:length_mar_2]
                MT_pred_y[x_zz] = MT_pred_y[x_zz][:length_mar_2]
                
            temp_st = []
            temp_mt = []
            
            for zz_z in range(0,len(ST_pred_y[0])):
            
                temp_st = [ST_pred_y[0][zz_z], ST_pred_y[1][zz_z], ST_pred_y[2][zz_z], ST_pred_y[3][zz_z], ST_pred_y[4][zz_z]]
                temp_mt = [MT_pred_y[0][zz_z], MT_pred_y[1][zz_z], MT_pred_y[2][zz_z], MT_pred_y[3][zz_z], MT_pred_y[4][zz_z]]
                try:
                    previous_prices_ls = previous_prices.loc[previous_prices.index == previous_prices.index[zz_z]].values[0]
                except:
                    continue
                    #return previous_prices_ls, zz_z, previous_prices, len(ST_pred_y[0]), ST_pred_y
                
                if (zz_z < length_mar):
                    temp_st = temp_st
                    temp_mt = temp_mt
                    
                elif (zz_z < length_may):
                    temp_st.pop()
                    temp_mt.pop()
                    
                elif (zz_z < length_jul):
                    temp_st.pop()
                    temp_mt.pop()
                    temp_st.pop()
                    temp_mt.pop()
                    
                elif (zz_z < length_oct):
                    temp_st.pop()
                    temp_mt.pop()
                    temp_st.pop()
                    temp_mt.pop()
                    temp_st.pop()
                    temp_mt.pop()
                    
                elif (zz_z < length_mar_2):
                    temp_st.pop()
                    temp_mt.pop()
                    temp_st.pop()
                    temp_mt.pop()
                    temp_st.pop()
                    temp_mt.pop()
                    temp_st.pop()
                    temp_mt.pop()

                expirations = [self.march_expiry, self.may_expiry, self.jul_expiry, self.oct_expiry, self.mar_2_expiry]
                mill_temp.hedge_Decision(last_date, previous_prices_ls, temp_st, temp_mt, fundamental_indicator, price_data, expirations)
                
                last_date = last_date + datetime.timedelta(days = 7)
            
            record_book = pd.concat([record_book, mill_temp.record_book], ignore_index = True)
        
        return record_book
    
        march_expiry = pd.to_datetime('2023-03-31')
        may_expiry = pd.to_datetime('2023-05-30')
        jul_expiry = pd.to_datetime('2023-07-31')
        oct_expiry = pd.to_datetime('2023-10-31')
        mar_2_expiry = pd.to_datetime('2024-03-31')