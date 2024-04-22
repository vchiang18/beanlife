from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from beanlife import settings
from django.utils import timezone
from datetime import datetime, timedelta
from celery.schedules import crontab
from .models import Log


@shared_task(bind=True)
def test_task(self):
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

#filters for current time + 90m
@shared_task
def send_90m_alert(self):
    threshold_time = datetime.now() - timedelta(minutes=3)

    users_to_email = Log.objects.filter(time_of_serving__gte=threshold_time)
    print("users to email: ", users_to_email)

    for user in users_to_email:
        mail_subject = "Celery - Timed Test"
        message = "It's been 90m since your last serving. You're clear for more fats or fiber!"
        to_email = Log.user.username
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Done"

    # if SendEmailAt.objects.filter(when=timezone.now().date()).exists():
    #     send_email_task
