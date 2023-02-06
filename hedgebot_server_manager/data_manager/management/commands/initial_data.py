from django.core.management.base import BaseCommand, CommandError
from data_manager import models



class Command(BaseCommand):

    def handle(self, *args, **options):
        data_df = pd.read_csv('Final_Final_MC.csv', index_col=False)
        print(data_df)
