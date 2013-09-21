from django import template
from ngramengine.models import NGrams

register = template.Library()


@register.inclusion_tag('ngramengine/_popular_ngrams_partial.html')
def render_popular_ngrams(daterange=1, number=5):
    popular_ngrams = NGrams.get_popular_ngram(daterange,number)
    return {
        'popular_ngrams': popular_ngrams,
        'daterange':daterange,
        'number': number,
    }