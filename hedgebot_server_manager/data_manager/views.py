from django.shortcuts import render
import numpy as np
import pandas as pd
import numpy as np
import numpy as np
import datetime
import re
import statistics
from scipy.stats import norm, percentileofscore
from django.db.models import F, Q, When, Max, Avg, Window, StdDev
from data_manager.models import user_forecasts_assumptions_results
from data_manager.models import hedgebot_results
from data_manager.models import financial_simulation_meta_data_historical
from data_manager.models import financial_simulations_results
from data_manager.models import monte_carlo_market_data
from data_manager.models import market_data
from data_manager.models import sugar_position_info_2
from data_manager.models import user_list, target_prices, hedgebot_results_meta_data, user_forecasts_assumptions_results, current_financial_simulations
from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from data_manager.serializers import SugarPosition2Serializers, MonteCarloDataSerializer, MarketDataSerializer, FinSimMetaDataSerializer, UserListSerializers, HistMCDataSerializer, HedgebotBestSerializer
from rest_framework.renderers import JSONRenderer

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
    final_value_dict = full_simulation_run.main(current_season_df, prev_season_df, mc_meta_data)
    
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
        print(date_range[i])
        hedgebot_results.objects.get_or_create(username = username, forecast_period = date_range[i].strftime('%Y-%m-%d'))
    financial_simulations_results.objects.get_or_create(username=username)
    target_prices.objects.get_or_create(username=username)
    sugar_position_info_2.objects.get_or_create(username=username)
    user_forecasts_assumptions_results.objects.get_or_create(username=username)
    user_forecasts_assumptions_results.objects.get_or_create(username=username, season = '22_23')


@api_view(['GET'])
def market_data_api(request):

    if request.method == "GET":
        columns_ls = ['SB1 Comdty','USDBRL Curncy','BAAWHYDP Index','BAAWANAB Index']
        data = market_data.objects.filter(ticker__in = columns_ls)

        serializer = MarketDataSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def mc_data_api(request):

    if request.method == "GET":
        data = monte_carlo_market_data.objects.all()

        serializer = MonteCarloDataSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def sugar_position_api(request):

    if request.method == "GET":
        print(request.user)
        data = sugar_position_info_2.objects.filter(username = request.user)
        serializer = SugarPosition2Serializers(data, context={'request': request}, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def historical_mc_data_api(request):

    temp_date = date.today() + relativedelta(months=-6)
    data = monte_carlo_market_data.objects.filter(simulation_date__gte = temp_date)
    serializer = HistMCDataSerializer(data, context={'request':request}, many=True)
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
        data = hedgebot_results.objects.filter(username = request.user)
        serializer = HedgebotBestSerializer(data, context={'request':request}, many=True)
        return Response(serializer.data)

