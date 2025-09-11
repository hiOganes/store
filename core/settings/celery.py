import os

from dotenv import load_dotenv


load_dotenv()

CELERY = {
    'task_track_started': True,
    'result_backend': 'django-db',
    'result_extended': True,
    'broker_url': os.getenv("ENV_BROKER_URL"),
}