from django import template

register = template.Library()

@register.filter(name='power_to_font_size')
def power_to_font_size(power):
    return str(0.5+(power*4)).replace(",", ".")