from django.utils import simplejson
import random
import itertools
from dajaxice.decorators import dajaxice_register
from ngramengine.models import *

@dajaxice_register
def get_popular_ngram_slot(request):
    popular = random.choice(NGrams.get_popular_ngram(1,100))
    return '<span><center><a class="color-black clickable" href="%s">%s</a></center></span>' % (popular.get_absolute_url(), popular)
