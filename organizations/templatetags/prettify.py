from django import template
from django.utils.safestring import SafeString

register = template.Library()

ASSESSMENT_MAPPING = {
    'red-close': SafeString('<i class="red fa fa-close"></i>'),
    'red-check': SafeString('<i class="red fa fa-check"></i>'),
    'green-close': SafeString('<i class="green fa fa-close"></i>'),
    'green-check': SafeString('<i class="green fa fa-check"></i>')
}


def pretty_assessment(value):
    """ Prettifies the assessment string """
    new_value = ASSESSMENT_MAPPING.get(value)
    if new_value:
        return new_value
    else:
        return value


register.filter('pretty_assessment', pretty_assessment)