# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext as _

# Custom Imports
from tokenizer import Tokenizer



"""
Word Stems a stem for ngrams with the same stem
"""
class WordStems(models.Model):
    # The Stem of a set of Ngrams
    stem        = models.CharField(max_length=255,unique=True)
    
    def __unicode__(self):
        return self.stem
    
    class Meta:
        verbose_name = 'Word Stem'
        verbose_name_plural = 'Word Stems'
        ordering = ['stem',]
        
        
"""
Part Of Speech typify the ngram for their part of speech
"""
class PartOfSpeech(models.Model):
    # The Part of Speech of a set of Ngrams
    type        = models.CharField(max_length=255,unique=True)
    # Part of Speech related to NGrams
    ngrams = models.ManyToManyField('NGrams', related_name="partofspeech", blank=True, null=True)
    # Boolean if the part or speech indicates meaninglessness of the ngram
    # Meaninglessness is better inferred from the part of speech than meaningfulness
    semantic_meaningless = models.BooleanField(default=False)
    # How many ngrams have this part of speech
    ngram_count = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return self.type
    
    def count_ngrams(self):
        self.ngram_count = self.ngrams.count()
        self.save()
        return self.ngram_count
    
    def save(self):
        #self.count_ngrams(self)
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
    ngrams = models.ManyToManyField('NGrams', related_name="language", blank=True, null=True)
    # How many ngrams have this language
    ngram_count = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return self.language
    
    def count_ngrams(self):
        self.ngram_count = self.ngrams.count()
        self.save()
        return self.ngram_count
    
    def save(self):
        #self.count_ngrams(self)
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

    def __unicode__(self):
        return self.target#"%s <synonym> &s"%(self.source,self.target)
    
    class Meta:
        verbose_name = 'Synonym'
        verbose_name_plural = 'Synonyms'
"""
Antonyms of an ngram
"""
class Antonyms(models.Model):
    source  = models.ForeignKey('NGrams', related_name="antonym")
    target  = models.ForeignKey('NGrams', related_name="antonym_of")
    # How many times the Antonym was rated
    t_rated = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.target#"%s <antonym> &s"%(self.source,self.target)
    
    class Meta:
        verbose_name = 'Antonym'
        verbose_name_plural = 'Antonyms'
"""
SuperCategory of an ngram
"""
class SuperCategory(models.Model):
    source  = models.ForeignKey('NGrams', related_name="supercategory")
    target  = models.ForeignKey('NGrams', related_name="supercategory_of")
    # How many times the Super Category was rated
    t_rated = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return self.target#"%s <super> &s"%(self.source,self.target)
    
    class Meta:
        verbose_name = 'Super Category'
        verbose_name_plural = 'Super Categories'
"""
SubCategory of an ngram
"""
class SubCategory(models.Model):
    source  = models.ForeignKey('NGrams', related_name="subcategory")
    target  = models.ForeignKey('NGrams', related_name="subcategory_of")
    # How many times the Sub Category was rated
    t_rated = models.PositiveIntegerField(default=0)

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
    token       = models.CharField(max_length=255,unique=True)
    # Counter how many times the token was injected into the system
    t_occurred  = models.PositiveIntegerField(default=0)
    # Word Stem of the token
    wordstem = models.ForeignKey(WordStems, blank=True, null=True)
    # Boolean if the ngram is meaningless (if true: overrides partofspeech.semantic_meaninglessness)
    semantic_meaningless = models.BooleanField(default=False)
    # Dirty Flag: Indicates the object has changed
    dirty = models.BooleanField(default=True)
    
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
                for target_index,target_ngram in enumerate(ngram_list):
                    # Identical ngrams (their token equivalence) do __not__ co-occure
                    if source_index != target_index and source_ngram != target_ngram:
                        # If eigther source.token or target.token indicates semantic meaninglessness: they do __not__ co-occure
                        if source_ngram.is_meaningful() and target_ngram.is_meaningful():
                            # Inject Co-Occurrence with the positional difference from the source (hits the database)
                            cooc = CoOccurrences.inject(source_ngram,target_ngram,target_index-source_index)
        
    @classmethod
    def inject(cls,token,times=1):
        ngram, created = NGrams.objects.get_or_create(token=token)
        if times > 0:
            # if zero (or less) self.t_occurred is not modified
            ngram.t_occurred = ngram.t_occurred + times
        ngram.dirty = True
        ngram.save()
        return ngram
    
    def is_meaningful(self):
        """
        Checks if the ngram is semantically meaningless, or
        if it belongs to a part of speech that indicates meaninglessness
        """
        if self.semantic_meaningless == True:
            return False
        else:
            for pos in self.partofspeech.all():#_set:
                if pos.semantic_meaningless == True:
                    return False
        return True
    
    def languages(self):
        return self.languages
    
    def save(self, *args, **kwargs):
        super(NGrams, self).save(*args, **kwargs)
        # Set PartofSpeech to Zahlzeichen and language to International if token is_numeric
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
    
    @classmethod
    def inject(cls,source_ngram,target_ngram,position,times=1):
        cooc, created = CoOccurrences.objects.get_or_create(source=source_ngram,target=target_ngram)
        if times > 0:
            cooc.t_cooccured = cooc.t_cooccured + times
        cooc.positions += str(position) + ","
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
        sum  = CoOccurrences.objects.filter(source=self.source).aggregate(Sum('t_cooccured'))['t_cooccured__sum']
        if sum:
            try:
                self.power = self.t_cooccured/float(sum - self.t_cooccured)
                return self.power
            except:
                return 0.0
    
    def is_meaningful(self):
        """
        Checks if source and target is semantically meaningful, 
        i.e. does not belong to a partofspeech that is semantically meaningless
        """
        if self.source.is_meaningful() and self.target.is_meaningful():
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
    power = models.FloatField()
    
    def compute_discriminatory_power(self):
        sum  = self.source.association_outbound_set.t_associated__sum
        return self.t_associated/float(sum - self.t_associated)
    
    def __unicode__(self):
        return self.source.token + " <"+self.mean_position()+"> " + self.target.token
    
    class Meta:
        verbose_name = 'Association'
        verbose_name_plural = 'Associations'
    
    
    
"""
InputStack holds the text sequences about to enter the system
"""
class InputStack(models.Model):
    content = models.CharField(max_length=2000)
    
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
