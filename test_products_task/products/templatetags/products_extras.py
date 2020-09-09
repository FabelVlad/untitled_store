from django import template

from test_products_task.products.models import Cart

register = template.Library()


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        if filtered_querystring:
            encoded_querystring = '&'.join(filtered_querystring)
            url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.simple_tag
def items_in_cart(user):
    """ Return total items in cart for authenticated user. """
    return Cart.objects.filter(user=user).count()
