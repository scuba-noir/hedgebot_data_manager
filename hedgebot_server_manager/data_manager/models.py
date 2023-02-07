from django.db import models
import django.utils.timezone

class financial_simulation_output(models.Model):
    #add season
    id = models.BigAutoField(primary_key=True)
    account = models.CharField(max_length=50)
    data_group = models.CharField(max_length=50, default='Not Listed')
    value = models.FloatField(default=0)

    def __str__(self):
        return self.id

    def return_all(self):
        return {
            'account':self.account,
            'data_group':self.data_group,
            'value':self.value
        }

class waterfall_data(models.Model):

    id = models.BigAutoField(primary_key=True)
    account = models.CharField(max_length=50)
    data_group = models.CharField(max_length=50, default='Not Listed')
    value = models.CharField(default='-', max_length=50)

    def __str__(self):
        return self.account

    def return_all(self):
        return {
            'account':self.account,
            'data_group':self.data_group,
            'value':self.value
        }

    def return_values(self):
        return self.value

class forecast_assumptions_user_fin_sim(models.Model):

    id = models.AutoField(primary_key=True)
    factor_label = models.CharField(max_length=50)
    season = models.CharField(max_length=50)
    entry_date = models.DateField(default=django.utils.timezone.now)
    value = models.FloatField()

    def __str__(self):
        return self.id

class sugar_trade_book(models.Model):

    id = models.AutoField(primary_key=True)
    factor_label = models.CharField(max_length=50)
    season = models.CharField(max_length=50)
    entry_date = models.DateField(default=django.utils.timezone.now)
    value = models.FloatField()

    def __str__(self):
        return self.id

class simulation_drivers(models.Model):

    id = models.AutoField(primary_key=True)
    date = models.DateField(default = django.utils.timezone.now)
    sugar_price =  models.DecimalField(max_digits=4, decimal_places=2)
    hydrous_price = models.DecimalField(max_digits=5, decimal_places=0)
    anhydrous_price = models.DecimalField(max_digits=5, decimal_places=0)
    energy_price = models.DecimalField(max_digits=5, decimal_places=0)
    fx_rate = models.DecimalField(max_digits=5, decimal_places=2)
    selic_rate = models.DecimalField(max_digits=5, decimal_places=2)
    foreign_debt_rate = models.DecimalField(max_digits=5, decimal_places=2)
    inflation_rate = models.DecimalField(max_digits=5, decimal_places=2)
    crude_price = models.DecimalField(max_digits=5, decimal_places=2)
    fertilizer_price = models.DecimalField(max_digits=5, decimal_places=0)

    def __str__(self):
        return self.id

    def return_all(self):
        return {
            'date':self.date,
            'user_account':self.user_account,
            'sugar_price':self.sugar_price,
            'hydrous_price':self.hydrous_price,
            'anhydrous_price':self.anhydrous_price,
            'energy_price':self.energy_price,
            'fx_rate':self.fx_rate,
            'selic_rate':self.selic_rate,
            'foreign_debt_rate':self.foreign_debt_rate,
            'inflation_rate':self.inflation_rate,
            'crude_price':self.crude_price,
            'fertilizer_price':self.fertilizer_price
        }

