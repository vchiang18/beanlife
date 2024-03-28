from django.urls import path
from django.contrib.auth.views import LoginView
from users.views import user_login, user_logout, user_signup, create_targets, edit_targets

app_name = 'users'

urlpatterns = [
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("signup/", user_signup, name="signup"),
    path("<int:id>/targets/create", create_targets, name="create_targets"),
    path("<int:id>/targets/edit", edit_targets, name="edit_targets"),

]
