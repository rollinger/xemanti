# -*- coding: utf-8 -*-
# Generic Import Statement
from django.contrib import auth
from django import forms
from django.utils.translation import ugettext as _
from django.utils.html import strip_tags, escape
from django.http import HttpResponse
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

# Custom Import Statement
from forms import RatePartOfSpeechForm
from ngramengine.models import NGrams

def rating_partofspeech_view(request):
    
    ngram = NGrams.objects.filter(partofspeech=None).order_by('-t_occurred')[0]
    
    # Form submitted:
    if request.method == 'POST':
        form = RatePartOfSpeechForm(request.POST,instance=ngram)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse( 'rating_partofspeech' ) )
    # Form not submitted:
    else:
        #ngram = NGrams.objects.filter(partofspeech=None).order_by('-t_occurred')[:1].get()
        form = RatePartOfSpeechForm(instance=ngram) 
    # Render Template Home
    return render_to_response('ngramengine/rate.html', {
        "form":form
    }, context_instance=RequestContext(request))