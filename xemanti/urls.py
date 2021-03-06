# -*- coding: utf-8 -*-
#
# URL ROOT CONFIG
#
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.contrib.sitemaps import GenericSitemap
from zinnia.models import Entry
from ngramengine.models import NGrams
from views import *

# Admin Autodiscover
from django.contrib import admin
admin.autodiscover()

# Dajaxice Autodiscover
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('xemanti.views',
    # General Views
    url(r'^$', StartView.as_view(), name='home'),
    url(r'^faq/', FAQView.as_view(), name='faq'),
    url(r'^impressum/',  ImpressumView.as_view(), name='impressum'),
    #
    # Registration Views
    #
    url(r'^accounts/login/', LoginView.as_view(), name='login_view'),
    url(r'^accounts/logout/', LogoutView.as_view(), name='logout_view'),
    url(r'^accounts/registration/',RegistrationView.as_view(), name='registration_view'),
    #
    # Application URL Includes
    #
    url(r'^engine/', include('ngramengine.urls')),
    url(r'^rating/', include('rating.urls')),
    url(r'^reporting/', include('reporting.urls')),
    
    #
    # Zinnia Weblog URLs
    #
    url(r'^blog/', include('zinnia.urls'), name='blog'),
    url(r'^comments/', include('django.contrib.comments.urls')),

    #
    # Admin URLs
    #
    # Mainenance Action via Celery
    #url(r'^maintenance/', 'XemantiCom.views.maintenance', name='maintenance'),
    
    # Admin Interface (Backend)
    url(r'^admin/', include(admin.site.urls)),
    # Admin Documentation 
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Dajaxice
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    # Robots.txt
    url(r'^robots.txt$', TemplateView.as_view(template_name='xemanti/robots.txt')),

)

# Add Staticfiles-Urlpattern to urlpattern
urlpatterns += staticfiles_urlpatterns()

# Sitemap.xml addition
blog_info_dict = {
    'queryset': Entry.published.all(),
    'date_field': 'start_publication',
}
ngram_info_dict = {
    'queryset': NGrams.objects.filter(active=True),
    'date_field': 'updated',
}
sitemaps = {
    'blog': GenericSitemap(blog_info_dict, priority=0.4, changefreq='daily'),
    'ngram': GenericSitemap(ngram_info_dict, priority=0.6, changefreq='hourly'),
}

urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)
