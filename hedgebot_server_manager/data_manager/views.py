from django.shortcuts import render
import numpy as np
import pandas as pd
import numpy as np
import numpy as np
import datetime
import re
import statistics
import json
from scipy.stats import norm, percentileofscore
from django.db.models import F, Q, When, Max, Avg, Window, StdDev
from data_manager.models import user_forecasts_assumptions_results
from data_manager.models import hedgebot_results
from data_manager.models import financial_simulation_meta_data_historical
from data_manager.models import financial_simulations_results
from data_manager.models import monte_carlo_market_data
from data_manager.models import market_data, market_forecasts
from data_manager.models import sugar_position_info_2
from data_manager.models import user_list, target_prices, user_forecasts_assumptions_results, current_financial_simulations
from data_manager.forms import userInputForm, userSugarPositionInput_2
from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics
from data_manager.serializers import SugarPosition2Serializers, MonteCarloDataSerializer, MarketDataSerializer, FinSimMetaDataSerializer, UserListSerializers, HistMCDataSerializer, HedgebotBestSerializer
from data_manager.serializers import RiskManagementUserInputTableSerializer, ProbabilityRangeScoresSerializer

from . import full_simulation_run

class Probability(object):
    def __init__(self, probability, created = None):
        self.probability = probability

def findnth(string, substring, n):
   parts = string.split(substring, n + 1)
   if len(parts) <= n + 1:
      return -1
   return len(string) - len(parts[-1]) - len(substring)

def return_current_season_df(username):
    
    current_season_df = user_forecasts_assumptions_results.objects.filter(username = username).filter(season='2023_24')
    verbose_name_dict = user_forecasts_assumptions_results.return_verbose(user_forecasts_assumptions_results)
    max_sim_date = current_season_df.latest('date').date
    current_season_df = current_season_df.filter(date = max_sim_date)
    max_id = current_season_df.latest('id').id
    current_season_df = current_season_df.filter(id = max_id)
    current_season_df = pd.DataFrame(current_season_df.values())
    counter = 0

    for key in verbose_name_dict:
        temp_ls = []
        temp_str = verbose_name_dict[key]
        temp_values = current_season_df[key].values[0]
        temp_ls.append(temp_str)
        temp_ls.append(temp_values)
        try:
            var_name = temp_str[:temp_str.index('-')]
        except:
            var_name = temp_str
        
        temp_ls.append(var_name)
        
        try:
            group_name = re.search('-(.*)-', temp_str).group(1)
        except:
            group_name = "not_listed"
        
        temp_ls.append(group_name)
        
        try:
            index = findnth(temp_str, '-', 1)
            units = temp_str[index+1:]
        except:
            units ='not_listed'
        
        temp_ls.append(units)

        if counter == 0:
            temp_df = pd.DataFrame([temp_ls], columns = ['Original','Value','Variable_name_eng','Data_group','Units'])
        else:
            df_temp = pd.DataFrame([temp_ls], columns = ['Original','Value','Variable_name_eng','Data_group','Units'])
            temp_df = pd.concat([temp_df, df_temp], ignore_index=True)
        counter += 1


    return temp_df

def return_prev_season_df(username):
    current_season_df = user_forecasts_assumptions_results.objects.filter(username = username).filter(season='2022_23')
    verbose_name_dict = user_forecasts_assumptions_results.return_verbose(user_forecasts_assumptions_results)
    max_id = current_season_df.latest('id').id
    current_season_df = current_season_df.filter(id = max_id)
    current_season_df = pd.DataFrame(current_season_df.values())
    current_season_df['date'] = pd.to_datetime(current_season_df['date'])
    current_season_df = current_season_df.loc[current_season_df['date'] == max(current_season_df['date'])]
    counter = 0

    for key in verbose_name_dict:
        temp_ls = []
        temp_str = verbose_name_dict[key]
        temp_values = current_season_df[key].values[0]
        temp_ls.append(temp_str)
        temp_ls.append(temp_values)
        try:
            var_name = temp_str[:temp_str.index('-')]
        except:
            var_name = temp_str
        
        temp_ls.append(var_name)
        
        try:
            group_name = re.search('-(.*)-', temp_str).group(1)
        except:
            group_name = "not_listed"
        
        temp_ls.append(group_name)
        
        try:
            index = findnth(temp_str, '-', 1)
            units = temp_str[index+1:]
        except:
            units ='not_listed'
        
        temp_ls.append(units)

        if counter == 0:
            temp_df = pd.DataFrame([temp_ls], columns = ['Original','Value','Variable_name_eng','Data_group','Units'])
        else:
            df_temp = pd.DataFrame([temp_ls], columns = ['Original','Value','Variable_name_eng','Data_group','Units'])
            temp_df = pd.concat([temp_df, df_temp], ignore_index=True)
        counter += 1

    return temp_df

