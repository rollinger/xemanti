# -*- coding: utf-8 -*-
#
# URL RATING CONFIG
#
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('rating.views',
    
    # Rating View
    url(r'^$', 'rate_assoc_view', name='rate_assoc'),
    url(r'^(?P<ngram>[\w\ -_]+)/$', 'rate_assoc_view', name='rate_assoc'),
    url(r'^sort/(?P<ngram>[\w\ -_]+)/$', 'sort_ngram_view', name='sort_ngram'),
    url(r'^eval/sd/(?P<ngram>[\w\ -_]+)/$', 'eval_sem_diff_view', name='eval_sem_diff'),
    
    # DEPRECATED: NGram Setup Rating view for Admin
    #url(r'^ngramsetup/', 'ngram_setup_view', name='ngram_setup'),
)
