#!/usr/bin/env python
"""
Debug database connection script
This will show detailed error information
"""
import os
import sys

# Set up Django with render settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trumpcoin_benefit.render_settings')

try:
    import django
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

from django.conf import settings
print(f"📊 Database configuration:")
print(f"   Engine: {settings.DATABASES['default']['ENGINE']}")
print(f"   Name: {settings.DATABASES['default']['NAME']}")
print(f"   Host: {settings.DATABASES['default']['HOST']}")
print(f"   Port: {settings.DATABASES['default']['PORT']}")
print(f"   User: {settings.DATABASES['default']['USER']}")

try:
    from django.db import connection
    print("\n🔌 Testing database connection...")
    
    # Test basic connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"✅ Database connection successful!")
        print(f"   PostgreSQL version: {version[0]}")
        
except Exception as e:
    print(f"❌ Database connection failed!")
    print(f"   Error: {e}")
    print(f"   Error type: {type(e).__name__}")
    
    # Additional debugging
    import traceback
    print("\n🔍 Full error traceback:")
    traceback.print_exc()
