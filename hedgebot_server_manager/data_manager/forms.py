import django
import django.forms as forms
from django.forms import ModelForm
from data_manager.models import sugar_trade_book, simulation_drivers, user_forecasts_assumptions_results, sugar_position_info, sugar_position_info_2
from django.core.validators import MinValueValidator, MaxValueValidator
        
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class userInputForm(ModelForm):

    class Meta:
        attribute_dict = {'class':'form-control text-right form-control-sm'}
        model = user_forecasts_assumptions_results
        fields = ['season','own_area', 'leased_area', 'yield_mt', 'own_cane', 'lease_cost', 'avg_trs', 'lease_cost_2', 'planting_area', 'third_party_cane', 'avg_trs_cane_contract', 'third_party_cane_cost', 'avg_trs_2', 'sugar_mix', 'hydrous_mix', 'anhydrous_mix', 'trs_sugar', 'atr_hydrous', 'atr_anhydrous', 'energy_production', 'sugar_price', 'hydrous_price', 'anhydrous_price', 'energy_price', 'fx_rate', 'trs_price', 'dom_ir', 'foreign_ir', 'inflation', 'crude_oil', 'fertilizers', 'initial_cash', 'acc_rec', 'inventories', 'orther_current_assets', 'other_non_current_assets', 'st_acc_pay', 'other_current_liabilities', 'other_non_current_liabilities', 'issued_capital', 'income_tax_rate', 'sales_expense', 'admin_expense', 'other_sga', 'avg_cost_usd_debt_libor', 'avg_cost_usd_debt_cdi', 'usd_debt_st_usd', 'usd_debt_lt_usd', 'usd_debt_lt_brl', 'usd_debt_st_brl',  'brl_debt_st', 'brl_debt_lt', 'fin_expenses_usd_debt', 'fin_expenses_brl_debt', 'total_financial_expenses', 'inputs', 'fuel', 'freights', 'labor_cost', 'industrial_cost', 'depreciation_prod_cost', 'planting_cost', 'cane_crushed', 'sugar_production', 'hydrous_production', 'anhydrous_production', 'energy_production_2', 'sugar_revenues_usd', 'sugar_revenues_brl', 'hydrous_revenues', 'anhydrous_revenues', 'energy_revenues', 'total_revenues', 'lease_cost_3', 'third_party_cane_cost_2', 'inputs_2', 'fuel_2', 'freights_2', 'labor_cost_2', 'industrial_cost_2', 'depreciation_2', 'planting_cost_2', 'total_cogs', 'gross_profit', 'sales_expenses', 'administrative_expenses', 'other_sga_2', 'total_sga', 'ebit', 'financial_expenses', 'profit_before_taxes', 'income_tax', 'net_income', 'depreciation', 'working_capital_variation', 'cash_flow_from_operations', 'capex', 'write_offs', 'cash_flow_from_investment_activities', 'debt_amortization', 'new_debt', 'cash_financing', 'change_in_cash', 'initial_cash_2', 'ending_cash', 'minimum_refinancing', 'cash', 'accounts_receivable', 'inventories_2', 'other_current_assets', 'total_current_assets', 'ppe', 'other_non_current_assets_2', 'total_non_current_assets', 'total_assets', 'short_term_accounts_payable', 'short_term_debt', 'other_current_liabilities_2', 'total_current_liabilities', 'long_term_debt', 'other_non_current_liabilities_2', 'total_non_current_liabilities', 'total_liabilities', 'issued_capital_2', 'retained_earnings', 'total_equity', 'liabilities_plus_equity', 'gross_margin', 'ebitda', 'ebitda_margin', 'net_income_margin', 'net_debt', 'net_debt_ebitda', 'net_debt_mt_of_cane', 'indebtedness', 'short_term', 'current_ratio', 'revenue_variation', 'income_variation', 'dscr']
        widgets = {
            'season':forms.TextInput(attrs=attribute_dict),
            'username':forms.TextInput(attrs=attribute_dict),
            'own_area':forms.NumberInput(attrs=attribute_dict),
            'leased_area':forms.NumberInput(attrs=attribute_dict),
            'yield_mt':forms.NumberInput(attrs=attribute_dict),
            'own_cane':forms.NumberInput(attrs=attribute_dict),
            'lease_cost':forms.NumberInput(attrs=attribute_dict),
            'avg_trs':forms.NumberInput(attrs=attribute_dict),
            'lease_cost_2':forms.NumberInput(attrs=attribute_dict),
            'planting_area':forms.NumberInput(attrs=attribute_dict),
            'third_party_cane':forms.NumberInput(attrs=attribute_dict),
            'avg_trs_cane_contract':forms.NumberInput(attrs=attribute_dict),
            'third_party_cane_cost':forms.NumberInput(attrs=attribute_dict),
            'avg_trs_2':forms.NumberInput(attrs=attribute_dict),
            'sugar_mix':forms.NumberInput(attrs=attribute_dict),
            'hydrous_mix':forms.NumberInput(attrs=attribute_dict),
            'anhydrous_mix':forms.NumberInput(attrs=attribute_dict),
            'trs_sugar':forms.NumberInput(attrs=attribute_dict),
            'atr_hydrous':forms.NumberInput(attrs=attribute_dict),
            'atr_anhydrous':forms.NumberInput(attrs=attribute_dict),
            'energy_production':forms.NumberInput(attrs=attribute_dict),
            'sugar_price':forms.NumberInput(attrs=attribute_dict),
            'hydrous_price':forms.NumberInput(attrs=attribute_dict),
            'anhydrous_price':forms.NumberInput(attrs=attribute_dict),
            'energy_price':forms.NumberInput(attrs=attribute_dict),
            'fx_rate':forms.NumberInput(attrs=attribute_dict),
            'trs_price':forms.NumberInput(attrs=attribute_dict),
            'dom_ir':forms.NumberInput(attrs=attribute_dict),
            'foreign_ir':forms.NumberInput(attrs=attribute_dict),
            'inflation':forms.NumberInput(attrs=attribute_dict),
            'crude_oil':forms.NumberInput(attrs=attribute_dict),
            'fertilizers':forms.NumberInput(attrs=attribute_dict),
            'initial_cash':forms.NumberInput(attrs=attribute_dict),
            'acc_rec':forms.NumberInput(attrs=attribute_dict),
            'inventories':forms.NumberInput(attrs=attribute_dict),
            'orther_current_assets':forms.NumberInput(attrs=attribute_dict),
            'other_non_current_assets':forms.NumberInput(attrs=attribute_dict),
            'st_acc_pay':forms.NumberInput(attrs=attribute_dict),
            'other_current_liabilities':forms.NumberInput(attrs=attribute_dict),
            'other_non_current_liabilities':forms.NumberInput(attrs=attribute_dict),
            'issued_capital':forms.NumberInput(attrs=attribute_dict),
            'income_tax_rate':forms.NumberInput(attrs=attribute_dict),
            'sales_expense':forms.NumberInput(attrs=attribute_dict),
            'admin_expense':forms.NumberInput(attrs=attribute_dict),
            'other_sga':forms.NumberInput(attrs=attribute_dict),
            'avg_cost_usd_debt_libor':forms.NumberInput(attrs=attribute_dict),
            'avg_cost_usd_debt_cdi':forms.NumberInput(attrs=attribute_dict),
            'usd_debt_st_usd':forms.NumberInput(attrs=attribute_dict),
            'usd_debt_lt_usd':forms.NumberInput(attrs=attribute_dict),
            'usd_debt_lt_brl':forms.NumberInput(attrs=attribute_dict),
            'usd_debt_st_brl':forms.NumberInput(attrs=attribute_dict),
            'brl_debt_st':forms.NumberInput(attrs=attribute_dict),
            'brl_debt_lt':forms.NumberInput(attrs=attribute_dict),
            'fin_expenses_usd_debt':forms.NumberInput(attrs=attribute_dict),
            'fin_expenses_brl_debt':forms.NumberInput(attrs=attribute_dict),
            'total_financial_expenses':forms.NumberInput(attrs=attribute_dict),
            'inputs':forms.NumberInput(attrs=attribute_dict),
            'fuel':forms.NumberInput(attrs=attribute_dict),
            'freights':forms.NumberInput(attrs=attribute_dict),
            'labor_cost':forms.NumberInput(attrs=attribute_dict),
            'industrial_cost':forms.NumberInput(attrs=attribute_dict),
            'planting_cost':forms.NumberInput(attrs=attribute_dict),
            'depreciation_prod_cost':forms.NumberInput(attrs=attribute_dict),
            'cane_crushed':forms.NumberInput(attrs=attribute_dict),
            'sugar_production':forms.NumberInput(attrs=attribute_dict),
            'hydrous_production':forms.NumberInput(attrs=attribute_dict),
            'anhydrous_production':forms.NumberInput(attrs=attribute_dict),
            'energy_production_2':forms.NumberInput(attrs=attribute_dict),
            'sugar_revenues_usd':forms.NumberInput(attrs=attribute_dict),
            'sugar_revenues_brl':forms.NumberInput(attrs=attribute_dict),
            'hydrous_revenues':forms.NumberInput(attrs=attribute_dict),
            'anhydrous_revenues':forms.NumberInput(attrs=attribute_dict),
            'energy_revenues':forms.NumberInput(attrs=attribute_dict),
            'total_revenues':forms.NumberInput(attrs=attribute_dict),
            'lease_cost_3':forms.NumberInput(attrs=attribute_dict),
            'third_party_cane_cost_2':forms.NumberInput(attrs=attribute_dict),
            'inputs_2':forms.NumberInput(attrs=attribute_dict),
            'fuel_2':forms.NumberInput(attrs=attribute_dict),
            'freights_2':forms.NumberInput(attrs=attribute_dict),
            'labor_cost_2':forms.NumberInput(attrs=attribute_dict),
            'industrial_cost_2':forms.NumberInput(attrs=attribute_dict),
            'depreciation_2':forms.NumberInput(attrs=attribute_dict),
            'planting_cost_2':forms.NumberInput(attrs=attribute_dict),
            'total_cogs':forms.NumberInput(attrs=attribute_dict),
            'gross_profit':forms.NumberInput(attrs=attribute_dict),
            'sales_expenses':forms.NumberInput(attrs=attribute_dict),
            'administrative_expenses':forms.NumberInput(attrs=attribute_dict),
            'other_sga_2':forms.NumberInput(attrs=attribute_dict),
            'total_sga':forms.NumberInput(attrs=attribute_dict),
            'ebit':forms.NumberInput(attrs=attribute_dict),
            'financial_expenses':forms.NumberInput(attrs=attribute_dict),
            'profit_before_taxes':forms.NumberInput(attrs=attribute_dict),
            'income_tax':forms.NumberInput(attrs=attribute_dict),
            'net_income':forms.NumberInput(attrs=attribute_dict),
            'depreciation':forms.NumberInput(attrs=attribute_dict),
            'working_capital_variation':forms.NumberInput(attrs=attribute_dict),
            'cash_flow_from_operations':forms.NumberInput(attrs=attribute_dict),
            'capex':forms.NumberInput(attrs=attribute_dict),
            'write_offs':forms.NumberInput(attrs=attribute_dict),
            'cash_flow_from_investment_activities':forms.NumberInput(attrs=attribute_dict),
            'debt_amortization':forms.NumberInput(attrs=attribute_dict),
            'new_debt':forms.NumberInput(attrs=attribute_dict),
            'cash_financing':forms.NumberInput(attrs=attribute_dict),
            'change_in_cash':forms.NumberInput(attrs=attribute_dict),
            'initial_cash_2':forms.NumberInput(attrs=attribute_dict),
            'ending_cash':forms.NumberInput(attrs=attribute_dict),
            'minimum_refinancing':forms.NumberInput(attrs=attribute_dict),
            'cash':forms.NumberInput(attrs=attribute_dict),
            'accounts_receivable':forms.NumberInput(attrs=attribute_dict),
            'inventories_2':forms.NumberInput(attrs=attribute_dict),
            'other_current_assets':forms.NumberInput(attrs=attribute_dict),
            'total_current_assets':forms.NumberInput(attrs=attribute_dict),
            'ppe':forms.NumberInput(attrs=attribute_dict),
            'other_non_current_assets_2':forms.NumberInput(attrs=attribute_dict),
            'total_non_current_assets':forms.NumberInput(attrs=attribute_dict),
            'total_assets':forms.NumberInput(attrs=attribute_dict),
            'short_term_accounts_payable':forms.NumberInput(attrs=attribute_dict),
            'short_term_debt':forms.NumberInput(attrs=attribute_dict),
            'other_current_liabilities_2':forms.NumberInput(attrs=attribute_dict),
            'total_current_liabilities':forms.NumberInput(attrs=attribute_dict),
            'long_term_debt':forms.NumberInput(attrs=attribute_dict),
            'other_non_current_liabilities_2':forms.NumberInput(attrs=attribute_dict),
            'total_non_current_liabilities':forms.NumberInput(attrs=attribute_dict),
            'total_liabilities':forms.NumberInput(attrs=attribute_dict),
            'issued_capital_2':forms.NumberInput(attrs=attribute_dict),
            'retained_earnings':forms.NumberInput(attrs=attribute_dict),
            'total_equity':forms.NumberInput(attrs=attribute_dict),
            'liabilities_plus_equity':forms.NumberInput(attrs=attribute_dict),
            'gross_margin':forms.NumberInput(attrs=attribute_dict),
            'ebitda':forms.NumberInput(attrs=attribute_dict),
            'ebitda_margin':forms.NumberInput(attrs=attribute_dict),
            'net_income_margin':forms.NumberInput(attrs=attribute_dict),
            'net_debt':forms.NumberInput(attrs=attribute_dict),
            'net_debt_ebitda':forms.NumberInput(attrs=attribute_dict),
            'net_debt_mt_of_cane':forms.NumberInput(attrs=attribute_dict),
            'indebtedness':forms.NumberInput(attrs=attribute_dict),
            'short_term':forms.NumberInput(attrs=attribute_dict),
            'current_ratio':forms.NumberInput(attrs=attribute_dict),
            'revenue_variation':forms.NumberInput(attrs=attribute_dict),
            'income_variation':forms.NumberInput(attrs=attribute_dict),
            'dscr':forms.NumberInput(attrs=attribute_dict)
        }

    def __init__(self, *args, **kwargs):
        super(userInputForm, self).__init__(*args, **kwargs)
        fields = self.fields.keys()
        for obj in fields: 
            self.fields[obj].required = False
            self.fields[obj].widget.attrs['placeholder'] = self.instance.return_field_value(obj)

    def set_season(self, season):
        data = self.data.copy()
        data['season'] = season
        self.data = data

    def set_username(self, username):
        data = self.data.copy()
        data['username'] = username
        self.data = data