def financial_sim_update(username, num_sims = 1000):

    current_season_df = return_current_season_df(username)
    prev_season_df = return_prev_season_df(username)

    mc_meta_data = pd.DataFrame(monte_carlo_market_data.objects.all().values())
    final_value_dict = full_simulation_run.main(current_season_df, prev_season_df, mc_meta_data, num_sims)
    
    pd.DataFrame.from_dict(final_value_dict).to_csv('final_value_dict_output.csv')
    final_value_dict = pd.DataFrame.from_dict(final_value_dict)


    temp = current_financial_simulations.objects.create(
        user = username,
        sugar_price = statistics.mean(list(final_value_dict['sugar_price'])),
        hydrous_price = statistics.mean(list(final_value_dict['hydrous_price'])),
        anhydrous_price = statistics.mean(list(final_value_dict['anhydrous_price'])),
        energy_price = statistics.mean(list(final_value_dict['energy_price'])),
        fx_rate = statistics.mean(list(final_value_dict['fx_rate'])),
        selic_rate = statistics.mean(list(final_value_dict['selic_rate'])),
        foreign_debt_rate = statistics.mean(list(final_value_dict['foreign_debt_rate'])),
        inflation_rate = statistics.mean(list(final_value_dict['inflation_rate'])),
        crude_price = statistics.mean(list(final_value_dict['crude_price'])),
        fertilizer_price = statistics.mean(list(final_value_dict['fertilizer_price'])),
        sugar_revenues = statistics.mean(list(final_value_dict['sugar_revenues'])),
        hydrous_revenues = statistics.mean(list(final_value_dict['hydrous_revenues'])),
        anhydrous_revenues = statistics.mean(list(final_value_dict['anhydrous_revenues'])),
        energy_revenues = statistics.mean(list(final_value_dict['energy_revenues'])),
        input_costs = statistics.mean(list(final_value_dict['input_costs'])),
        fuel_costs = statistics.mean(list(final_value_dict['fuel_costs'])),
        freight_costs = statistics.mean(list(final_value_dict['freight_costs'])),
        labor_costs = statistics.mean(list(final_value_dict['labor_costs'])),
        indutrial_costs = statistics.mean(list(final_value_dict['indutrial_costs'])),
        depreciation = statistics.mean(list(final_value_dict['depreciation'])),
        planting_costs = statistics.mean(list(final_value_dict['planting_costs'])),
        lease_costs = statistics.mean(list(final_value_dict['lease_costs'])),
        cogs = statistics.mean(list(final_value_dict['cogs'])),
        gross_profit = statistics.mean(list(final_value_dict['gross_profit'])),
        sga_costs = statistics.mean(list(final_value_dict['sga_costs'])),
        ebit = statistics.mean(list(final_value_dict['ebit'])),
        financial_costs = statistics.mean(list(final_value_dict['financial_costs'])),
        ebt = statistics.mean(list(final_value_dict['ebt'])),
        tax = statistics.mean(list(final_value_dict['tax'])),
        net_income = statistics.mean(list(final_value_dict['net_income'])),
        gross_margin = statistics.mean(list(final_value_dict['gross_margin'])),
        ebitda_margin = statistics.mean(list(final_value_dict['ebitda_margin'])),
        net_margin = statistics.mean(list(final_value_dict['net_margin'])),
        net_debt_to_ebitda = statistics.mean(list(final_value_dict['net_debt_to_ebitda'])),
        net_debt_to_mt_cane = statistics.mean(list(final_value_dict['net_debt_to_mt_cane'])),
        indebtness = statistics.mean(list(final_value_dict['indebtness'])),
        short_term_debt = statistics.mean(list(final_value_dict['short_term_debt'])),
        current_ratio = statistics.mean(list(final_value_dict['current_ratio'])),
        sugar_price_std = statistics.stdev(final_value_dict['sugar_price']),
        hydrous_price_std = statistics.stdev(final_value_dict['hydrous_price']),
        anhydrous_price_std = statistics.stdev(final_value_dict['anhydrous_price']),
        energy_price_std = statistics.stdev(final_value_dict['energy_price']),
        fx_rate_std = statistics.stdev(final_value_dict['fx_rate']),
        selic_rate_std = statistics.stdev(final_value_dict['selic_rate']),
        foreign_debt_rate_std = statistics.stdev(final_value_dict['foreign_debt_rate']),
        inflation_rate_std = statistics.stdev(final_value_dict['inflation_rate']),
        crude_price_std = statistics.stdev(final_value_dict['crude_price']),
        fertilizer_price_std = statistics.stdev(final_value_dict['fertilizer_price']),
        sugar_revenues_std = statistics.stdev(final_value_dict['sugar_revenues']),
        hydrous_revenues_std = statistics.stdev(final_value_dict['hydrous_revenues']),
        anhydrous_revenues_std = statistics.stdev(final_value_dict['anhydrous_revenues']),
        energy_revenues_std = statistics.stdev(final_value_dict['energy_revenues']),
        input_costs_std = statistics.stdev(final_value_dict['input_costs']),
        fuel_costs_std = statistics.stdev(final_value_dict['fuel_costs']),
        freight_costs_std = statistics.stdev(final_value_dict['freight_costs']),
        labor_costs_std = statistics.stdev(final_value_dict['labor_costs']),
        indutrial_costs_std = statistics.stdev(final_value_dict['indutrial_costs']),
        depreciation_std = statistics.stdev(final_value_dict['depreciation']),
        planting_costs_std = statistics.stdev(final_value_dict['planting_costs']),
        lease_costs_std = statistics.stdev(final_value_dict['lease_costs']),
        cogs_std = statistics.stdev(list(final_value_dict['cogs'])),
        gross_profit_std = statistics.stdev(final_value_dict['gross_profit']),
        sga_costs_std = statistics.stdev(final_value_dict['sga_costs']),
        ebit_std = statistics.stdev(final_value_dict['ebit']),
        financial_costs_std = statistics.stdev(final_value_dict['financial_costs']),
        ebt_std = statistics.stdev(final_value_dict['ebt']),
        tax_std = statistics.stdev(final_value_dict['tax']),
        net_income_std = statistics.stdev(final_value_dict['net_income']),
        gross_margin_std = statistics.stdev(final_value_dict['gross_margin']),
        ebitda_margin_std = statistics.stdev(final_value_dict['ebitda_margin']),
        net_margin_std = statistics.stdev(final_value_dict['net_margin']),
        net_debt_to_ebitda_std = statistics.stdev(final_value_dict['net_debt_to_ebitda']),
        net_debt_to_mt_cane_std = statistics.stdev(final_value_dict['net_debt_to_mt_cane']),
        indebtness_std = statistics.stdev(final_value_dict['indebtness']),
        short_term_debt_std = statistics.stdev(final_value_dict['short_term_debt']),
        current_ratio_std = statistics.stdev(final_value_dict['current_ratio'])       
    )

