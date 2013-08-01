# -*- coding: utf-8 -*-
from rollyourown import seo
from django.utils.translation import ugettext as _

class SiteMetadata(seo.Metadata):
    def default_title(self, **kwargs):
        return "Xemanti"
    default_title.short_description = "Standard title will be used"
    def default_description(self, **kwargs):
        return _("Xemanti - Sprachtools für deine Texte. Finde Assoziationen, Synonyme, und viel mehr für deine Wörter und Texte.")
    default_description.short_description = "Standard Description will be used"
    def default_keyword(self, **kwargs):
        return _("sprachtools,sprachtool,assoziation,text,texten,rhetorik,kommunikation,bedeutung,synonym,antonym,wörterbuch")
    default_keyword.short_description = "Standard Keywords will be used"
    
    title       = seo.Tag(head=True, max_length=68, populate_from=default_title)
    description = seo.MetaTag(max_length=155, populate_from=default_description)
    keywords    = seo.KeywordTag(populate_from=default_keyword)
    heading     = seo.Tag(name="h1")
    
    class Meta:
        seo_models = ('ngramengine.ngrams',)
        #seo_views = ('my_app', )
        backends = ("path", "modelinstance", "model", "view")