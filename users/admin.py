from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        "username",
        "first_name",
        "last_name",
        "servings_fiber",
        "servings_fat",
        "separate_fats",
    ]
    list_editable = ["servings_fiber", "servings_fat", "separate_fats"]


admin.site.register(User, CustomUserAdmin)
