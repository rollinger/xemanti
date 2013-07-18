# -*- coding: utf-8 -*-
# Generic Import Statement
from django.contrib import auth
from django import forms
#from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext as _
from django.utils.html import strip_tags, escape
from django.http import HttpResponse
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

# Custom Import Statement
from forms import UserCreationForm
from ngramengine.models import NGrams
from ngramengine.tasks import add_text_to_system
from usr_profile.models import Profile
#from ngram_engine_de.models import Sentences, Association

#from ngram_engine_de.tasks import *#add_sentences_to_stack, rate_sentences, calculate_devianz

#
# Home Page View for text submission and main navigation view
#
def home_view(request):
    return HttpResponseRedirect(reverse('inspect_query'))
    # Render Template Home
    #return render_to_response('xemanti/home.html', {
    #}, context_instance=RequestContext(request))



def faq_view(request):
    return render_to_response('xemanti/faq.html', {}, context_instance=RequestContext(request))

def impressum_view(request):
    return render_to_response('xemanti/impressum.html', {}, context_instance=RequestContext(request))

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/")
    else:
        # Show an error page
        return HttpResponseRedirect("/")
    
def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    url = reverse('home')
    return HttpResponseRedirect(url)

def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_profile = Profile(user=new_user, balance=settings.REGISTRATION_START_BALANCE)
            new_profile.save()
            return HttpResponseRedirect(reverse('login_view'))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })
