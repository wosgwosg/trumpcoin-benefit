#!/usr/bin/env python
"""
PostgreSQL Database Connection Fix Script for Render.com
This script will help diagnose and fix database connection issues
"""
import os
import sys

def test_database_with_settings(settings_module):
    """Test database connection with specific settings module"""
    print(f"\n🧪 Testing with {settings_module}")
    print("=" * 50)
    
    # Set Django settings
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
    
    try:
        import django
        django.setup()
        print("✅ Django setup successful")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    from django.conf import settings
    from django.db import connection
    
    # Display database configuration
    db_config = settings.DATABASES['default']
    print(f"📊 Database Configuration:")
    print(f"   Engine: {db_config.get('ENGINE', 'Not set')}")
    print(f"   Name: {db_config.get('NAME', 'Not set')}")
    print(f"   Host: {db_config.get('HOST', 'Not set')}")
    print(f"   Port: {db_config.get('PORT', 'Not set')}")
    print(f"   User: {db_config.get('USER', 'Not set')}")
    
    # Test connection
    try:
        print("\n🔌 Testing database connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            print(f"✅ Connection successful!")
            print(f"   PostgreSQL version: {version[0]}")
            return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

def main():
    print("🔧 PostgreSQL Database Connection Diagnostic Tool")
    print("=" * 60)
    
    # Test different settings modules
    settings_modules = [
        'trumpcoin_benefit.render_settings_fixed',
        'trumpcoin_benefit.render_settings',
        'trumpcoin_benefit.production_settings',
    ]
    
    successful_connections = []
    
    for module in settings_modules:
        try:
            # Reset Django
            if 'django' in sys.modules:
                del sys.modules['django']
            if 'django.conf' in sys.modules:
                del sys.modules['django.conf']
            
            success = test_database_with_settings(module)
            if success:
                successful_connections.append(module)
        except Exception as e:
            print(f"❌ Failed to test {module}: {e}")
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    
    if successful_connections:
        print("✅ Successful connections:")
        for module in successful_connections:
            print(f"   - {module}")
        print(f"\n💡 Recommendation: Use {successful_connections[0]} for deployment")
    else:
        print("❌ No successful connections found")
        print("\n🔍 Troubleshooting steps:")
        print("1. Verify your database credentials are correct")
        print("2. Check if the database server is running")
        print("3. Ensure your IP is whitelisted (if applicable)")
        print("4. Verify the database URL format")
        print("5. Check network connectivity to the database host")

if __name__ == '__main__':
    main()
