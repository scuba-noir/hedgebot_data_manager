"""hedgebot_server_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.urls import re_path
from data_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/sugar_position/$', views.sugar_position_api),
    re_path(r'^api/hist_mc_data/$', views.historical_mc_data_api),
    re_path(r'^api/fin_sim_meta/$', views.fin_sim_meta_data_api),
    re_path(r'^api/current_mc_data/$', views.current_mc_data_api),
    re_path(r'^api/market_data/$', views.market_data_api),
    re_path(r'^api/user_list/$', views.userlist_api),
    re_path(r'^api/hedgebot_bp/$', views.hedgebot_best_path_api),
    re_path(r'^api/risk_var_table_api/$', views.risk_var_table_api),    
    re_path(r'^api/risk_management_table_api/$', views.risk_management_table_api), 
    re_path(r'^api/return_current_season_df_api/$', views.return_current_season_df_api),
    re_path(r'^api/probabily_range_api/$', views.range_probabilities_api),     
    re_path(r'^api/update_user_forecast_assumptions/$', views.update_user_forecast_assumptions),     
    re_path(r'^api/financial_account_probability_range/$', views.financial_account_range_probabilities),         
    ]
