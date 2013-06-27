# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ngramengine.models import *


class PartofSpeechesInline(admin.TabularInline):
    model = PartOfSpeech.ngrams.through
    extra = 0
class LanguagesInline(admin.TabularInline):
    model = Languages.ngrams.through
    extra = 0
class SynonymsInline(admin.TabularInline):
    model = Synonyms
    fk_name = 'source'
    extra = 0
class AntonymsInline(admin.TabularInline):
    model = Antonyms
    fk_name = 'source'
    extra = 0
class SuperCategoryInline(admin.TabularInline):
    model = SuperCategory
    fk_name = 'source'
    extra = 0
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    fk_name = 'source'
    extra = 0
class IntervalListFilter(admin.SimpleListFilter):
    title = _('Interval Occurrence Filter')
    parameter_name = 'intervall_occurrence'
    def lookups(self, request, model_admin):
        return (
            (1, _('1')),
            (2, _('<10')),
            (3, _('<100')),
            (3, _('<1000')),
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
    list_display = ('token', 't_occurred', "dirty")
    list_filter = ['dirty',]# IntervalListFilter,'partofspeech', 'language']
    search_fields = ('token', )
    ordering = ('-t_occurred',)
    inlines = [PartofSpeechesInline,LanguagesInline,SynonymsInline,AntonymsInline,SuperCategoryInline,SubCategoryInline]
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
    ordering = ('-t_cooccured',)
admin.site.register(CoOccurrences, CoOccurrencesAdmin)



class WordStemsAdmin(admin.ModelAdmin):
    pass
admin.site.register(WordStems, WordStemsAdmin)

class PartOfSpeechAdmin(admin.ModelAdmin):
    pass
admin.site.register(PartOfSpeech, PartOfSpeechAdmin)

class LanguagesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Languages, LanguagesAdmin)

class AssociationsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Associations, AssociationsAdmin)

class InputStackAdmin(admin.ModelAdmin):
    pass
admin.site.register(InputStack, InputStackAdmin)
