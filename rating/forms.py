"""
PR-130627: Rating Forms
"""
from django import forms
from django.forms import ModelChoiceField
from django.utils.translation import ugettext as _
from ngramengine.models import NGrams, SemanticDifferential, SensoryDimensions

class RateAssociationForm(forms.Form):
    rating = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("State your immediate association..."),'autofocus':'autofocus','class':'unit-100'}), min_length=2, max_length=255)
    target = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        if "ngram" in kwargs: ngram = kwargs.pop('ngram')
        super(RateAssociationForm, self).__init__(*args, **kwargs)
        if "ngram" in locals(): 
            self.fields['rating'].label = ngram.token



class SortAssociationForm(forms.Form):
    #rating = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("State your immediate association..."),'autofocus':'autofocus','class':'unit-100'}), min_length=2, max_length=255)
    
    sorting = forms.CharField(widget=forms.HiddenInput())
    ngram = forms.CharField(widget=forms.HiddenInput())
    source = forms.CharField(widget=forms.HiddenInput())



class SemanticDifferentialForm(forms.ModelForm):
    class Meta:
         model = SemanticDifferential
         fields = ('evaluation', 'potency', 'activity')
         widgets = {
            'evaluation': forms.HiddenInput(),
            'potency': forms.HiddenInput(),
            'activity': forms.HiddenInput()
            }



class SensoryDimensionForm(forms.ModelForm):
    class Meta:
         model = SensoryDimensions
         fields = ('visual', 'auditory', 'cognition','kinesthetic', 'olfactory', 'gustatory')
         widgets = {
            'visual': forms.HiddenInput(),
            'auditory': forms.HiddenInput(),
            'cognition': forms.HiddenInput(),
            'kinesthetic': forms.HiddenInput(),
            'olfactory': forms.HiddenInput(),
            'gustatory': forms.HiddenInput()
            }