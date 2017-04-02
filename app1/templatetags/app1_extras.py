from django import template
from app1.models import Division,Question

register = template.Library()


@register.inclusion_tag('app1/divs.html')
def get_division_list():
    return {'divs': Division.objects.all()}


@register.filter
def in_page(image_list, page):
    return image_list.filter(page=page)


@register.filter
def is_user_question(question_list, user_id):
    if question_list.get(id=user_id):
        return True
    else:
        return False
