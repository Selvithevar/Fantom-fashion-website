from atexit import register
from django import template
from posts.models import category,Tag,post

register = template.Library()

@register.simple_tag(name="categories")
def all_categories():
    return category.objects.all()

@register.simple_tag(name='tags')
def all_tags():
    return Tag.objects.all()

@register.simple_tag(name='hit_posts')
def hit_posts():
    return post.objects.order_by('-hit')[:5]
