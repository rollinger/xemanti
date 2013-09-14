# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from django.db import IntegrityError

from ngramengine.models import *

from merge import merge_model_objects



class PartofSpeechesInline(admin.TabularInline):
    model = PartOfSpeech.ngrams.through
    raw_id_fields = ('ngrams',)
    extra = 0
class LanguagesInline(admin.TabularInline):
    model = Languages.ngrams.through
    raw_id_fields = ('ngrams',)
    extra = 0
class SynonymsInline(admin.TabularInline):
    model = Synonyms
    fk_name = 'source'
    raw_id_fields = ('source','target',)
    extra = 0
class AntonymsInline(admin.TabularInline):
    model = Antonyms
    fk_name = 'source'
    raw_id_fields = ('source','target',)
    extra = 0
class SuperCategoryInline(admin.TabularInline):
    model = SuperCategory
    fk_name = 'source'
    raw_id_fields = ('source','target',)
    extra = 0
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    fk_name = 'source'
    raw_id_fields = ('source','target',)
    extra = 0
class AssociationInline(admin.TabularInline):
    model = Associations
    fk_name = 'source'
    raw_id_fields = ('source','target',)
    extra = 0
class NotRelatedInline(admin.TabularInline):
    model = NotRelated
    fk_name = 'source'
    raw_id_fields = ('source','target',)
    extra = 0
class SemanticDifferentialInline(admin.TabularInline):
    model = SemanticDifferential#.ngrams.through
    #raw_id_fields = ('ngrams',)
    extra = 0
class IntervalListFilter(admin.SimpleListFilter):
    title = _('Interval Occurrence Filter')
    parameter_name = 'intervall_occurrence'
    def lookups(self, request, model_admin):
        return (
            (1, _('1')),
            (2, _('<10')),
            (3, _('<100')),
            (4, _('<1000')),
            )
    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(t_occurred=1)
        elif self.value() == "2":
            return queryset.filter(t_occurred__lte=10,t_occurred__gte=2)
        elif self.value() == "3":
            return queryset.filter(t_occurred__lte=100,t_occurred__gte=11)
        elif self.value() == "4":
            return queryset.filter(t_occurred__lte=1000,t_occurred__gte=101)
        else:
            return queryset
class NGramsAdmin(admin.ModelAdmin):
    list_display = ('token', 't_occurred', 't_rated','t_visited', "dirty","qualified",'created','updated',"wiktionary_url")
    list_filter = ['dirty', "qualified", IntervalListFilter,'partofspeech', 'language']
    search_fields = ('token', )
    ordering = ('-t_occurred',)
    inlines = [SemanticDifferentialInline,PartofSpeechesInline,LanguagesInline,AssociationInline,NotRelatedInline,SynonymsInline,AntonymsInline,\
               SuperCategoryInline,SubCategoryInline]
    
    fields = ('token', 'coocurrence_relevancy', ('t_occurred', 't_rated','t_visited'), ("dirty","qualified"),('wordstem', 'numerus','genus'), ('created','updated'))
    readonly_fields = ('created','updated')
    actions = ['merge','set_meaningless','set_qualified', 'make_qualified_german_substantive','make_qualified_german_verb',\
               'make_qualified_german_adjektiv','make_uppercase','make_lowercase','unset_substantiv','set_substantiv',\
               'unset_verb','set_verb','set_buchstabe','unset_buchstabe','set_zahl']
    
    def merge(self, request, queryset):
        queryset = list(queryset)
        merge_model_objects(primary_object=queryset[0],alias_objects=queryset[1:])
    merge.short_description = "Merge marked NGrams"
    def set_meaningless(self, request, queryset):
        queryset.update(coocurrence_relevancy=True)
    set_meaningless.short_description = "Mark selected ngrams as semantically meaningless"
    def set_qualified(self, request, queryset):
        queryset.update(qualified=True)
    set_qualified.short_description = "Mark selected ngrams as qualified"
    
    def make_qualified_german_substantive(self, request, queryset):
        lang = Languages.objects.get(language="Deutsch")
        pos = PartOfSpeech.objects.get(type="Substantiv")
        for ngram in queryset.all():
            #try:
            ngram.token = unicode( ngram.token.title() )
            ngram.language.add(lang)
            ngram.partofspeech.add(pos)
            ngram.qualified = True
            ngram.save()
            #except IntegrityError, e: # Delete if double (uppercasing)
                #ngram.delete()
    make_qualified_german_substantive.short_description = "Sets the ngram to german, substantive and qualified"
    
    def make_qualified_german_verb(self, request, queryset):
        lang = Languages.objects.get(language="Deutsch")
        pos = PartOfSpeech.objects.get(type="Verb")
        for ngram in queryset.all():
            ngram.token = ngram.token.lower()
            ngram.language.add(lang)
            ngram.partofspeech.add(pos)
            ngram.qualified = True
            ngram.save()
    make_qualified_german_verb.short_description = "Sets the ngram to german, verb and qualified"
    
    def make_qualified_german_adjektiv(self, request, queryset):
        lang = Languages.objects.get(language="Deutsch")
        pos = PartOfSpeech.objects.get(type="Adjektiv")
        for ngram in queryset.all():
            ngram.token = ngram.token.lower()
            ngram.language.add(lang)
            ngram.partofspeech.add(pos)
            ngram.qualified = True
            ngram.save()
    make_qualified_german_adjektiv.short_description = "Sets the ngram to german, adjektiv and qualified"
    
    def make_uppercase(self, request, queryset):
        for ngram in queryset.all():
            ngram.token = ngram.token.title()
            ngram.save()
    make_uppercase.short_description = "Convert selected ngrams to uppercase"
    def make_lowercase(self, request, queryset):
        for ngram in queryset.all():
            ngram.token = ngram.token.lower()
            ngram.save()
    make_lowercase.short_description = "Convert selected ngrams to lowercase"
    def set_substantiv(self, request, queryset):
        for ngram in queryset.all():
            ngram.partofspeech.add(PartOfSpeech.objects.get(type="Substantiv"))
            ngram.save()
    set_substantiv.short_description = "Set Part of Speech `Substantiv´"
    def unset_substantiv(self, request, queryset):
        for ngram in queryset.all():
            ngram.partofspeech.remove(PartOfSpeech.objects.get(type="Substantiv"))
            ngram.save()
    unset_substantiv.short_description = "Unset Part of Speech `Substantiv´"
    def set_verb(self, request, queryset):
        for ngram in queryset.all():
            ngram.partofspeech.add(PartOfSpeech.objects.get(type="Verb"))
            ngram.save()
    set_verb.short_description = "Set Part of Speech `Verb´"
    def unset_verb(self, request, queryset):
        for ngram in queryset.all():
            ngram.partofspeech.remove(PartOfSpeech.objects.get(type="Verb"))
            ngram.save()
    unset_verb.short_description = "Unset Part of Speech `Verb´"
    def unset_buchstabe(self, request, queryset):
        for ngram in queryset.all():
            ngram.partofspeech.remove(PartOfSpeech.objects.get(type="Buchstabe"))
            ngram.save()
    unset_buchstabe.short_description = "Set Part of Speech `Buchstabe´"
    def set_buchstabe(self, request, queryset):
        for ngram in queryset.all():
            ngram.partofspeech.add(PartOfSpeech.objects.get(type="Buchstabe"))
            ngram.save()
    set_buchstabe.short_description = "Unset Part of Speech `Buchstabe´"
    def set_zahl(self, request, queryset):
        lang = Languages.objects.get(language="International")
        for ngram in queryset.all():
            ngram.partofspeech.add(PartOfSpeech.objects.get(type="Zahlzeichen"))
            ngram.language.add(lang)
            ngram.qualified = True
            ngram.save()
    set_zahl.short_description = "Set Part of Speech `Zahlzeichen´, International and qualified"
    
    def wiktionary_url(self, obj):
        return '<a href="http://de.wiktionary.org/wiki/%s" target="_blank">%s</a>' % (obj.token, obj.token)
    wiktionary_url.allow_tags = True
    wiktionary_url.short_description = 'Wiktionary entry'
    
