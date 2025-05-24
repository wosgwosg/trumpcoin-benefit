# create_superuser.py
import os
import django
import sys

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trumpcoin_benefit.render_settings')
django.setup()

# Import necessary Django components
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()

def create_superuser():
    username = 'admin'
    email = 'admin@trumpcoin-benefit.live'
    password = 'The7isstrong!'  # Change this to a secure password
    
    try:
        # Check if superuser already exists
        if not User.objects.filter(username=username).exists():
            print(f"Creating superuser {username}...")
            User.objects.create_superuser(username=username, email=email, password=password)
            print("Superuser created successfully!")
        else:
            print(f"Superuser {username} already exists.")
    except IntegrityError:
        print("Error: Superuser could not be created.")
        
if __name__ == '__main__':
    create_superuser()