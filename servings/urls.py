from django.urls import path
from servings.views import api_logs, home, create_log, view_log, edit_log, delete_log, celery_test,send_email, schedule_email

urlpatterns = [
    path("", home, name="home"),
    path("create/", create_log, name="create_log"),
    path("<int:log_id>", view_log, name="view_log"),
    path("<int:log_id>/edit", edit_log, name="edit_log"),
    path("<int:log_id>/delete", delete_log, name="delete_log"),
    path("test/", celery_test, name="celery_test"),
    path("sendemail/", send_email, name="send_email"),
    path("schedtest/", schedule_email, name="schedule_email"),

    path("logs/", api_logs, name="api_log"),
    # path("logs/<int:log_id>", api_log, name="api_log"),


]
