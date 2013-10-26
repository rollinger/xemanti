from django.utils import simplejson
import random
import itertools
from dajaxice.decorators import dajaxice_register
from ngramengine.models import *

@dajaxice_register
def sort_ngram(request, type, source, target):
    source = NGrams.inject(token=source.strip())
    target = NGrams.inject(token=target.strip())
    # inject sorted target
    if type == "not_related_container":
        NotRelated.inject(source,target)
    elif type == "association_container":
        Associations.inject(source,target)
    elif type == "synonym_container":
        Synonyms.inject(source,target)
    elif type == "antonym_container":
        Antonyms.inject(source,target)
    elif type == "sub_category_container":
        SubCategory.inject(source,target)
    elif type == "super_category_container":
        SuperCategory.inject(source,target)
    # increase users income
    if request.user.is_authenticated():
        request.user.profile.income(2.22)
    return request.user.profile.balance

"""
DEPRECATED: BOUND FOR DELETION
@dajaxice_register
def get_next_word(request, ngram):
    ngram = NGrams.objects.get(token=ngram)
    token_list = list( set( itertools.chain( *ngram.get_all_outbound_tokens() ) ) )
    if token_list:
        token = random.choice( token_list )
        return token
    else:
        return None
"""