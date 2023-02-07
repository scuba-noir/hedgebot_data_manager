from django.contrib import admin
from .models import forecast_assumptions_user_fin_sim, sugar_trade_book, simulation_drivers, user_forecasts_assumptions_results, hedgebot_results, sugar_position_info
from .models import financial_simulation_meta_data_historical, monte_carlo_market_data, market_data, sugar_position_info_2

# Register your models here.
admin.site.register(forecast_assumptions_user_fin_sim)
admin.site.register(sugar_trade_book)
admin.site.register(simulation_drivers)
admin.site.register(hedgebot_results)
admin.site.register(sugar_position_info)

@admin.register(market_data)
class marketAdmin(admin.ModelAdmin):
    list_display = ('ticker','date','value','units')

@admin.register(financial_simulation_meta_data_historical)
class finSimMetaAdmin(admin.ModelAdmin):
    list_display = ('simulation_date', 'account', 'mean_returned', 'std_returned', 'username')

@admin.register(user_forecasts_assumptions_results)
class userForAssumAdmin(admin.ModelAdmin):
    list_display = [field.name for field in user_forecasts_assumptions_results._meta.get_fields()]

@admin.register(monte_carlo_market_data)
class monteCarloAdmin(admin.ModelAdmin):
    list_display = [field.name for field in monte_carlo_market_data._meta.get_fields()]

@admin.register(sugar_position_info_2)
class sugarPosition2Admin(admin.ModelAdmin):
    list_display = [field.name for field in sugar_position_info_2._meta.get_fields()]