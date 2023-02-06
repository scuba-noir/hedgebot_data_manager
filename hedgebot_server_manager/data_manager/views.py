from django.shortcuts import render
import numpy as np
import pandas as pd
import numpy as np
import numpy as np
import datetime

from scipy.stats import norm, percentileofscore
from django.db.models import F, Q, When, Max, Avg, Window, StdDev
from data_manager.models import user_forecasts_assumptions_results
from data_manager.models import hedgebot_results
from data_manager.models import sugar_position_info
from data_manager.models import financial_simulation_meta_data_historical
from data_manager.models import current_financial_simulations
from data_manager.models import monte_carlo_market_data
from data_manager.models import market_data, risk_var_table
from data_manager.models import sugar_position_info_2
from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from data_manager.serializers import SugarPositionSerializers, MonteCarloDataSerializer, MarketDataSerializer, FinSimMetaDataSerializer, RiskVarTableSerializer


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

def update_market_data_model():

    label_dict = {
        'SBMAY1 Comdty':'SBMAY1 Comdty',
        'SBJUL1 Comdty':'SBJUL1 Comdty',
        'SBOCT1 Comdty':'SBOCT1 Comdty',
        'SBMAR2 Comdty':'SBMAR2 Comdty',
        'NY No.11':'SB1 Comdty',
        'Hydrous Ethanol':'BAAWHYDP Index',
        'Anhydrous Ethanol':'BAAWANAB Index',
        'Fertilizer Costs':'Fert_Costs',
        'Brent Crude':'CL1 Comdty',
        'USDBRL':'USDBRL Curncy',
        'Energy Prices':'Energy_Costs',
        'SBMAR1 Comdty':'SBMAR1 Comdty'
        }

    temp_price_data = pd.read_csv("temp_price_data.csv")
    temp_price_data['Date'] = pd.to_datetime(temp_price_data['Date'])
    for keys in label_dict.keys():
        temp_label = label_dict[keys]
        max_date_bool = False
        try:
            max_date = market_data.objects.filter(ticker = temp_label).latest('date').date
            max_date = datetime.datetime(max_date.year, max_date.month, max_date.day)
            max_date_bool = True
        except:
            print('No data for ' + str(keys))
        temp_price_data_df = temp_price_data.filter([keys, 'Date'], axis = 1)
        temp_price_data_df = temp_price_data_df.dropna()
        if max_date_bool == True:
            temp_price_data_df = temp_price_data_df.loc[temp_price_data_df['Date'] > max_date]
        for row, items in temp_price_data_df.iterrows():
            temp_val = items[keys]
            temp_date = items['Date']
            
            market_data.objects.get_or_create(ticker = label_dict[keys], date = temp_date, value = temp_val, units = 'temp_fill')
            
    return 0 

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
def market_data_api(request):

    if request.method == "GET":
        data = market_data.objects.all()

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
        #Final Temp DF is dataframe of all simulations
        #Current mc data df is dataframe of most recent MC sim meta variables

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
        
        """
        #current_mc_data_df['end_date'] = '2024-03-31'
        current_mc_data_df.index = pd.to_datetime(current_mc_data_df['target_date'])
        final_temp_df = []
        counter = 0
        for reference in relevant_factors:
            temp_df = current_mc_data_df.loc[current_mc_data_df['factor_label'] == reference]
            temp_rows = []
            for items, rows in temp_df.iterrows():
                temp_rows = [reference]
                temp_rows.append(rows['target_date'])
                temp_mu = rows['pct_change']
                temp_std = rows['std_returned']
                temp_drift = temp_mu - (0.5 * temp_std**2)
                
                temp_row_final = np.exp(temp_drift + temp_std * norm.ppf(np.random.rand(1, 1000)))
                temp_rows.extend(temp_row_final[0])
                if counter == 0:
                    final_temp_df = pd.DataFrame([temp_rows])
                    counter += 1
                else:
                    final_temp_df = pd.concat([final_temp_df, pd.DataFrame([temp_rows])], ignore_index=True)
        
        serializer = SugarPositionSerializers(data, context={'request': request}, many=True)

        return Response(serializer.data)
        """

@api_view
def 

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


