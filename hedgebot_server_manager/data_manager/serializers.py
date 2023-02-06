from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from models import fields
from .models import sugar_position_info, monte_carlo_market_data, market_data, financial_simulation_meta_data_historical, risk_var_table, sugar_position_info_2
from .models import current_mc_data

class SugarPositionSerializers(serializers.ModelSerializer):

    class Meta:
        model = sugar_position_info
        fields = ('season','date','total_production','mar1_total','may_total','jul_total','oct_total','mar2_total','total_hedged',
        'mar1_hedged','may_hedged','jul_hedged','oct_hedged','mar2_hedged',
        'total_unhedged','mar1_unhedged','may_unhedged','jul_unhedged','oct_unhedged','mar2_unhedged','username')

class SugarPosition2Serializers(serializers.ModelSerializer):

    class Meta:
        model = sugar_position_info_2
        field = (
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
            'mar2_brlfixed_obligation',
            'mar2_brlfixed_fixed',
            'mar2_brlfixed_avg_price_cts',
            'mar2_brlfixed_avg_price_brl',
        )

class MonteCarloDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = monte_carlo_market_data
        fields = ('simulation_date','forecast_period','end_date','reference','mean_returned', 'std_returned')

class MarketDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = market_data
        fields = ('ticker','date','value','units')

class FinSimMetaDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = financial_simulation_meta_data_historical
        fields = ('simulation_date','account','datagroup','mean_returned','std_returned','season','username')

class RiskVarTableSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    class Meta:
        model = risk_var_table
        fields = ('label','prev_season','actual_estimate','low_10','high_90','prob_estimate')    
