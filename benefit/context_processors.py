import os

def base_template(request):
    """
    Context processor to determine which base template to use.
    If running on Render.com, use base_render.html, otherwise use base.html.
    """
    # Check if running on Render.com by looking for Render-specific environment variables
    is_render = 'RENDER' in os.environ
    
    base_template = 'benefit/base_render.html' if is_render else 'benefit/base.html'
    
    return {
        'BASE_TEMPLATE': base_template
    }