class user_forecasts_assumptions_results(models.Model):

    desc_names = ['Own area-Own Cane Assumptions-ha', 
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
            'DSCR-Financial KPI Forecasts-%']

    id = models.BigAutoField(primary_key=True)
    date = models.DateField(default = django.utils.timezone.now)
    season = models.CharField(max_length=10, verbose_name='Season', editable=True, default = '23_24')
    i = 0
    own_area = models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    leased_area= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    yield_mt= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    own_cane= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    lease_cost= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    avg_trs= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    lease_cost_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    planting_area= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    third_party_cane= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    avg_trs_cane_contract= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    third_party_cane_cost= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    avg_trs_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    sugar_mix= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    hydrous_mix= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    anhydrous_mix= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    trs_sugar= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    atr_hydrous= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    atr_anhydrous= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    energy_production= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    sugar_price= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    hydrous_price= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    anhydrous_price= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    energy_price= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    fx_rate= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    trs_price= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    dom_ir= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    foreign_ir= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    inflation= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    crude_oil= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    fertilizers= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    initial_cash= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    acc_rec= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    inventories= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    orther_current_assets= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    other_non_current_assets= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    st_acc_pay= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    other_current_liabilities= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    other_non_current_liabilities= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    issued_capital= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    income_tax_rate= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    sales_expense= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    admin_expense= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    other_sga= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    avg_cost_usd_debt_libor= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    avg_cost_usd_debt_cdi= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    usd_debt_st_usd= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    usd_debt_lt_usd= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    usd_debt_total_usd= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    usd_debt_lt_brl= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    usd_debt_st_brl= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    usd_debt_total_brl= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    brl_debt_st= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    brl_debt_lt= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_debt_st= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_debt_lt= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_debt= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    fin_expenses_usd_debt= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    fin_expenses_brl_debt= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_financial_expenses= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    inputs= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    fuel= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    freights= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    labor_cost= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    industrial_cost= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    depreciation_prod_cost = models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    planting_cost= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    cane_crushed= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    sugar_production= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    hydrous_production= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    anhydrous_production= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    energy_production_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    sugar_revenues_usd= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    sugar_revenues_brl= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    hydrous_revenues= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    anhydrous_revenues= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    energy_revenues= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_revenues= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    lease_cost_3= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    third_party_cane_cost_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    inputs_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    fuel_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    freights_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    labor_cost_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    industrial_cost_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    depreciation_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    planting_cost_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_cogs= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    gross_profit= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    sales_expenses= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    administrative_expenses= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    other_sga_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_sga= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    ebit= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    financial_expenses= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    profit_before_taxes= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    income_tax= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    net_income= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    depreciation= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    working_capital_variation= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    cash_flow_from_operations= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    capex= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    write_offs= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    cash_flow_from_investment_activities= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    debt_amortization= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    new_debt= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    cash_financing= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    change_in_cash= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    initial_cash_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    ending_cash= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    minimum_refinancing= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    cash= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    accounts_receivable= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    inventories_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    other_current_assets= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_current_assets= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    ppe= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    other_non_current_assets_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_non_current_assets= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_assets= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    short_term_accounts_payable= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    short_term_debt= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    other_current_liabilities_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_current_liabilities= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    long_term_debt= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    other_non_current_liabilities_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_non_current_liabilities= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_liabilities= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    issued_capital_2= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    retained_earnings= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    total_equity= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    liabilities_plus_equity= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    gross_margin= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    ebitda= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    ebitda_margin= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    net_income_margin= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    net_debt= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    net_debt_ebitda= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    net_debt_mt_of_cane= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    indebtedness= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    short_term= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    current_ratio= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    revenue_variation= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    income_variation= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    dscr= models.FloatField(default=0, verbose_name=desc_names[i]); i += 1 
    username = models.CharField(max_length=30, verbose_name='Username')
    
    def return_values(self, id_child):

        temp_self = user_forecasts_assumptions_results.objects.filter(id = int(id_child)).first()
        field_names = temp_self._meta.get_fields()
        data_ls = {}
        date_boolean = False
        for field in field_names:
            temp_ls = {}          
            data_ls[field.attname] = (getattr(temp_self, field.attname))
        return data_ls

    def return_field_value(self, field_name):
        return getattr(self, field_name)

    def set_field_value(self, field_name, field_value):
        self.__setattr__(field_name, field_value)

    def __str__(self):
        return str(self.id)

    def return_instance(self, child_id):
        temp_self = user_forecasts_assumptions_results.objects.filter(id = int(child_id).first())
        return temp_self

    def return_verbose(self):

        temp_self = user_forecasts_assumptions_results.objects.last()
        field_names = temp_self._meta.get_fields()
        data_ls = {}
        date_boolean = False
        for field in field_names:
            temp_ls = {}          
            data_ls[field.name] = field.verbose_name
        return data_ls

