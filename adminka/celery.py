import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminka.settings')
celery_app = Celery('adminka', include=['adminka.tasks'])
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
celery_app.conf.timezone = settings.TIME_ZONE

celery_app.conf.beat_schedule = {
     'check_is_games_end': {
         'task': 'adminka.tasks.check_is_games_end',
         'schedule': crontab(minute='*/10'),
    },
    'update_played_games': {
        'task': 'adminka.tasks.update_played_games',
        'schedule': crontab(minute=0, hour=0, day_of_month=1),
    },
    'update_teams': {
        'task': 'adminka.tasks.update_teams',
        'schedule': crontab(minute=0, hour=0, day_of_month=1),
    },
}
