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
from django.db.models import Q

# Custom Import Statement
from forms import NGramSetupForm
from ngramengine.models import *

#
# Setup View for Admins introducing 
#
def ngram_setup_view(request):
    
    
    # Form submitted:
    if request.method == 'POST': 
        # TODO: USE A normal form not a model
        form = NGramSetupForm(request.POST)
        if form.is_valid():
            ngram = form.save()
            # save m2m (lang & pos)
            ngram.language.add()
            ngram.partofspeech.add()
        return HttpResponseRedirect(reverse('ngram_setup'))
    # Form not submitted:
    else:
        # Get NGram and 
        ngram = NGrams.objects.filter(Q(language=None)|Q(partofspeech=None)).order_by("t_occurred")[0]
        languages = Languages.objects.all()#.order_by("ngram_count")
        partofspeeches = PartOfSpeech.objects.all()#.order_by("ngram_count")
        form = NGramSetupForm(instance=ngram,languages=languages,partofspeeches=partofspeeches)
    
    # Render Template Home
    return render_to_response('rating/ngram_setup.html', {
        "form":form
    }, context_instance=RequestContext(request))