class sugar_position_info(models.Model):

    id = models.BigAutoField(primary_key=True)
    season = models.CharField(max_length=10, verbose_name='Season', choices=[('2021_22','2021_22'),('2022_23','2022_23'), ('2023_24','2023_24')], default='2023_24')
    date = models.DateField(default = django.utils.timezone.now)
    total_production = models.FloatField(default=0, verbose_name='Total Sugar Production (mt)')
    mar1_total = models.FloatField(default=0, verbose_name='Sugar for first Mar Contract (mt)')
    may_total = models.FloatField(default=0, verbose_name='Sugar for May Contract (mt)')
    jul_total = models.FloatField(default=0, verbose_name='Sugar for Jul Contract (mt)')
    oct_total = models.FloatField(default=0, verbose_name='Sugar for Oct Contract (mt)')
    mar2_total = models.FloatField(default=0, verbose_name='Sugar for second Mar Contract (mt)')
    total_hedged = models.FloatField(default=0, verbose_name='Total Sugar Production Hedged (mt)')
    mar1_hedged = models.FloatField(default=0, verbose_name='Hedged Sugar for first Mar Contract (mt)')
    may_hedged = models.FloatField(default=0, verbose_name='Hedged Sugar for May Contract (mt)')
    jul_hedged= models.FloatField(default=0, verbose_name='Hedged Sugar for Jul Contract (mt)')
    oct_hedged = models.FloatField(default=0, verbose_name='Hedged Sugar for Oct Contract (mt)')
    mar2_hedged = models.FloatField(default=0, verbose_name='Hedged Sugar for second Mar Contract (mt)')
    total_unhedged = models.FloatField(default=0, verbose_name='Total Sugar Production Hedged (mt)')
    mar1_unhedged = models.FloatField(default=0, verbose_name='Hedged Sugar for first Mar Contract (mt)')
    may_unhedged = models.FloatField(default=0, verbose_name='Hedged Sugar for May Contract (mt)')
    jul_unhedged= models.FloatField(default=0, verbose_name='Hedged Sugar for Jul Contract (mt)')
    oct_unhedged = models.FloatField(default=0, verbose_name='Hedged Sugar for Oct Contract (mt)')
    mar2_unhedged = models.FloatField(default=0, verbose_name='Hedged Sugar for second Mar Contract (mt)')
    username = models.CharField(max_length=30, verbose_name='Username', default="Default User")

    def return_values(self):
        
        field_names = self._meta.get_fields()
        data_ls = {}
        date_boolean = False
        for field in field_names:
            temp_ls = {}          
            data_ls[field.attname] = (getattr(self, field.attname))
        return data_ls
    
    def return_field_value(self, field_name):
        return getattr(self, field_name)

