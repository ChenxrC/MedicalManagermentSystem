"""
ASGI config for video_viewer project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_viewer.settings')

application = get_asgi_application()
