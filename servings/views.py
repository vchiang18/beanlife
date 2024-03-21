from django.shortcuts import render, get_object_or_404, redirect
from .models import Log, Progress
# from servings.forms import LogForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@login_required
def home(request):
    logs = Log.objects.filter(user=request.user)
    context = {
        "logs": logs
    }
    return render(request, "servings/home.html", context)
    # return HttpResponse("I didn't choose the bean life, the bean life chose me.")

@login_required
def create_log(request):
    if request.method=="POST":
        form = LogForm(request.POST)
        if form.is_valid():
            log = form.save(False)
            log.user = request.user
            log.save()
            return redirect ("home")
    else:
        form = LogForm()
    context = {
        "form": form,
    }
    return render(request, "logs/create.html", context)

@login_required
def view_log(request):
    pass

@login_required
def edit_log(request):
    pass

@login_required
def view_logs(request):
    pass

@login_required
def delete_log(request):
    pass