class sugar_position_info_2(models.Model):

    id = models.BigAutoField(primary_key=True)
    season = models.CharField(max_length=10, verbose_name='Season', default='23_24')
    date = models.DateField(default = django.utils.timezone.now)
    mar1_fxpassive_obligation = models.FloatField(default=0)
    mar1_fxpassive_fixed = models.FloatField(default=0)
    mar1_fxpassive_avg_price_cts = models.FloatField(default=0)
    mar1_fxpassive_avg_price_brl = models.FloatField(default=0)
    may_fxpassive_obligation = models.FloatField(default=0)
    may_fxpassive_fixed = models.FloatField(default=0)
    may_fxpassive_avg_price_cts = models.FloatField(default=0)
    may_fxpassive_avg_price_brl = models.FloatField(default=0)
    jul_fxpassive_obligation = models.FloatField(default=0)
    jul_fxpassive_fixed = models.FloatField(default=0)
    jul_fxpassive_avg_price_cts = models.FloatField(default=0)
    jul_fxpassive_avg_price_brl = models.FloatField(default=0)
    oct_fxpassive_obligation = models.FloatField(default=0)
    oct_fxpassive_fixed = models.FloatField(default=0)
    oct_fxpassive_avg_price_cts = models.FloatField(default=0)
    oct_fxpassive_avg_price_brl = models.FloatField(default=0)
    mar2_fxpassive_obligation = models.FloatField(default=0)
    mar2_fxpassive_fixed = models.FloatField(default=0)
    mar2_fxpassive_avg_price_cts = models.FloatField(default=0)
    mar2_fxpassive_avg_price_brl = models.FloatField(default=0)
    mar1_brlfixed_obligation = models.FloatField(default=0)
    mar1_brlfixed_fixed = models.FloatField(default=0)
    mar1_brlfixed_avg_price_cts = models.FloatField(default=0)
    mar1_brlfixed_avg_price_brl = models.FloatField(default=0)
    may_brlfixed_obligation = models.FloatField(default=0)
    may_brlfixed_fixed = models.FloatField(default=0)
    may_brlfixed_avg_price_cts = models.FloatField(default=0)
    may_brlfixed_avg_price_brl = models.FloatField(default=0)
    jul_brlfixed_obligation = models.FloatField(default=0)
    jul_brlfixed_fixed = models.FloatField(default=0)
    jul_brlfixed_avg_price_cts = models.FloatField(default=0)
    jul_brlfixed_avg_price_brl = models.FloatField(default=0)
    oct_brlfixed_obligation = models.FloatField(default=0)
    oct_brlfixed_fixed = models.FloatField(default=0)
    oct_brlfixed_avg_price_cts = models.FloatField(default=0)
    oct_brlfixed_avg_price_brl = models.FloatField(default=0)
    mar2_brlfixed_obligation = models.FloatField(default=0)
    mar2_brlfixed_fixed = models.FloatField(default=0)
    mar2_brlfixed_avg_price_cts = models.FloatField(default=0)
    mar2_brlfixed_avg_price_brl = models.FloatField(default=0)
    username = models.CharField(max_length=30, verbose_name='Username')

    def return_values(self, id_child):
        temp_self = sugar_position_info_2.objects.filter(id = int(id_child)).first()
        field_names = temp_self._meta.get_fields()
        data_ls = {}
        date_boolean = False
        for field in field_names:
            temp_ls = {}          
            data_ls[field.attname] = (getattr(temp_self, field.attname))
        return data_ls

    def __str__(self):
        return str(self.id)

    def return_field_value(self, field_name):
        return getattr(self, field_name)
    
    def set_field_value(self, field_name, field_value):
        self.__setattr__(field_name, field_value)

    def return_instance(self, child_id):
        temp_self = sugar_position_info_2.objects.filter(id = int(child_id).first())
        return temp_self