def transformPrices(daily_chgs, price_data, price_date_ls):

    mc_dates_final = pd.to_datetime(daily_chgs['target_date'], format = "%Y-%m-%d")
    reference = daily_chgs['factor_label'].values[0]
    date_ls = mc_dates_final.min().strftime("%m/%d/%Y")
    daily_chgs = daily_chgs.drop(['factor_label', 'target_date'], axis = 1).values
    starting_price = price_data[price_date_ls.index(date_ls)]
    price_list = np.zeros_like(daily_chgs)
    price_list[0] = starting_price

    for dt in range(1, len(daily_chgs)):
        price_list[dt] = price_list[dt-1] * daily_chgs[dt]
        
    final_df = pd.DataFrame(price_list, index = mc_dates_final)
    final_df['factor_label'] = reference
    return final_df

def initiate_models(username):
    
    end_season_date = datetime.datetime(2024, 3, 31)
    today = datetime.datetime.now()
    date_range = pd.date_range(today, end_season_date, freq = 'W-FRI').to_list()
    for i in range(0,len(date_range)):
        hedgebot_results.objects.get_or_create(username = username, forecast_period = date_range[i].strftime('%Y-%m-%d'))
    financial_simulations_results.objects.get_or_create(username=username)
    target_prices.objects.get_or_create(username=username)
    sugar_position_info_2.objects.get_or_create(username=username)
    user_forecasts_assumptions_results.objects.get_or_create(username=username)
    user_forecasts_assumptions_results.objects.get_or_create(username=username, season = '22_23')

def at_market_sim(initial_sim_data, prev_year_fin_df):

    #Runs financial sim by using same calculation as financial_sim_update but user must input necessary variables
    """
        Runs a full financial simulation but only runs a single simulation (num_sims = 1) and passes current values with std of 0 as mc_meta_data
    
    """
    most_recent_mc_date = monte_carlo_market_data.objects.latest('simulation_date').simulation_date
    mc_meta_data_current_prices = pd.DataFrame(monte_carlo_market_data.objects.filter(simulation_date = most_recent_mc_date).filter(forecast_period = most_recent_mc_date).values())
    mc_meta_data_current_prices['std_returned'] = 0
    final_value_dict = full_simulation_run.main(initial_sim_data, prev_year_fin_df, mc_meta_data_current_prices, 1)
    return final_value_dict

