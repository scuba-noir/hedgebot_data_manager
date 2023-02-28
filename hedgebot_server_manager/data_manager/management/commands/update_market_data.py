from django.core.management.base import BaseCommand, CommandError
from data_manager import models
from data_manager.models import monte_carlo_market_data, market_data
import pandas as pd
import pymysql

class Command(BaseCommand):

    def handle(self, *args, **options):

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
        data_df = data_df.loc[data_df['ticker'].isin(ticker_ls)]

        print(data_df)