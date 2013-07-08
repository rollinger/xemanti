# -*- coding: utf-8 -*-
from ngramengine.models import *
from tokenizer import Tokenizer

from django.db.models import Q, F

from celery import task
import celery
import time



# Add text to system (user trigger)
@celery.task(name='tasks.add_text_to_system')
def add_text_to_system(text):
    """
    Add a text to the system (add ngrams and cooccurrences).
    """
    start_time = time.time()
    
    # Main Routine
    NGrams.add_text_to_system( text )
    
    # Performance Message
    duration =  time.time() - start_time
    ntok = len(Tokenizer.linear_token_list(text))
    print "N_Token: " + str(ntok)
    print "Duration: " + str(duration)
    print "Time per Token: " + str(ntok/duration) 



# Calculate ngram_count of Languages and PartofSpeech (cronjob)
@celery.task(name='tasks.calc_ngram_count')
def calc_ngram_count():
    """
    Calculates the number of ngrams that Languages and PartofSpeech objects are related to.
    """
    start_time = time.time()
    
    # Main Routine
    n_lang = 0; n_pos = 0;
    for language in Languages.objects.all():
        language.count_ngrams()
        n_lang += 1
    for pos in PartOfSpeech.objects.all():
        pos.count_ngrams()
        n_pos += 1
    
    # Performance Message
    duration =  time.time() - start_time
    print "N_Language: " + str(n_lang)
    print "N_os: " + str(n_pos)
    print "Duration: " + str(duration)
    print "Time per Object: " + str((n_lang+n_pos)/duration) 



# Process for Maintaining Co-Occurrence (every hour)
@celery.task(name='tasks.ngram_maintenance')
def ngram_maintenance():
    """
    Periodic Maintenance of NGrams
    - Delete Cooccurrences over 100 ordered by t_cooccurred
    - Calculate statistics 
    """
    start_time = time.time()
    
    COOCCURRENCE_CUTOFF = 100
    # fetch all (100) dirty ngrams
    dirty_query = NGrams.objects.filter(dirty=True).order_by('?')[:100]
    for obj in dirty_query:
        #print "NGRAM: " + str(obj)
        #
        # CoOccurrence Maintenance
        #
        if obj.coocurrence_outbound.exists():
            # Delete non-meaningful coocurrences
            for cooc in obj.coocurrence_outbound.all():
                if not cooc.is_meaningful():
                    cooc.delete()
            # Delete Cooccurence by Cutoff (Delete after COOCCURRENCE_CUTOFF)
            for cooc in obj.coocurrence_outbound.order_by('-t_cooccured')[COOCCURRENCE_CUTOFF:]:
                    #print str(cooc) + " >> " + str(cooc.t_cooccured)
                    cooc.delete()
            # Calculate Statistics for remaining CoOccurrences
            for cooc in obj.coocurrence_outbound.all():
                #print cooc
                cooc.compute_mean_position()
                cooc.compute_discriminatory_power()
                cooc.dirty = False
                cooc.save()
        
        #
        # NGram Maintenance
        #
        obj.dirty = False
        obj.save()
        
    # Performance Message
    duration =  time.time() - start_time
    ntok = len(dirty_query)
    print "N_NGrams: " + str(ntok)
    print "Duration: " + str(duration)
    print "Time per Token: " + str(ntok/duration) 



# Calculate ngram_count of Languages and PartofSpeech (cronjob)
@celery.task(name='tasks.add_random_wikipedia_article_to_system')
def add_random_wikipedia_article_to_system():
    """
    Fetch a random wikipedia article and add the text to the system
    """
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
    #Add text to system
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
            
# Process for Maintaining Co-Occurrence (every hour)
@celery.task(name='tasks.cooccurrence_maintenance')
def cooccurrence_maintenance():

    Periodic Maintenance of Cooccurrences
    - Delete Cooccurrences if not meaningfull
    - Calculate statistics 

    # fetch all dirty cooccurrences
    dirty_query = CoOccurrences.objects.filter(dirty=True)
    for obj in dirty_query:
        #if obj.t_cooccured == 1:
        #    obj.delete()
        #    continue
        #el
        if not obj.is_meaningful():
            obj.delete()
            continue
        else:
            # Compute Stats after Deletion Process
            obj.compute_mean_position()
            obj.compute_discriminatory_power()
            obj.dirty = False
            obj.save()
"""
