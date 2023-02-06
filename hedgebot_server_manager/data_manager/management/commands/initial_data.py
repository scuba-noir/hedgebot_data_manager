from django.core.management.base import BaseCommand, CommandError
from data_manager import models
from data_manager.models import monte_carlo_market_data
import pandas as pd



class Command(BaseCommand):

    def handle(self, *args, **options):
        next = False
        emp_2 = True
        if next == True:
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
        else:
                relevant_factors = ['sugar_1', 'hydrous', 'anhydrous', 'usdbrl']
                max_date = monte_carlo_market_data.objects.latest('simulation_date').simulation_date
                current_mc_data_df = pd.DataFrame(monte_carlo_market_data.objects.filter(reference__in = relevant_factors).filter(simulation_date = max_date).values())
                current_mc_data_df.columns = ['Id','start_date', 'target_date', 'end_date', 'factor_label', 'mean_returned', 'std_returned']
                current_mc_data_df['season'] = '23_24'
                current_mc_data_df = current_mc_data_df.drop(['Id'], axis = 1).drop_duplicates()
                current_mc_data_df.loc[current_mc_data_df['std_returned'] < 0.0001, 'std_returned'] = 0
                current_mc_data_df['std_returned'] = current_mc_data_df['std_returned'].div(current_mc_data_df['mean_returned'])
                current_mc_data_df['pct_change'] = current_mc_data_df.groupby('factor_label')['mean_returned'].pct_change().fillna(0)
                print(current_mc_data_df)
        if emp_2 == True:
            data_df = pd.read_csv('temp_price_csv.csv')
            temp_cols = data_df.columns
            for cols in temp_cols:
                if cols == 'date':
                    continue
                temp_ref = cols
                temp_df = data_df.filter([temp_ref, 'date'])
                print(temp_df)