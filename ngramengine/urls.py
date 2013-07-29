# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('ngramengine.views',
    #
    # Anonymous User URLs
    #
    
    # Home View
    url(r'^partofspeech/', 'rating_partofspeech_view', name='rating_partofspeech'),
    # Admins Bulk upload View
    url(r'^admin/bulk/ngram/', 'bulk_ngram_upload_view', name='bulk_ngram_upload'),
)