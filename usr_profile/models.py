# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from fields import MoneyField
from ngramengine.models import NGrams
from django.utils import timezone



class Profile(models.Model):
    """
    Xeti Account for a User
    """
    user            = models.OneToOneField(User)
    # Xeti Accounting
    balance         = MoneyField(default=0.00)
    total_earnings  = MoneyField(default=0.00)
    total_spendings = MoneyField(default=0.00)
    
    def has_booked(self, ngram):
        booked = self.ngram_bookings.filter(ngram=ngram)
        if booked:
            return booked[0].is_booked()
        return False
    
    def book(self, ngram):
        booking, created = NGramBooking.objects.get_or_create(ngram=ngram, profile=self)
        if not created:
            booking.book()
        return booking.save()
        
    def income(self, value):
        self.balance = self.balance + float(value)
        self.total_earnings = self.total_earnings + float(value)
        self.save()
        return True
        
    def payment(self, value):
        # User can pay
        if self.balance >= value:
            self.balance = self.balance - float(value)
            self.total_spendings = self.total_spendings + float(value)
            self.save()
            return True
        else:
            return False
    
    def __unicode__(self):
        return str(self.user)



class NGramBooking(models.Model):
    """
    NGrams the user_profile currently has booked
    """
    BOOKING_PERIOD_HOURS = 24
    profile         = models.ForeignKey(Profile, related_name="ngram_bookings")
    ngram           = models.ForeignKey(NGrams)
    # Model Timestamp
    created         = models.DateTimeField(auto_now_add=True)
    booked          = models.DateTimeField(auto_now=True)
    expires         = models.DateTimeField(default=datetime.now()+timedelta(hours=BOOKING_PERIOD_HOURS))
    
    def is_booked(self):
        """
        Returns True if the NGram is still booked by the user
        """
        if self.expires > timezone.now():
            return True
        return False
    
    def book(self):
        """
        Books the instance for a user for a period of BOOKING_PERIOD_HOURS into the future 
        """
        self.booked = timezone.now()
        self.expires = timezone.now()+timedelta(hours=self.BOOKING_PERIOD_HOURS)
        self.save()
        
    def __unicode__(self):
        return u"%s %s"%(self.ngram, self.profile)
    
    class Meta:
        verbose_name = 'NGram Booking'
        verbose_name_plural = 'NGrams Bookings'
        unique_together = ('ngram','profile')
        ordering = ['ngram',]