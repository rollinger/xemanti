"""
PR-130427: Main Input Form
"""
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from captcha.fields import CaptchaField



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    
    def clean_email(self):
        data = self.cleaned_data['email']
        #TODO: Add real email validation
        return data
    
    class Meta:
        model = User
        fields = ("username", "email", )
