# -*- coding: utf-8 -*-
from ngramengine.models import *
from tokenizer import Tokenizer

from celery import task
import celery

# Add text to system (user trigger)
@celery.task(name='tasks.add_text_to_system')
def add_text_to_system(text):
    NGrams.add_text_to_system( text )
    #sentence_list = Tokenizer.tokenize_sentences(text)
    #for sentence in sentence_list:
    #    NGrams.add_text_to_system( sentence )



# Calculate ngram_count of Languages and PartofSpeech (cronjob)
@celery.task(name='tasks.calc_ngram_count')
def calc_ngram_count():
    for language in Languages.objects.all():
        language.count_ngrams()
    for pos in PartOfSpeech.objects.all():
        pos.count_ngrams()



# Process for Maintaining Co-Occurrence (every hour)
@celery.task(name='tasks.cooccurrence_maintenance')
def cooccurrence_maintenance():
    # fetch all dirty cooccurrences
    dirty_query = CoOccurrences.objects.filter(dirty=True)
    for obj in dirty_query:
        if obj.t_cooccured == 1:
            obj.delete()
            continue
        elif not obj.is_meaningful():
            obj.delete()
            continue
    # Compute Stats after Deletion Process
    for obj in dirty_query:
            obj.compute_mean_position()
            obj.compute_discriminatory_power()
            obj.dirty = False
            obj.save()

# Calculate ngram_count of Languages and PartofSpeech (cronjob)
@celery.task(name='tasks.add_random_wikipedia_article_to_system')
def add_random_wikipedia_article_to_system():
    import urllib
    import urllib2
    import re
    from bs4 import BeautifulSoup
    
    #ngram = NGrams.objects.order_by('?')[0]
    #print ngram.token
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20110506 Firefox/4.0.1')]
    #url = "http://de.wikipedia.org/wiki/"+ngram.token
    #url = "http://de.wikipedia.org/w/index.php?title="+"&printable=yes"
    url = "http://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite"
    #url = "http://de.wikipedia.org/wiki/Crist%C3%B3bal_Gregorio_VI_Portocarrero_Osorio_Villalpando_y_Guzm%C3%A1n"
    html = opener.open(url.encode('utf-8'))
    soup = BeautifulSoup(html)
    texts = soup.find("div", {"id": "mw-content-text"}).findAll(text=True)
    text =  "".join(texts).split('NewPP limit report')[0]
    #print text
    add_text_to_system(text)

"""
# Process for Deleting bad Co-Occurrence (trigerable)
@celery.task(name='tasks.cooccurrence_deletion')
def cooccurrence_deletion():
    # Delete non meaningful co-occurences
    dirty_query = CoOccurrences.objects.filter()
    
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
