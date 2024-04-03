from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beanlife.settings')

print("environ: /n/n/n", os.environ.get('REDIS_HOST'))

# redis_var = f"redis//{os.environ.get('REDIS_HOST')}:6379/0"
# app = Celery('beanlife', broker=redis_var)

# redis_var = "redis//%s:6379/0" % os.environ.get('REDIS_HOST')
app = Celery('beanlife', broker="redis//%s/0" % os.environ.get('REDIS_HOST'))


app.conf.update(timezone = 'America/Los_Angeles',
                       enable_utc=True,
                       broker_connection_retry_on_startup=True)

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# # Celery Beat Settings
# app.conf.beat_schedule = {
#     'send-email-after-90m': {
#         'task': 'send_mail_app.tasks.send_mail_func',
#         'schedule': crontab(hour=0, minute=46, day_of_month=19, month_of_year = 6),
#         #'args': (2,)
#     }

# }

# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html
