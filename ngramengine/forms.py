# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from models import NGrams
from django.forms.widgets import Select

NGRAM_LINKING_CHOICES = (
       ("assoc", _("assoc")),
       ("notrelated", _("notrelated")),
       ("synonym", _("synonym")),
       ("antonym", _("antonym")),
       ("super", _("super")),
       ("sub", _("sub")),
       ("lang", _("lang")),
       ("pos", _("pos")),
   )
class NGramBulkUploadForm(forms.Form):
    source  = forms.CharField(widget=forms.TextInput())
    type    = forms.ChoiceField(choices=NGRAM_LINKING_CHOICES)
    target  = forms.CharField(widget=forms.TextInput())



class RatePartOfSpeechForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RatePartOfSpeechForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['token'].widget.attrs['readonly'] = True
    class Meta:
        model = NGrams
        fields = ['token',]#'partofspeech','language']
