from time import time

from django.utils.text import slugify


def get_ip_from_request(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_unique_slug(name):
    slug = slugify(name, allow_unicode=True)
    return slug + '-' + str(int(time()))
