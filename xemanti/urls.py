# -*- coding: utf-8 -*-
#
# URL ROOT CONFIG
#
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('xemanti.views',
    #
    # Anonymous User URLs
    #
    
    # Home View
    url(r'^$', 'home_view', name='home'),
    # Frequently Asked Questions
    url(r'^faq/', 'faq_view', name='faq'),
    # Impressum
    url(r'^impressum/', 'impressum_view', name='impressum'),
    url(r'^accounts/login/', login, name='login_view'),
    url(r'^accounts/logout/', 'logout_view', name='logout_view'),
    url(r'^accounts/registration/','registration_view', name='registration_view'),
    
    #
    # Application URL Includes
    #
    # TODO: $-sign might be wrong
    url(r'^de/', include('ngramengine.urls')),
    url(r'^rating/', include('rating.urls')),
    #url(r'^reporting/', include('reporting.urls')),
    
    #
    # Admin URLs
    #
    # Mainenance Action via Celery
    #url(r'^maintenance/', 'XemantiCom.views.maintenance', name='maintenance'),
    # Admin Interface (Backend)
    url(r'^admin/', include(admin.site.urls)),
    # Admin Documentation 
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# Add Staticfiles-Urlpattern to urlpattern
urlpatterns += staticfiles_urlpatterns()
