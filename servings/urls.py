from django.urls import path
from servings.views import api_logs, home, create_log, view_log, edit_log, delete_log, schedule_email

urlpatterns = [
    path("", home, name="home"),
    path("create/", create_log, name="create_log"),
    path("<int:log_id>", view_log, name="view_log"),
    path("<int:log_id>/edit", edit_log, name="edit_log"),
    path("<int:log_id>/delete", delete_log, name="delete_log"),
    path("schedtest/", schedule_email, name="schedule_email"),

    path("logs/", api_logs, name="api_logs"),
    # path("logs/<int:log_id>", api_log, name="api_log"),


]
