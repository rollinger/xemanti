from django.utils import simplejson
import random
import itertools
import urllib, urllib2
import requests
from dajaxice.decorators import dajaxice_register
from ngramengine.models import *
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



@dajaxice_register
def verify_captcha(request, register, form):
    results = requests.get("http://www.google.com/recaptcha/api/verify",
              params={'privatekey': '6LeZp-kSAAAAAELZ7izZXA78Zh6J7rBn6Pje0324',
                      'remoteip': get_client_ip(request),
                      'challenge': form['recaptcha_challenge_field'],
                      'response': form['recaptcha_response_field'],})
    # Check response code and return to callback
    print "Verify Captcha"
    print results.text.split('\n')[0]
    print results.text.split('\n')[1]
    if results.text.split('\n')[0] == 'true':
        # Set session var to false because captcha was solved
        request.session['captcha_active'] = 'false'
        return simplejson.dumps({'status':'true','register':register})
    else:
        return simplejson.dumps({'status':'false','register':register})