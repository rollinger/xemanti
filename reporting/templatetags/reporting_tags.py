from django import template

register = template.Library()



@register.filter(name='power_to_font_size')
def power_to_font_size(power):
    return str(0.75+(power*2)).replace(",", ".")



@register.inclusion_tag('reporting/_tag_cloud_partial.html')
def render_tag_cloud(ngram, type, reverse=False):
    visible = getattr(ngram, type).filter(power__gte=0.01).order_by('-power')
    invisible = getattr(ngram, type).filter(power__lte=0.01).order_by('-power')
    return {
        'ngram': ngram,
        'type':type,
        'visible': visible,
        'invisible': invisible,
        'reverse':reverse,
    }