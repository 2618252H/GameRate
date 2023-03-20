from django import template
from gamerateapp.models import Category

register = template.Library()

@register.inclusion_tag('gamerateapp/categories.html')
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
            'current_category': current_category}