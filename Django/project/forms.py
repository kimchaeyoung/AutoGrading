from django import forms
from .models import *


class SignUpForm(forms.Form):

    id = forms.CharField(max_length=30)
    name = forms.CharField(max_length=30)
    other = forms.IntegerField()


