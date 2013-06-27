# -*- coding: utf-8 -*-
from ngramengine.models import NGrams, CoOccurrences
from tokenizer import Tokenizer

from celery import task
import celery

# Add text to system (user trigger)
@celery.task(name='tasks.add_text_to_system')
def add_text_to_system(text):
    sentence_list = Tokenizer.tokenize_sentences(text)
    for sentence in sentence_list:
        print sentence
        NGrams.add_text_to_system( sentence )


# Process for Maintaining Co-Occurrence (every hour)
@celery.task(name='tasks.cooccurrence_maintenance')
def cooccurrence_maintenance():
    # fetch all dirty cooccurrences
    dirty_query = CoOccurrences.objects.filter(dirty=True)
    for obj in dirty_query:
        obj.compute_mean_position()
        obj.compute_discriminatory_power()
        obj.dirty = False
        obj.save()

# Process for Deleting bad Co-Occurrence (trigerable)
@celery.task(name='tasks.cooccurrence_deletion')
def cooccurrence_deletion():
    # Delete non meaningful co-occurences
    filter = ['substantiv',"verb","adjektiv"]
    dirty_query = CoOccurrences.objects.exclude(source__partofspeech__in=filter).exclude(source__partofspeech__isnull=True)
    print dirty_query.count()
    for obj in dirty_query:
        obj.delete()
    dirty_query = CoOccurrences.objects.exclude(target__partofspeech__in=filter).exclude(target__partofspeech__isnull=True)
    print dirty_query.count()
    for obj in dirty_query:
        obj.delete()
    # Delete Co-Occurences that occurred only once
    dirty_query = CoOccurrences.objects.filter(t_cooccured=1)
    print dirty_query.count()
    for obj in dirty_query:
        obj.delete()
"""
@celery.task(name='tasks.calculate_devianz')
def calculate_devianz():
    one = OneGram.objects.filter(dirty=True)
    two = TwoGram.objects.filter(dirty=True)
    three = ThreeGram.objects.filter(dirty=True)
    array = list(chain(one,two,three))
    for obj in array:
        obj.calculate_devianz()
        print str(obj) + ": " + str(obj.devianz)

@celery.task(name='tasks.add_ngrams_to_sentence_queue')
def add_ngrams_to_sentence_queue():
    # Add ngrams that 
    # - dirty = true
    # - times_occured >= 2
    # - (times_nonsense/times_occurred) < 0.33
    # TODO: refactor
    one = OneGram.objects.filter(dirty=True).filter(times_occured__gte=2)
    two = TwoGram.objects.filter(dirty=True).filter(times_occured__gte=2)
    three = ThreeGram.objects.filter(dirty=True).filter(times_occured__gte=2)
    array = list(chain(one,two,three))
    for obj in array:
        if (obj.times_nonsense/obj.times_occured*1.0) < 0.005:
            s = Sentences(content=str(obj))
            print str(obj)
            s.save()
        else:
            print "NOT ADDED!!!" + str(obj)
"""