# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext as _
from itertools import chain
from django.core.urlresolvers import reverse

from datetime import datetime, timedelta

# Custom Imports
from tokenizer import Tokenizer



"""
Word Stems a stem for ngrams with the same stem
"""
class WordStems(models.Model):
    # The Stem of a set of Ngrams
    stem        = models.CharField(max_length=255,unique=True)
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.stem
    
    class Meta:
        verbose_name = 'Word Stem'
        verbose_name_plural = 'Word Stems'
        ordering = ['stem',]
        
"""
Genus of an ngram
"""
class Genus(models.Model):
    # The Genus of Ngrams
    type        = models.CharField(max_length=255,unique=True)
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.type
    
    class Meta:
        verbose_name = 'Genus'
        verbose_name_plural = 'Genus'
        ordering = ['type',]
"""
Numerus of an ngram
"""
class Numerus(models.Model):
    # The Stem of a set of Ngrams
    type        = models.CharField(max_length=255,unique=True)
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.type
    
    class Meta:
        verbose_name = 'Numerus'
        verbose_name_plural = 'Numerus'
        ordering = ['type',]
"""
Part Of Speech typify the ngram for their part of speech
"""
class PartOfSpeech(models.Model):
    # The Part of Speech of a set of Ngrams
    type                    = models.CharField(max_length=255,unique=True)
    # Part of Speech related to NGrams
    ngrams                  = models.ManyToManyField('NGrams', related_name="partofspeech", blank=True, null=True)
    # Boolean if the part or speech indicates meaninglessness of the ngram
    # Meaninglessness is better inferred from the part of speech than meaningfulness [old: semantic_meaningless
    coocurrence_relevancy   = models.NullBooleanField(_('Relevant for Co-Occurrences'),blank=True, null=True)
    # How many ngrams have this part of speech
    ngram_count             = models.PositiveIntegerField(default=0)
    
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.type
    
    def count_ngrams(self):
        self.ngram_count = self.ngrams.count()
        self.save()
        return self.ngram_count
    
    class Meta:
        verbose_name = 'Part Of Speech'
        verbose_name_plural = 'Part Of Speeches'
        ordering = ['type',]
"""
Languages of a ngram
"""
class Languages(models.Model):
    # The Stem of a set of Ngrams
    language        = models.CharField(max_length=255,unique=True)
    # Language of NGram 
    ngrams          = models.ManyToManyField('NGrams', related_name="language", blank=True, null=True)
    # How many ngrams have this language
    ngram_count     = models.PositiveIntegerField(default=0)
    
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.language
    
    def count_ngrams(self):
        self.ngram_count = self.ngrams.count()
        self.save()
        return self.ngram_count
    
    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        ordering = ['language',]
"""
Synonyms of an ngram
"""
class Synonyms(models.Model):
    source  = models.ForeignKey('NGrams', related_name="synonyms")
    target  = models.ForeignKey('NGrams', related_name="synonym_of")
    # How many times the synonym was rated
    t_rated = models.PositiveIntegerField(default=0)
    # Discriminatory Power
    power = models.FloatField(default=0.0)

    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    @classmethod
    def inject(cls,source_ngram,target_ngram,times=1):
        synonym, created = Synonyms.objects.get_or_create(source=source_ngram,target=target_ngram)
        if times > 0:
            synonym.t_rated = synonym.t_rated + times
        synonym.source.set_dirty()
        synonym.save()
        return synonym
    
    def compute_discriminatory_power(self):
        # Returns the mean position of the target ngram from the source ngram
        sum  = self.source.synonyms.all().aggregate(Sum('t_rated'))['t_rated__sum']
        if sum:
            try:
                self.power = self.t_rated/float(sum)
                self.save()
                return self.power
            except:
                return 0.0
    
    def __unicode__(self):
        return self.target#"%s <synonym> &s"%(self.source,self.target)
    
    class Meta:
        verbose_name = 'Synonym'
        verbose_name_plural = 'Synonyms'
