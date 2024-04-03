from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['ups_name', 'ups_serial_number', 'mobile_number', 'alternate_mobile_number', 'email', 'address']


# enroll/forms.py

from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