class hedgebot_results(models.Model):

    longnames = [
        'ID',
        'Date',
        'Forecast Period',
        'Season',
        'Weighted Average Price',
        'Fixed Revenues',
        'Unhedged Volumes Mar 1',
        'Unhedged Volumes May',
        'Unhedged Volumes Jul',
        'Unhedged Volumes Oct',
        'Unhedged Volumes Mar',
        'Hedge_Boolean_1',
        'Hedge_Boolean_2',
        'Hedge_Boolean_3',
        'Hedge_Boolean_4',
        'Hedge_Boolean_5',
        'ST_1',
        'ST_2',
        'ST_3',
        'ST_4',
        'ST_5',
        'Target Price 1',
        'Target Price 2',
        'Target Price 3',
        'Target Price 4',
        'Target Price 5',
        'Current Price Mar',
        'Current Price May',
        'Current Price Jul',
        'Current Price Oct',
        'Current Price Mar 2',
        'Attribute A',
        'Attribute B',
        'Attribute C',
        'Attribute D',
        'MT_1',
        'MT_2',
        'MT_3',
        'MT_4',
        'MT_5',
        'Hedged_Revenues_1',
        'Hedged_Revenues_2',
        'Hedged_Revenues_3',
        'Hedged_Revenues_4',
        'Hedged_Revenues_5',
        'Hedged_Volumes_1',
        'Hedged_Volumes_2',
        'Hedged_Volumes_3',
        'Hedged_Volumes_4',
        'Hedged_Volumes_5',
        'Avg_Market_Price_1',
        'Avg_Market_Price_2',
        'Avg_Market_Price_3',
        'Avg_Market_Price_4',
        'Avg_Market_Price_5',
        'Identity'
    ]

    id = models.AutoField(primary_key=True, verbose_name=longnames[0])
    date = models.DateField(default = django.utils.timezone.now, verbose_name=longnames[1])
    forecast_period = models.DateField(default=django.utils.timezone.now, verbose_name=longnames[2])
    season = models.CharField(max_length=50, verbose_name=longnames[3], default='23_24')
    weighted_average_price = models.FloatField(default = 0, verbose_name=longnames[4])
    fixed_revenues = models.IntegerField(default = 0, verbose_name=longnames[5])
    unhedged_volumes_march_1 = models.IntegerField(default = 0, verbose_name=longnames[6])
    unhedged_volumes_may = models.IntegerField(default = 0, verbose_name=longnames[7])
    unhedged_volumes_july = models.IntegerField(default = 0, verbose_name=longnames[8])
    unhedged_volumes_october = models.IntegerField(default = 0, verbose_name=longnames[9])
    unhedged_volumes_march_2 = models.IntegerField(default = 0, verbose_name=longnames[10])
    hedge_booleans_march_1 = models.IntegerField(default = 0, verbose_name=longnames[11])
    hedge_booleans_may = models.IntegerField(default = 0, verbose_name=longnames[12])
    hedge_booleans_july = models.IntegerField(default = 0, verbose_name=longnames[13])
    hedge_booleans_october = models.IntegerField(default = 0, verbose_name=longnames[14])
    hedge_booleans_march_2 = models.IntegerField(default = 0, verbose_name=longnames[15])
    short_term_indicators_march_1 = models.FloatField(default = 0, verbose_name=longnames[16])
    short_term_indicators_may = models.FloatField(default = 0, verbose_name=longnames[17])
    short_term_indicators_july = models.FloatField(default = 0, verbose_name=longnames[18])
    short_term_indicators_october = models.FloatField(default = 0, verbose_name=longnames[19])
    short_term_indicators_march_2 = models.FloatField(default = 0, verbose_name=longnames[20])
    target_prices_march_1 = models.FloatField(default = 0, verbose_name=longnames[21])
    target_prices_may = models.FloatField(default = 0, verbose_name=longnames[22])
    target_prices_july = models.FloatField(default = 0, verbose_name=longnames[23])
    target_prices_october = models.FloatField(default = 0, verbose_name=longnames[24])
    target_prices_march_2 = models.FloatField(default = 0, verbose_name=longnames[25])
    current_prices_march_1 = models.FloatField(default = 0, verbose_name=longnames[26])
    current_prices_may = models.FloatField(default = 0, verbose_name=longnames[27])
    current_prices_july = models.FloatField(default = 0, verbose_name=longnames[28])
    current_prices_october = models.FloatField(default = 0, verbose_name=longnames[29])
    current_prices_march_2 = models.FloatField(default = 0, verbose_name=longnames[30])
    attributes_a = models.IntegerField(default = 0, verbose_name=longnames[31])
    attributes_b = models.IntegerField(default = 0, verbose_name=longnames[32])
    attributes_c = models.IntegerField(default = 0, verbose_name=longnames[33])
    attributes_d = models.IntegerField(default = 0, verbose_name=longnames[34])
    mid_term_indicators_march_1 = models.FloatField(default = 0, verbose_name=longnames[35])
    mid_term_indicators_may = models.FloatField(default = 0, verbose_name=longnames[36])
    mid_term_indicators_july = models.FloatField(default = 0, verbose_name=longnames[37])
    mid_term_indicators_october = models.FloatField(default = 0, verbose_name=longnames[38])
    mid_term_indicators_march_2 = models.FloatField(default = 0, verbose_name=longnames[39])
    hedged_revenues_march_1 = models.IntegerField(default = 0, verbose_name=longnames[40])
    hedged_revenues_may = models.IntegerField(default = 0, verbose_name=longnames[41])
    hedged_revenues_july = models.IntegerField(default = 0, verbose_name=longnames[42])
    hedged_revenues_october = models.IntegerField(default = 0, verbose_name=longnames[43])
    hedged_revenues_march_2 = models.IntegerField(default = 0, verbose_name=longnames[44])
    hedged_volumes_march_1 = models.IntegerField(default = 0, verbose_name=longnames[45])
    hedged_volumes_may = models.IntegerField(default = 0, verbose_name=longnames[46])
    hedged_volumes_july = models.IntegerField(default = 0, verbose_name=longnames[47])
    hedged_volumes_october = models.IntegerField(default = 0, verbose_name=longnames[48])
    hedged_volumes_march_2 = models.IntegerField(default = 0, verbose_name=longnames[49])
    average_market_price_march_1 = models.FloatField(default = 0, verbose_name=longnames[50])
    average_market_price_may = models.FloatField(default = 0, verbose_name=longnames[51])
    average_market_price_july = models.FloatField(default = 0, verbose_name=longnames[52])
    average_market_price_october = models.FloatField(default = 0, verbose_name=longnames[53])
    average_market_price_march_2 = models.FloatField(default = 0, verbose_name=longnames[54])
    mill_identification_number = models.FloatField(default = 0, verbose_name=longnames[55])
    username = models.CharField(max_length=30, verbose_name='Username', default="Default User")
    
    def return_column_labels(self='missing'):

        return([
                    'ID',
                    'Date',
                    'Forecast Period',
                    'Season',
                    'Weighted Average Price',
                    'Fixed Revenues',
                    'Unhedged Volumes Mar 1',
                    'Unhedged Volumes May',
                    'Unhedged Volumes Jul',
                    'Unhedged Volumes Oct',
                    'Unhedged Volumes Mar 2',
                    'Hedge_Boolean_1',
                    'Hedge_Boolean_2',
                    'Hedge_Boolean_3',
                    'Hedge_Boolean_4',
                    'Hedge_Boolean_5',
                    'ST_1',
                    'ST_2',
                    'ST_3',
                    'ST_4',
                    'ST_5',
                    'Target Price',
                    'Target Price',
                    'Target Price',
                    'Target Price',
                    'Target Price',
                    'Current Price Mar',
                    'Current Price May',
                    'Current Price Jul',
                    'Current Price Oct',
                    'Current Price Mar 2',
                    'Attribute A',
                    'Attribute B',
                    'Attribute C',
                    'Attribute D',
                    'MT_1',
                    'MT_2',
                    'MT_3',
                    'MT_4',
                    'MT_5',
                    'Hedged_Revenues_1',
                    'Hedged_Revenues_2',
                    'Hedged_Revenues_3',
                    'Hedged_Revenues_4',
                    'Hedged_Revenues_5',
                    'Hedged_Volumes_1',
                    'Hedged_Volumes_2',
                    'Hedged_Volumes_3',
                    'Hedged_Volumes_4',
                    'Hedged_Volumes_5',
                    'Avg_Market_Price_1',
                    'Avg_Market_Price_2',
                    'Avg_Market_Price_3',
                    'Avg_Market_Price_4',
                    'Avg_Market_Price_5',
                    'Identity'
                ])

    def return_values(self):
        
        field_names = self._meta.get_fields()
        data_ls = {}
        date_boolean = False
        for field in field_names:
            temp_ls = {}          
            data_ls[field.attname] = (getattr(self, field.attname))
        return data_ls

