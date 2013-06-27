# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('ngramengine.views',
    #
    # Anonymous User URLs
    #
    
    # Home View
    url(r'^partofspeech/', 'rating_partofspeech_view', name='rating_partofspeech')
)