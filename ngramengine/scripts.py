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
    json_data=open(importfile,'r')
    data = json.load(json_data)
    
    #pprint(data)
    
    for word, dict in data.iteritems():
        ngram = word
        language = dict['language']
        partofspeech = dict['partofspeech']
        synonyme = dict['synonyme']
        antonyme = dict['antonyme']
        supercategory = dict['supercategory']
        subcategory = dict['subcategory']
        
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
        for lang in language:
            lang,created = Languages.objects.get_or_create(language=lang)
            lang.save()
            lang.ngrams.add( ngram )
        for pos in partofspeech:
            pos,created = PartOfSpeech.objects.get_or_create(type=pos)
            pos.save()
            pos.ngrams.add( ngram )
        for syn in synonyme:
            syn,created = NGrams.objects.get_or_create(token=syn)
            syn.save()
            Synonyms.objects.get_or_create(source=ngram,target=syn)
        for aty in antonyme:
            aty,created = NGrams.objects.get_or_create(token=aty)
            aty.save()
            Antonyms.objects.get_or_create(source=ngram,target=syn)
        for super in supercategory:
            super,created = NGrams.objects.get_or_create(token=super)
            super.save()
            SuperCategory.objects.get_or_create(source=ngram,target=super)
        for sub in subcategory:
            sub,created = NGrams.objects.get_or_create(token=sub)
            sub.save()
            SubCategory.objects.get_or_create(source=ngram,target=sub)
        
    json_data.close()