class userSugarPositionInput_2(ModelForm):

    class Meta:
        model = sugar_position_info_2
        fields = [
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
        ]
        
        widgets = {
            'mar1_fxpassive_obligation':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar1_fxpassive_fixed':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar1_fxpassive_avg_price_cts':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar1_fxpassive_avg_price_brl':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'may_fxpassive_obligation':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'may_fxpassive_fixed':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'may_fxpassive_avg_price_cts':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'may_fxpassive_avg_price_brl':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'jul_fxpassive_obligation':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'jul_fxpassive_fixed':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'jul_fxpassive_avg_price_cts':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'jul_fxpassive_avg_price_brl':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),       
            'oct_fxpassive_obligation':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'oct_fxpassive_fixed':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'oct_fxpassive_avg_price_cts':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'oct_fxpassive_avg_price_brl':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),       
            'mar2_fxpassive_obligation':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar2_fxpassive_fixed':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar2_fxpassive_avg_price_cts':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar2_fxpassive_avg_price_brl':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar1_brlfixed_obligation':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar1_brlfixed_fixed':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar1_brlfixed_avg_price_cts':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar1_brlfixed_avg_price_brl':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'may_brlfixed_obligation':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'may_brlfixed_fixed':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'may_brlfixed_avg_price_cts':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'may_brlfixed_avg_price_brl':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'jul_brlfixed_obligation':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'jul_brlfixed_fixed':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'jul_brlfixed_avg_price_cts':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'jul_brlfixed_avg_price_brl':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),       
            'oct_brlfixed_obligation':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'oct_brlfixed_fixed':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'oct_brlfixed_avg_price_cts':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'oct_brlfixed_avg_price_brl':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),       
            'mar2_brlfixed_obligation':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar2_brlfixed_fixed':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar2_brlfixed_avg_price_cts':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
            'mar2_brlfixed_avg_price_brl':forms.NumberInput(attrs={'class':"form-control form-control-sm", 'type':'number', 'style':'text-align:center;'}),
        }

    def __init__(self, *args, **kwargs):
        super(userSugarPositionInput_2, self).__init__(*args, **kwargs)
        fields = self.fields.keys()
        for obj in fields: 
            self.fields[obj].required = False
            self.fields[obj].widget.attrs['placeholder'] = self.instance.return_field_value(obj)

    
    def set_username(self, username):
        data = self.data.copy()
        data['username'] = username
        self.data = data