from django.core.management.base import BaseCommand, CommandError
from data_manager import models
from data_manager.models import monte_carlo_market_data, market_data
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **options):
         r = 1