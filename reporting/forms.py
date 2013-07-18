"""
PR-130627: Reporting Forms
"""
from django import forms
from django.utils.translation import ugettext as _

class QueryNGramForm(forms.Form):
    ngram = forms.CharField( widget=forms.TextInput(attrs={
                                                            'placeholder': _("State your Word you want to inspect"),
                                                            'autofocus':'autofocus','class':'unit-100'}),
                              min_length=2, max_length=255, label=_("Inspect the Word: "))
    
    
class TextAnalyticInputForm(forms.Form):
    textinput = forms.CharField(widget=forms.Textarea(attrs={'placeholder': _("State your text you want to analyze..."),'autofocus':'autofocus'}), min_length=2)
    #locale = forms.ChoiceField()
