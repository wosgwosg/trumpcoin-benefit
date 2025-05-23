#!/usr/bin/env python
"""
Script to update all Django templates to use the BASE_TEMPLATE context variable.
This script will find all template files that extend from 'benefit/base.html' and
update them to use '{% extends BASE_TEMPLATE|default:"benefit/base.html" %}'.
"""

import os
import re

def update_template(file_path):
    """Update a template file to use the BASE_TEMPLATE context variable."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the template extends from 'benefit/base.html'
    if re.search(r'{% extends [\'"]benefit/base.html[\'"] %}', content):
        # Replace the extends tag
        updated_content = re.sub(
            r'{% extends [\'"]benefit/base.html[\'"] %}',
            '{% extends BASE_TEMPLATE|default:\'benefit/base.html\' %}',
            content
        )
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return True
    
    return False

def main():
    """Main function to update all templates."""
    templates_dir = 'templates/benefit'
    updated_count = 0
    
    # Walk through all files in the templates directory
    for root, _, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if update_template(file_path):
                    updated_count += 1
                    print(f"Updated: {file_path}")
    
    print(f"\nTotal templates updated: {updated_count}")

if __name__ == '__main__':
    main()
