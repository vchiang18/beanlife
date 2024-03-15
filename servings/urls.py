from django.urls import path
from servings.views import home, create_log
urlpatterns = [
    path("", home, name="home"),
    path("create/", create_log, name="create_receipt"),
]
