# -*- coding: utf-8 -*-
#
# URL RATING CONFIG
#
from django.conf.urls.defaults import patterns, include, url
# Dajaxice Autodiscover
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

from views import *

urlpatterns = patterns('rating.views',
    #
    # Rating Views
    #
    url(r'^eval/semantic/(?P<ngram>[\w\ -_]+)/$', 'eval_sem_diff_view', name='eval_sem_diff'),
    url(r'^eval/sensory/(?P<ngram>[\w\ -_]+)/$', 'eval_sensory_dim_view', name='eval_sensory_dim'),
    url(r'^sort/(?P<ngram>[\w\ -_]+)/$', 'sort_ngram_view', name='sort_ngram'),
    url(r'^(?P<ngram>[\w\ -_]+)/(?P<repeated>[\w\ -_]+)/$', 'rate_assoc_view', name='rate_assoc'),
    url(r'^(?P<ngram>[\w\ -_]+)/$', 'rate_assoc_view', name='rate_assoc'),
    url(r'^$', 'rate_assoc_view', name='rate_assoc'),
    
    # DEPRECATED: NGram Setup Rating view for Admin
    #url(r'^ngramsetup/', 'ngram_setup_view', name='ngram_setup'),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)
