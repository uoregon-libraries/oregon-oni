from django import template
from core.utils import image_urls

register = template.Library()

@register.simple_tag
def custom_image_url(page, width):
    return image_urls.resize_url(page, width)