class currentForecasts(models.Model):

    id = models.AutoField(primary_key=True)
    factor_label = models.CharField(max_length=50)
    entry_date = models.DateField(default=django.utils.timezone.now)
    forecast_date = models.CharField(max_length=50)
    value = models.FloatField()

    def __str__(self):
        return self.id 

class financial_simulation_meta_data_historical(models.Model):

    id = models.BigAutoField(primary_key=True)
    simulation_date = models.DateField(default=django.utils.timezone.now)
    account = models.CharField(max_length=50)
    datagroup = models.CharField(max_length=50, default = "")
    mean_returned = models.FloatField(default = 0)
    std_returned = models.FloatField(default=0)
    season = models.CharField(max_length=10, default='23_24')
    username = models.CharField(max_length=30, verbose_name='Username', default="Default User")

    def __str__(self):
        return self.id

class financial_simulations_results(models.Model):

    id = models.BigAutoField(primary_key=True)
    sugar_price = models.FloatField(default=0, verbose_name='Sugar')
    hydrous_price = models.FloatField(default=0, verbose_name='Hydrous')
    anhydrous_price = models.FloatField(default=0, verbose_name ='Anhydrous')
    energy_price = models.FloatField(default=0, verbose_name='Energy')
    fx_rate = models.FloatField(default=0, verbose_name='Exchange rate')
    selic_rate = models.FloatField(default=0, verbose_name = 'Domestic interest rate')
    foreign_debt_rate = models.FloatField(default=0, verbose_name = 'Foreign interest rate')
    inflation_rate = models.FloatField(default=0, verbose_name = 'Inflation')
    crude_price = models.FloatField(default=0, verbose_name='Crude oil')
    fertilizer_price = models.FloatField(default=0, verbose_name='Fertilizers')
    sugar_revenues = models.FloatField(default=0, verbose_name='Sugar Revenues BRL')
    hydrous_revenues = models.FloatField(default=0, verbose_name='Hydrous Revenues BRL')
    anhydrous_revenues = models.FloatField(default=0, verbose_name ='Anhydrous Revenues BRL')
    energy_revenues = models.FloatField(default=0, verbose_name='Energy Revenues BRL')
    input_costs = models.FloatField(default=0, verbose_name='Input Cost BRL')
    fuel_costs = models.FloatField(default=0, verbose_name='Fuel Cost BRL')
    freight_costs = models.FloatField(default=0, verbose_name='Freight Cost BRL')
    labor_costs = models.FloatField(default=0, verbose_name='Labor Cost BRL')
    indutrial_costs = models.FloatField(default=0, verbose_name='Industrial Cost BRL')
    depreciation = models.FloatField(default=0, verbose_name='Depreciation BRL')
    planting_costs = models.FloatField(default=0, verbose_name='Planting Cost BRL')
    lease_costs = models.FloatField(default=0, verbose_name='Lease Cost BRL')
    gross_profit = models.FloatField(default=0, verbose_name='Gross Profit BRL')
    sga_costs = models.FloatField(default=0, verbose_name='Total SG&A BRL')
    ebit = models.FloatField(default=0, verbose_name='EBIT')
    financial_costs = models.FloatField(default=0, verbose_name='Financial Expenses BRL')
    ebt = models.FloatField(default=0, verbose_name='Profit Before Tax BRL')
    tax = models.FloatField(default=0, verbose_name='Income Tax BRL')
    net_income = models.FloatField(default=0, verbose_name='Net Income BRL')
    gross_margin = models.FloatField(default=0, verbose_name='Gross Margin')
    ebitda_margin = models.FloatField(default=0, verbose_name='EBITDA Margin')
    net_margin = models.FloatField(default=0, verbose_name='Net Margin')
    net_debt_to_ebitda = models.FloatField(default=0, verbose_name='Net Debt / EBITDA')
    net_debt_to_mt_cane = models.FloatField(default=0, verbose_name='Net Debt / MT of Cane')
    indebtness = models.FloatField(default=0, verbose_name='Indebtness')
    short_term_debt = models.FloatField(default=0, verbose_name='Short Term Debt Percent')
    current_ratio = models.FloatField(default=0, verbose_name='Current Ratio')
    season = models.CharField(max_length=10, default='23_24')
    username = models.CharField(max_length=30, verbose_name='Username')