def user_input_sim(user_input, initial_sim_data, prev_year_fin_df):

    most_recent_mc_date = monte_carlo_market_data.objects.latest('simulation_date').simulation_date
    max_forecast_period = monte_carlo_market_data.objects.latest('simulation_date').forecast_period
    mc_meta_data_current_prices_upper = pd.DataFrame(monte_carlo_market_data.objects.filter(simulation_date = most_recent_mc_date).filter(forecast_period = max_forecast_period).values())
    mc_meta_data_current_prices_lower = mc_meta_data_current_prices_upper.copy()
    relevent_market_var_ls = ['sugar_1','hydrous','anhydrous','usdbrl']
    for i in range(0,len(relevent_market_var_ls)):
        mc_meta_data_current_prices_upper['mean_returned'].loc[mc_meta_data_current_prices_upper['reference'] == relevent_market_var_ls[i]] = float(user_input[relevent_market_var_ls[i] + '_upper'])
        mc_meta_data_current_prices_lower['mean_returned'].loc[mc_meta_data_current_prices_lower['reference'] == relevent_market_var_ls[i]] = float(user_input[relevent_market_var_ls[i] + '_lower'])
        mc_meta_data_current_prices_upper['std_returned'].loc[mc_meta_data_current_prices_upper['reference'] == relevent_market_var_ls[i]] = 0
        mc_meta_data_current_prices_lower['std_returned'].loc[mc_meta_data_current_prices_lower['reference'] == relevent_market_var_ls[i]] = 0
    
    initial_sim_data['Value'].loc[(initial_sim_data['Variable_name_eng'] == 'Yield') & (initial_sim_data['Data_group'] == 'Own Cane Assumption')] = float(user_input['cane_yield'])
    initial_sim_data['Value'].loc[(initial_sim_data['Variable_name_eng'] == 'Average TRS') & (initial_sim_data['Data_group'] == 'Production Mix Assumption')] = float(user_input['trs'])
    initial_sim_data['Value'].loc[(initial_sim_data['Variable_name_eng'] == 'Sugar') & (initial_sim_data['Data_group'] == 'Production Mix Assumption')] = float(user_input['production_mix_sugar'])
    initial_sim_data['Value'].loc[(initial_sim_data['Variable_name_eng'] == 'Hydrous') & (initial_sim_data['Data_group'] == 'Production Mix Assumption')] = float(user_input['production_mix_hydrous'])
    initial_sim_data['Value'].loc[(initial_sim_data['Variable_name_eng'] == 'Anhydrous') & (initial_sim_data['Data_group'] == 'Production Mix Assumption')] = float(user_input['production_mix_anhydrous'])
    
    initial_sim_df = initial_sim_data

    final_value_dict_lower = full_simulation_run.main(initial_sim_df, prev_year_fin_df, mc_meta_data_current_prices_lower, 1) 
    final_value_dict_upper = full_simulation_run.main(initial_sim_df, prev_year_fin_df, mc_meta_data_current_prices_upper, 1)

    return final_value_dict_lower, final_value_dict_upper

@api_view(['GET','POST'])
def risk_management_table_api(request):


    if request.method == 'GET':
        username = request.query_params.get('username')
        user_input = request.query_params
        initial_sim_variables = return_current_season_df(username)

        prev_season_df = return_prev_season_df(username)
        at_market_data = at_market_sim(initial_sim_data=initial_sim_variables, prev_year_fin_df=prev_season_df)
        current_expectations = current_financial_simulations.objects.filter(user = username)
        max_date = current_expectations.latest('date').date
        max_current_expectation_id = current_expectations.latest('id').id
        current_expectations = pd.DataFrame.from_dict(current_expectations.filter(date = max_date).filter(id = max_current_expectation_id).values())
        current_expectations = pd.DataFrame(current_expectations.iloc[:1])
        final_value_dict_lower, final_value_dict_upper = user_input_sim(user_input, initial_sim_variables, prev_season_df)

        relevent_sim_variables = ['sugar_price','hydrous_price','anhydrous_price','fx_rate','sugar_revenues','hydrous_revenues','anhydrous_revenues','cogs', 'gross_profit','sga_costs','ebit','financial_costs','net_income']
        return_values_dict = {}
        for i in range(0,len(relevent_sim_variables)):
            relevent_std_var = relevent_sim_variables[i] + '_std'
            temp_mean_returned = current_expectations[relevent_sim_variables[i]][0]
            temp_std_returned = current_expectations[relevent_std_var][0]
            return_values_dict[relevent_sim_variables[i]] = [float("{:.2f}".format(temp_mean_returned))]
            temp_dist = np.random.normal(loc=temp_mean_returned, scale=temp_std_returned, size = 1000)
            return_values_dict[relevent_sim_variables[i] + '_var'] = [float("{:.2f}".format(np.percentile(temp_dist, 5)))]
            return_values_dict[relevent_sim_variables[i] + '_at_market'] = [float("{:.2f}".format(at_market_data[relevent_sim_variables[i]][0]))]
            return_values_dict[relevent_sim_variables[i] + '_lower'] = [float("{:.2f}".format(final_value_dict_lower[relevent_sim_variables[i]][0]))]
            return_values_dict[relevent_sim_variables[i] + '_upper'] = [float("{:.2f}".format(final_value_dict_upper[relevent_sim_variables[i]][0]))]

        data = return_values_dict
        data = json.dumps(data)

        return Response(data)
    
    if request.method == 'POST':
        user_input = request.POST
        username = user_input.get('username')

        initial_sim_variables = return_current_season_df(username)

        prev_season_df = return_prev_season_df(username)
        at_market_data = at_market_sim(initial_sim_data=initial_sim_variables, prev_year_fin_df=prev_season_df)
        current_expectations = current_financial_simulations.objects.filter(user = username)
        max_date = current_expectations.latest('date').date
        max_current_expectation_id = current_expectations.latest('id').id
        current_expectations = pd.DataFrame.from_dict(current_expectations.filter(date = max_date).filter(id = max_current_expectation_id).values())
        current_expectations = pd.DataFrame(current_expectations.iloc[:1])
        final_value_dict_lower, final_value_dict_upper = user_input_sim(user_input, initial_sim_variables, prev_season_df)

        relevent_sim_variables = ['sugar_price','hydrous_price','anhydrous_price','fx_rate','sugar_revenues','hydrous_revenues','anhydrous_revenues','cogs', 'gross_profit','sga_costs','ebit','financial_costs','net_income']
        return_values_dict = {}
        for i in range(0,len(relevent_sim_variables)):
            relevent_std_var = relevent_sim_variables[i] + '_std'
            temp_mean_returned = current_expectations[relevent_sim_variables[i]][0]
            temp_std_returned = current_expectations[relevent_std_var][0]
            return_values_dict[relevent_sim_variables[i]] = [float("{:.2f}".format(temp_mean_returned))]
            temp_dist = np.random.normal(loc=temp_mean_returned, scale=temp_std_returned, size = 1000)
            return_values_dict[relevent_sim_variables[i] + '_var'] = [float("{:.2f}".format(np.percentile(temp_dist, 5)))]
            return_values_dict[relevent_sim_variables[i] + '_at_market'] = [float("{:.2f}".format(at_market_data[relevent_sim_variables[i]][0]))]
            return_values_dict[relevent_sim_variables[i] + '_lower'] = [float("{:.2f}".format(final_value_dict_lower[relevent_sim_variables[i]][0]))]
            return_values_dict[relevent_sim_variables[i] + '_upper'] = [float("{:.2f}".format(final_value_dict_upper[relevent_sim_variables[i]][0]))]

        data = return_values_dict
        data = json.dumps(data)

        return Response(data)

