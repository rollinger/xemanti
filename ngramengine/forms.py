# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from models import NGrams
from django.forms.widgets import Select

class RatePartOfSpeechForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RatePartOfSpeechForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['token'].widget.attrs['readonly'] = True
    class Meta:
        model = NGrams
        fields = ['token',]#'partofspeech','language']
