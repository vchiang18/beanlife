from django import forms
from .models import Log, Progress
from datetime import datetime

class LogForm(forms.ModelForm):
    time_of_serving = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        initial=datetime.now()
    )

    # time_of_serving = forms.DateTimeField(
    #     input_formats=['%d/%m/%Y %H:%M'],
    #     widget=forms.DateTimeInput(attrs={
    #         'class': 'form-control datetimepicker-input',
    #         'data-target': '#datetimepicker1'
    #     })
    # )

    class Meta:
        model = Log
        fields = ["time_of_serving", "serving_type"]

    def __init__(self, *args, **kwargs):
        super(LogForm, self).__init__(*args, **kwargs)
        self.fields['time_of_serving'].required = True
        self.fields['serving_type'].required = True

# class ProgressForm(ModelForm):
#     class Meta:
#         model = Progress
#         fields = []
