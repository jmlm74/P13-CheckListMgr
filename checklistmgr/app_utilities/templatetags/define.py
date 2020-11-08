from django import template

register = template.Library()

"""
Template tags to define a variable and to add a number to a variable not using |add only usable 
for a display {{toto|add}}
used in detail_view
"""


@register.simple_tag
def define_int(val=None):
    """
    define a value int (better than with... or other tricks in templates
    """
    return int(val)


@register.simple_tag
def plus(var, value):
    """
    template tag to add 2 values and return the result
    """
    return int(var) + int(value)

@register.simple_tag
def define_str(val=None):
    return str(val)

@register.simple_tag
def concat_str(var1, var2):
    """
    concat to args (may be integer) and returns concatenated str
    """
    print(f"{var1} - {var2}")
    return str(var1) + str(var2)
