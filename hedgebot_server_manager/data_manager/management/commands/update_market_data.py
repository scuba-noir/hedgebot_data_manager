from django.core.management.base import BaseCommand, CommandError
from data_manager import models
from data_manager.models import monte_carlo_market_data, market_data
import pandas as pd
import pymysql

class Command(BaseCommand):

    def handle(self, *args, **options):

        old_data = pd.DataFrame(market_data.objects.all().values())
        all_tickers = old_data['ticker'].unique()
        print(all_tickers)
        old_data_df = pd.DataFrame(columns=['id','date','ticker','value','units'])
        for ticker in all_tickers:
            temp_max_date = max(old_data['date'].loc[old_data['ticker'] == ticker])
            temp_row = old_data.loc[(old_data['ticker'] == ticker) & (old_data['date'] == temp_max_date)]
            old_data_df = pd.concat([old_data_df, temp_row])

        print(old_data_df)


        ticker_ls = ['SB1 Comdty','USDBRL Curncy','BAAWHYDP Index','BAAWANAB Index']
        db = pymysql.connect(host = 'database-1.c8dbzf9wtrjo.us-east-2.rds.amazonaws.com', user = 'admin', password = 'Ktr321ugh!')
        cursor = db.cursor()

        sql = '''use collateral_prices'''
        cursor.execute(sql)

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