from django import template

register = template.Library()

"""
Template tags to define a variable and to add a number to a variable not using |add only usable 
for a display {{toto|add}}
used in detail_view
"""


@register.simple_tag
def define(val=None):
    return int(val)


@register.simple_tag
def plus(var, value):
    return int(var) + int(value)

