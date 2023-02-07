from django.shortcuts import render
import numpy as np
import pandas as pd
import numpy as np
import numpy as np
import datetime
import re

from scipy.stats import norm, percentileofscore
from django.db.models import F, Q, When, Max, Avg, Window, StdDev
from data_manager.models import user_forecasts_assumptions_results
from data_manager.models import hedgebot_results
from data_manager.models import sugar_position_info
from data_manager.models import financial_simulation_meta_data_historical
from data_manager.models import financial_simulations_results
from data_manager.models import monte_carlo_market_data
from data_manager.models import market_data
from data_manager.models import sugar_position_info_2
from data_manager.models import user_list, target_prices, hedgebot_results_meta_data, user_forecasts_assumptions_results
from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from data_manager.serializers import SugarPositionSerializers, MonteCarloDataSerializer, MarketDataSerializer, FinSimMetaDataSerializer, UserListSerializers

def current_financial_sim(username):

    current_season_df = user_forecasts_assumptions_results.objects.filter(username = username).filter(season='23_24')
    verbose_name_dict = user_forecasts_assumptions_results.return_verbose(user_forecasts_assumptions_results)
    for key in verbose_name_dict:
        temp_str = verbose_name_dict[key]
        try:
            var_name = temp_str[:temp_str.index('-')]
            
        except:
            var_name = temp_str
        print('test', temp_str)
        try:
            group_name = re.search('-(.*)-', temp_str).group(1)
        except:
            group_name = "not_listed"

        try:
            units = re.search('-(.*)', temp_str).group(2)
        except:
            units ='not_listed'
        print('-------------')
        print(var_name)
        print(group_name)
        print(units)
    current_season_df = pd.DataFrame(current_season_df.values())
    current_season_df['date'] = pd.to_datetime(current_season_df['date'])
    

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
    
    financial_simulations_results.objects.get_or_create(username=username)
    hedgebot_results.objects.get_or_create(username=username)
    target_prices.objects.get_or_create(username=username)
    sugar_position_info_2.objects.get_or_create(username=username)
    user_forecasts_assumptions_results.objects.get_or_create(username=username)
    user_forecasts_assumptions_results.objects.get_or_create(username=username, season = '22_23')

@api_view(['GET'])
def fin_sim_meta_data_api(request):
    
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
        data = sugar_position_info.objects.all()
    
        serializer = SugarPositionSerializers(data, context={'request': request}, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def historical_mc_data_api(request):

    hist_mc_data_df = pd.DataFrame(monte_carlo_market_data.objects.all().values())
    hist_mc_data_df.columns = ['Id','start_date', 'target_date', 'end_date', 'factor_label', 'mean_returned', 'std_returned']
    hist_mc_data_df['season'] = '23_24'
    season_bool = '23_24'
    temp_date = date.today() + relativedelta(months=-6)
    hist_mc_data_df = hist_mc_data_df.loc[(hist_mc_data_df['season'] == season_bool) & (pd.to_datetime(hist_mc_data_df['start_date']) >= pd.to_datetime(temp_date))]
    return hist_mc_data_df

@api_view(['GET'])
def current_mc_data_api(request):

    if request.method == "GET":
        relevant_factors = ['sugar_1', 'hydrous', 'anhydrous', 'usdbrl']
        max_date = monte_carlo_market_data.objects.latest('simulation_date').simulation_date    
        data = monte_carlo_market_data.objects.filter(reference__in = relevant_factors).filter(simulation_date = max_date)
        serializer = MonteCarloDataSerializer(data, context={'request':request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def market_price_data_api(request):

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

@api_view(['GET', 'PUT', 'POST'])
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

current_financial_sim('ct_beast')