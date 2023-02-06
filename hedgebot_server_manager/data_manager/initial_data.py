from hedgebot_server_manager.data_manager import models
import pandas as pd


data_df = pd.read_csv('Final_Final_MC.csv', index_col=False)
print(data_df)