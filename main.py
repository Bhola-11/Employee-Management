#!/usr/bin/env python
"""
WorkSphere Enterprise HRMS — Primary Application Entry Point
"""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worksphere.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc
        
    if len(sys.argv) == 1:
        # Default behavior when run directly: start development server
        print("=" * 60)
        print("Starting WorkSphere Enterprise HRMS Platform...")
        print("Access dashboard at: http://127.0.0.1:8000/")
        print("=" * 60)
        execute_from_command_line(['main.py', 'runserver', '0.0.0.0:8000'])
    else:
        execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
