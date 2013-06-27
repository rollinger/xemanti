"""
PR-130627: Main Rating Form
"""
from django import forms
from django.utils.translation import ugettext as _

class RatingForm(forms.Form):
    textinput = forms.CharField(widget=forms.Textarea(attrs={'placeholder': _("State your text you want to analyze..."),'autofocus':'autofocus'}), min_length=2)
