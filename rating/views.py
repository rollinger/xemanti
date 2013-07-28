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
from forms import RateAssociationForm
from ngramengine.tokenizer import Tokenizer
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
                if len( form.cleaned_data['rating'] ) >= 100:
                    # reload if the input exceeds 100 Chars
                    return HttpResponseRedirect(reverse('rate_assoc'))
                # get source and target ngram
                source = NGrams.inject(token=form.cleaned_data['target'])
                target = NGrams.inject(token=form.cleaned_data['rating'])
                # Save Association
                Associations.inject(source, target)
                # Multiple Associations if multiple_tokens 
                multiple_tokens = Tokenizer.linear_token_list(form.cleaned_data['rating'])
                if len(multiple_tokens) > 1:
                    for t in multiple_tokens:
                        atomic_target = NGrams.inject(token=t)
                        Associations.inject(source, atomic_target)
                if request.user.is_authenticated():
                    request.user.profile.income(1.11)
                    return HttpResponseRedirect(reverse('rate_assoc'))
                else:
                    # Increment anonymous_rating session
                    request.session['anonymous_rating']['state'] = int( request.session['anonymous_rating']['state'] ) + 1
                    request.session.modified = True
                    return HttpResponseRedirect( reverse( 'rate_assoc' ) )
            else:
                return HttpResponseRedirect(reverse('rate_assoc'))
    # Form not submitted:
    else:
        # Get random qualified NGram to rate
        #ngram = NGrams.objects.filter(qualified=True).order_by("?")[0]
        ngram = NGrams.objects.order_by("?")[0]
        # Get Suggestions for rating (json)
        rating_suggestions = simplejson.dumps( sorted( list(  itertools.chain(*ngram.get_all_outbound_tokens())  ) ) )
        # Unbound form
        form = RateAssociationForm(ngram=ngram)
        form.fields['target'] = forms.CharField(initial=ngram.token, widget=forms.widgets.HiddenInput())
    
    # Render Template Home
    return render_to_response('rating/ngram_rating.html', {
        "form":form,
        "ngram":ngram,
        "rating_suggestions":rating_suggestions,
    }, context_instance=RequestContext(request))



#
# Sorting View for an NGram
#
def sort_ngram_view(request, ngram):
    
    # Get random qualified NGram to rate
    ngram = NGrams.objects.get(token=ngram)
    
    # Get Suggestions for rating (json)
    #sorting_tokens = simplejson.dumps( sorted( list(  itertools.chain(*ngram.get_all_outbound_tokens())  ) ) )
    #sorting_tokens = sorted( list(  itertools.chain(*ngram.get_all_outbound_tokens())  ) )
        
    # Render Template Home
    return render_to_response('rating/ngram_sorting.html', {
        "ngram":ngram,
        #"sorting_tokens":sorting_tokens,
    }, context_instance=RequestContext(request))