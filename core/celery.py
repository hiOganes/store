import os
from celery import Celery

from core.settings.celery import CELERY


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.main')

app = Celery('core')
app.config_from_object(CELERY)
app.autodiscover_tasks()