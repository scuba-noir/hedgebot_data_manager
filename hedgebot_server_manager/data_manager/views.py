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
from data_manager.models import market_data, risk_management_user_input_table
from data_manager.models import sugar_position_info_2
from data_manager.models import user_list, target_prices, hedgebot_results_meta_data, user_forecasts_assumptions_results, current_financial_simulations
from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics
from data_manager.serializers import SugarPosition2Serializers, MonteCarloDataSerializer, MarketDataSerializer, FinSimMetaDataSerializer, UserListSerializers, HistMCDataSerializer, HedgebotBestSerializer
from rest_framework.renderers import JSONRenderer
from data_manager.serializers import RiskManagementUserInputTableSerializer

from . import full_simulation_run

def findnth(string, substring, n):
   parts = string.split(substring, n + 1)
   if len(parts) <= n + 1:
      return -1
   return len(string) - len(parts[-1]) - len(substring)

def return_current_season_df(username):
    
    current_season_df = user_forecasts_assumptions_results.objects.filter(username = username).filter(season='23_24')
    verbose_name_dict = user_forecasts_assumptions_results.return_verbose(user_forecasts_assumptions_results)
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

def return_prev_season_df(username):
    current_season_df = user_forecasts_assumptions_results.objects.filter(username = username).filter(season='22_23')
    verbose_name_dict = user_forecasts_assumptions_results.return_verbose(user_forecasts_assumptions_results)
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

def financial_sim_update(username):

    current_season_df = return_current_season_df(username)
    prev_season_df = return_prev_season_df(username)

    mc_meta_data = pd.DataFrame(monte_carlo_market_data.objects.all().values())
    final_value_dict = full_simulation_run.main(current_season_df, prev_season_df, mc_meta_data, 1000)
    
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
        sugar_price_std = statistics.stdev(list(final_value_dict['sugar_price'])),
        hydrous_price_std = statistics.stdev(list(final_value_dict['hydrous_price'])),
        anhydrous_price_std = statistics.stdev(list(final_value_dict['anhydrous_price'])),
        energy_price_std = statistics.stdev(list(final_value_dict['energy_price'])),
        fx_rate_std = statistics.stdev(list(final_value_dict['fx_rate'])),
        selic_rate_std = statistics.stdev(list(final_value_dict['selic_rate'])),
        foreign_debt_rate_std = statistics.stdev(list(final_value_dict['foreign_debt_rate'])),
        inflation_rate_std = statistics.stdev(list(final_value_dict['inflation_rate'])),
        crude_price_std = statistics.stdev(list(final_value_dict['crude_price'])),
        fertilizer_price_std = statistics.stdev(list(final_value_dict['fertilizer_price'])),
        sugar_revenues_std = statistics.stdev(list(final_value_dict['sugar_revenues'])),
        hydrous_revenues_std = statistics.stdev(list(final_value_dict['hydrous_revenues'])),
        anhydrous_revenues_std = statistics.stdev(list(final_value_dict['anhydrous_revenues'])),
        energy_revenues_std = statistics.stdev(list(final_value_dict['energy_revenues'])),
        input_costs_std = statistics.stdev(list(final_value_dict['input_costs'])),
        fuel_costs_std = statistics.stdev(list(final_value_dict['fuel_costs'])),
        freight_costs_std = statistics.stdev(list(final_value_dict['freight_costs'])),
        labor_costs_std = statistics.stdev(list(final_value_dict['labor_costs'])),
        indutrial_costs_std = statistics.stdev(list(final_value_dict['indutrial_costs'])),
        depreciation_std = statistics.stdev(list(final_value_dict['depreciation'])),
        planting_costs_std = statistics.stdev(list(final_value_dict['planting_costs'])),
        lease_costs_std = statistics.stdev(list(final_value_dict['lease_costs'])),
        gross_profit_std = statistics.stdev(list(final_value_dict['gross_profit'])),
        sga_costs_std = statistics.stdev(list(final_value_dict['sga_costs'])),
        ebit_std = statistics.stdev(list(final_value_dict['ebit'])),
        financial_costs_std = statistics.stdev(list(final_value_dict['financial_costs'])),
        ebt_std = statistics.stdev(list(final_value_dict['ebt'])),
        tax_std = statistics.stdev(list(final_value_dict['tax'])),
        net_income_std = statistics.stdev(list(final_value_dict['net_income'])),
        gross_margin_std = statistics.stdev(list(final_value_dict['gross_margin'])),
        ebitda_margin_std = statistics.stdev(list(final_value_dict['ebitda_margin'])),
        net_margin_std = statistics.stdev(list(final_value_dict['net_margin'])),
        net_debt_to_ebitda_std = statistics.stdev(list(final_value_dict['net_debt_to_ebitda'])),
        net_debt_to_mt_cane_std = statistics.stdev(list(final_value_dict['net_debt_to_mt_cane'])),
        indebtness_std = statistics.stdev(list(final_value_dict['indebtness'])),
        short_term_debt_std = statistics.stdev(list(final_value_dict['short_term_debt'])),
        current_ratio_std = statistics.stdev(list(final_value_dict['current_ratio']))        
    )

