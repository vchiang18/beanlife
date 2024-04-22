from django.shortcuts import render, get_object_or_404, redirect
from .models import Log, Progress
from users.models import User
from servings.forms import LogForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
import datetime
from django.conf import settings
from .tasks import test_task, send_email_task
from celery.schedules import crontab
from beanlife.settings import EMAIL_HOST_PASSWORD
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import os
import json
from django.utils.timezone import activate
from pytz import timezone
from common.json import ModelEncoder

class UserEncoder(ModelEncoder):
    model = User
    properties = ["id",
                  "username"]

class LogEncoder(ModelEncoder):
    model = Log
    properties = ["time_of_serving",
                  "user",
                  "log_id"
                ]
    encoders = {"user": UserEncoder()}

#CELERY
#celery test
def celery_test(request):
    test_task.delay()
    return HttpResponse("Done")

#email test
def send_email(request):
    send_email_task.delay()
    # print(EMAIL_HOST_PASSWORD)
    return HttpResponse("Sent")

#schedule task test
def schedule_email(request):
    activate(timezone('America/Los_Angeles'))
    schedule, created = CrontabSchedule.objects.get_or_create(hour = 11, minute = 11,
            timezone='America/Los_Angeles'
            )
    #name below needs to be unique, such as w user_id
    task = PeriodicTask.objects.create(
        crontab=schedule,
        name="schedule_email_task"+"14",
        task='servings.tasks.send_90m_alert',
        )#, args = json.dumps([[2,3]]))
    return HttpResponse("Done")

#function to get user's timezone
def get_user_timezone(request):
    user_timezone = getattr(request.user, 'timezone', None)
    return user_timezone if user_timezone else settings.DEFAULT_TIME_ZONE


#APIs - no login required
@require_http_methods(["GET", "POST"])
def api_logs(request):
    if request.method == "GET":
        user = Token.objects.get(key=request.META.get("HTTP_AUTHORIZATION")).user
        logs = user.logs.all().order_by("-time_of_serving")
        return JsonResponse({"logs": logs}, encoder=LogEncoder, safe=False)
    else:
        content = json.loads(request.body)
        # add try except blocks?
        log = Log.objects.create(**content)
        return JsonResponse(
            log,
            encoder=LogEncoder,
            safe=False
        )

#token-based auth example
# @require_http_methods(["GET", "POST"])
# def api_log(request):
#     if request.method == "GET":
#         user = Token.objects.get(key=request.META.get("HTTP_AUTHORIZATION")).user
#         logs = Log.objects.filter(user=request.user).order_by("-time_of_serving")
#     else:
#         pass

#template-based views
@login_required
def home(request):
    logs = Log.objects.filter(user=request.user).order_by("-time_of_serving")
    context = {
        "logs": logs
    }
    return render(request, "servings/home.html", {"logs": logs})

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
