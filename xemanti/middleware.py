# -*- coding: utf-8 -*-
# Generic Import Statement
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Custom Import Statement
from django.conf import settings

class AnonymousRatingMiddleware(object):
    def process_request(self, request):
            if request.session.has_key('anonymous_rating'):
                anonymous_rating = request.session.get('anonymous_rating')
                if request.path != reverse( anonymous_rating['target'] ):
                    if int( anonymous_rating['state'] ) < int( anonymous_rating['max'] ):
                        return HttpResponseRedirect(reverse( anonymous_rating['target'] ) )
                else:
                    if int( anonymous_rating['state'] ) >= int( anonymous_rating['max'] ):
                        return anonymous_rating['success_redirect']