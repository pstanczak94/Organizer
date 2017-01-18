# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "organizer.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from organizer.tools import InitAppsCheckingSystem
InitAppsCheckingSystem()
