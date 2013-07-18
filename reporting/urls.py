# -*- coding: utf-8 -*-
#
# URL REPORTING CONFIG
#
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('reporting.views',
    
    # Probe Views
    url(r'^inspect/query/$', 'inspect_query_view', name='inspect_query'),
    url(r'^inspect/query/(?P<ngram_id>\d+)/$', 'inspect_query_view', name='inspect_query'),
    
    # Report Views
    url(r'^report/init/$', 'initiate_report_view', name='initiate_report'),
)
