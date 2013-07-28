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

# Admin Autodiscover
from django.contrib import admin
admin.autodiscover()

# Dajaxice Autodiscover
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

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
    url(r'^de/', include('ngramengine.urls')),
    url(r'^rate/', include('rating.urls')),
    url(r'^report/', include('reporting.urls')),
    
    #
    # Zinnia Weblog URLs
    #
    url(r'^weblog/', include('zinnia.urls')),
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
    url(r'^googlec40e2556575ffb52.html$', TemplateView.as_view(template_name='xemanti/googlec40e2556575ffb52.html')),

)

# Add Staticfiles-Urlpattern to urlpattern
urlpatterns += staticfiles_urlpatterns()

# Sitemap.xml addition
blog_info_dict = {
    'queryset': Entry.published.all(),
    'date_field': 'start_publication',
}
ngram_info_dict = {
    'queryset': NGrams.objects.all(),
    'date_field': 'updated',
}
sitemaps = {
    'blog': GenericSitemap(blog_info_dict, priority=0.6),
    'ngram': GenericSitemap(ngram_info_dict, priority=0.6),
}

urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)
