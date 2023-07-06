from django import forms
from .models import Car_details,User

class Car_Detail(forms.ModelForm): 
    class Meta:
        model=Car_details
        fields="__all__"

class Users(forms.ModelForm):
    class Meta:
        model=User
        fields="__all__"