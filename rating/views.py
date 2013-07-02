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
# Rating View for user rating of various models
#
def rating_view(request,model=None):
    
    # Form submitted:
    if request.method == 'POST': 
        form = RatingForm(request.POST)
        if form.is_valid():
	    # DO STUFF...
 	    return HttpResponseRedirect(reverse('rating'))
    # Form not submitted:
    else:
        form = RatingForm()
    
    # Render Template Home
    return render_to_response('rating/rating.html', {
        "form":form
    }, context_instance=RequestContext(request))