"""
Antonyms of an ngram
"""
class Antonyms(models.Model):
    source  = models.ForeignKey('NGrams', related_name="antonyms")
    target  = models.ForeignKey('NGrams', related_name="antonym_of")
    # How many times the Antonym was rated
    t_rated = models.PositiveIntegerField(default=0)
    # Discriminatory Power
    power = models.FloatField(default=0.0)
    
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    @classmethod
    def inject(cls,source_ngram,target_ngram,times=1):
        antonym, created = Antonyms.objects.get_or_create(source=source_ngram,target=target_ngram)
        if times > 0:
            antonym.t_rated = antonym.t_rated + times
        antonym.source.set_dirty()
        antonym.save()
        return antonym
    
    def compute_discriminatory_power(self):
        # Returns the mean position of the target ngram from the source ngram
        sum  = self.source.antonyms.all().aggregate(Sum('t_rated'))['t_rated__sum']
        if sum:
            try:
                self.power = self.t_rated/float(sum)
                self.save()
                return self.power
            except:
                return 0.0
    
    def __unicode__(self):
        return self.target#"%s <antonym> &s"%(self.source,self.target)
    
    class Meta:
        verbose_name = 'Antonym'
        verbose_name_plural = 'Antonyms'
"""
SuperCategory of an ngram
"""
class SuperCategory(models.Model):
    source  = models.ForeignKey('NGrams', related_name="supercategories")
    target  = models.ForeignKey('NGrams', related_name="supercategory_of")
    # How many times the Super Category was rated
    t_rated = models.PositiveIntegerField(default=0)
    # Discriminatory Power
    power = models.FloatField(default=0.0)
    
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    @classmethod
    def inject(cls,source_ngram,target_ngram,times=1):
        super, created = SuperCategory.objects.get_or_create(source=source_ngram,target=target_ngram)
        if times > 0:
            super.t_rated = super.t_rated + times
        super.source.set_dirty()
        super.save()
        return super
    
    def compute_discriminatory_power(self):
        # Returns the mean position of the target ngram from the source ngram
        sum  = self.source.supercategories.all().aggregate(Sum('t_rated'))['t_rated__sum']
        if sum:
            try:
                self.power = self.t_rated/float(sum)
                self.save()
                return self.power
            except:
                return 0.0
    
    def __unicode__(self):
        return self.target#"%s <super> &s"%(self.source,self.target)
    
    class Meta:
        verbose_name = 'Super Category'
        verbose_name_plural = 'Super Categories'
"""
SubCategory of an ngram
"""
class SubCategory(models.Model):
    source  = models.ForeignKey('NGrams', related_name="subcategories")
    target  = models.ForeignKey('NGrams', related_name="subcategory_of")
    # How many times the Sub Category was rated
    t_rated = models.PositiveIntegerField(default=0)
    # Discriminatory Power
    power = models.FloatField(default=0.0)

    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    @classmethod
    def inject(cls,source_ngram,target_ngram,times=1):
        sub, created = SubCategory.objects.get_or_create(source=source_ngram,target=target_ngram)
        if times > 0:
            sub.t_rated = sub.t_rated + times
        sub.source.set_dirty()
        sub.save()
        return sub
    
    def compute_discriminatory_power(self):
        # Returns the mean position of the target ngram from the source ngram
        sum  = self.source.subcategories.all().aggregate(Sum('t_rated'))['t_rated__sum']
        if sum:
            try:
                self.power = self.t_rated/float(sum)
                self.save()
                return self.power
            except:
                return 0.0
    
    def __unicode__(self):
        return self.target#"%s <sub> &s"%(self.source,self.target)
    
    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'



"""
Semantic Differential of an ngram
"""
class SemanticDifferential(models.Model):
    # Semantic Differential of this Ngram
    ngram       = models.OneToOneField('NGrams', blank=True, null=True,)
    # Three main dimensions of the semantic differential
    evaluation  = models.FloatField(_('Evaluative Dimension'), default=0.0)
    potency     = models.FloatField(_('Potency Dimension'), default=0.0)
    activity    = models.FloatField(_('Activity Dimension'), default=0.0)
    # Counter how many times the Semantic Differential was rated
    t_rated     = models.PositiveIntegerField(_('Times Rated'),default=0)
    e_sum       = models.IntegerField(_('Evaluative Dimension Sum'), default=0)
    p_sum       = models.IntegerField(_('Potency Dimension Sum'), default=0)
    a_sum       = models.IntegerField(_('Activity Dimension Sum'), default=0)

    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def record(self, evaluation, potency, activity):
        self.e_sum += int(evaluation)
        self.p_sum += int(potency)
        self.a_sum += int(activity)
        self.t_rated += 1
        self.evaluation = float(self.e_sum) / self.t_rated
        self.potency = float(self.p_sum) / self.t_rated
        self.activity = float(self.a_sum) / self.t_rated
        self.save()
    
    def __unicode__(self):
        return u"%s"%(self.ngram)
    
    class Meta:
        verbose_name = 'Semantic Differential'
        verbose_name_plural = 'Semantic Differential'



