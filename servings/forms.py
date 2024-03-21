from django.forms import ModelForm
from .models import Log, Progress

class LogForm(ModelForm):
    class Meta:
        model = Log
        fields = ["time_of_serving", "serving_type"]

# class ProgressForm(ModelForm):
#     class Meta:
#         model = Progress
#         fields = []
