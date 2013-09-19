# -*- coding: utf-8 -*-
from django.contrib import admin
from usr_profile.models import Profile, NGramBooking

class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile, ProfileAdmin)

class NGramBookingAdmin(admin.ModelAdmin):
    pass
admin.site.register(NGramBooking, NGramBookingAdmin)