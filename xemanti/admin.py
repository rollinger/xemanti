#-*- coding: utf-8 -*-
from rollyourown.seo.admin import register_seo_admin
from django.contrib import admin
from xemanti.seo import SiteMetadata

register_seo_admin(admin.site, SiteMetadata)