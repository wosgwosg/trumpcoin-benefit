# Configuring Django to Use PostgreSQL on Render.com

This guide provides step-by-step instructions for configuring your TrumpCoin Benefit Django application to use PostgreSQL on Render.com instead of SQLite.

## Why Use PostgreSQL Instead of SQLite?

- **Scalability**: PostgreSQL can handle more concurrent users and larger datasets
- **Advanced Features**: Full-text search, JSON support, and more complex queries
- **Reliability**: Better for production environments with multiple connections
- **Backups**: Render.com provides automatic daily backups for PostgreSQL databases

## Step 1: Update Your Local Project

### 1.1. Install Required Packages

First, add the necessary packages to your `requirements.txt` file:

```
# Add these lines to requirements.txt
dj-database-url==2.1.0
psycopg2-binary==2.9.6
```

Then install them locally:

```bash
pip install -r requirements.txt
```

### 1.2. Update Your render.yaml File

Make sure your `render.yaml` file includes a PostgreSQL database configuration:

```yaml
services:
  - type: web
    name: trumpcoin-benefit
    env: python
    buildCommand: pip install -r requirements.txt && mkdir -p staticfiles && python manage.py collectstatic --noinput
    startCommand: gunicorn trumpcoin_benefit.wsgi:application --log-level debug
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: WEB_CONCURRENCY
        value: 4
      - key: DJANGO_SETTINGS_MODULE
        value: trumpcoin_benefit.render_settings
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: trumpcoin-db
          property: connectionString

databases:
  - name: trumpcoin-db
    databaseName: trumpcoin
    user: trumpcoin_user
    plan: free
```

### 1.3. Update Your render_settings.py File

Ensure your `trumpcoin_benefit/render_settings.py` file is configured to use the PostgreSQL database:

```python
import os
import dj_database_url
from .settings import *

# ... other settings ...

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
}

# ... other settings ...
```

## Step 2: Deploy to Render.com

### 2.1. Commit and Push Your Changes

```bash
git add .
git commit -m "Configured PostgreSQL database"
git push
```

### 2.2. Create a New Web Service on Render.com

