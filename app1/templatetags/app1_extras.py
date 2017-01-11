from django import template
from app1.models import Division

register = template.Library()

@register.inclusion_tag('app1/divs.html')
def get_division_list():
    return {'divs': Division.objects.all()}
