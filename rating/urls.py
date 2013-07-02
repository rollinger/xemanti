# -*- coding: utf-8 -*-
#
# URL RATING CONFIG
#
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('rating.views',
    
    # Rating View
    url(r'^$', 'rating_view', name='rating'),

)
