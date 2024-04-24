from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

#initalize celery app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beanlife.settings')
app = Celery('beanlife')
app.conf.broker_url = 'redis://redis:6379/0'
app.conf.update(timezone = 'America/Los_Angeles',
                       enable_utc=True,
                       broker_connection_retry_on_startup=True,
                       result_backend='django-db',
                       result_extended=True,
                       include=['servings.tasks',],
                       CELERYD_CONCURRENCY=1
                       )

app.config_from_object(settings, namespace='CELERY')

#import tasks from registered django app modules
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html
