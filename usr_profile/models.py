# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from fields import MoneyField

class Profile(models.Model):
    user            = models.OneToOneField(User)
    # Xeti Accounting
    balance         = MoneyField(default=0.00)
    total_earnings  = MoneyField(default=0.00)
    total_spendings = MoneyField(default=0.00)
    
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
