# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models import F

from ngramengine.models import *


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
    list_display = ('token', 't_occurred', 't_rated', "dirty","qualified","wiktionary_url")
    list_filter = ['dirty', "qualified", IntervalListFilter,'partofspeech', 'language']
    search_fields = ('token', )
    ordering = ('-t_occurred',)
    inlines = [PartofSpeechesInline,LanguagesInline,SynonymsInline,AntonymsInline,SuperCategoryInline,SubCategoryInline]
    
    actions = ['set_meaningless','set_qualified', 'make_uppercase','make_lowercase','unset_substantiv','set_substantiv',\
               'unset_verb','set_verb','set_buchstabe','unset_buchstabe']

    def set_meaningless(self, request, queryset):
        queryset.update(semantic_meaningless=True)
    set_meaningless.short_description = "Mark selected ngrams as semantically meaningless"
    def set_qualified(self, request, queryset):
        queryset.update(qualified=True)
    set_qualified.short_description = "Mark selected ngrams as qualified"
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
            ngram.partofspeech.add(PartOfSpeech.objects.get(type="Buchstabe"))
            ngram.save()
    unset_buchstabe.short_description = "Set Part of Speech `Buchstabe´"
    def set_buchstabe(self, request, queryset):
        for ngram in queryset.all():
            ngram.partofspeech.remove(PartOfSpeech.objects.get(type="Buchstabe"))
            ngram.save()
    set_buchstabe.short_description = "Unset Part of Speech `Buchstabe´"
    
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
            # Calls the method is_meaningful of each CoOccurrence
            # exclude yields better performance, due less deletion from the queryset
            return queryset.exclude(is_meaningful=False)
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
    list_display = ('type', 'semantic_meaningless', 'ngram_count')
    exclude = ['ngrams',]
admin.site.register(PartOfSpeech, PartOfSpeechAdmin)

class LanguagesAdmin(admin.ModelAdmin):
    list_display = ('language', 'ngram_count')
    exclude = ['ngrams',]
admin.site.register(Languages, LanguagesAdmin)

class AssociationsAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 't_associated', 'power')
admin.site.register(Associations, AssociationsAdmin)

class InputStackAdmin(admin.ModelAdmin):
    pass
admin.site.register(InputStack, InputStackAdmin)
