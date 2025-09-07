"""
WSGI config for video_viewer project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')

application = get_wsgi_application()
