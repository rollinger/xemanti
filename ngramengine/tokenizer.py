# -*- coding: utf-8 -*-

# Imports
import re
from django.utils.encoding import smart_str, smart_unicode

"""
Tokenizer Class for String handling in the GERMAN NGram Engine
--> RuleSet for different Tokenization Problems
"""
class Tokenizer():
    
    
    
    @classmethod
    def linear_token_list(cls, text):
        # Returns a linear list of tokens (words and stopwords)
        text = smart_unicode(text)
        return cls.tokenize_words(text)
    
    
    
    # Pattern for Word Tokenization
    @classmethod
    def tokenize_words(cls, text ):
        # Tokenize text on whitespace 
        nonword_pat = re.compile(r'[.!?:;,]+', re.UNICODE)
        word_pat = re.compile(r'[\w.]+', re.UNICODE)
        text = re.sub(nonword_pat, ' ' , text)
        # Removed to lower case text.lower()
        # Reason: Case implies difference in semantic meaning (
        return word_pat.findall( text ) 
    
    
    
    @classmethod
    # Pattern for Sentence Tokenization
    def tokenize_sentences(cls, text ):
        # Known Bug: splits also on Dates (6.6.2013) and Numerals (4.)
        # TODO: IMPROVE!!! 
        pat = re.compile(r'''[^.!?\s][^.!?]*(?:[.!?](?!['"]?\s|$)[^.!?]*)*[.!?]?['"]?(?=\s|$)''', re.L)
        sentences = pat.findall(text)
        return sentences
    
    
    
    @classmethod
    def tokenize_to_ngrams(cls,text, order=[1,2,3],unique=False):
        # Make tokenization
        token = cls.tokenize_words(text)
        ngrams = []
        for i in xrange(0,len(token)):
            for j in order:
                #print str(i) + "|" + str(j)
                # Append if not out of range
                if len( token[i:i+j] ) == j:
                    ngrams.append( " ".join( token[i:i+j] ) )
        if unique:
            return cls.unique(ngrams)
        else:
            return ngrams
    
    @classmethod
    def unique(cls,list):   
        #make list unique (no order preserved) (fast)
        keys = {}
        for e in list:
            keys[e] = 1
        return keys.keys()