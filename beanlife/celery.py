from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beanlife.settings')
app = Celery('beanlife')
app.conf.broker_url = 'redis://redis:6379/0'
app.conf.update(timezone = 'America/Los_Angeles',
                       enable_utc=True,
                       broker_connection_retry_on_startup=True,
                       result_backend='django-db',
                       result_extended=True,
                       include=['servings.tasks',],
                       )

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# # Celery Beat Settings
app.conf.beat_schedule = {
    'send-email-after-90m': {
        'task': 'servings.tasks.send_email_task',
        'schedule': crontab(hour=16, minute=56, day_of_month=16, month_of_year = 4),
        #'args': (2,)
    }

}

# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html
