# -*- coding: utf-8 -*-
from django.contrib import admin
from usr_profile.models import Profile, NGramBooking

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'total_earnings','total_spendings')
admin.site.register(Profile, ProfileAdmin)

class NGramBookingAdmin(admin.ModelAdmin):
    list_display = ('profile', 'ngram', 'created','booked','expires')
admin.site.register(NGramBooking, NGramBookingAdmin)