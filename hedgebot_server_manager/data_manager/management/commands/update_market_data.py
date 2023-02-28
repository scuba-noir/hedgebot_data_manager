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
        all_tickers = ['SBMAY1 Comdty', 'SBJUL1 Comdty', 'SBOCT1 Comdty', 'SBMAR2 Comdty', 'GCFPUBGC Index', 'CL1 Comdty', 'BZCESECA Index', 'SBMAR1 Comdty','SB1 Comdty', 'USDBRL Curncy', 'BAAWHYDP Index', 'BAAWANAB Index']
        labels_ls = ['SBMAY1 Comdty', 'SBJUL1 Comdty', 'SBOCT1 Comdty', 'SBMAR2 Comdty', 'Fert_Costs', 'CL1 Comdty', 'Energy_Costs', 'SBMAR1 Comdty','SB1 Comdty', 'USDBRL Curncy', 'BAAWHYDP Index', 'BAAWANAB Index']
        
        if check_entries_bool == True:

            obj_delete = market_data.objects.exclude(ticker__in = labels_ls)
            print(pd.DataFrame(obj_delete.values())['ticker'].unique().tolist())
            obj_delete.delete()
        
        old_data_df = pd.DataFrame(columns=['id','date','ticker','value','units'])
        
        for ticker in labels_ls:

            temp_max_date = max(old_data['date'].loc[old_data['ticker'] == ticker])
            temp_row = old_data.loc[(old_data['ticker'] == ticker) & (old_data['date'] == temp_max_date)]
            print(temp_row)

            sql = '''SELECT * FROM market_data_prices WHERE ticker = '''
            sql = sql + str(ticker)
            sql = sql + '''AND date > ''' + str(temp_max_date)
            temp_data_df = pd.read_sql(sql = sql, con = db)
            print(temp_data_df.values.tolist())

        
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