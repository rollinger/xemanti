# -*- coding: utf-8 -*-
# Generic Import Statement
from django.contrib import auth
from django import forms
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.db.models import Q, F
from django.db.models import Count
from django.utils import simplejson
import itertools

# Custom Import Statement
from forms import RateAssociationForm, NGramSetupForm, NGramExtensiveForm
from ngramengine.models import *

#
# Rating View for Associations
#
def rate_assoc_view(request):
    # Form submitted:
    if request.method == 'POST':
        form = RateAssociationForm(request.POST)
        if 'skip' in request.POST:
            return HttpResponseRedirect(reverse('rate_assoc'))
        elif 'rate' in request.POST:
            if form.is_valid():
                # get source and target ngram
                source = NGrams.inject(token=form.cleaned_data['target'])
                target = NGrams.inject(token=form.cleaned_data['rating'])
                # Save Association
                Associations.inject(source, target)
            return HttpResponseRedirect(reverse('rate_assoc'))
    # Form not submitted:
    else:
        # Get NGram to rate (german and qualified, sorted ascending by t_occurred and t_rated
        rateable_languages = Languages.objects.filter(language="Deutsch")
        ngram = NGrams.objects.filter(language__in=rateable_languages).filter(qualified=True).order_by("?")[0]#.order_by("-t_occurred").order_by("t_rated")[0]
        # Get Suggestions for rating (json)
        rating_suggestions = simplejson.dumps( sorted( list( itertools.chain(*ngram.get_all_outbounds().values_list('target__token') ) ) ) )
        # Unbound form
        form = RateAssociationForm(ngram=ngram)
        form.fields['target'] = forms.CharField(initial=ngram.token, widget=forms.widgets.HiddenInput())
    
    # Render Template Home
    return render_to_response('rating/ngram_rating.html', {
        "form":form,
        "rating_suggestions":rating_suggestions,
    }, context_instance=RequestContext(request))




#
# Setup View for Admins introducing 
#
def ngram_setup_view(request):

    # Form submitted:
    if request.method == 'POST':
        form = NGramExtensiveForm(request.POST)
        if 'delete' in request.POST:
            pass
            # delete ngram
            #ngram.delete()
        elif 'update' in request.POST:
            pass
            # update ngram
            #ngram.save()
        return HttpResponseRedirect(reverse('ngram_setup'))
    # Form not submitted:
    else:
        # Get NGram
        ngram = NGrams.objects.order_by("?")[0]
        # Unbound form
        form = NGramExtensiveForm(instance=ngram)
    
    # Render Template Home
    return render_to_response('rating/ngram_setup.html', {
        #"ngram":ngram,
        "form":form,
    }, context_instance=RequestContext(request))
    
    
    
    
    
    
def ngram_setup_view_old(request):

    # Form submitted:
    if request.method == 'POST':
        form = NGramSetupForm(request.POST)
        ngram = NGrams.objects.get(token=form.data['token'])
        if 'delete' in request.POST:
            # delete ngram
            ngram.delete()
        elif 'update' in request.POST:
            # update ngram
            ngram.save()
            if form.data['languages']:
                ngram.language.add(Languages.objects.get(pk=int(form.data['languages'])))
            if form.data['partofspeeches']:
                ngram.partofspeech.add(PartOfSpeech.objects.get(pk=int(form.data['partofspeeches'])))
        return HttpResponseRedirect(reverse('ngram_setup'))
    # Form not submitted:
    else:
        # Get NGram and languages and part of speech
        relevant_language = None #Languages.objects.get(language="Englisch")
        languages = Languages.objects.all().order_by('-ngram_count')
        partofspeeches = PartOfSpeech.objects.all().order_by('-ngram_count')
        try:
            ngram = NGrams.objects.filter(Q(language=relevant_language)).filter(Q(partofspeech=None)).order_by("-t_occurred")[0]
        except:
            return HttpResponseRedirect(reverse('home'))
        # Unbound form
        form = NGramSetupForm(instance=ngram,languages=languages,partofspeeches=partofspeeches)
    
    # Render Template Home
    return render_to_response('rating/ngram_setup.html', {
        "ngram":ngram,
        "form":form,
    }, context_instance=RequestContext(request))