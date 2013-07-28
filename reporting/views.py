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
from forms import QueryNGramForm, TextAnalyticInputForm
from ngramengine.tokenizer import Tokenizer
from ngramengine.models import *
from ngramengine.tasks import add_text_to_system

#
# Query an Ngram for Inspection
#
def inspect_query_view(request, ngram_id=None):
    if request.method == 'POST':
        form = QueryNGramForm(request.POST)
        if form.is_valid():
            if len( form.cleaned_data['ngram'] ) >= 100:# reload if the input exceeds 100 Chars
                    return HttpResponseRedirect(reverse('inspect_query'))
            ngram = NGrams.inject(token=form.cleaned_data['ngram'])
            return HttpResponseRedirect(reverse('inspect_query', kwargs={'ngram_id': ngram.pk}))
    else:
        form = QueryNGramForm()
        if ngram_id:
            ngram = NGrams.objects.get(pk=ngram_id)
            if request.user.is_authenticated():
                request.user.profile.payment(1)
            else:
                if request.session.has_key('anonymous_rating'):
                    if int(request.session['anonymous_rating']['state']) >= int(request.session['anonymous_rating']['max']):
                        del request.session['anonymous_rating']
                else:
                    success_redirect = HttpResponseRedirect(reverse('inspect_query', kwargs={'ngram_id': ngram.pk}))
                    request.session['anonymous_rating'] = {'state':0,'max':1,'target':'rate_assoc','success_redirect':success_redirect}
                    return HttpResponseRedirect( reverse( 'rate_assoc' ) )
        else:
            ngram = None
    
    # Render Template ngram_query
    return render_to_response('reporting/inspect_show.html', {
        "ngram":ngram,
        "form":form,
    }, context_instance=RequestContext(request))
    
    
    
#
# Add Text to System and initiate Reporting process
#
def initiate_report_view(request):
    # Form submitted:
    if request.method == 'POST': 
        form = TextAnalyticInputForm(request.POST) # A form bound     to the POST data
        if form.is_valid(): # All validation rules pass
            text_to_analyze = form.cleaned_data['textinput']
            # Add NGrams to the system
            # TODO: Strip text anonymous = 500 chars; authenticated = 2500 chars; (???) 
            add_text_to_system.delay(text_to_analyze)
            #NGrams.add_text_to_system(text_to_analyze)
            # TODO: Initiate Report generation
            if request.user.is_authenticated():
                return HttpResponseRedirect( reverse( 'rate_assoc' ) )
            else:
                # Set Cookie for rating
                response = HttpResponseRedirect( reverse( 'rate_assoc' ) )
                response.set_cookie("rating_gauge",0)
                # Redirect to rating 
                return response
            # TODO: Pass more options (Expiration, etc...) see: http://www.djangobook.com/en/2.0/chapter14.html
            #
            
    # Form not submitted:
    else:
        form = TextAnalyticInputForm() # An unbound form
    # Render Template Home
    return render_to_response('reporting/initiate_report.html', {
        "form":form
    }, context_instance=RequestContext(request))