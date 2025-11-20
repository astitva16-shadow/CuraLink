"""
WSGI config for curalink project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'curalink.settings')

application = get_wsgi_application()
