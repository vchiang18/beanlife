from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Log, Progress

# Register your models here.

@admin.register(Log)
class Log (admin.ModelAdmin):
    list_display= [
        "user",
        "log_id",
        "time_of_serving",
    ]

@admin.register(Progress)
class Progress (admin.ModelAdmin):
    list_display= [
        "user",
        "progress_id",
        "fiber_actual",
        "fat_actual",
        "date"
    ]
