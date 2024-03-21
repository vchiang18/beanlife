from django.urls import path
from django.contrib.auth.views import LoginView
from users.views import user_login, user_logout, user_signup
app_name = 'users'

urlpatterns = [
    path("login/", user_login, name="user_login"),
    path("logout/", user_logout, name="logout"),
    path("signup/", user_signup, name="signup"),
]
