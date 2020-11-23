from django import template
from app_utilities.models import Translation
from datetime import datetime
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
    except KeyError as e:
        language = "FR"
    except AttributeError as e:
        language = "FR"
    text_to_display = Translation.get_translation(value, language=language)
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


@register.simple_tag(takes_context=True)
def dis_play_date(context):
    """
        Template tag to display dates in regional format
        Args :
            Context --> use to get session data
            day,mont,year --> key for the translation model
        Return:
              date in FR, UK... format --> defaulkt or error is UK format
    """
    try:
        if (language := context.request.session['language']) == "UK":
            return datetime.today().strftime('%Y/%m/%d')
        elif language == "FR":
            return datetime.today().strftime('%d/%m/%Y')
        else:
            return datetime.today().strftime('%Y/%m/%d')
    except KeyError:
        return datetime.today().strftime('%Y/%m/%d')
    return datetime.today().strftime('%Y/%m/%d')


@register.filter
def to_str(value):
    """
    return the value in arg in str (don't exist in django)
    """
    return str(value)


@register.simple_tag
def find_value_in_listdict(value, my_list_dict):
    """
    Template tag to find if a value is in dict
    :param value: value to find
    :param my_list_dict: a list of dict
    :return: boolean
    """
    found = False
    for my_dict in my_list_dict:
        if value in my_dict.values():
            found = True
    return found


@register.simple_tag(takes_context=True)
def dis_play_result(context, item):
    """
        Template tag to return the choice of specific Item in checklist (Valid, N/A, Not Valid)
        Args :
            Context --> use to get session data
            the item_id
        Return:
              choice (string)
    """
    if str(item) + "-on" in context['dict_choices']:
        return "valid"
    elif str(item) + "-na" in context['dict_choices']:
        return "n/a"
    return 'default'

@register.simple_tag(takes_context=True)
def dis_play_remark(context, rem_id):
    """
        Template tag to return the remarks in checklist
        Args :
            Context --> use to get session data
            the remark_id
        Return:
              remark (string)
    """
    remark_id = "text-"+str(rem_id)
    try:
        remark = context['dict_remarks'][remark_id]
        return remark.replace("{CRLF}", "\r\n")
    except KeyError:
        return 'ERREUR'

@register.filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    """
    Template tag to return a date format
    args :timestamp format
    returns : dattime format
    """
    return datetime.date.fromtimestamp(int(timestamp))
