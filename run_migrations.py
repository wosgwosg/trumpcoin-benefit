# run_migrations.py
import os
import django
import sys

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trumpcoin_benefit.render_settings')
django.setup()

# Import necessary Django components
from django.core.management import call_command

def run_migrations():
    print("Running migrations...")
    call_command('migrate')
    print("Migrations completed successfully!")

if __name__ == '__main__':
    run_migrations()