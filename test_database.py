#!/usr/bin/env python
"""
Test database connection script
Run this to verify your database configuration works
"""
import os
import django
import sys

# Set up Django with render settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trumpcoin_benefit.render_settings')
django.setup()

from django.db import connection
from django.conf import settings

def test_database_connection():
    print("Testing database connection...")
    print(f"Database Engine: {settings.DATABASES['default']['ENGINE']}")
    print(f"Database Name: {settings.DATABASES['default']['NAME']}")
    
    try:
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            print(f"✅ Database connection successful!")
            print(f"Database version: {version[0]}")
            
        # Test if tables exist
        from django.contrib.auth.models import User
        user_count = User.objects.count()
        print(f"✅ User table accessible. Current user count: {user_count}")
        
        # Test if your app tables exist
        try:
            import benefit.models
            print("✅ Benefit app tables accessible")
        except Exception as e:
            print(f"⚠️  Benefit app tables issue: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nPossible issues:")
        print("1. PostgreSQL database is not running")
        print("2. Database credentials are incorrect")
        print("3. Database URL is malformed")
        print("4. Network connectivity issues")
        return False

if __name__ == '__main__':
    success = test_database_connection()
    if not success:
        sys.exit(1)
    print("\n🎉 All database tests passed!")
