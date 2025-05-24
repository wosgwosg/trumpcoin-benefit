"""
Diagnostic views for troubleshooting deployment issues.
"""
import os
import sys
import django
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def debug_info(request):
    """
    View that returns debug information about the environment.
    """
    # Collect basic information
    info = {
        "django_version": django.get_version(),
        "python_version": sys.version,
        "settings_module": os.environ.get('DJANGO_SETTINGS_MODULE', 'unknown'),
        "debug_mode": settings.DEBUG,
        "allowed_hosts": settings.ALLOWED_HOSTS,
        "static_root": settings.STATIC_ROOT,
        "static_url": settings.STATIC_URL,
        "staticfiles_dirs": [str(dir_path) for dir_path in settings.STATICFILES_DIRS],
        "staticfiles_storage": settings.STATICFILES_STORAGE,
        "middleware": settings.MIDDLEWARE,
        "installed_apps": settings.INSTALLED_APPS,
        "database_engine": settings.DATABASES['default']['ENGINE'],
        "request_method": request.method,
        "request_path": request.path,
        "request_headers": dict(request.headers),
        "request_get": dict(request.GET),
        "request_post": dict(request.POST),
        "environment_variables": {
            key: value for key, value in os.environ.items() 
            if key.startswith(('DJANGO', 'PYTHON', 'RENDER', 'DATABASE'))
        },
    }
    
    # Check if static files directory exists
    static_root_exists = os.path.exists(settings.STATIC_ROOT)
    info["static_root_exists"] = static_root_exists
    
    if static_root_exists:
        # List files in static root
        static_files = []
        for root, dirs, files in os.walk(settings.STATIC_ROOT):
            for file in files:
                static_files.append(os.path.join(root, file).replace(settings.STATIC_ROOT, ''))
        info["static_files"] = static_files[:20]  # Limit to first 20 files
    
    # Check if static dirs exist
    static_dirs_info = []
    for static_dir in settings.STATICFILES_DIRS:
        dir_exists = os.path.exists(static_dir)
        dir_info = {
            "path": str(static_dir),
            "exists": dir_exists
        }
        if dir_exists:
            # Count files
            file_count = sum(len(files) for _, _, files in os.walk(static_dir))
            dir_info["file_count"] = file_count
        static_dirs_info.append(dir_info)
    
    info["static_dirs_info"] = static_dirs_info
    
    # Format as pretty JSON
    response_content = json.dumps(info, indent=2)
    return HttpResponse(response_content, content_type="application/json")

def test_500(request):
    """
    View that deliberately raises an exception to test 500 error handling.
    """
    # This will raise a ZeroDivisionError
    1 / 0
    return HttpResponse("This should never be returned")

def test_template(request):
    """
    View that renders a simple template to test template rendering.
    """
    from django.shortcuts import render
    return render(request, 'benefit/test_template.html', {
        'title': 'Template Test',
        'message': 'If you can see this, template rendering is working correctly!'
    })
