from django.core.management.base import BaseCommand, CommandError
from data_manager import models
from data_manager.models import market_data
import pandas as pd



class Command(BaseCommand):

    def handle(self, *args, **options):
        label_dict = {
            'SBMAY1 Comdty':'SBMAY1 Comdty',
            'SBJUL1 Comdty':'SBJUL1 Comdty',
            'SBOCT1 Comdty':'SBOCT1 Comdty',
            'SBMAR2 Comdty':'SBMAR2 Comdty',
            'NY No.11':'SB1 Comdty',
            'Hydrous Ethanol':'BAAWHYDP Index',
            'Anhydrous Ethanol':'BAAWANAB Index',
            'Fertilizer Costs':'Fert_Costs',
            'Brent Crude':'CL1 Comdty',
            'USDBRL':'USDBRL Curncy',
            'Energy Prices':'Energy_Costs',
            'SBMAR1 Comdty':'SBMAR1 Comdty'
            }

        temp_price_data = pd.read_csv("temp_price_data.csv")
        temp_price_data['Date'] = pd.to_datetime(temp_price_data['Date'])
        for keys in label_dict.keys():
            temp_label = label_dict[keys]
            max_date_bool = False
            try:
                max_date = market_data.objects.filter(ticker = temp_label).latest('date').date
                max_date = datetime.datetime(max_date.year, max_date.month, max_date.day)
                max_date_bool = True
            except:
                print('No data for ' + str(keys))
            temp_price_data_df = temp_price_data.filter([keys, 'Date'], axis = 1)
            temp_price_data_df = temp_price_data_df.dropna()
            if max_date_bool == True:
                temp_price_data_df = temp_price_data_df.loc[temp_price_data_df['Date'] > max_date]
            for row, items in temp_price_data_df.iterrows():
                temp_val = items[keys]
                temp_date = items['Date']
                
                market_data.objects.get_or_create(ticker = label_dict[keys], date = temp_date, value = temp_val, units = 'temp_fill')
                