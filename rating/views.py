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
from django.contrib import messages
from django.views.generic import View, TemplateView, RedirectView, FormView
import itertools
from random import choice

# Custom Import Statement
from forms import RateAssociationForm, SemanticDifferentialForm, SensoryDimensionForm
from ngramengine.tokenizer import Tokenizer
from ngramengine.models import *



def rate_assoc_view(request, ngram=None, repeated=False):
    ngram_token = ngram
    # Form submitted:
    if request.method == 'POST':
        form = RateAssociationForm(request.POST)
        if 'skip' in request.POST:
            return HttpResponseRedirect(reverse('rate_assoc'))
        elif 'rate' in request.POST:
            if form.is_valid():
                # reload if the input exceeds 100 Chars
                if len( form.cleaned_data['rating'] ) >= 100:
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
                # Success Message
                messages.add_message(request, messages.SUCCESS, _('Thanks for rating!'), fail_silently=True)
                # Redirect
                if request.user.is_authenticated():
                    request.user.profile.income(1.11)
                    if repeated:
                        return HttpResponseRedirect(reverse('rate_assoc', args=(ngram_token, True)))
                    else:
                        return HttpResponseRedirect(reverse('rate_assoc'))
                else:
                    # Increment anonymous_rating session
                    if request.session.has_key('anonymous_rating'):
                        request.session['anonymous_rating']['state'] = int( request.session['anonymous_rating']['state'] ) + 1
                        request.session.modified = True
                    return HttpResponseRedirect( reverse( 'rate_assoc' ) )
            else:
                return HttpResponseRedirect(reverse('rate_assoc'))
    # Form not submitted:
    else:
        if ngram == None:
            excludes = PartOfSpeech.objects.filter(coocurrence_relevancy=False)
            ngram = choice( NGrams.objects.filter(qualified=True).exclude(partofspeech__in=excludes).order_by("-rating_index")[:500] )
        else:
            ngram = NGrams.objects.get(token=ngram_token)
        # Get Suggestions for rating (json)
        rating_suggestions = simplejson.dumps( sorted( list(  itertools.chain(*ngram.get_all_outbound_tokens())  ) ) )
        # Unbound form
        form = RateAssociationForm(ngram=ngram)
        form.fields['target'] = forms.CharField(initial=ngram.token, widget=forms.widgets.HiddenInput())
        
        # Information for redirected Users: 
        if request.session.has_key('anonymous_rating'):
            messages.add_message(request, messages.INFO, _('Rate one Word and you will get redirected!'), fail_silently=True)
            
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
    # Get Sorting List
    token_list = list( set( itertools.chain( *ngram.get_all_outbound_tokens() ) ) )
    # Render Template Home
    return render_to_response('rating/ngram_sorting.html', {
        "ngram":ngram,
        "token_list":simplejson.dumps( token_list ),
    }, context_instance=RequestContext(request))



def eval_sem_diff_view(request, ngram):
    """
    View for adding attitude (via semantic differential) to an NGram
    """
    if request.method == 'POST':
        ngram = NGrams.objects.get(token=ngram)
        form = SemanticDifferentialForm(request.POST, instance=ngram)
        if form.is_valid():
            semdiff, created = SemanticDifferential.objects.get_or_create(ngram=ngram)
            semdiff.record(form.cleaned_data['evaluation'],form.cleaned_data['potency'],form.cleaned_data['activity'])
            if request.user.is_authenticated():
                # Increment authenticated profile
                request.user.profile.income(3.33)
            else:
                # Increment anonymous_rating session
                if request.session.has_key('anonymous_rating'):
                    request.session['anonymous_rating']['state'] = int( request.session['anonymous_rating']['state'] ) + 1
                    request.session.modified = True
            return HttpResponseRedirect(reverse('inspect_query', kwargs={'ngram':ngram.token}))
    else:
        ngram = NGrams.objects.get(token=ngram)
        form = SemanticDifferentialForm(instance=ngram)
    # Render Template Home
    return render_to_response('rating/ngram_eval_sem_diff.html', {
        "ngram":ngram,
        "form":form,
    }, context_instance=RequestContext(request))



def eval_sensory_dim_view(request, ngram):
    """
    View for adding the sensory dimensions involved for an NGram
    """
    if request.method == 'POST':
        ngram = NGrams.objects.get(token=ngram)
        form = SensoryDimensionForm(request.POST, instance=ngram)
        if form.is_valid():
            sensdim, created = SensoryDimensions.objects.get_or_create(ngram=ngram)
            sensdim.record(form.cleaned_data['visual'],
                           form.cleaned_data['auditory'],
                           form.cleaned_data['cognition'],
                           form.cleaned_data['kinesthetic'],
                           form.cleaned_data['olfactory'],
                           form.cleaned_data['gustatory'],)
            if request.user.is_authenticated():
                # Increment authenticated profile
                request.user.profile.income(6.66)
            else:
                # Increment anonymous_rating session
                if request.session.has_key('anonymous_rating'):
                    request.session['anonymous_rating']['state'] = int( request.session['anonymous_rating']['state'] ) + 1
                    request.session.modified = True
            return HttpResponseRedirect(reverse('inspect_query', kwargs={'ngram':ngram.token}))
    else:
        ngram = NGrams.objects.get(token=ngram)
        form = SensoryDimensionForm(instance=ngram)
    # Render Template Home
    return render_to_response('rating/ngram_eval_sensory_dim.html', {
        "ngram":ngram,
        "form":form,
    }, context_instance=RequestContext(request))