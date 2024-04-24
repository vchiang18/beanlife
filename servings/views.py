from django.shortcuts import render, get_object_or_404, redirect
from .models import Log, Progress
from users.models import User
from servings.forms import LogForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from django.conf import settings
# from .tasks import test_task, send_email_task
from celery.schedules import crontab
from beanlife.settings import EMAIL_HOST_PASSWORD
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import os
import json
from django.utils.timezone import activate
from django.utils import timezone
from pytz import timezone
from common.json import ModelEncoder
from datetime import datetime, timedelta


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
# #celery test
# def celery_test(request):
#     test_task.delay()
#     return HttpResponse("Done")

# #email test
# def send_email(request):
#     send_email_task.delay()
#     # print(EMAIL_HOST_PASSWORD)
#     return HttpResponse("Sent")


# #schedule task test
def schedule_email(request):
    activate(timezone('America/Los_Angeles'))
    schedule, created = CrontabSchedule.objects.get_or_create(hour = 16, minute = 49,
                                                              month_of_year = 4, day_of_month = 23,
            timezone='America/Los_Angeles'
            )
    #name below needs to be unique, such as w user_id
    task = PeriodicTask.objects.create(
        crontab=schedule,
        name="4-23.e",
        task='servings.tasks.send_90m_email',
        )
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

            # #converts time_of_serving into user's timezone
            # datetime_from_user = form.cleaned_data['time_of_serving']
            # user_timezone = request.user.timezone

            # server_timezone = timezone.get_default_timezone()  # Get the server's timezone
            # user_timezone_obj = pytz.timezone(user_timezone)  # Get the user's timezone object
            # aware_datetime = user_timezone_obj.localize(datetime_from_user)  # Make the datetime aware in the user's timezone
            # converted_datetime = aware_datetime.astimezone(server_timezone)

            # log.time_of_serving = aware_datetime

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
