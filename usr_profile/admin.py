# -*- coding: utf-8 -*-
from django.contrib import admin
from usr_profile.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile, ProfileAdmin)