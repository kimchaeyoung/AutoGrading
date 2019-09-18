from django import forms
from .models import *


class SignUpForm(forms.Form):

    id = forms.CharField(max_length=30)
    name = forms.CharField(max_length=30)
    other = forms.IntegerField(required=False)

class HWInfo(forms.Form):
    link = forms.CharField(max_length=200)
    datetime = forms.DateTimeField(
        input_formats=['%Y %m %d %H:%M'],
        widget = forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepickerl'
        })
    ) 
