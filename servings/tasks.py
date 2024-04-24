from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from beanlife import settings
from django.utils import timezone
from datetime import datetime, timedelta
from celery.schedules import crontab
from .models import Log


@shared_task
def send_90m_email():
    #datetime.now() or timezone.now()? test
    threshold_time = timezone.now() - timedelta(minutes=90)
    print("threshold time: ", threshold_time)

    logs_to_email = Log.objects.filter(time_of_serving__lte=threshold_time)
    print("users to email: ", logs_to_email)

    for log in logs_to_email:
        mail_subject = "90m alert"
        message = f"Log ID: {log.pk}\n\nTime of Serving: {log.time_of_serving}\n\nThis is a 90m alert."
        to_email = log.user.username
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
