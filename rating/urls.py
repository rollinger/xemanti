# -*- coding: utf-8 -*-
#
# URL RATING CONFIG
#
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('rating.views',
    
    # Rating View
    #url(r'^$', 'rating_view', name='rating'),
    # NGram Setup Rating view for Admin
    url(r'^ngramsetup/$', 'ngram_setup_view', name='ngram_setup'),
)
