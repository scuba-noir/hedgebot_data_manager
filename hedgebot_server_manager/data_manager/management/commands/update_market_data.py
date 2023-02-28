from django.core.management.base import BaseCommand, CommandError
from data_manager import models
from data_manager.models import monte_carlo_market_data, market_data
import pandas as pd
import pymysql
import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):

        check_entries_bool = False
        db = pymysql.connect(host = 'database-1.c8dbzf9wtrjo.us-east-2.rds.amazonaws.com', user = 'admin', password = 'Ktr321ugh!')
        cursor = db.cursor()
        sql = '''use collateral_prices'''
        cursor.execute(sql)

        old_data = pd.DataFrame(market_data.objects.all().values())
        old_data['date'] = pd.to_datetime(old_data['date'])
        all_tickers = ['SBMAY1 Comdty', 'SBJUL1 Comdty', 'SBOCT1 Comdty', 'SBMAR2 Comdty', 'GCFPUBGC Index', 'CL1 Comdty', 'BZCESECA Index', 'SBMAR1 Comdty','SB1 Comdty', 'USDBRL Curncy', 'BAAWHYDP Index', 'BAAWANAB Index']
        labels_ls = ['SBMAY1 Comdty', 'SBJUL1 Comdty', 'SBOCT1 Comdty', 'SBMAR2 Comdty', 'Fert_Costs', 'CL1 Comdty', 'Energy_Costs', 'SBMAR1 Comdty','SB1 Comdty', 'USDBRL Curncy', 'BAAWHYDP Index', 'BAAWANAB Index']
        
        if check_entries_bool == True:

            obj_delete = market_data.objects.exclude(ticker__in = labels_ls)
            print(pd.DataFrame(obj_delete.values())['ticker'].unique().tolist())
            obj_delete.delete()
        
            
        for ticker in labels_ls:

            temp_max_date = max(old_data['date'].loc[old_data['ticker'] == ticker])
            temp_row = old_data.loc[(old_data['ticker'] == ticker) & (old_data['date'] == temp_max_date)]

            sql = '''SELECT * FROM market_data_prices WHERE ticker = "'''
            sql = sql + str(ticker)
            sql = sql + '''" AND date > ''' + temp_max_date.strftime("%Y-%m-%d")
            temp_data_df = pd.read_sql(sql = sql, con = db)
            print(temp_data_df)
            for row, items in temp_data_df.iterrows():
                print(items)
                #try:
                #    market_data.objects.get_or_create(ticker = items.ticker, value = items.value, units = items.units, date = items.date)
                #except:
                #    continue
            


        
        """    
        columns = ['Id','Ticker', 'Description', 'Origin', 'Dashboard', 'Units', 'Date','Value','Most Recent']
        sql = '''
            WITH list AS (
                SELECT m.*, ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY date DESC) AS rn
                FROM market_data_prices as m
            )
            SELECT * FROM list where rn = 1;
            '''

        data_df = pd.read_sql(sql = sql, con = db)
        db.close()
        data_df = data_df.loc[data_df['ticker'].isin(ticker_ls)]

        print(data_df)
        """