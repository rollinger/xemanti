# -*- coding: utf-8 -*-
# Generic Import Statement
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Custom Import Statement
from django.conf import settings

class AnonymousRatingMiddleware(object):
    def process_request(self, request):
            if 'rating_gauge' in request.COOKIES:
                #print request.COOKIES['rating_gauge']
                if request.path != reverse('rate_assoc'):
                    if int( request.COOKIES['rating_gauge'] ) < settings.ANONYMOUS_RATING_CYCLES:
                        return HttpResponseRedirect(reverse('rate_assoc'))
                