# Create your views here.
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
    final_value_dict = full_simulation_run.main(initial_sim_data, prev_year_fin_df, mc_meta_data_current_prices, 1)
    return final_value_dict

def user_input_sim(user_input, initial_sim_data, prev_year_fin_df):


    most_recent_mc_date = monte_carlo_market_data.objects.latest('simulation_date').simulation_date
    max_forecast_period = monte_carlo_market_data.objects.latest('simulation_date').forecast_period
    mc_meta_data_current_prices_upper = pd.DataFrame(monte_carlo_market_data.objects.filter(simulation_date = most_recent_mc_date).filter(forecast_period = max_forecast_period).values())
    mc_meta_data_current_prices_lower = mc_meta_data_current_prices_upper
    relevent_market_var_ls = ['sugar_1','hydrous','anhydrous','usdbrl']
    for i in range(0,len(relevent_market_var_ls)):
        mc_meta_data_current_prices_upper['mean_returned'].loc[mc_meta_data_current_prices_upper['reference'] == relevent_market_var_ls[i]] = float(user_input[relevent_market_var_ls[i] + '_upper'])
        mc_meta_data_current_prices_lower['mean_returned'].loc[mc_meta_data_current_prices_lower['reference'] == relevent_market_var_ls[i]] = float(user_input[relevent_market_var_ls[i] + '_lower'])
        mc_meta_data_current_prices_upper['std_returned'].loc[mc_meta_data_current_prices_upper['reference'] == relevent_market_var_ls[i]] = 0
        mc_meta_data_current_prices_lower['std_returned'].loc[mc_meta_data_current_prices_lower['reference'] == relevent_market_var_ls[i]] = 0
    

    temp_yield = float(user_input['cane_yield'])
    temp_trs = float(user_input['trs'])
    temp_production_mix_sugar = float(user_input['production_mix_sugar'])
    temp_production_mix_hydrous = float(user_input['production_mix_hydrous'])
    temp_production_mix_anhydrous = float(user_input['production_mix_anhydrous'])
    temp_cane_area = float(initial_sim_data['Value'].loc[(initial_sim_data['Variable_name_eng'] == 'Planting area') & (initial_sim_data['Data_group'] == 'Own Cane Assumptions')])
    temp_atr = float(temp_cane_area) * float(temp_yield) * float(temp_trs) + initial_sim_data['Value'].loc[(initial_sim_data['Variable_name_eng'] == 'Third party cane') & (initial_sim_data['Units'] == '000 mt')]
    temp_sugar_prod = (temp_atr * temp_production_mix_sugar)/1000/1.06
    temp_hydrous_prod = (temp_atr * temp_production_mix_hydrous)/1000/1.53
    temp_anhydrous_prod = (temp_atr * temp_production_mix_anhydrous)/1000/1.53
    
    initial_sim_df = initial_sim_data
    initial_sim_df['Value'].loc[(initial_sim_df['Variable_name_eng'] == 'Sugar production') & (initial_sim_df['Data_group'] == 'Final Volume Forecasts')] = temp_sugar_prod
    initial_sim_df['Value'].loc[(initial_sim_df['Variable_name_eng'] == 'Hydrous production') & (initial_sim_df['Data_group'] == 'Final Volume Forecasts')] = temp_hydrous_prod
    initial_sim_df['Value'].loc[(initial_sim_df['Variable_name_eng'] == 'Anydrous production') & (initial_sim_df['Data_group'] == 'Final Volume Forecasts')] = temp_anhydrous_prod

    final_value_dict_lower = full_simulation_run.main(initial_sim_df, prev_year_fin_df, mc_meta_data_current_prices_lower, 1) 
    final_value_dict_upper = full_simulation_run.main(initial_sim_df, prev_year_fin_df, mc_meta_data_current_prices_upper, 1)


    return final_value_dict_lower, final_value_dict_upper