"""
NGram holds the ngrams
"""
class NGrams(models.Model):
    # Unique key for a token
    token                   = models.CharField(_('NGram'),max_length=255,unique=True)
    # Counter how many times the token was injected into the system
    t_occurred              = models.PositiveIntegerField(_('Times Occurred'),default=0)
    # Counter how many times the token was rated by a user (Association)
    t_rated                 = models.PositiveIntegerField(_('Times Rated'),default=0)
    # Counter how many times the token was rated by a user (Association)
    t_visited               = models.PositiveIntegerField(_('Times Visited'),default=0)
    # t_occurred + t_visited - (t_rated*2)
    rating_index            = models.IntegerField(_('Calculated Index for ratings left'), default=0)
    # Boolean if the ngram is meaningless (if true: overrides partofspeech.semantic_meaninglessness) [old: semantic_meaningless]
    coocurrence_relevancy   = models.NullBooleanField(_('Relevant for Co-Occurrences'),blank=True, null=True)
    # Dirty Flag: Indicates the object has changed
    dirty                   = models.BooleanField(_('Dirty'),default=True)
    # Qualified Flag: True if Staff has checked, qualified and updated the ngram and associated models
    qualified               = models.BooleanField(_('Qualified'),default=False)
    
    # Word Stem of the token
    wordstem                = models.ForeignKey(WordStems, blank=True, null=True)
    # Numerus of the token
    numerus                 = models.ForeignKey(Numerus, blank=True, null=True)
    # Genus of the token
    genus                   = models.ForeignKey(Genus, blank=True, null=True)
    
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    
    @classmethod
    def add_text_to_system(cls, text):
        # Performance: 100 words = 105 sec
        #text should be the complete (user) input
        token_list_complete = Tokenizer.linear_token_list(text)
        ngram_list_complete = []
        # Get or create all ngrams and store them in ngram_list (performance)
        for token in token_list_complete:
            ngram = NGrams.inject(token=token) # Each token hits the database once (performance)
            # Append if not present in list (make unique list)
            if not ngram in ngram_list_complete:
                ngram_list_complete.append( ngram )
        
        # Make List of sentences
        sentences_list = Tokenizer.tokenize_sentences(text)
        for sentence in sentences_list:
            # Make linear token list for sentence
            token_list = Tokenizer.linear_token_list(sentence)
            ngram_list = []
            # Make ngram_list from token_list and ngram_list_complete
            for token in token_list:
                for ngram in ngram_list_complete:
                    if ngram.token == token:
                        ngram_list.append( ngram )
            # Add CoOccurrence inside sentence to the system
            for source_index,source_ngram in enumerate(ngram_list):
                for target_index,target_ngram in enumerate(ngram_list[source_index+1:source_index+11]):
                    # Identical ngrams (their token equivalence) do __not__ co-occure
                    if source_ngram != target_ngram:
                        # If eigther source.token or target.token indicates semantic meaninglessness: they do __not__ co-occure
                        if source_ngram.is_relevant_for_cooccurrences() and target_ngram.is_relevant_for_cooccurrences():
                            # Inject Co-Occurrence with the positional difference from the source (hits the database)
                            cooc = CoOccurrences.inject(source_ngram,target_ngram,target_index+1)
    @classmethod
    def inject(cls,token,times=1):
        ngram, created = NGrams.objects.get_or_create(token=token)
        if times > 0:
            # if zero (or less) self.t_occurred is not modified
            ngram.t_occurred = ngram.t_occurred + times
        ngram.dirty = True
        ngram.save()
        return ngram
    
    def set_dirty(self):
        self.dirty = True
        self.save()
    def set_clean(self):
        self.dirty = False
        self.save()
        
    def incr_t_rated(self,times=1):
        self.t_rated = self.t_rated + times
        self.save()
    
    def is_relevant_for_cooccurrences(self):
        """
        Checks if the ngram is semantically relevant for coocurrence, or
        if it belongs to a part of speech that indicates meaninglessness
        """
        if self.coocurrence_relevancy == True:
            return True
        else:
            for pos in self.partofspeech.all():#_set:
                if pos.coocurrence_relevancy == False:
                    return False
        return True
    
    def languages(self):
        return self.languages
    
    def get_all_outbound_tokens(self):
        outbound_list = chain( self.association_outbound.all().values_list('target__token'), \
                               self.supercategories.all().values_list('target__token'), \
                               self.subcategories.all().values_list('target__token'), \
                               self.synonyms.all().values_list('target__token'), \
                               self.antonyms.all().values_list('target__token'), \
                               self.coocurrence_outbound.all().values_list('target__token'))
        return outbound_list
    def get_all_association_token(self):
        return list( chain( *self.association_outbound.all().values_list('target__token') ) )
    
    def save(self, *args, **kwargs):
        super(NGrams, self).save(*args, **kwargs)
        # Set PartofSpeech to Zahlzeichen and language to International if token is_numeric
        # TODO: Think of similar shortcut-inferences
        if self.token.isnumeric():
            self.partofspeech.add(PartOfSpeech.objects.get(type="Zahlzeichen"))
            self.language.add(Languages.objects.get(language="International"))
    
    def occurrence_frequency_tag(self):
        """
        Returns a string indicating its relative frequency to the most frequent occurred ngram
        """
        freq = self.t_occurred
        tags = [_('Almost never'),_('Rarely'),_('Occasionally'),_('Often'),_('Frequently'),]
        interval = (NGrams.objects.order_by('-t_occurred')[0].t_occurred / float(len(tags)) )
        if freq <= interval: return tags[0]
        elif freq <= interval*2: return tags[1]
        elif freq <= interval*3: return tags[2]
        elif freq <= interval*4: return tags[3]
        elif freq <= interval*5: return tags[4]
        else: return _('Unknown')
        
    def rating_frequency_tag(self):
        """
        Returns a string indicating its relative frequency to the most frequent occurred ngram
        """
        freq = self.t_rated
        tags = [_('Almost never'),_('Rarely'),_('Occasionally'),_('Often'),_('Frequently'),]
        interval = (NGrams.objects.order_by('-t_rated')[0].t_rated / float(len(tags)) )
        if freq <= interval: return tags[0]
        elif freq <= interval*2: return tags[1]
        elif freq <= interval*3: return tags[2]
        elif freq <= interval*4: return tags[3]
        elif freq <= interval*5: return tags[4]
        else: return _('Unknown')
        
    def association_outbound_sorted(self):
        return self.association_outbound.order_by('-power')
    
    def calculate_rating_index(self):
        self.rating_index = self.t_occurred + self.t_visited - (self.t_rated * 2)
        return self.rating_index
    
    def get_absolute_url(self):
        return reverse('inspect_query', kwargs={'ngram':self.token})
    
    def get_similar_ngrams(self):
        pass
    
    @classmethod
    def get_popular_ngram(cls, daterange=1, number=100):
        #return NGrams.objects.dates('updated', daterange).order_by('t_rated')[:number]
        yesterday = datetime.now() - timedelta(days=daterange)
        return NGrams.objects.filter(updated__gt=yesterday).order_by('-t_visted')[:number]
    
    def __unicode__(self):
        return self.token
    
    class Meta:
        verbose_name = 'NGram'
        verbose_name_plural = 'NGrams'
        ordering = ['token',]



