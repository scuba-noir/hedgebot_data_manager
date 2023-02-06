# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 00:44:11 2021

@author: ChristopherTHOMPSON
"""
import numpy as np
import pandas as pd
import Regression_Costs_Sao_Domingos as GBoost
import LSTM_ML_Regression as LTSM
from ta.volatility import BollingerBands

"""
Contract dependant datapoints:
    total call open interest
    total put open interest
    last price

Non-contract dependant datapoints:
    CSC1SNCN Index - CFTC net non-commercial position
    30D IVOL at 100.0% Mnyns LIVE
    60 D IVOL at 100.0% Mnyns LIVE
    3M 100% IVOL
    6M IVOL at 100.0% Mnyns LIVE
    1Y 100% IVOL
"""
"""
Data Grab:
    Fields = ['PX_LAST','PR243','PR244','VL137','VL151','VL158','VL165','VL172']
    Tickers = ['SBMAR1 Comdty', 'SBMAY1 Comdty', 'SBJUL1 Comdty', 'SBOCT1 Comdty', 'SBMAR2 Comdty']
    con = pdblp.BCon(debug=False, port=8194, timeout=100000)
    con.start()
    
    data = con.bdh(Tickers, Fields, '20100101','20211220')
"""

#Mid-term Indicator
def mt_indicator(mid_indicator_data, tickers, MT_regressor, trial_boolean, model_name):
    
    pred_y_ls = []
    MT_regressor_ls = []
    
    for i in range(len(tickers)):
        
        temp_df = mid_indicator_data.filter(like = tickers[i], axis = 1)
        temp_df = temp_df.resample('W-FRI', closed = 'left').last()
        temp_temp = temp_df.filter(like = 'Total Put', axis = 1).div(temp_df.filter(like = 'Total Call', axis = 1).values)
        temp_df = temp_df.pct_change()
        temp_df['Put Call Ratio'] = temp_temp
        
        y = temp_df.filter(like = 'PX_LAST', axis = 1)
        drop_index = list(temp_df.columns).index(y.columns.values[0])
        X = temp_df.drop(temp_df.columns[drop_index], axis = 1)
        temp_df = temp_df.dropna(axis = 0)

        temp_X_f = pd.DataFrame(np.zeros(shape = (100,X.shape[1])), columns = X.columns)
        mu = np.array(X.mean(axis = 0))
        sigma = np.array(X.std(axis = 0))
        
        for z in range(0,100):
            rand_data = np.random.normal(mu, sigma, size = (8, X.shape[1]))
            temp_X_f.iloc[z,:] = rand_data.mean(axis = 0)
        
        temp_X_f = temp_X_f.mean(axis = 0)
        
        #return temp_X_f, mu, sigma
        X = temp_df.drop(temp_df.columns[drop_index], axis = 1)
        y = temp_df.filter(like = 'PX_LAST', axis = 1)
        X = np.array(X)
        #y = list(y.ravel())
        X_f = np.array(temp_X_f)
        
        pred_y_label = list(y.columns)
        substring = 'PX_LAST'
        pred_y_label = [j for j in pred_y_label if substring in j][0]
        
        if (trial_boolean == False):
            pred_y, MT_regressor = LTSM.main(temp_df, temp_df.shape[1] - 1, 1, pred_y_label, False, model_name[i])
            MT_regressor_ls.append(MT_regressor)
        else:
            MT_regressor_ls = MT_regressor
            #rng = np.random.RandomState(42)
            #xx = np.atleast_2d(rng.uniform(X_f.min(), X_f.max(), X.shape[1]))
            #pred_y = LTSM.main(temp_df, temp_df.shape[1] - 1, 1, pred_y_label, MT_regressor_ls[i], True, X_f)
            #print(model_name[i])
            pred_y, kill_var = LTSM.main(temp_df, temp_df.shape[1] - 1, 1, pred_y_label, True, model_name[i])
        
        pred_y_ls.append(pred_y)
        
    return pred_y_ls, MT_regressor_ls
    
    
def st_indicator(st_indicator_df, tickers, ST_regressor, trial_boolean, model_name):
    #Short Term Indicator
    
    st_indicator_df.index = pd.to_datetime(st_indicator_df['Date'])
    st_indicator_df = st_indicator_df.dropna(axis = 0)
    st_indicator_df = st_indicator_df.filter(like = 'PX_LAST')
    
    pred_y_ls = []
    ST_regressor_ls = []
    
    for i_b in range(0,len(tickers)):
        
        temp_df_2 = pd.DataFrame(index = st_indicator_df.index)
        
        if (st_indicator_df.columns[i_b] != 'Date'):
            
            temp_df = st_indicator_df.filter(like = st_indicator_df.columns[i_b], axis = 1)
            temp_df = temp_df.sort_index()
            temp_df = temp_df.loc[~temp_df.index.duplicated(), :]
            temp_df = temp_df.loc[:, ~temp_df.columns.duplicated()]
            x_temp = BollingerBands(temp_df, window = 20, window_dev = 2)
            #x_temp = x_temp.loc[~x_temp.index.duplicated(), :]
            temp_df_2['Lower Band'] = x_temp._lband
            temp_df_2['Upper Band'] = x_temp._hband
            temp_df_2['Distance to Upper'] = temp_df_2['Upper Band'] - temp_df[st_indicator_df.columns[i_b]] 
            temp_df_2['Distance to Lower'] = temp_df[st_indicator_df.columns[i_b]] - temp_df_2['Lower Band']
            temp_df_2 = temp_df_2.drop(['Lower Band','Upper Band'], axis = 1)
            X_f = temp_df_2.values[len(temp_df_2)-1]
            temp_df_2['Price'] = temp_df
            temp_df_2 = temp_df_2.shift(-1)
            #temp_df_2 = temp_df_2.dropna()
            temp_df_2['Distance to Upper'] = temp_df_2['Distance to Upper'] / temp_df_2['Price']
            temp_df_2['Distance to Lower'] = temp_df_2['Distance to Lower'] / temp_df_2['Price']
            temp_df_2['Price'] = temp_df_2['Price'].pct_change()
            temp_df_2 = temp_df_2.resample('W-FRI', closed = 'left').last()
            temp_df_2 = temp_df_2.dropna()
            
            X = np.array(temp_df_2.filter(like = 'Distance to', axis = 1))
            y = np.array(temp_df_2['Price'].values)
            
            
            pred_y_label = list(temp_df_2.columns)
            substring = 'Price'
            pred_y_label = [j for j in pred_y_label if substring in j][0]
            
            if (trial_boolean == False):
                pred_y, ST_regressor = LTSM.main(temp_df_2, temp_df_2.shape[1] - 1, 1, pred_y_label, False, model_name[i_b])
                ST_regressor_ls.append(ST_regressor)
            else:
                ST_regressor_ls = ST_regressor
                #rng = np.random.RandomState(42)
                ##xx = np.atleast_2d(rng.uniform(X_f.min(), X_f.max(), X.shape[1]))
               # print(i_b)
               # print(model_name[i_b])
                pred_y, kill_var = LTSM.main(temp_df_2, temp_df_2.shape[1] - 1, 1, pred_y_label, True, model_name[i_b])
            
            pred_y_ls.append(pred_y)
            
    return pred_y_ls, ST_regressor_ls

def fundamental_Indicator():
    
    data_df = pd.read_excel("C:\\Users\\ChristopherTHOMPSON\\Desktop\\AnacondaWorkspace\\SaoDomingos_HedgeBot_Proposal.xlsx", sheet_name = 'Fundamental Data (Sugar)')
    
    price_data_df = data_df.filter(like = 'Expiry', axis = 1)
    price_data_df = price_data_df.dropna()

    temp_columns = price_data_df.columns
    
    data_df = data_df.drop(temp_columns, axis = 1)
    
    data_df = data_df.drop(['Season'], axis = 1)
    
    for i in range (0, len(data_df.columns)):
        
        if ((data_df.columns[i] == ('World GDP Growth')) or (data_df.columns[i] == ('Emerging Market GDP Growth'))):
            continue
        else:
            continue
            data_df[data_df.columns[i]] = data_df[data_df.columns[i]].pct_change()

    data_df = data_df.dropna()
            
    X_f = np.array(data_df.iloc[data_df.shape[0]-1,:])
    X = np.array(data_df.iloc[:data_df.shape[0]-1,:])
    y_pred_ls = []
    
    for z in range (0, len(price_data_df.columns)):
        
        y = price_data_df[price_data_df.columns[z]].dropna()
        y_pred_ls.append(GBoost.GradientBoostingRegression(X, y, X_f))
    
    return data_df, X_f, X, y_pred_ls
    
    
def run_MT_ST_Indicators(tickers, data_df, trial_boolean, ST_regressor, MT_regressor):
    
    mid_indicator_data = data_df
    mid_indicator_data['Date'] = mid_indicator_data.index
    mid_indicator_data.index = pd.to_datetime(mid_indicator_data['Date'])
    mid_indicator_data = mid_indicator_data.loc[mid_indicator_data['Date'] > pd.to_datetime('2015-04-01')]
    
    st_indicator_df = data_df
    st_indicator_df = st_indicator_df.loc[st_indicator_df['Date'] > pd.to_datetime('2015-04-01')]
    
    model_name_st = ['SBMAR1_Comdty_ST.h5', 'SBMAY1_Comdty_ST.h5', 'SBJUL1_Comdty_ST.h5', 'SBOCT1_Comdty_ST.h5', 'SBMAR2_Comdty_ST.h5']
    model_name_mt = ['SBMAR1_Comdty_MT.h5', 'SBMAY1_Comdty_MT.h5', 'SBJUL1_Comdty_MT.h5', 'SBOCT1_Comdty_MT.h5', 'SBMAR2_Comdty_MT.h5']
    
    if (trial_boolean == False):

        MT_pred_y, MT_regressor = mt_indicator(mid_indicator_data, tickers, MT_regressor, trial_boolean, model_name_mt)
        ST_pred_y, ST_regressor = st_indicator(st_indicator_df, tickers, ST_regressor, trial_boolean, model_name_st)
        trial_boolean = True
        
    elif (trial_boolean == True):

        MT_pred_y, MT_regressor = mt_indicator(mid_indicator_data, tickers, MT_regressor, trial_boolean, model_name_mt)
        ST_pred_y, ST_regressor = st_indicator(st_indicator_df, tickers, ST_regressor, trial_boolean, model_name_st)
        
    return MT_pred_y, trial_boolean, ST_pred_y, trial_boolean

