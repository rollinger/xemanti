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

# Custom Import Statement
from forms import *
from ngramengine.models import *

#
# Setup View for Admins introducing 
#
def ngram_setup_view(request,model=None):
    # Get NGram
    ngram = NGrams.objects.get()
    print ngram
    
    # Form submitted:
    if request.method == 'POST': 
        form = NGramSetupForm(request.POST)
        if form.is_valid():
	    # DO STUFF...
 	    return HttpResponseRedirect(reverse('rating'))
    # Form not submitted:
    else:
        form = NGramSetupForm()
    
    # Render Template Home
    return render_to_response('rating/ngram_setup.html', {
        "form":form
    }, context_instance=RequestContext(request))