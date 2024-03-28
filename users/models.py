from django.db import models
from django.contrib.auth.models import AbstractUser
import pytz

# Create your models here.
class User(AbstractUser):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    timezone = models.CharField(max_length=32, choices=TIMEZONES,
    default='UTC')
    servings_fiber = models.PositiveIntegerField(default=3)
    servings_fat = models.PositiveIntegerField(default=1)
    separate_fats = models.BooleanField(default=True)
