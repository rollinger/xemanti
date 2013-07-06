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

# Custom Import Statement
from forms import NGramSetupForm
from ngramengine.models import *

#
# Setup View for Admins introducing 
#
def ngram_setup_view(request):

    # Form submitted:
    if request.method == 'POST':
        form = NGramSetupForm(request.POST)
        ngram = NGrams.objects.get(token=form.data['token'])
        if 'delete' in request.POST:
            # delete ngram
            ngram.delete()
        elif 'update' in request.POST:
            # update ngram
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
            ngram = NGrams.objects.filter(language=relevant_language).filter(Q(partofspeech=None)).order_by("t_occurred")[0]
        except:
            return HttpResponseRedirect(reverse('home'))
        # Unbound form
        form = NGramSetupForm(instance=ngram,languages=languages,partofspeeches=partofspeeches)
    
    # Render Template Home
    return render_to_response('rating/ngram_setup.html', {
        "ngram":ngram,
        "form":form,
    }, context_instance=RequestContext(request))