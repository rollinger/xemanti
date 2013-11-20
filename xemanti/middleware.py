# -*- coding: utf-8 -*-
# Generic Import Statement
from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
import random

# Custom Import Statement
from django.conf import settings

BotNames=['Googlebot','Slurp','Twiceler','msnbot','KaloogaBot','YodaoBot','"Baiduspider','googlebot','Speedy Spider','DotBot']
param_name='deny_crawlers'



class CrawlerBlockerMiddleware(object):
    """
    Deny access for requests without user agent
    Deny access for crawler for specific views, where param_name in view_kwargs
    # See https://djangosnippets.org/snippets/1865/
    """
    def process_request(self, request):
        user_agent=request.META.get('HTTP_USER_AGENT',None)

        if not user_agent:
            return HttpResponseForbidden('Request without username are not supported!')
        request.is_crawler=False

        for botname in BotNames:
            # TODO: Better whitelist ip-ranges from Crawlers - user-agent can be set to anything by spammers
            if botname in user_agent:
                request.is_crawler=True


    def process_view(self, request, view_func, view_args, view_kwargs):
        if param_name in view_kwargs:
            if view_kwargs[param_name]:
                del view_kwargs[param_name]
                if request.is_crawler:
                    return HttpResponseForbidden('Adress removed from crawling. Check robots.txt')



class AnonymousRatingMiddleware(object):
    """
    Handles Rating for anonymous user
    """
    def process_request(self, request):
        if not request.is_crawler: # Only if not crawler
        #any(x in request.META['HTTP_USER_AGENT'] for x in BotNames): #Allow robots to access the page and sitemap
            if request.session.has_key('anonymous_rating'):
                anonymous_rating = request.session.get('anonymous_rating')
                if request.path != reverse( anonymous_rating['target'] ): 
                    if int( anonymous_rating['state'] ) < int( anonymous_rating['max'] ):
                        return HttpResponseRedirect(reverse( anonymous_rating['target'] ) )
                else:
                    if int( anonymous_rating['state'] ) >= int( anonymous_rating['max'] ):
                        return anonymous_rating['success_redirect']



class AnonymousSpamProtectionMiddleware(object):
    """
    Handles Captchas for anonymous users
    Sets variable open_captcha to True so that the modal dialog in the base template is triggered.
    """
    def process_request(self, request):
        # Reload Protection: If session has key captcha_active==true show dialog
        # else remove key and do not show dialog

        # General Routine: Probability check, if captcha should be presented to user.
        request.open_captcha_dialog = 'false'
        if not request.user.is_authenticated():
            if request.session.has_key('captcha_active'):
                #print request.session.get('captcha_active')
                if request.session.get('captcha_active') == 'true':
                    request.open_captcha_dialog = 'true'
                    request.session['captcha_active'] = 'true'
            if random.random() <= settings.SPAM_PROTECTED_PROBABILITY:
                if any(x in request.path for x in settings.SPAM_PROTECTED_URLS):
                    request.open_captcha_dialog = 'true'
                    request.session['captcha_active'] = 'true'
