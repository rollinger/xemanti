# -*- coding: utf-8 -*-
# Generic Import Statement
from django.contrib import auth
from django import forms
from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext as _
from django.utils.html import strip_tags, escape
from django.http import HttpResponse
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.views.generic import View, TemplateView, RedirectView, FormView

# Custom Import Statement
from forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from ngramengine.models import NGrams
from ngramengine.tasks import add_text_to_system
from usr_profile.models import Profile
#from ngram_engine_de.models import Sentences, Association

#from ngram_engine_de.tasks import *#add_sentences_to_stack, rate_sentences, calculate_devianz



class StartView(RedirectView):
    """
    Start View Redirect
    """
    def get_redirect_url(self, *args, **kwargs):
        return reverse('inspect_query')



class FAQView(TemplateView):
    """
     Frequently Asked Question View
    """
    template_name = 'xemanti/faq.html'



class ImpressumView(TemplateView):
    """
    Impressum View
    """
    template_name = 'xemanti/impressum.html'



class LoginView(View):
    """
    Handles User Login
    """
    def get(self, request, *args, **kwargs):
        """
        Shows Flash Message and renders login screen
        """
        messages.add_message(request, 
                             messages.INFO,
                             _('Fill in your Credentials and log into Xemanti!'),
                             fail_silently=True)
        return render(request, "registration/login.html", {})
    
    def post(self, request, *args, **kwargs):
        """
        Handles Login Submission, Messages and Redirect
        """
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _('Welcome to Xemanti!'),
                                 fail_silently=True)
            # Redirect to a success page.
            return HttpResponseRedirect("/")
        else:
            # Error logging in 
            messages.add_message(request, messages.ERROR,
                                 _('Something went wrong! Username or Password did not validate.'),
                                 fail_silently=True)
            return HttpResponseRedirect("login_view")
    
    
    
class LogoutView(View):
    """
    Handles User Login
    """
    def get(self, request, *args, **kwargs):
        """
        Logs out, shows Flash Message and renders redirect
        """
        auth.logout(request)
        messages.add_message(request,
                             messages.SUCCESS,
                             _('See you soon on Xemanti!'),
                             fail_silently=True)
        return HttpResponseRedirect(reverse('home'))



class RegistrationView(View):
    """
    Handles User Registration
    """
    template_name = 'registration/register.html'
    
    def get(self, request, *args, **kwargs):
        """
        Shows User Registration Form 
        """
        form = CustomUserCreationForm()
        messages.add_message(request,
                             messages.INFO,
                             _('Please fill in your registration form.'),
                             fail_silently=True)
        return render(request, self.template_name, {
                                                    'form': form,
                                                    })
    
    def post(self, request, *args, **kwargs):
        """
        Handles User Registration Form, Messages and Redirect
        """
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_profile = Profile(user=new_user, balance=settings.REGISTRATION_START_BALANCE)
            new_profile.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _('Thanks for registering on Xemanti!'),
                                 fail_silently=True)
            return HttpResponseRedirect(reverse('login_view'))
        else:
            messages.add_message(request,
                                 messages.SUCCESS,
                                 _('Something went wrong with your registration!'),
                                 fail_silently=True)
            return HttpResponseRedirect(reverse('registration_view'))