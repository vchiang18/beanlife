from django.urls import path
from servings.views import home, create_log, view_log, edit_log
urlpatterns = [
    path("", home, name="home"),
    path("create/", create_log, name="create_log"),
    path("<int:log_id>", view_log, name="view_log"),
    # path("<int:id>/edit", edit_log, name="edit_log"),

]
