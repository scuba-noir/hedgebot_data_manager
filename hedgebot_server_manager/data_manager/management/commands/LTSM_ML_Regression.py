# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 16:31:21 2021

@author: ChristopherTHOMPSON
"""

import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

def sequential_to_supervised(data_df, lag_steps = 1, n_out = 1, dropnan = True):
    
    features = 1 if type(data_df) is list else data_df.shape[1]
    temp_df = pd.DataFrame(data_df)
    cols = list()
    feature_names = list()
    
    for i in range(lag_steps, 0, -1):
        cols.append(temp_df.shift(i)) #Creates the shifted dataset
        feature_names += [(str(temp_df.columns[j])) + '(t-%d)' % (i) for j in range(features)]
        
    for i in range(0, n_out):
        cols.append(data_df.shift(-i))
        if (i == 0):
            feature_names += [(str(temp_df.columns[j])) + '(t)' for j in range (features)]
        else:
            feature_names += [(str(temp_df.columns[j])) + '(t+%d)' % (i) for j in range(features)]
            
    agg = pd.concat(cols, axis = 1)
    agg.columns = feature_names
    
    if dropnan:
        agg.dropna(inplace = True)
    return agg

def main(data_df, num_features, lag_steps, label_feature, model_boolean, model_name):
    
        #data_df = pd.read_csv(csv_filepath, header = 0, index_col = 0, squeeze = True, usecols = (i for i in range(0, num_features+1)))
        supervised_dataset = sequential_to_supervised(data_df, lag_steps)
        #Move label column to the end of dataset
        cols_at_end = [label_feature + '(t)']
        supervised_dataset = supervised_dataset[[c for c in supervised_dataset if c not in cols_at_end] + [c for c in cols_at_end if c in supervised_dataset]]
        
        # Dropping the current timestep columns of features other than the one being predicted, which will be the label or y 
        supervised_dataset.drop(supervised_dataset.columns[(num_features*lag_steps) : (num_features*lag_steps + num_features -1)], axis=1, inplace=True)
        scaler = MinMaxScaler(feature_range=(0, 1))
        supervised_dataset_scaled = scaler.fit_transform(supervised_dataset) # Scaling all values
    
        split = int(supervised_dataset_scaled.shape[0]*.80) # Splitting for traning and testing
        train = supervised_dataset_scaled[:split, :]
        test = supervised_dataset_scaled[split:, :]
        
        train_X, train_y = train[:, :-1], train[:, -1] # The label column is separated out
        test_X, test_y = test[:, :-1], test[:, -1]
        train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1])) # Reshaping done for LSTM as it need 3D input
        test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
        
        if (model_boolean == False):
            # Defining the LSTM model to be fit
            model = Sequential()
            model.add(LSTM(85, input_shape=(train_X.shape[1], train_X.shape[2]), go_backwards = True))
            model.add(Dense(1))
            model.compile(loss='mae', optimizer='adam')
            
            # Fitting the model
            history = model.fit(train_X, train_y, epochs=70, batch_size=32, validation_data=(test_X, test_y), verbose=0, shuffle=False)
            
            """
            # Plotting the training progression
            pyplot.plot(history.history['loss'], label='train')
            pyplot.plot(history.history['val_loss'], label='test')
            pyplot.legend()
            pyplot.show()   
            """
            # Using the trained model to predict the label values in test dataset
            yhat = model.predict(test_X)
        
        else:
            model_temp = load_model(model_name)
            yhat = model_temp.predict(test_X)
        
        # Reshaping back into 2D for inversing the scaling
        test_X = test_X.reshape((test_X.shape[0], test_X.shape[2])) 
        
        # Concatenating the predict label column with Test data input features, needed for inversing the scaling
        inv_yhat = np.concatenate((test_X[:, 0:], yhat), axis=1) 
        inv_yhat = scaler.inverse_transform(inv_yhat) # Rescaling back
        inv_yhat = inv_yhat[:, num_features*lag_steps] # Extracting the rescaled predicted label column
        
        test_y = test_y.reshape((len(test_y), 1))
        inv_y = np.concatenate((test_X[:, 0:], test_y), axis=1) # Re joing the test dataset for inversing the scaling
        inv_y = scaler.inverse_transform(inv_y) # Rescaling the actual label column values
        inv_y = inv_y[:, num_features*lag_steps] # Extracting the rescaled actual label column
        
        rmse = np.sqrt(mean_squared_error(inv_y, inv_yhat)) # Calculating RMSE
        """
        print('Test RMSE: %.3f' % rmse)
        
        pyplot.plot(inv_y, label = 'Actual')
        pyplot.plot(inv_yhat, label = 'Predicted')
        pyplot.legend()
        pyplot.show()
        
        """
        return inv_y, inv_yhat, yhat
        
        if (model_boolean == False):    
            model.save(model_name)
            return inv_yhat, model_name
        else:
            return inv_yhat, model_name
    
def test_method():
    csv_filepath =  "C:\\Users\\ChristopherTHOMPSON\\Desktop\\AnacondaWorkspace\\IVOL_Indicator.csv"
    tickers = ['SBMAR1','SBMAY1','SBJUL1','SBOCT1','SBMAR2']
    data_df = pd.read_csv(csv_filepath, header = 0, index_col = 0, squeeze = True)
    data_df.index = pd.to_datetime(data_df.index)
    data_df = data_df.sort_index()    
    temp = []
    for i in range(len(tickers)):
        temp_df = data_df.copy()
        temp_df = temp_df.filter(like = tickers[i])
        pred_y_label = list(temp_df.columns)
        substring = 'PX_LAST'
        pred_y_label = [j for j in pred_y_label if substring in j][0]
        temp.append(main(temp_df, temp_df.shape[1], 1, pred_y_label, False, False, 0))
        return temp, data_df

