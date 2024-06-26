from django.urls import path
from servings.views import home, create_log, view_log, edit_log, delete_log, welcome, celery_test, schedule_email

urlpatterns = [
    path("", home, name="home"),
    path("create/", create_log, name="create_log"),
    path("<int:log_id>", view_log, name="view_log"),
    path("<int:log_id>/edit", edit_log, name="edit_log"),
    path("<int:log_id>/delete", delete_log, name="delete_log"),
    path("welcome/", welcome, name="welcome")
    # path("test/", celery_test, name="celery_test"),
    # path("sendemail/", send_email, name="send_email"),
    # path("schedtest/", schedule_email, name="schedule_email")
]
