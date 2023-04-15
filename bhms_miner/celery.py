import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bhms_miner.settings')
app = Celery('bhms_miner')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