@api_view(['GET','POST'])
def risk_management_table_api(request):

    username = request.query_params.get('username')

    if request.method == 'GET':

        user_input = request.query_params
        initial_sim_variables = return_current_season_df(username)
        prev_season_df = return_prev_season_df(username)
        at_market_data = at_market_sim(initial_sim_data=initial_sim_variables, prev_year_fin_df=prev_season_df)
        current_expectations = current_financial_simulations.objects.filter(user = username)
        max_date = current_expectations.latest('date').date
        current_expectations = pd.DataFrame.from_dict(current_expectations.filter(date = max_date).values())
        current_expectations = pd.DataFrame(current_expectations.iloc[:1])
        final_value_dict_lower, final_value_dict_upper = user_input_sim(user_input, initial_sim_variables, prev_season_df)
        print(at_market_data)

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

        #data_obj = risk_management_user_input_table.objects.update_or_create(**return_values_dict)
        #serializer = RiskManagementUserInputTableSerializer(data_obj, context = {'request':request}, many = True)
        
        data = return_values_dict
        data = json.dumps(data)

        return Response(data)


@api_view(['GET'])
def market_data_api(request):

    if request.method == "GET":
        columns_ls = ['SB1 Comdty','USDBRL Curncy','BAAWHYDP Index','BAAWANAB Index']
        data = market_data.objects.filter(ticker__in = columns_ls)

        serializer = MarketDataSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def sugar_position_api(request):

    if request.method == "GET":
        print(request)
        username = request.query_params.get('username')
        data = sugar_position_info_2.objects.filter(username = username)
        serializer = SugarPosition2Serializers(data, context={'request': request}, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def historical_mc_data_api(request):

    temp_date = datetime.datetime.today() + relativedelta(months=-12)
    forecast_date = monte_carlo_market_data.objects.latest('forecast_period').forecast_period
    #print('Forecast period: ' + forecast_date.strftime("%Y-%m-%d"))
    #print('Simulation Date: ' + temp_date.strftime("%Y-%m-%d"))
    data = monte_carlo_market_data.objects.filter(simulation_date__gte = temp_date).filter(forecast_period__gte = forecast_date)
    serializer = MonteCarloDataSerializer(data, context={'request':request}, many=True)
    #print(data.values())
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

        new_user = request.data.get('username')
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
    
    desc_names = [
            'Id',
            'Date',
            'Season',
            'Own area-Own Cane Assumptions-ha', 
            'Leased area-Own Cane Assumptions-ha',
            'Yield-Own Cane Assumptions-mt of cane/ha',
            'Own cane-Own Cane Assumptions-000 mt',
            'Lease cost-Own Cane Assumptions-mt of cane/ha',
            'Average TRS, lease contract-Own Cane Assumptions-kg/mt of cane',
            'Lease cost-Own Cane Assumptions-BRL/ha',
            'Planting area-Own Cane Assumptions-000 ha',
            'Third party cane-Third Party Cane Assumptions-000 mt',
            'Average TRS, cane contract-Third Party Cane Assumptions-kg/mt of cane',
            'Third party cane cost-Third Party Cane Assumptions-BRL/mt of cane',
            'Average TRS-Production Mix Assumptions-kg/mt of cane',
            'Sugar-Production Mix Assumptions-%',
            'Hydrous-Production Mix Assumptions-%',
            'Anhydrous-Production Mix Assumptions-%',
            'TRS x Sugar-Production Mix Assumptions-kg x kg',
            'ATR x Hydrous-Production Mix Assumptions-kg x l',
            'ATR x Anhydrous-Production Mix Assumptions-kg x l',
            'Energy production-Production Mix Assumptions-MWh',
            'Sugar-Price Assumptions-cts/lb',
            'Hydrous-Price Assumptions-BRL/m3',
            'Anhydrous-Price Assumptions-BRL/m3',
            'Energy-Price Assumptions-BRL/MWh',
            'Exchange rate-Price Assumptions-BRL/USD',
            'TRS-Price Assumptions-BRL/kg',
            'Domestic interest rate-Price Assumptions-% p.a.',
            'Foreign interest rate-Price Assumptions-% p.a.',
            'Inflation-Price Assumptions-% a.a',
            'Crude oil-Price Assumptions-USD/bbl',
            'Fertilizers-Price Assumptions-USD/mt',
            'Initial cash-Balance Sheet Assumptions-000 BRL',
            'Accounts receivable-Balance Sheet Assumptions-days',
            'Inventories-Balance Sheet Assumptions-days',
            'Other current assets-Balance Sheet Assumptions-% of revenues',
            'Other non current assets-Balance Sheet Assumptions-% of revenues',
            'Short term accounts payable-Balance Sheet Assumptions-days',
            'Other current liabilities-Balance Sheet Assumptions-% of COGS',
            'Other non current liabilities-Balance Sheet Assumptions-% of COGS',
            'Issued capital-Balance Sheet Assumptions-000 BRL',
            'Income tax rate-Balance Sheet Assumptions-%',
            'Sales expenses-SGA Assumptions-BRL/mt of cane',
            'Administrative expenses-SGA Assumptions-BRL/mt of cane',
            'Other SG&A-SGA Assumptions-BRL/mt of cane',
            'Average cost (coupon), USD debt-Indebtness Assumptions-Libor +, p.a.',
            'Average cost (coupon), USD debt-Indebtness Assumptions-CDI +, p.a.',
            'US$ debt, short term-Indebtness Assumptions-000 USD',
            'US$ debt, long term-Indebtness Assumptions-000 USD',
            'US$ debt, total-Indebtness Assumptions-000 USD',
            'US$ debt, short term-Indebtness Assumptions-000 BRL',
            'US$ debt, long term-Indebtness Assumptions-000 BRL',
            'US$ debt, total-Indebtness Assumptions-000 BRL',
            'R$ debt, short term-Indebtness Assumptions-000 BRL',
            'R$ debt, long term-Indebtness Assumptions-000 BRL',
            'Total debt, short term-Indebtness Assumptions-000 BRL',
            'Total debt, long term-Indebtness Assumptions-000 BRL',
            'Total debt-Indebtness Assumptions-000 BRL',
            'Financial expenses, US$ debt-Indebtness Assumptions-000 BRL',
            'Financial expenses, R$ debt-Indebtness Assumptions-000 BRL',
            'Total financial expenses-Indebtness Assumptions-000 BRL',
            'Inputs-Production Cost Assumptions-BRL/mt of cane',
            'Fuel-Production Cost Assumptions-BRL/mt of cane',
            'Freights-Production Cost Assumptions-BRL/mt of cane',
            'Labor cost-Production Cost Assumptions-BRL/mt of cane',
            'Industrial cost-Production Cost Assumptions-BRL/mt of cane',
            'Depreciation-Production Cost Assumptions-BRL/mt of cane',
            'Planting cost-Production Cost Assumptions-BRL/ha',
            'Cane crushed-Final Volume Forecasts-000 mt',
            'Sugar production-Final Volume Forecasts-000 mt',
            'Hydrous production-Final Volume Forecasts-000 m3',
            'Anhydrous production-Final Volume Forecasts-000 m3',
            'Energy production-Final Volume Forecasts-MWh',
            'Sugar revenues-Income Statement Forecasts-000 USD',
            'Sugar Revenues-Income Statement Forecasts-000 BRL',
            'Hydrous revenues-Income Statement Forecasts-000 BRL',
            'Anhydrous revenues-Income Statement Forecasts-000 BRL',
            'Energy revenues-Income Statement Forecasts-000 BRL',
            'Total revenues-Income Statement Forecasts-000 BRL',
            'Lease cost-Income Statement Forecasts-000 BRL',
            'Third party cane cost-Income Statement Forecasts-000 BRL',
            'Inputs-Income Statement Forecasts-000 BRL',
            'Fuel-Income Statement Forecasts-000 BRL',
            'Freights-Income Statement Forecasts-000 BRL',
            'Labor cost-Income Statement Forecasts-000 BRL',
            'Industrial cost-Income Statement Forecasts-000 BRL',
            'Depreciation-Income Statement Forecasts-000 BRL',
            'Planting cost-Income Statement Forecasts-000 BRL',
            'Total COGS-Income Statement Forecasts-000 BRL',
            'Gross profit-Income Statement Forecasts-000 BRL',
            'Sales expenses-Cash Flow Statement Forecasts-000 BRL',
            'Administrative expenses-Cash Flow Statement Forecasts-000 BRL',
            'Other SG&A-Cash Flow Statement Forecasts-000 BRL',
            'Total SG&A-Cash Flow Statement Forecasts-000 BRL',
            'EBIT-Cash Flow Statement Forecasts-000 BRL',
            'Financial expenses-Cash Flow Statement Forecasts-000 BRL',
            'Profit before taxes-Cash Flow Statement Forecasts-000 BRL',
            'Income tax-Cash Flow Statement Forecasts-000 BRL',
            'Net income-Cash Flow Statement Forecasts-000 BRL',
            'Depreciation-Cash Flow Statement Forecasts-000 BRL',
            'Working capital variation-Cash Flow Statement Forecasts-000 BRL',
            'Cash flow from operations-Cash Flow Statement Forecasts-000 BRL',
            'CAPEX-Cash Flow Statement Forecasts-000 BRL',
            'Write offs-Cash Flow Statement Forecasts-000 BRL',
            'Cas flow from investment activities-Cash Flow Statement Forecasts-000 BRL',
            'Debt amortization-Cash Flow Statement Forecasts-000 BRL',
            'New debt-Cash Flow Statement Forecasts-000 BRL',
            'Cash flow from financing activities-Cash Flow Statement Forecasts-000 BRL',
            'Change in cash-Cash Flow Statement Forecasts-000 BRL',
            'Initial cash-Cash Flow Statement Forecasts-000 BRL',
            'Ending cash-Cash Flow Statement Forecasts-000 BRL',
            'Minimum refinancing-Cash Flow Statement Forecasts-000 BRL',
            'Cash-Asset Sheet Forecasts-000 BRL',
            'Accounts receivable-Asset Sheet Forecasts-000 BRL',
            'Inventories-Asset Sheet Forecasts-000 BRL',
            'Other current assets-Asset Sheet Forecasts-000 BRL',
            'Total current assets-Asset Sheet Forecasts-000 BRL',
            'PP&E-Asset Sheet Forecasts-000 BRL',
            'Other non current assets-Asset Sheet Forecasts-000 BRL',
            'Total non current assets-Asset Sheet Forecasts-000 BRL',
            'Total assets-Asset Sheet Forecasts-000 BRL',
            'Short term accounts payable-Liabilities Sheet Forecasts-000 BRL',
            'Short term debt-Liabilities Sheet Forecasts-000 BRL',
            'Other current liabilities-Liabilities Sheet Forecasts-000 BRL',
            'Total current liabilities-Liabilities Sheet Forecasts-000 BRL',
            'Long term debt-Liabilities Sheet Forecasts-000 BRL',
            'Other non current liabilities-Liabilities Sheet Forecasts-000 BRL',
            'Total non current liabilities-Liabilities Sheet Forecasts-000 BRL',
            'Total liabilities-Liabilities Sheet Forecasts-000 BRL',
            'Issued capital-Liabilities Sheet Forecasts-000 BRL',
            'Retained earnings-Liabilities Sheet Forecasts-000 BRL',
            'Total equity-Liabilities Sheet Forecasts-000 BRL',
            'Liabilities + equity-Liabilities Sheet Forecasts-000 BRL',
            'Gross margin-Financial KPI Forecasts-%',
            'EBITDA-Financial KPI Forecasts-000 BRL',
            'EBITDA margin-Financial KPI Forecasts-%',
            'Net income margin-Financial KPI Forecasts-%',
            'Net debt-Financial KPI Forecasts-000 BRL',
            'Net debt/EBITDA-Financial KPI Forecasts-%',
            'Net debt/mt of cane-Financial KPI Forecasts-%',
            'Indebtedness-Financial KPI Forecasts-%',
            'Short term-Financial KPI Forecasts-% of total',
            'Current ratio-Financial KPI Forecasts-%',
            'Revenue variation-Financial KPI Forecasts-% YoY',
            'Income variation-Financial KPI Forecasts-% YoY',
            'DSCR-Financial KPI Forecasts-%',
            'Username'
            ]

    data = financial_simulation_meta_data_historical.objects.filter(username = request.user).filter(season = '23_24')
    max_date = data.latest('simulation_date').simulation_date
    data_df = pd.DataFrame(data.filter(simulation_date = max_date).values())
    temp_ls = []
    company_forecast_df = pd.DataFrame(user_forecasts_assumptions_results.objects.filter(username = request.user).filter(season='23_24').values())
    company_forecast_df.columns = desc_names
    obj, created = user_forecasts_assumptions_results.objects.get_or_create(username = request.user, season = '23_24')
    obj, created = user_forecasts_assumptions_results.objects.get_or_create(username = request.user, season = '22_23')
    old_company_forecast = pd.DataFrame(user_forecasts_assumptions_results.objects.filter(username = request.user).filter(season='22_23').values())
    old_company_forecast.columns = desc_names
    relevant_accounts = ['Total assets','Net debt/mt of cane','EBITDA','Gross margin','Total revenues','Net income']
    account_labels = ['CMV Total (000 R$)','Dívida Líquida/EBITDA','EBITDA (000 R$)','Margem Líquida (%)','Receita Total (000 R$)','Resultado Líquido (000 R$)']
    data_df = data_df.loc[data_df['account'].isin(relevant_accounts)]
    for row, items in data_df.iterrows():
        temp_account = items['account']
        if (temp_account in relevant_accounts) == False:
            continue
        final_label = account_labels[relevant_accounts.index(temp_account)]
        temp_datagroup = items['datagroup']
        subs = temp_account + '-' + temp_datagroup
        temp_index_name = [i for i in desc_names if subs in i]
        temp_mu = items['mean_returned']
        temp_sigma = items['std_returned']
        temp_distribution = np.random.normal(temp_mu, temp_sigma, 1000)
        temp_comp_forecast = company_forecast_df[temp_index_name].values.tolist()[0]
        try:
            temp_comp_forecast = temp_comp_forecast[0]
        except:
            temp_comp_forecast = temp_comp_forecast

        try:
            temp_comp_forecast = temp_comp_forecast[0]
        except:
            temp_comp_forecast = temp_comp_forecast

        temp_perc_comp_fore = percentileofscore(temp_distribution, temp_comp_forecast, kind = 'weak')
        temp_prev_season = old_company_forecast[temp_index_name].values.tolist()[0]

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
            obj = risk_var_table.objects.update_or_create(label = final_label, prev_season = int(temp_prev_season), actual_estimate = int(temp_comp_forecast), low_10 = int(temp_low_10), high_90 = int(temp_high_90), prob_estimate = temp_perc_comp_fore, username = request.user)
        except:
            continue

    data = risk_var_table.objects.filter(username = request.user)
    serializer = RiskVarTableSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)   