class hedgebot_results_meta_data(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    simulation_date = models.DateField(default=django.utils.timezone.now)
    account = models.CharField(max_length=50)
    mean_returned = models.FloatField(default = 0)
    std_returned = models.FloatField(default=0)
    username = models.CharField(max_length=30, verbose_name='Username', default="Default User")

class monte_carlo_market_data(models.Model):

    id = models.BigAutoField(primary_key=True)
    simulation_date = models.DateField(default=django.utils.timezone.now)
    forecast_period = models.DateField()
    end_date = models.DateField(default='2024-03-31')
    reference = models.CharField(max_length=50)
    mean_returned = models.FloatField(default = 0)
    std_returned = models.FloatField(default=0)

class market_data(models.Model):

    id = models.BigAutoField(primary_key=True)
    ticker = models.CharField(max_length=30)
    date = models.DateField()
    value = models.FloatField()
    units = models.CharField(max_length=30)

class target_prices(models.Model):

    id = models.BigAutoField(primary_key=True)
    season = models.CharField(max_length=30, default = '23_24')
    username = models.CharField(max_length=30, verbose_name='Username')
    date = models.DateField(default = django.utils.timezone.now)
    mar1_cts = models.FloatField(default = 0)
    mar1_brl = models.FloatField(default= 0)
    may_cts = models.FloatField(default= 0)
    may_brl  = models.FloatField(default= 0)
    jul_cts = models.FloatField(default= 0)
    jul_brl = models.FloatField(default= 0)
    oct_cts = models.FloatField(default= 0)
    oct_brl = models.FloatField(default= 0)
    mar2_cts = models.FloatField(default= 0)
    mar2_brl = models.FloatField(default= 0)

class current_mc_data(models.Model):

    id = models.BigAutoField(primary_key=True)
    start_date = models.DateField(default=django.utils.timezone.now)
    target_date = models.DateField()
    end_date = models.DateField(default='2024-03-31')
    factor_label = models.CharField(max_length=50)
    mean_returned = models.FloatField(default = 0)
    std_returned = models.FloatField(default=0)
    season = models.CharField(max_length=10)
    pct_change = models.FloatField()

class user_list(models.Model):

    username = models.CharField(max_length=20, primary_key=True, unique=True)
    create_date = models.DateField(default=django.utils.timezone.now)

class current_financial_simulations(models.Model):

    id = models.BigAutoField(primary_key=True)
    simulation_number = models.IntegerField()
    sugar_price = models.FloatField(default=0, verbose_name='Sugar')
    hydrous_price = models.FloatField(default=0, verbose_name='Hydrous')
    anhydrous_price = models.FloatField(default=0, verbose_name ='Anhydrous')
    energy_price = models.FloatField(default=0, verbose_name='Energy')
    fx_rate = models.FloatField(default=0, verbose_name='Exchange rate')
    selic_rate = models.FloatField(default=0, verbose_name = 'Domestic interest rate')
    foreign_debt_rate = models.FloatField(default=0, verbose_name = 'Foreign interest rate')
    inflation_rate = models.FloatField(default=0, verbose_name = 'Inflation')
    crude_price = models.FloatField(default=0, verbose_name='Crude oil')
    fertilizer_price = models.FloatField(default=0, verbose_name='Fertilizers')
    sugar_revenues = models.FloatField(default=0, verbose_name='Sugar Revenues BRL')
    hydrous_revenues = models.FloatField(default=0, verbose_name='Hydrous Revenues BRL')
    anhydrous_revenues = models.FloatField(default=0, verbose_name ='Anhydrous Revenues BRL')
    energy_revenues = models.FloatField(default=0, verbose_name='Energy Revenues BRL')
    input_costs = models.FloatField(default=0, verbose_name='Input Cost BRL')
    fuel_costs = models.FloatField(default=0, verbose_name='Fuel Cost BRL')
    freight_costs = models.FloatField(default=0, verbose_name='Freight Cost BRL')
    labor_costs = models.FloatField(default=0, verbose_name='Labor Cost BRL')
    indutrial_costs = models.FloatField(default=0, verbose_name='Industrial Cost BRL')
    depreciation = models.FloatField(default=0, verbose_name='Depreciation BRL')
    planting_costs = models.FloatField(default=0, verbose_name='Planting Cost BRL')
    lease_costs = models.FloatField(default=0, verbose_name='Lease Cost BRL')
    gross_profit = models.FloatField(default=0, verbose_name='Gross Profit BRL')
    sga_costs = models.FloatField(default=0, verbose_name='Total SG&A BRL')
    ebit = models.FloatField(default=0, verbose_name='EBIT')
    financial_costs = models.FloatField(default=0, verbose_name='Financial Expenses BRL')
    ebt = models.FloatField(default=0, verbose_name='Profit Before Tax BRL')
    tax = models.FloatField(default=0, verbose_name='Income Tax BRL')
    net_income = models.FloatField(default=0, verbose_name='Net Income BRL')
    gross_margin = models.FloatField(default=0, verbose_name='Gross Margin')
    ebitda_margin = models.FloatField(default=0, verbose_name='EBITDA Margin')
    net_margin = models.FloatField(default=0, verbose_name='Net Margin')
    net_debt_to_ebitda = models.FloatField(default=0, verbose_name='Net Debt / EBITDA')
    net_debt_to_mt_cane = models.FloatField(default=0, verbose_name='Net Debt / MT of Cane')
    indebtness = models.FloatField(default=0, verbose_name='Indebtness')
    short_term_debt = models.FloatField(default=0, verbose_name='Short Term Debt Percent')
    current_ratio = models.FloatField(default=0, verbose_name='Current Ratio')