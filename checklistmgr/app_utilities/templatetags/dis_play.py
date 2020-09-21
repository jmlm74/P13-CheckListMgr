from django import template
from app_utilities.models import Translation
import re

register = template.Library()

"""
Template tags to define a variable and to add a number to a variable not using |add only usable 
for a display {{toto|add}}
used in detail_view
"""


@register.simple_tag(takes_context=True)
def dis_play(context, value):
    """
        Template tag to display datas from translation modele
        Args :
            Context --> use to get session data
            Value --> key for the translation model
        Return:
              Field from Translation model --> language (FR, UK..)
    """
    try:
        language = context.request.session['language']
    except KeyError:
        language = "UK"
    text_to_display = Translation.get_translation(value, language)
    return text_to_display


@register.filter
def get_error_msg(value):
    """
        Filter to remove all the tags of an error message to get the message
        remove also some specials chars
        Args :
            The complete error message
        Return:
            The message to be displayed
    """
    value = str(value)
    pattern = "<li>(.*?)</li>"
    try:
        value = re.search(pattern, value).group(1)
    except AttributeError:
        value = re.search(pattern, value)
    value = re.sub("’", ' ', value)
    return value
