#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pandas as pd

def initial_data():

    from data_manager import models
    
    data_df = pd.read_csv('Final_Final_MC.csv', index_col=False)
    print(data_df)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hedgebot_server_manager.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    initial_data()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
