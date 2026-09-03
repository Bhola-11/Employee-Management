#!/usr/bin/env python
"""
WorkSphere Enterprise HRMS — ASGI/WSGI Production Application Entry Point
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worksphere.settings')

application = get_wsgi_application()

if __name__ == '__main__':
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(['app.py', 'runserver', '127.0.0.1:8000'])