1. Log in to your [Render.com dashboard](https://dashboard.render.com/)
2. Click "New" and select "Blueprint"
3. Connect to your GitHub repository
4. Render will detect your `render.yaml` file and set up the services automatically
5. Click "Apply" to create the web service and database

## Step 3: Verify Database Creation

1. In your Render.com dashboard, go to the "Databases" section
2. You should see a new PostgreSQL database named "trumpcoin-db"
3. Click on it to view details like connection string, status, and plan

## Step 4: Run Migrations

Since you don't have access to the Render.com shell on the free plan, we'll need to add a one-time script to run migrations automatically during deployment.

### 4.1. Create a Migration Script

Create a file named `run_migrations.py` in your project root:

```python
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
```

### 4.2. Update render.yaml to Run Migrations

Update your `render.yaml` file to run migrations during the build process:

```yaml
services:
  - type: web
    name: trumpcoin-benefit
    env: python
    buildCommand: >
      pip install -r requirements.txt && 
      mkdir -p staticfiles && 
      python manage.py collectstatic --noinput &&
      python run_migrations.py
    startCommand: gunicorn trumpcoin_benefit.wsgi:application --log-level debug
    # ... rest of your configuration ...
```

## Step 5: Create a Superuser

Since you don't have shell access, you'll need to create a superuser through your application code. Here's how to add a one-time superuser creation script:

### 5.1. Create a Superuser Script

Create a file named `create_superuser.py` in your project root:

```python
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
    password = 'your-secure-password'  # Change this to a secure password
    
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
```

**Important**: Replace `'your-secure-password'` with a strong password.

### 5.2. Update render.yaml to Create Superuser

Update your `render.yaml` file to create a superuser during the build process:

```yaml
services:
  - type: web
    name: trumpcoin-benefit
    env: python
    buildCommand: >
      pip install -r requirements.txt && 
      mkdir -p staticfiles && 
      python manage.py collectstatic --noinput &&
      python run_migrations.py &&
      python create_superuser.py
    startCommand: gunicorn trumpcoin_benefit.wsgi:application --log-level debug
    # ... rest of your configuration ...
```

## Step 6: Export Data from SQLite to PostgreSQL (Optional)

If you have existing data in your SQLite database that you want to transfer to PostgreSQL, you'll need to:

### 6.1. Create a Data Export Script

Create a file named `export_data.py` in your project root:

```python
# export_data.py
import os
import json
import django

# Set up Django with local settings (SQLite)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trumpcoin_benefit.settings')
django.setup()

from django.core.serializers.json import DjangoJSONEncoder
from django.apps import apps

def export_data():
    data = {}
    
    # Get all models from your app
    app_models = apps.get_app_config('benefit').get_models()
    
    for model in app_models:
        model_name = model.__name__
        print(f"Exporting {model_name}...")
        
        # Get all instances of the model
        instances = model.objects.all()
        
        # Convert to list of dictionaries
        model_data = []
        for instance in instances:
            instance_dict = {}
            for field in instance._meta.fields:
                field_name = field.name
                field_value = getattr(instance, field_name)
                instance_dict[field_name] = field_value
            model_data.append(instance_dict)
        
        data[model_name] = model_data
    
    # Write to JSON file
    with open('data_export.json', 'w') as f:
        json.dump(data, f, cls=DjangoJSONEncoder, indent=2)
    
    print("Data export completed successfully!")

if __name__ == '__main__':
    export_data()
```

### 6.2. Create a Data Import Script

Create a file named `import_data.py` in your project root:

```python
# import_data.py
import os
import json
import django

# Set up Django with Render settings (PostgreSQL)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trumpcoin_benefit.render_settings')
django.setup()

from django.apps import apps
from django.db import transaction

def import_data():
    try:
        # Read the JSON file
        with open('data_export.json', 'r') as f:
            data = json.load(f)
        
        # Get all models from your app
        app_models = {model.__name__: model for model in apps.get_app_config('benefit').get_models()}
        
        # Import data for each model
        with transaction.atomic():
            for model_name, model_data in data.items():
                if model_name in app_models:
                    model = app_models[model_name]
                    print(f"Importing {model_name}...")
                    
                    for instance_dict in model_data:
                        # Create a new instance
                        instance = model()
                        
                        # Set field values
                        for field_name, field_value in instance_dict.items():
                            setattr(instance, field_name, field_value)
                        
                        # Save the instance
                        instance.save()
        
        print("Data import completed successfully!")
    except Exception as e:
        print(f"Error importing data: {e}")

if __name__ == '__main__':
    import_data()
```

### 6.3. Run the Export Script Locally

```bash
python export_data.py
```

### 6.4. Upload the Export File to Render.com

Since you don't have shell access on the free plan, you'll need to include the export file in your repository:

```bash
git add data_export.json
git commit -m "Add data export for PostgreSQL migration"
git push
```

### 6.5. Update render.yaml to Import Data

Update your `render.yaml` file to import data during the build process:

```yaml
services:
  - type: web
    name: trumpcoin-benefit
    env: python
    buildCommand: >
      pip install -r requirements.txt && 
      mkdir -p staticfiles && 
      python manage.py collectstatic --noinput &&
      python run_migrations.py &&
      python import_data.py &&
      python create_superuser.py
    startCommand: gunicorn trumpcoin_benefit.wsgi:application --log-level debug
    # ... rest of your configuration ...
```

## Step 7: Verify the PostgreSQL Connection

After deploying, you can verify that your application is using PostgreSQL by:

1. Logging in to your admin dashboard
2. Creating, updating, or deleting some records
3. Checking that the changes persist after restarting the application

## Step 8: Clean Up (After Successful Migration)

Once you've confirmed that your application is working correctly with PostgreSQL, you can:

1. Remove the data export/import scripts from your repository
2. Update your `render.yaml` file to remove the import step
3. Consider removing the SQLite database file from your repository

## Troubleshooting

### Common Issues and Solutions

1. **Database connection errors**:
   - Check that the `DATABASE_URL` environment variable is correctly set in Render.com
   - Verify that the PostgreSQL database is running (check status in Render dashboard)
   - Make sure `psycopg2-binary` is installed

2. **Migration errors**:
   - Check the build logs in Render.com for specific error messages
   - Try running migrations locally with the same settings to debug

3. **Data import errors**:
   - Ensure your JSON export file is properly formatted
   - Check for data type mismatches between SQLite and PostgreSQL

4. **Performance issues**:
   - Consider adding database indexes for frequently queried fields
   - Use Django's `select_related` and `prefetch_related` to optimize queries

## Additional Resources

- [Django Database Documentation](https://docs.djangoproject.com/en/5.2/ref/databases/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Render.com PostgreSQL Documentation](https://render.com/docs/databases)
- [dj-database-url Documentation](https://github.com/jazzband/dj-database-url)
