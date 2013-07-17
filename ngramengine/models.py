# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext as _
from itertools import chain

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
    
    def save(self):
        super(PartOfSpeech, self).save()
    
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
    
    def save(self):
        super(Languages, self).save()
    
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

    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
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

    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
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
    
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
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

    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.target#"%s <sub> &s"%(self.source,self.target)
    
    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'



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
        outbound_list = chain( self.coocurrence_outbound.all().values_list('target__token'), \
                               self.association_outbound.all().values_list('target__token'), \
                               self.supercategories.all().values_list('target__token'), \
                               self.subcategories.all().values_list('target__token'), \
                               self.synonyms.all().values_list('target__token'), \
                               self.antonyms.all().values_list('target__token'))
        return outbound_list
    
    def save(self, *args, **kwargs):
        super(NGrams, self).save(*args, **kwargs)
        # Set PartofSpeech to Zahlzeichen and language to International if token is_numeric
        # TODO: Think of similar shortcut-inferences
        if self.token.isnumeric():
            self.partofspeech.add(PartOfSpeech.objects.get(type="Zahlzeichen"))
            self.language.add(Languages.objects.get(language="International"))
    
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
InputStack holds the text sequences about to enter the system
"""
class InputStack(models.Model):
    content = models.CharField(max_length=2000)
    
    # Model Timestamp
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    @classmethod
    def add(cls, text):
        pass
        """
        # Tokenize and save Sentences
        sentence_list = Tokenizer.tokenize_sentences( text )
        for sentence in sentence_list:
            s = InputStack(content=sentence)
            s.save()
        return sentence_list
        """
    
    @classmethod
    def pop_random(cls):
        pass
        """
        count = cls.objects.count()
        random_index = random.randint(0, count - 1)
        return cls.objects.all()[random_index]
        """
    
    def __unicode__(self):
        return self.content
    
    class Meta:
        verbose_name = 'Input Stack'
        verbose_name_plural = 'Input Stack Elements'
