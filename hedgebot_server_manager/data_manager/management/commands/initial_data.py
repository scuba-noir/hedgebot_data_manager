from django.core.management.base import BaseCommand, CommandError
from data_manager import models
import pandas as pd



class Command(BaseCommand):

    def handle(self, *args, **options):
        data_df = pd.read_csv('Final_Final_MC.csv', index_col=False)
        data_df['sim_date'] = pd.to_datetime(data_df['sim_date'])
        data_df['end_date'] = pd.to_datetime(data_df['end_date'])
        data_df['forecast_period'] = pd.to_datetime(data_df['forecast_period'])
        
        for row, items in data_df.iterrows():
            temp_ref = items['reference']
            temp_sim_date = items['sim_date']
            temp_f_period = items['forecast_period']
            temp_mu = items['mean_returned']
            temp_sigma = items['std_returned']
            temp_end_date = items['end_date']

            obj = models.monte_carlo_market_data.objects.update_or_create(simulation_date = temp_sim_date, forecast_period=temp_f_period, reference=temp_ref, mean_returned=temp_mu, std_returned=temp_sigma, end_date=temp_end_date)
