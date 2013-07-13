"""
PR-130427: Main Input Form
"""
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label = "Email")

    class Meta:
        model = User
        fields = ("username", "email", )
        
class TextAnalyticInputForm(forms.Form):
    textinput = forms.CharField(widget=forms.Textarea(attrs={'placeholder': _("State your text you want to analyze..."),'autofocus':'autofocus'}), min_length=2)
    #locale = forms.ChoiceField()
    