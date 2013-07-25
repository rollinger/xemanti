"""
PR-130627: Rating Forms
"""
from django import forms
from django.forms import ModelChoiceField
from django.utils.translation import ugettext as _
from ngramengine.models import NGrams

class RateAssociationForm(forms.Form):
    rating = forms.CharField( widget=forms.TextInput(attrs={'placeholder': _("State your immediate association..."),'autofocus':'autofocus','class':'unit-100'}), min_length=2, max_length=255)
    target = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        if "ngram" in kwargs: ngram = kwargs.pop('ngram')
        super(RateAssociationForm, self).__init__(*args, **kwargs)
        if "ngram" in locals(): 
            self.fields['rating'].label = ngram.token
            #self.fields['target'].value = ngram.token
            
    #def clean(self):
        #rating = self.cleaned_data['rating']
        #target = self.cleaned_data['target']


# DEPRECATED
class NGramSetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if "languages" in kwargs: languages = kwargs.pop('languages')
        if "partofspeeches" in kwargs: partofspeeches = kwargs.pop('partofspeeches')
        super(NGramSetupForm, self).__init__(*args, **kwargs)
        if "languages" in locals(): self.fields['languages'] = ModelChoiceField(queryset=languages)
        if "partofspeeches" in locals(): self.fields['partofspeeches'] = ModelChoiceField(queryset=partofspeeches)
    #for item in range(5):
    #    self.fields['test_field_%d' % item] = CharField(max_length=255)
    class Meta:
        model = NGrams
        fields = ['token',]
        
        
        
class NGramExtensiveForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NGramExtensiveForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = NGrams