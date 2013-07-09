"""
PR-130627: Main Rating Form
"""
from django import forms
from django.forms import ModelChoiceField
from django.utils.translation import ugettext as _
from ngramengine.models import NGrams

class RatingForm(forms.Form):
    textinput = forms.CharField(widget=forms.Textarea(attrs={'placeholder': _("State your text you want to analyze..."),'autofocus':'autofocus'}), min_length=2)



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