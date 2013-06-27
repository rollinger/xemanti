"""
PR-130427: Main Input Form
"""
from django import forms
from django.utils.translation import ugettext as _

class TextAnalyticInputForm(forms.Form):
    textinput = forms.CharField(widget=forms.Textarea(attrs={'placeholder': _("State your text you want to analyze..."),'autofocus':'autofocus'}), min_length=2)
    #locale = forms.ChoiceField()
    
class RateAssociationForm(forms.Form):
    rating = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("State your immediate thought..."),'autofocus':'autofocus'}), min_length=2, max_length=255)
    rating_sentence = forms.CharField(widget=forms.HiddenInput())