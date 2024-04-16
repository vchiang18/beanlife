from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from beanlife import settings
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def test_func(self):
    #operations
    for i in range(10):
        print(i)
    return "Done"

@shared_task(bind=True)
def send_email_task(self):
    users = get_user_model().objects.all()
    #timezone.localtime(users.date_time) + timedelta(days=2)
    for user in users:
        mail_subject = "Celery Testing"
        message = "It's been 90m since your last serving. You're clear for more fats or fiber!"
        to_email = user.username
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Done"

# @shared_task
# @shared_task(bind=True)
# def send_email(self):
#     users = get_user_model().objects.all()
#     #timezone.localtime(users.date_time) + timedelta(days=2)
#     for user in users:
#         mail_subject = "Celery Testing"
#         message = "It's been 90m since your last serving. You're clear for more fats or fiber!"
#         to_email = user.username
#         send_mail(
#             subject = mail_subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[to_email],
#             fail_silently=True,
#         )
#     return "Done"
