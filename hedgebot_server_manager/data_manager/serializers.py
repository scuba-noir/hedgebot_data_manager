from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import sugar_position_info, monte_carlo_market_data, market_data, financial_simulation_meta_data_historical, sugar_position_info_2, user_list
from .models import current_mc_data, market_data, current_financial_simulations, hedgebot_results, risk_management_user_input_table, market_forecasts
from django.db import models

class MarketForecastSerializer(serializers.ModelSerializer):

    class Meta:
        model = market_forecasts
        fields = ('published_date','description','forecast_date','value')

class SugarPositionSerializers(serializers.ModelSerializer):

    class Meta:
        model = sugar_position_info
        fields = ('season','date','total_production','mar1_total','may_total','jul_total','oct_total','mar2_total','total_hedged',
        'mar1_hedged','may_hedged','jul_hedged','oct_hedged','mar2_hedged',
        'total_unhedged','mar1_unhedged','may_unhedged','jul_unhedged','oct_unhedged','mar2_unhedged','username')

class SugarPosition2Serializers(serializers.ModelSerializer):

    class Meta:
        model = sugar_position_info_2
        fields = (
            'id',
            'date',
            'mar1_fxpassive_obligation',
            'mar1_fxpassive_fixed',
            'mar1_fxpassive_avg_price_cts',
            'mar1_fxpassive_avg_price_brl',
            'may_fxpassive_obligation',
            'may_fxpassive_fixed',
            'may_fxpassive_avg_price_cts',
            'may_fxpassive_avg_price_brl',
            'jul_fxpassive_obligation',
            'jul_fxpassive_fixed',
            'jul_fxpassive_avg_price_cts',
            'jul_fxpassive_avg_price_brl',
            'oct_fxpassive_obligation',
            'oct_fxpassive_fixed',
            'oct_fxpassive_avg_price_cts',
            'oct_fxpassive_avg_price_brl',
            'mar2_fxpassive_obligation',
            'mar2_fxpassive_fixed',
            'mar2_fxpassive_avg_price_cts',
            'mar2_fxpassive_avg_price_brl',
            'mar1_brlfixed_obligation',
            'mar1_brlfixed_fixed',
            'mar1_brlfixed_avg_price_cts',
            'mar1_brlfixed_avg_price_brl',
            'may_brlfixed_obligation',
            'may_brlfixed_fixed',
            'may_brlfixed_avg_price_cts',
            'may_brlfixed_avg_price_brl',
            'jul_brlfixed_obligation',
            'jul_brlfixed_fixed',
            'jul_brlfixed_avg_price_cts',
            'jul_brlfixed_avg_price_brl',
            'oct_brlfixed_obligation',
            'oct_brlfixed_fixed',
            'oct_brlfixed_avg_price_cts',
            'oct_brlfixed_avg_price_brl',
            'mar2_brlfixed_obligation',
            'mar2_brlfixed_fixed',
            'mar2_brlfixed_avg_price_cts',
            'mar2_brlfixed_avg_price_brl',
        )

class MonteCarloDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = monte_carlo_market_data
        fields = ('simulation_date','forecast_period','end_date','reference','mean_returned', 'std_returned')

class FinSimMetaDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = financial_simulation_meta_data_historical
        fields = ('simulation_date','account','datagroup','mean_returned','std_returned','season','username')

class UserListSerializers(serializers.ModelSerializer):

    class Meta:
        model = user_list
        fields = ('username', 'create_date')

class MarketDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = market_data
        fields = ('ticker','date','value','units')

class CurrentFinSimSerializer(serializers.ModelSerializer):

    class Meta:
        model = current_financial_simulations
        fields ='__all__'

class HistMCDataSerializer(serializers.Serializer):

    class Meta:
        model = monte_carlo_market_data
        fields = ('simulation_date','forecast_period','end_date','reference','mean_returned', 'std_returned')

class HedgebotBestSerializer(serializers.ModelSerializer):

    class Meta:
        model = hedgebot_results
        fields = '__all__'

class RiskManagementUserInputTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = risk_management_user_input_table
        fields = '__all__'

class ProbabilityRangeScoresSerializer(serializers.Serializer):

    probability = models.FloatField(default = 0)