admin.site.register(NGrams, NGramsAdmin)



class MeaningfulCoOccurrenceListFilter(admin.SimpleListFilter):
    title = _('Meaningful Co-Occurrence')
    parameter_name = 'meaningful'
    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
            )
    def queryset(self, request, queryset):
        #filter = ['substantiv',"verb","adjektiv"]
        if self.value() == 'yes':
            # Calls the method is_relevant_for_cooccurrences of each CoOccurrence
            # exclude yields better performance, due less deletion from the queryset
            return queryset.exclude(coocurrence_relevancy=False)
        if self.value() == 'no':
            return queryset
class CoOccurrencesAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 't_cooccured', 'mean_position', 'power', "dirty")
    list_filter = ['dirty', MeaningfulCoOccurrenceListFilter,]
    search_fields = ('source__token', )
    ordering = ('-t_cooccured',)
    raw_id_fields = ('source','target',)
admin.site.register(CoOccurrences, CoOccurrencesAdmin)



class WordStemsAdmin(admin.ModelAdmin):
    pass
admin.site.register(WordStems, WordStemsAdmin)

class GenusAdmin(admin.ModelAdmin):
    pass
admin.site.register(Genus, GenusAdmin)

class NumerusAdmin(admin.ModelAdmin):
    pass
admin.site.register(Numerus, NumerusAdmin)

class PartOfSpeechAdmin(admin.ModelAdmin):
    list_display = ('type', 'coocurrence_relevancy', 'ngram_count')
    exclude = ['ngrams',]
    actions = ['set_relevant_for_coocurrences','set_not_relevant_for_coocurrences']

    def set_relevant_for_coocurrences(self, request, queryset):
        queryset.update(coocurrence_relevancy=True)
    set_relevant_for_coocurrences.short_description = "Mark selected ngrams as relevant for cooccurrences"
    def set_not_relevant_for_coocurrences(self, request, queryset):
        queryset.update(coocurrence_relevancy=False)
    set_not_relevant_for_coocurrences.short_description = "Mark selected ngrams as not relevant for cooccurrences"
    
admin.site.register(PartOfSpeech, PartOfSpeechAdmin)

class LanguagesAdmin(admin.ModelAdmin):
    list_display = ('language', 'ngram_count')
    exclude = ['ngrams',]
admin.site.register(Languages, LanguagesAdmin)

class AssociationsAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 't_associated', 'power')
    raw_id_fields = ('source','target',)
admin.site.register(Associations, AssociationsAdmin)

class NotRelatedAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 't_rated')
    raw_id_fields = ('source','target',)
admin.site.register(NotRelated, NotRelatedAdmin)

class SemanticDifferentialAdmin(admin.ModelAdmin):
    pass
admin.site.register(SemanticDifferential, SemanticDifferentialAdmin)
