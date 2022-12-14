"""
WSGI config for xwords project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from whitenoise import WhiteNoise
from xwords.settings import STATIC_ROOT
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xwords.settings')
application = WhiteNoise(get_wsgi_application(), root=STATIC_ROOT)
