from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from users.forms import LoginForm, SignupForm, TargetForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

User = get_user_model()

# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()
    context = {
        "form": form,
        }
    return render(request, "registration/login.html", context)


def user_logout(request):
    logout(request)
    # return HttpResponse("Logged out, see you soon!")
    return redirect("home")


def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['password_confirmation']

            if password == password_confirmation:
                user = User.objects.create_user(
                    username,
                    password=password
                )
                login(request, user)
                return redirect("home")
            else:
                form.add_error("password", "the passwords do not match")
    else:
        form = SignupForm()
        context = {
            "form": form,
        }
    return render(request, "registration/signup.html", context)

# @require_http_methods(["POST", "PUT"])
# def api_targets(request):
#     if request.method == "POST":
#         pass
#     elif request.method == "PUT":
#         #validation servings must be at least 1

@login_required
def create_targets(request):
    if request.method == "POST":
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.save(False)
            target.user = request.user
            target.save()
            return redirect("home")
    else:
        form = TargetForm()
        context = {
            "form": form,
        }
    return render(request, "registration/set_targets.html", context)

@login_required
def edit_targets(request, id):
    target = get_object_or_404(User, id=id)
    if request.method == "POST":
        form = TargetForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TargetForm(instance=target)
        context = {
            "form": form,
            "target": target
        }
    return render(request, "registration/edit_targets.html", context)
