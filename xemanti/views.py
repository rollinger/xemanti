# -*- coding: utf-8 -*-
# Generic Import Statement
from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext as _
from django.utils.html import strip_tags, escape
from django.http import HttpResponse
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

# Custom Import Statement
from forms import TextAnalyticInputForm, RateAssociationForm
from ngramengine.models import NGrams
from ngramengine.tasks import add_text_to_system
#from ngram_engine_de.models import Sentences, Association
#from usr_profile.models import Profile
#from ngram_engine_de.tasks import *#add_sentences_to_stack, rate_sentences, calculate_devianz

#
# Home Page View for text submission and main navigation view
#
def home_view(request):
    # Form submitted:
    if request.method == 'POST': 
        form = TextAnalyticInputForm(request.POST) # A form bound     to the POST data
        if form.is_valid(): # All validation rules pass
            text_to_analyze = form.cleaned_data['textinput']
            # Add NGrams to the system
            add_text_to_system.delay(text_to_analyze)
            # TODO: Initiate Report generation
            # Redirect to Rating Process after POST
            #url = reverse('rating')
            #response = HttpResponseRedirect(url)
            # Set Cookie for rating
            # TODO: Pass more options (Expiration, etc...) see: http://www.djangobook.com/en/2.0/chapter14.html
            #response.set_cookie("rating_gauge",0)
            return HttpResponseRedirect( reverse( 'home' ) )
    # Form not submitted:
    else:
        form = TextAnalyticInputForm() # An unbound form
    # Render Template Home
    return render_to_response('xemanti/home.html', {
        "form":form
    }, context_instance=RequestContext(request))



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
            #new_profile = Profile(user=new_user, balance=settings.REGISTRATION_XEMANTI_PRESENT)
            #new_profile.save()
            return HttpResponseRedirect(reverse('login_view'))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })