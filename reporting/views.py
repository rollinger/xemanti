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
from forms import QueryNGramForm
from ngramengine.tokenizer import Tokenizer
from ngramengine.models import *


#
# Query an Ngram for Inspection
#
def inspect_query_view(request, ngram_id=None):
    if request.method == 'POST':
        form = QueryNGramForm(request.POST)
        if form.is_valid():
            ngram = NGrams.inject(token=form.cleaned_data['ngram'])
            return HttpResponseRedirect(reverse('inspect_query', kwargs={'ngram_id': ngram.pk}))
    else:
        form = QueryNGramForm()
        if ngram_id:
            ngram = NGrams.objects.get(pk=ngram_id)
            if request.user.is_authenticated():
                request.user.profile.payment(1)
        else:
            ngram = None
    
    # Render Template ngram_query
    return render_to_response('reporting/inspect_show.html', {
        "ngram":ngram,
        "form":form,
    }, context_instance=RequestContext(request))
    
