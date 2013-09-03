#
# Script file to start from shell ./manage.py shell
#
# Custom import
import os
import sys
import json
from pprint import pprint
from ngramengine.models import *


def wiktionary_import(importfile='ngramengine/data/wiktionary.json'):
    """
from ngramengine.scripts import wiktionary_import
wiktionary_import()
    """
    #importfile='ngramengine/data/xaa'
    json_data=open(importfile,'r')
    data = json.load(json_data)
    
    #pprint(data)
    
    
    for word, dict in data.iteritems():
        try:
            ngram = word
            language = dict['language']
            partofspeech = dict['partofspeech']
            synonyme = dict['synonyme']
            antonyme = dict['antonyme']
            supercategory = dict['supercategory']
            subcategory = dict['subcategory']
            
            if "Deutsch" in language:
                pprint(ngram)
                pprint(language)
                pprint(partofspeech)
                pprint(synonyme)
                pprint(antonyme)
                pprint(supercategory)
                pprint(subcategory)
                
                print
                
                # Create NGram
                ngram,created = NGrams.objects.get_or_create(token=ngram)
                # Save NGram
                ngram.save()
                if not created:
                    continue
                for lang in language:
                    lang,created = Languages.objects.get_or_create(language=lang)
                    lang.save()
                    ngram.language.add(lang)
                for pos in partofspeech:
                    pos,created = PartOfSpeech.objects.get_or_create(type=pos)
                    pos.save()
                    ngram.partofspeech.add(pos)
                for syn in synonyme:
                    Synonyms.inject(NGrams.inject(ngram,times=0),NGrams.inject(syn,times=0))
                for aty in antonyme:
                    Antonyms.inject(NGrams.inject(ngram,times=0),NGrams.inject(aty,times=0))
                for super in supercategory:
                    SuperCategory.inject(NGrams.inject(ngram,times=0),NGrams.inject(super,times=0))
                for sub in subcategory:
                    SubCategory.inject(NGrams.inject(ngram,times=0),NGrams.inject(sub,times=0))
                # Save NGram
                ngram.save()
        #except:
            #print "Something went wrong"
    json_data.close()