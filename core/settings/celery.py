CELERY = {
    'timezone': 'Europe/Moscow',
    'task_track_started': True,
    'result_backend': 'django-db',
    'result_extended': True,
    'broker_url': 'redis://localhost:6379/1',
}