"""
Co-Occurrence Class: NGrams that occure together
"""
class CoOccurrences(models.Model):
    source  = models.ForeignKey(NGrams, related_name="coocurrence_outbound")
    target  = models.ForeignKey(NGrams, related_name="coocurrence_inbound")
    # How many times co-occurred
    t_cooccured = models.PositiveIntegerField(default=0)
    # List of positions from the source (0 is the position of the source ngram)
    positions = models.CommaSeparatedIntegerField(max_length=10000)
    mean_position = models.FloatField(default=0.0)
    # Discriminatory Power
    power = models.FloatField(default=0.0)
    # Dirty Flag: Indicates the object has changed 
    dirty = models.BooleanField(default=True)
    
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    @classmethod
    def inject(cls,source_ngram,target_ngram,position,times=1):
        cooc, created = CoOccurrences.objects.get_or_create(source=source_ngram,target=target_ngram)
        if times > 0:
            cooc.t_cooccured = cooc.t_cooccured + times
        cooc.positions += str(position) + ","
        # The ngram is dirty not the related model
        # Refactor dirty to only ngram can be dirty
        cooc.source.set_dirty()
        cooc.dirty = True
        cooc.save()
        return cooc
    
    def compute_mean_position(self):
        # Returns the mean position of the target ngram from the source ngram
        try:
            positions = map(int, self.positions[:-1].split(','))
            if positions:
                self.mean_position = sum(positions)/float(len(positions))
                return self.mean_position
        except:
            return 0.0
    
    def compute_discriminatory_power(self):
        # Returns the mean position of the target ngram from the source ngram
        #sum  = CoOccurrences.objects.filter(source=self.source).aggregate(Sum('t_cooccured'))['t_cooccured__sum']
        sum  = self.source.coocurrence_outbound.all().aggregate(Sum('t_cooccured'))['t_cooccured__sum']
        if sum:
            try:
                #self.power = self.t_cooccured/float(sum - self.t_cooccured)
                self.power = self.t_cooccured/float(sum)
                self.save()
                return self.power
            except:
                return 0.0
    
    def is_relevant_for_cooccurrences(self):
        """
        Checks if source and target is semantically relevant for cooccurrence, 
        i.e. does not belong to a partofspeech that is semantically meaningless
        """
        if self.source.is_relevant_for_cooccurrences() and self.target.is_relevant_for_cooccurrences():
            return True
        return False

    def save(self, *args, **kwargs):
        super(CoOccurrences, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.source.token +" | " + self.target.token
    
    class Meta:
        verbose_name = 'Co-Occurrence'
        verbose_name_plural = 'Co-Occurrences'
        
    
    
    
"""
Association Class: NGrams that were associated by users
"""
class Associations(models.Model):
    source  = models.ForeignKey(NGrams, related_name="association_outbound")
    target  = models.ForeignKey(NGrams, related_name="association_inbound")
    # How many times associated
    t_associated = models.PositiveIntegerField(default=0)
    # Discriminative Power:
    power = models.FloatField(default=0.0)
    # Dirty Flag: Indicates the object has changed 
    dirty = models.BooleanField(default=True)
    
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    @classmethod
    def inject(cls,source_ngram,target_ngram,times=1):
        assoc, created = Associations.objects.get_or_create(source=source_ngram,target=target_ngram)
        if times > 0:
            assoc.t_associated = assoc.t_associated + times
        # The source_ngram is dirty not the related model
        # Refactor dirty to only ngram can be dirty
        assoc.source.set_dirty()
        # increment ngram counter t_rated
        assoc.source.incr_t_rated()
        assoc.dirty = True
        assoc.save()
        return assoc
    
    def compute_discriminatory_power(self):
        # Returns the mean position of the target ngram from the source ngram
        #sum  = self.source.association_outbound_set.t_associated__sum
        #sum  = Associations.objects.filter(source=self.source).aggregate(Sum('t_associated'))['t_associated__sum']
        sum  = self.source.association_outbound.all().aggregate(Sum('t_associated'))['t_associated__sum']
        if sum:
            try:
                #self.power = self.t_associated/float(sum - self.t_associated)
                self.power = self.t_associated/float(sum)
                self.save()
                return self.power
            except:
                return 0.0
    
    def __unicode__(self):
        return self.source.token + " <"+str(self.t_associated)+"> " + self.target.token
    
    class Meta:
        verbose_name = 'Association'
        verbose_name_plural = 'Associations'
    
    
    
"""
Not Related Class: An Ngram is not related to another Ngram
"""
class NotRelated(models.Model):
    source  = models.ForeignKey('NGrams', related_name="not_related_to")
    target  = models.ForeignKey('NGrams', related_name="not_related_from")
    # How many times the Non-Relationship was rated
    t_rated = models.PositiveIntegerField(default=0)
    # Discriminatory Power
    power = models.FloatField(default=0.0)

    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    @classmethod
    def inject(cls,source_ngram,target_ngram,times=1):
        notrelated, created = NotRelated.objects.get_or_create(source=source_ngram,target=target_ngram)
        if times > 0:
            notrelated.t_rated = notrelated.t_rated + times
        notrelated.source.set_dirty()
        notrelated.save()
        return notrelated
    
    def compute_discriminatory_power(self):
        # Returns the mean position of the target ngram from the source ngram
        sum  = self.source.not_related_to.all().aggregate(Sum('t_rated'))['t_rated__sum']
        if sum:
            try:
                self.power = self.t_rated/float(sum)
                self.save()
                return self.power
            except:
                return 0.0
    
    def __unicode__(self):
        return self.target#"%s <sub> &s"%(self.source,self.target)
    
    class Meta:
        verbose_name = 'Non-Relationship'
        verbose_name_plural = 'Non-Relationships'
    
    
    
