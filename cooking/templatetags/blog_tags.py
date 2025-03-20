from django import template
from django.db.models import Count, Q

from cooking.models import Category

register = template.Library()


@register.simple_tag()
def get_all_categories():
    """Category buttons."""
    return Category.objects.annotate(cnt=Count('posts', filter=Q(posts__is_published=True))).filter(cnt__gt=0)