@api_view(['GET'])
def return_current_season_df_api(request):
    
    username = request.query_params.get('username')
    current_season_df = user_forecasts_assumptions_results.objects.filter(username = username).filter(season='23_24')
    verbose_name_dict = user_forecasts_assumptions_results.return_verbose(user_forecasts_assumptions_results)
    current_season_df = pd.DataFrame(current_season_df.values())
    current_season_df['date'] = pd.to_datetime(current_season_df['date'])
    current_season_df = current_season_df.loc[current_season_df['date'] == max(current_season_df['date'])]
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

@api_view(['GET'])
def range_probabilities_api(request):

    print("Range Probability GET Request")
    var_name = request.query_params.get('var_name')
    upper_val = request.query_params.get('upper')
    lower_val = request.query_params.get('lower')
    probability = 0
    relevant_factors = [var_name]
    max_date = monte_carlo_market_data.objects.latest('simulation_date').simulation_date    
    data = monte_carlo_market_data.objects.filter(reference__in = relevant_factors).filter(simulation_date = max_date)
    max_forecast_period = data.latest('forecast_period').forecast_period
    data = data.filter(forecast_period = max_forecast_period)
    data_df = pd.DataFrame(data.values)
    serializer = MonteCarloDataSerializer(data, context={'request':request}, many=True)
    print(data_df)
    return Response(serializer.data)