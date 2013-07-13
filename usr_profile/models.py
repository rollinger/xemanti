# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user            = models.OneToOneField(User)
    # Xeti Accounting
    balance         = models.IntegerField(default=0)
    total_earnings  = models.PositiveIntegerField(default=0)
    total_spendings = models.PositiveIntegerField(default=0)
    
    def income(self, value):
        self.balance = self.balance + int(value)
        self.total_earnings = self.total_earnings + int(value)
        self.save()
        
    def payment(self, value):
        self.balance = self.balance - int(value)
        self.total_spendings = self.total_spendings + int(value)
        self.save()
    
    def __unicode__(self):
        return str(self.user)
