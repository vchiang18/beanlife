from django.db import models
from users.models import User


# Create your models here.
class Log(models.Model):
    FIBER = 'fiber'
    FAT = 'fat'
    SERVING_TYPE_CHOICES = [
        (FIBER, 'Fiber'),
        (FAT, 'Fat'),
    ]
    time_of_serving = models.DateTimeField(auto_now_add=True)
    serving_type = models.CharField(
        max_length=30,
        choices=SERVING_TYPE_CHOICES
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.user.username} - {self.log_id}"


class Progress(models.Model):
    fiber_actual = models.DecimalField(max_digits=10, decimal_places=2)
    fat_actual = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    progress_id = models.AutoField(primary_key=True)
