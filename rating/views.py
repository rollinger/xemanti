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
from forms import RateAssociationForm, SortAssociationForm, SemanticDifferentialForm, SensoryDimensionForm
from ngramengine.tokenizer import Tokenizer
from ngramengine.models import *



def get_random_ngram(ordering="-rating_index",size=500):
    """
    Selects a random ngram from a ordered set of ngrams
    """
    excludes = PartOfSpeech.objects.filter(coocurrence_relevancy=False)
    ngram = choice( NGrams.objects.filter(active=True).exclude(partofspeech__in=excludes).order_by(ordering)[:size])
    return ngram



def rate_assoc_view(request, ngram=None, repeated=False, success_url=None):
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
                    elif success_url:
                        return HttpResponseRedirect(reverse(success_url))
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
            ngram = get_random_ngram()
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
def sort_ngram_view(request, ngram, repeated=False, success_url=None):
    # Get random NGram to rate
    ngram = NGrams.objects.get(token=ngram)
    
    if request.method == 'POST':
        form = SortAssociationForm(request.POST)
        if form.is_valid():
            source = NGrams.objects.get(token=form.cleaned_data['source'])
             # Inject sorted target
            for type in form.cleaned_data['sorting'].split(","):
                if type == "not_related":
                    NotRelated.inject(ngram,source)
                elif type == "associated":
                    Associations.inject(ngram,source)
                elif type == "synonym":
                    Synonyms.inject(ngram,source)
                elif type == "antonym":
                    Antonyms.inject(ngram,source)
                elif type == "subcategory":
                    SubCategory.inject(ngram,source)
                elif type == "supercategory":
                    SuperCategory.inject(ngram,source)
                elif type == "example":
                    Examples.inject(ngram,source)
                elif type == "attribute":
                    Attributes.inject(ngram,source)
            # Success Message
            messages.add_message(request, messages.SUCCESS, _('Thanks for rating!'), fail_silently=True)
            # Process Payment
            if request.user.is_authenticated():
                # Increment authenticated profile
                request.user.profile.income(2.22)
            else:
                # Increment anonymous_rating session
                if request.session.has_key('anonymous_rating'):
                    request.session['anonymous_rating']['state'] = int( request.session['anonymous_rating']['state'] ) + 1
                    request.session.modified = True
            if repeated:
                return HttpResponseRedirect(reverse('sort_ngram', kwargs={'ngram':ngram.token, 'repeated':True}))
            elif success_url:
                return HttpResponseRedirect(reverse(success_url))
            else:
                return HttpResponseRedirect(reverse('sort_ngram', kwargs={'ngram':ngram.token}))
    else:
        # Get Sorting List
        # TODO: Throws error if no outbound_tokens are present
        outbound_tokens = ngram.get_all_outbound_tokens()
        if len(outbound_tokens) == 0:
            # Redirect if no tokens
            return HttpResponseRedirect(reverse('rate_assoc', kwargs={'ngram':ngram.token}))
        source = choice( list( set( itertools.chain( *outbound_tokens ) ) ) )
        # Setup Form
        form = SortAssociationForm(initial={'ngram': ngram.token,'source': source})
    
    # Render Template Home
    return render_to_response('rating/ngram_sorting.html', {
        "ngram":ngram,
        "source":source,
        "form":form,
        #"token_list":simplejson.dumps( token_list ),
    }, context_instance=RequestContext(request))



def eval_sem_diff_view(request, ngram, success_url=None):
    """
    View for adding attitude (via semantic differential) to an NGram
    """
    if request.method == 'POST':
        ngram = NGrams.objects.get(token=ngram)
        form = SemanticDifferentialForm(request.POST, instance=ngram)
        if form.is_valid():
            semdiff, created = SemanticDifferential.objects.get_or_create(ngram=ngram)
            semdiff.record(form.cleaned_data['evaluation'],form.cleaned_data['potency'],form.cleaned_data['activity'])
            # Success Message
            messages.add_message(request, messages.SUCCESS, _('Thanks for rating!'), fail_silently=True)
            if request.user.is_authenticated():
                # Increment authenticated profile
                request.user.profile.income(2.22)
            else:
                # Increment anonymous_rating session
                if request.session.has_key('anonymous_rating'):
                    request.session['anonymous_rating']['state'] = int( request.session['anonymous_rating']['state'] ) + 1
                    request.session.modified = True
            if success_url:
                return HttpResponseRedirect(reverse(success_url))
            else:
                return HttpResponseRedirect(reverse('inspect_query', kwargs={'ngram':ngram.token}))
    else:
        ngram = NGrams.objects.get(token=ngram)
        form = SemanticDifferentialForm(instance=ngram)
    # Render Template Home
    return render_to_response('rating/ngram_eval_sem_diff.html', {
        "ngram":ngram,
        "form":form,
    }, context_instance=RequestContext(request))



def eval_sensory_dim_view(request, ngram, success_url=None):
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
            # Success Message
            messages.add_message(request, messages.SUCCESS, _('Thanks for rating!'), fail_silently=True)
            if request.user.is_authenticated():
                # Increment authenticated profile
                request.user.profile.income(2.22)
            else:
                # Increment anonymous_rating session
                if request.session.has_key('anonymous_rating'):
                    request.session['anonymous_rating']['state'] = int( request.session['anonymous_rating']['state'] ) + 1
                    request.session.modified = True
            if success_url:
                return HttpResponseRedirect(reverse(success_url))
            else:
                return HttpResponseRedirect(reverse('inspect_query', kwargs={'ngram':ngram.token}))
    else:
        ngram = NGrams.objects.get(token=ngram)
        form = SensoryDimensionForm(instance=ngram)
    # Render Template Home
    return render_to_response('rating/ngram_eval_sensory_dim.html', {
        "ngram":ngram,
        "form":form,
    }, context_instance=RequestContext(request))



def random_rating_view(request, form_class=None, template_name=None, success_url='random_rating'):
    """
    View for random rating of an random ngram
    """
    # Get (weighted) random rating facillity
    rating_facillity = choice( ['rate_assoc','rate_assoc','rate_assoc','sort_ngram','sort_ngram','eval_sensory_dim','eval_sem_diff'] )
    # Get random NGram
    ngram = get_random_ngram()
    # Redirect to random rating facillity with this as success_url
    return HttpResponseRedirect(reverse(rating_facillity, kwargs={'ngram':ngram.token,'success_url':success_url}))