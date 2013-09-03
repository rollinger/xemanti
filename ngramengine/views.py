# -*- coding: utf-8 -*-
# Generic Import Statement
from django.contrib import auth
from django import forms
from django.utils.translation import ugettext as _
from django.utils.html import strip_tags, escape
from django.http import HttpResponse
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

# Custom Import Statement
from forms import RatePartOfSpeechForm, NGramBulkUploadForm
from ngramengine.models import *
from tokenizer import Tokenizer

def bulk_ngram_upload_view(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect( reverse( 'home' ) )
    
    # Form submitted:
    if request.method == 'POST':
        form = NGramBulkUploadForm(request.POST)
        if form.is_valid():
            sources = form.cleaned_data["source"]
            targets = form.cleaned_data["target"]
            type = form.cleaned_data["type"]
            # Implement Bulk upload
            
            if type == 'assoc':
                for source in Tokenizer.linear_token_list(sources):
                    for target in Tokenizer.linear_token_list(targets):
                            Associations.inject(NGrams.inject(source,times=0),NGrams.inject(target,times=0))
            elif type == 'notrelated':
                for source in Tokenizer.linear_token_list(sources):
                    for target in Tokenizer.linear_token_list(targets):
                        NotRelated.inject(NGrams.inject(source,times=0),NGrams.inject(target,times=0))
            elif type == 'synonym':
                for source in Tokenizer.linear_token_list(sources):
                    for target in Tokenizer.linear_token_list(targets):
                        Synonyms.inject(NGrams.inject(source,times=0),NGrams.inject(target,times=0))
            elif type == 'antonym':
                for source in Tokenizer.linear_token_list(sources):
                    for target in Tokenizer.linear_token_list(targets):
                        Antonyms.inject(NGrams.inject(source,times=0),NGrams.inject(target,times=0))
            elif type == 'super':
                for source in Tokenizer.linear_token_list(sources):
                    for target in Tokenizer.linear_token_list(targets):
                        SuperCategory.inject(NGrams.inject(source,times=0),NGrams.inject(target,times=0))
            elif type == 'sub':
                for source in Tokenizer.linear_token_list(sources):
                    for target in Tokenizer.linear_token_list(targets):
                        SubCategory.inject(NGrams.inject(source,times=0),NGrams.inject(target,times=0))
            elif type == 'lang':
                for source in Tokenizer.linear_token_list(sources):
                    for target in Tokenizer.linear_token_list(targets):
                        lang = Languages.objects.get(language=target)
                        ngram = NGrams.inject(source,times=0)
                        ngram.language.add(lang)
                        ngram.save()
            elif type == 'pos':
                for source in Tokenizer.linear_token_list(sources):
                    for target in Tokenizer.linear_token_list(targets):
                        lang = PartOfSpeech.objects.get(type=target)
                        ngram = NGrams.inject(source,times=0)
                        ngram.partofspeech.add(lang)
                        ngram.save()
            elif type == 'cooc':
                for source in Tokenizer.linear_token_list(sources):
                    for target in Tokenizer.linear_token_list(targets):
                        CoOccurrences.inject(NGrams.inject(source,times=0),NGrams.inject(target,times=0),position=1,times=0)
                    
            
            return HttpResponseRedirect( reverse( 'bulk_ngram_upload' ) )
    # Form not submitted:
    else:
        form = NGramBulkUploadForm() 
    # Render Template Home
    return render_to_response('ngramengine/rate.html', {
        "form":form
    }, context_instance=RequestContext(request))

def rating_partofspeech_view(request):
    
    ngram = NGrams.objects.filter(partofspeech=None).order_by('-t_occurred')[0]
    
    # Form submitted:
    if request.method == 'POST':
        form = RatePartOfSpeechForm(request.POST,instance=ngram)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse( 'rating_partofspeech' ) )
    # Form not submitted:
    else:
        #ngram = NGrams.objects.filter(partofspeech=None).order_by('-t_occurred')[:1].get()
        form = RatePartOfSpeechForm(instance=ngram) 
    # Render Template Home
    return render_to_response('ngramengine/rate.html', {
        "form":form
    }, context_instance=RequestContext(request))