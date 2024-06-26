from django.shortcuts import render, get_object_or_404, redirect
from .models import Log, Progress
from servings.forms import LogForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
from django.conf import settings
from .tasks import test_task
from celery.schedules import crontab
from beanlife.settings import EMAIL_HOST_PASSWORD
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import os
from django.utils.timezone import activate
from pytz import timezone

#celery test
def celery_test(request):
    test_task.delay()
    return HttpResponse("Done")

# #email test
# def send_email(request):
#     send_email_task.delay()
#     # print(EMAIL_HOST_PASSWORD)
#     return HttpResponse("Sent")

#schedule task test
def schedule_email(request):
    activate(timezone('America/Los_Angeles'))
    schedule, created = CrontabSchedule.objects.get_or_create(hour = 15, minute = 50,
                                                              day_of_month = 24, month_of_year = 4,
            timezone='America/Los_Angeles'
            )
    #name below needs to be unique, such as w user_id
    task = PeriodicTask.objects.create(
        crontab=schedule,
        name="4.24.a",
        task='servings.tasks.send_90m_email',
        )#, args = json.dumps([[2,3]]))
    return HttpResponse("Done")

# #function to get user's timezone
# def get_user_timezone(request):
#     user_timezone = getattr(request.user, 'timezone', None)
#     return user_timezone if user_timezone else settings.DEFAULT_TIME_ZONE


# Create your views here.
@login_required
def home(request):
    logs = Log.objects.filter(user=request.user).order_by("-time_of_serving")
    context = {
        "logs": logs
    }
    return render(request, "servings/home.html", context)

@login_required
def create_log(request):
    if request.method == "POST":
        form = LogForm(request.POST)
        if form.is_valid():
            log = form.save(False)
            log.user = request.user
            log.save()
            return redirect("home")
    else:
        form = LogForm()
    context = {
        "form": form,
    }
    return render(request, "servings/log.html", context)

@login_required
def view_log(request, log_id):
    print("view log id", log_id)
    log = get_object_or_404(Log, log_id=log_id)
    context = {
        "log": log
    }
    return render(request, "servings/detail.html", context)

@login_required
def edit_log(request, log_id):
    log = get_object_or_404(Log, log_id=log_id)
    if request.method == "POST":
        form = LogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = LogForm(instance=log)
    context = {"log_form": form,
               "log": log}
    return render(request, "servings/edit.html", context)

@login_required
def view_logs(request):
    pass

@login_required
def delete_log(request, log_id):
    log = get_object_or_404(Log, log_id=log_id)
    log.delete()
    return redirect("home")

def welcome(request):
    return render(request, "servings/welcome.html")