@api_view(['GET','POST'])
def market_data_api(request):

    if request.method == "GET":
        columns_ls = ['SB1 Comdty','USDBRL Curncy','BAAWHYDP Index','BAAWANAB Index']
        data = market_data.objects.filter(ticker__in = columns_ls)

        serializer = MarketDataSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)
    
    if request.method == 'POST':

        data = {
            'ticker': request.data.get('ticker'),
            'date': request.data.get('date'),
            'value':request.data.get('value'),
            'units':request.data.get('units')
        }

        serializer = MarketDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def sugar_position_api(request):

    if request.method == "GET":

        username = request.query_params.get('username')
        data = sugar_position_info_2.objects.filter(username = username)
        max_id = data.latest('id').id
        data = data.filter(id = max_id)
        serializer = SugarPosition2Serializers(data, context={'request': request}, many=True)

        return Response(serializer.data)
    
    if request.method == 'POST':

        form = userSugarPositionInput_2(request.POST)
                
        if form.is_valid():
            
            form.data = form.cleaned_data
            form.save(commit=False)
            form.set_username(username = request.query_params.get('username'))
            form_new = sugar_position_info_2.objects.create()
            for keys in form.data:
                if form.data[keys] != None:
                    form_new.set_field_value(keys, form.data[keys])
            form_new.full_clean()

            form_new.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print('non-valid')
            print(form.errors)
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def historical_mc_data_api(request):

    temp_date = datetime.datetime.today() + relativedelta(months=-12)
    forecast_date = monte_carlo_market_data.objects.latest('forecast_period').forecast_period
    data = monte_carlo_market_data.objects.filter(simulation_date__gte = temp_date).filter(forecast_period__gte = forecast_date)
    serializer = MonteCarloDataSerializer(data, context={'request':request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def current_mc_data_api(request):

    if request.method == "GET":
        relevant_factors = ['sugar_1', 'hydrous', 'anhydrous', 'usdbrl']
        max_date = monte_carlo_market_data.objects.latest('simulation_date').simulation_date    
        data = monte_carlo_market_data.objects.filter(reference__in = relevant_factors).filter(simulation_date = max_date)
        serializer = MonteCarloDataSerializer(data, context={'request':request}, many=True)
        return Response(serializer.data)

@api_view(['GET','POST'])
def market_price_data_api(request):

    if request.method == 'GET':

        columns_ls = ['SB1 Comdty','USDBRL Curncy','BAAWHYDP Index','BAAWANAB Index']
        price_data_df = pd.DataFrame(market_data.objects.filter(ticker__in = columns_ls).values())
        price_data_df.drop(['units', 'id'], axis = 1).drop_duplicates()
        price_data_df = price_data_df.pivot(index = 'date', columns='ticker', values='value').reset_index()
        column_ls = price_data_df.columns.to_list()
        
        new_column_ls = []
        for i in range(len(column_ls)):
            if column_ls[i] == 'date':
                new_column_ls.append('Date')
            elif column_ls[i] == 'SB1 Comdty':
                new_column_ls.append('NY No.11')
            elif column_ls[i] == 'USDBRL Curncy':
                new_column_ls.append('USDBRL')
            elif column_ls[i] == 'BAAWHYDP Index':
                new_column_ls.append('Hydrous Ethanol')
            elif column_ls[i] == 'BAAWANAB Index':
                new_column_ls.append('Anhydrous Ethanol')
        
        price_data_df.columns = new_column_ls
        price_data_df['Date'] = pd.to_datetime(price_data_df['Date'])
        price_data_df['Date'] = price_data_df['Date'].dt.strftime('%m/%d/%Y')
        price_data_df['Anhydrous Ethanol'] = price_data_df['Anhydrous Ethanol'].apply(lambda x: x*1000)
        price_data_df = price_data_df.dropna().to_dict(orient='list')
        
        return price_data_df

    if request.method == 'POST':

        id = request.data.get('id')
        ticker = request.data.get('ticker')
        date = request.data.get('date')
        value = request.data.get('')
        data = {
                'ticker': request.data.get('ticker'),
                'date': request.data.get('date'),
                'value': request.data.get('value'),
                'units':request.data.get('units')
            }
        serializer = MarketDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def userlist_api(request):

    if request.method == 'GET':
        
        data = user_list.objects.filter(username=request.user)
        serializer = UserListSerializers(data, context={'request':request})
        return Response(serializer.data)

    if request.method == 'POST':

        data = {
            'username': request.data.get('username'), 
            'create_date': request.data.get('create_date'), 
        }
        serializer = UserListSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            print('Saved New User')
            initiate_models(request.data.get('username'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fin_sim_meta_data_api(request):

    if request.method == 'GET':

        max_date =  current_financial_simulations.objects.latest("date").date
        data = market_data.objects.filter(user = request.user).filter(date__gte = max_date)
        serializer = MarketDataSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def hedgebot_best_path_api(request):

    if request.method == 'GET':
        username = request.query_params.get('username')
        data = hedgebot_results.objects.filter(username=username)
        serializer = HedgebotBestSerializer(data, context={'request':request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def hedgebot_best_path_api2(request):
    hedgebot_results_data = hedgebot_results.objects.all()
    fixed_revenues_max = hedgebot_results.objects.all().annotate(max_revenues_fixed = Max('fixed_revenues'))
    dates = list(hedgebot_results_data.dates('date', 'day', order='DESC'))
    forecast_period = list(hedgebot_results_data.dates('forecast_period', 'day', order='DESC'))
    final_date = max(dates)
    forecast_period_max = max(forecast_period)
    super_rev_ls = list(fixed_revenues_max.filter(date__gte= final_date).filter(forecast_period__gte=forecast_period_max).filter(fixed_revenues__gte = F('max_revenues_fixed')).values_list('max_revenues_fixed', flat=True))
    best_mill = list(fixed_revenues_max.filter(date__gte= final_date).filter(forecast_period__gte=forecast_period_max).filter(fixed_revenues__gte = F('max_revenues_fixed')).values_list('mill_identification_number', flat=True))
    super_rev = max(super_rev_ls)
    index_a = super_rev_ls.index(super_rev)
    best_mill_int = best_mill[index_a]
    best_mill_data = hedgebot_results.objects.all().filter(mill_identification_number = best_mill_int)
    best_mill_data_serialized = []
    for data in best_mill_data:
        x = data.return_values()
        x['date'] = x['date'].strftime("%Y-%m-%d")
        x['forecast_period'] = x['forecast_period'].strftime("%Y-%m-%d")
        best_mill_data_serialized.append(list(x.values()))

@api_view(['GET'])
def risk_var_table_api(request):

    username = request.query_params.get('username')
    data = current_financial_simulations.objects.filter(user = username)
    max_id = data.latest('id').id
    data_df = pd.DataFrame(data.filter(id = max_id).values())
    company_forecast_df = user_forecasts_assumptions_results.objects.filter(username = username).filter(season='2023_24')
    max_company_forecast_id = company_forecast_df.latest('id').id
    company_forecast_df = pd.DataFrame(user_forecasts_assumptions_results.objects.filter(id=max_company_forecast_id).values())
    old_company_forecast = pd.DataFrame(user_forecasts_assumptions_results.objects.filter(username = username).filter(season='2022_23').values())
    relevant_accounts = ['current_ratio','net_debt_to_mt_cane','gross_profit','gross_margin','net_income']
    company_forecast_accounts = ['current_ratio','net_debt_mt_of_cane','gross_profit','gross_margin','net_income']
    account_labels = ['Current Ratio','D??vida L??quida/EBITDA','EBITDA (000 R$)','Margem L??quida (%)','Resultado L??quido (000 R$)']
    final_dict = []

    '''
    'label':[],
        'prev_season':[],
        'actual_estimate':[],
        'low_10':[],
        'high_90':[],
        'prob_estimate':[]
    '''
    for account in relevant_accounts:
        final_label = account_labels[relevant_accounts.index(account)]
        company_forecast_account = company_forecast_accounts[relevant_accounts.index(account)]
        temp_mu = data_df[account]
        temp_sigma = data_df[account+'_std']
        temp_distribution = np.random.normal(temp_mu, temp_sigma, 1000)
        temp_comp_forecast = company_forecast_df[company_forecast_account].values.tolist()[0]
        try:
            temp_comp_forecast = temp_comp_forecast[0]
        except:
            temp_comp_forecast = temp_comp_forecast

        try:
            temp_comp_forecast = temp_comp_forecast[0]
        except:
            temp_comp_forecast = temp_comp_forecast

        temp_perc_comp_fore = percentileofscore(temp_distribution, temp_comp_forecast, kind = 'weak')
        temp_prev_season = old_company_forecast[company_forecast_account].values.tolist()[0]

        try:
            temp_prev_season = temp_prev_season[0]
        except:
            temp_prev_season = temp_prev_season

        try:
            temp_prev_season = temp_prev_season[0]
        except:
            temp_prev_season = temp_prev_season

        temp_low_10 = np.percentile(temp_distribution, 10)
        temp_high_90 = np.percentile(temp_distribution, 90)

        try:
            temp_dict = {
                'label':final_label,
                'prev_season':temp_prev_season,
                'actual_estimate':temp_comp_forecast,
                'low_10':temp_low_10,
                'high_90':temp_high_90,
                'prob_estimate':temp_perc_comp_fore
            }
            final_dict.append(temp_dict)
            
        except:
            continue

    final_dict = json.dumps(final_dict)
    return Response(final_dict)   

@api_view(['GET'])
def return_current_season_df_api(request):
    
    username = request.query_params.get('username')
    season_list = ['23_24', '2023_24']
    current_season_df = user_forecasts_assumptions_results.objects.filter(username = username).filter(season__in =season_list)
    verbose_name_dict = user_forecasts_assumptions_results.return_verbose(user_forecasts_assumptions_results)
    #max_sim_date = current_season_df.latest('date').date
    #current_season_df = current_season_df.filter(date = max_sim_date)
    max_id = current_season_df.latest('id').id
    current_season_df = current_season_df.filter(id = max_id)
    current_season_df = pd.DataFrame.from_dict(current_season_df.values())
    current_season_df = current_season_df.drop(['date'], axis = 1)
    counter = 0

    for key in verbose_name_dict:
        if key == 'date':
            continue
        temp_ls = []
        temp_str = verbose_name_dict[key]
        temp_values = current_season_df[key].values[0]
        temp_ls.append(temp_str)
        temp_ls.append(temp_values)
        try:
            var_name = temp_str[:temp_str.index('-')]
        except:
            var_name = temp_str
        
        temp_ls.append(var_name)
        
        try:
            group_name = re.search('-(.*)-', temp_str).group(1)
        except:
            group_name = "not_listed"
        
        temp_ls.append(group_name)
        
        try:
            index = findnth(temp_str, '-', 1)
            units = temp_str[index+1:]
        except:
            units ='not_listed'
        
        temp_ls.append(units)

        if counter == 0:
            temp_df = pd.DataFrame([temp_ls], columns = ['Original','Value','Variable_name_eng','Data_group','Units'])
        else:
            df_temp = pd.DataFrame([temp_ls], columns = ['Original','Value','Variable_name_eng','Data_group','Units'])
            temp_df = pd.concat([temp_df, df_temp], ignore_index=True)
        counter += 1

    data = json.dumps(temp_df.to_dict(orient = 'list'))
    return Response(data)

def return_percentiles(mu, std):

    temp_array = np.arange(0,100,1)
    temp_dist = np.random.normal(mu, std, 1000)
    return np.percentile(temp_dist, temp_array)

@api_view(['GET'])
def range_probabilities_api(request):
    
    
    relevant_factors = ['sugar_1', 'hydrous', 'anhydrous', 'usdbrl']
    max_date = monte_carlo_market_data.objects.latest('simulation_date').simulation_date    
    data = monte_carlo_market_data.objects.filter(reference__in = relevant_factors).filter(simulation_date = max_date)
    max_forecast_period = data.latest('forecast_period').forecast_period
    data = pd.DataFrame(list(data.filter(forecast_period = max_forecast_period).values()))
    final_dict = {

    }
    
    for i in range(0,len(relevant_factors)):
        temp_factor = relevant_factors[i]
        temp_mu = data['mean_returned'].loc[data['reference'] == temp_factor]
        temp_std = data['std_returned'].loc[data['reference'] == temp_factor]
        final_dict[temp_factor] = list(return_percentiles(temp_mu, temp_std))
    final_dict = json.dumps(final_dict)
    return Response(final_dict)

@api_view(['GET'])
def financial_account_range_probabilities(request):
    
    username = request.query_params.get('username')

    if request.method == 'GET':

        current_expectations = current_financial_simulations.objects.filter(user = username)
        max_current_expectation_id = current_expectations.latest('id').id
        current_expectations = pd.DataFrame.from_dict(current_expectations.filter(id = max_current_expectation_id).values())
        current_expectations = pd.DataFrame(current_expectations.iloc[:1])
        relevent_sim_variables = ['sugar_revenues','hydrous_revenues','anhydrous_revenues','cogs', 'gross_profit','sga_costs','ebit','financial_costs','net_income','ethanol_revenues']
        return_values_dict = {}
        for i in range(0,len(relevent_sim_variables)):
            if relevent_sim_variables[i] == 'ethanol_revenues':
                relevent_std_var_1 = 'hydrous_revenues_std'
                relevent_std_var_2 = 'anhydrous_revenues_std'
                temp_mean_returned_1 = current_expectations['hydrous_revenues'][0]
                temp_mean_returned_2 = current_expectations['anhydrous_revenues'][0]
                temp_std_returned_1 = current_expectations[relevent_std_var_1][0]
                temp_std_returned_2 = current_expectations[relevent_std_var_2][0]
                temp_mu = temp_mean_returned_1 + temp_mean_returned_2
                temp_sigma = temp_std_returned_1 + temp_std_returned_2
                return_values_dict[relevent_sim_variables[i]] = list(return_percentiles(temp_mu, temp_sigma))
            else:
                relevent_std_var = relevent_sim_variables[i] + '_std'
                temp_mean_returned = current_expectations[relevent_sim_variables[i]][0]
                temp_std_returned = current_expectations[relevent_std_var][0]
                if temp_std_returned == 0:
                    temp_std_returned = abs(temp_mean_returned * 0.01)
                return_values_dict[relevent_sim_variables[i]] = list(return_percentiles(temp_mean_returned, temp_std_returned))

        data = return_values_dict
        data = json.dumps(data)

        return Response(data)

@api_view(['POST'])
def update_user_forecast_assumptions(request):


    if request.method == "POST":
        username = request.query_params.get('username')
        form_2324 = userInputForm(request.POST, prefix = "form_2324")
        form_2223 = userInputForm(request.POST, prefix = "form_2223")
        form_2122 = userInputForm(request.POST, prefix = "form_2122")
    

        if form_2324.is_valid():
            
            form_2324.data = form_2324.cleaned_data
            form_2324.save(commit=False)
            form_2324.set_season(season = '2023_24')
            form_2324.set_username(username)
            form_new_2324 = user_forecasts_assumptions_results.objects.create()
            for keys in form_2324.data:
                if form_2324.data[keys] != None:
                    form_new_2324.set_field_value(keys, form_2324.data[keys])
            
            form_new_2324.full_clean()
            form_new_2324.save()
            financial_sim_update(username, 100)

        else:
            print('form 2324 non-valid')
            print(form_2324.errors)

        if form_2223.is_valid():

            form_2223.data = form_2223.cleaned_data
            form_2223.save(commit=False)
            form_2223.set_season(season ='2022_23')
            form_2223.set_username(username)
            form_new_2223 = user_forecasts_assumptions_results.objects.create()
            for keys in form_2223.data:
                if form_2223.data[keys] != None:
                    form_new_2223.set_field_value(keys, form_2223.data[keys])
            
            form_new_2223.full_clean()
            form_new_2223.save()

        else:
            print('form 2223 non-valid')
            print(form_2223.errors)

        if form_2122.is_valid():

            form_2122.data = form_2122.cleaned_data
            form_2122.save(commit=False)
            form_2122.set_season(season = '2021_22')
            form_2122.set_username(username)
            form_new_2122 = user_forecasts_assumptions_results.objects.create()
            for keys in form_2122.data:
                if form_2122.data[keys] != None:
                    form_new_2122.set_field_value(keys, form_2122.data[keys])
            
            form_new_2122.full_clean()
            form_new_2122.save()

        else:
            print('form 2122 non-valid')
            print(form_2122.errors)

        return Response("Success")

@api_view(['GET'])
def get_user_assumptions_results(request):

    username = request.query_params.get('username')
    season_list = ['23_24', '2023_24']
    current_season_df = user_forecasts_assumptions_results.objects.filter(username = username).filter(season__in =season_list)
    max_id = current_season_df.latest('id').id
    current_season_df = pd.DataFrame(current_season_df.filter(id = max_id).values())
    return Response(current_season_df.to_dict(orient='list'))

@api_view({'GET'})
def get_market_forecasts_api(request):

    data = market_forecasts.objects.filter.all()
    serializer = MarketForecastSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)