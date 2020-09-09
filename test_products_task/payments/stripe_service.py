import logging
from typing import Union

import stripe
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from test_products_task.payments.models import Customer, Order
from test_products_task.products.models import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


def make_payment(request, user, form, amount: float):
    customer_obj, created = _get_customer(user, request)
    _set_stripe_source(customer_obj, form.cleaned_data['stripe_token'], request)

    try:
        charge = _create_stripe_charge(customer_obj.stripe_id, int(amount * 100))
        _create_order(customer_obj, amount, charge.status, form.cleaned_data['address'])

        if charge.status == 'succeeded':  # todo add method to manager
            Cart.objects.filter(user=user).delete()

    except stripe.error.CardError as e:
        body = e.json_body
        err = body.get('error', {})
        logger.warning(f"{err.get('message')}")
        messages.warning(request, f"{err.get('message')}")
        return redirect("/")

    except stripe.error.RateLimitError as e:
        logger.warning(e)
        messages.warning(request, 'Too many requests made to the API at once.')
        return redirect("/")

    except stripe.error.InvalidRequestError as e:
        logger.warning(e)
        messages.warning(request, 'Invalid parameters were passed to the Stripe API.')
        return redirect("/")

    except stripe.error.AuthenticationError as e:
        logger.warning(e)
        messages.warning(request, 'Authentication API failed.')
        return redirect("/")

    except stripe.error.APIConnectionError as e:
        logger.warning(e)
        messages.warning(request, 'Network error.')
        return redirect("/")

    except stripe.error.StripeError as e:
        logger.error(e)
        messages.warning(request, 'Something went wrong. Please try again.')
        return redirect("/")

    except Exception as e:
        logger.error(e)
        messages.warning(request, 'A serious error occurred. We have been notifed.')
        return redirect("/")


def _create_order(customer: Customer, amount: Union[int, float], status: str, address: str):
    Order.objects.create(customer=customer, amount=amount, status=status, address=address)


def _create_stripe_charge(customer_stripe_id: str, amount: int, currency: str = 'usd') -> stripe.Charge:
    return stripe.Charge.create(
        customer=customer_stripe_id,
        amount=amount,
        currency=currency,
    )


def _create_stripe_customer() -> stripe.Customer:
    return stripe.Customer.create()


def _get_customer(user: str, request) -> Customer:
    try:
        return Customer.objects.get_or_create(user=user)
    except MultipleObjectsReturned as e:
        logger.error(e)
        messages.warning(request, 'A serious error occurred. We have been notifed.')
        return redirect("/")


def _retrieve_stripe_customer(customer_obj: Customer) -> stripe.Customer:
    return stripe.Customer.retrieve(customer_obj.stripe_id)


def _set_stripe_source(customer_obj: Customer, token: str, request):
    if customer_obj.stripe_id != '' and customer_obj.stripe_id is not None:
        customer = _retrieve_stripe_customer(customer_obj)
    else:
        customer = _create_stripe_customer()
        _set_stripe_id(customer_obj, customer)
    try:
        customer.sources.create(source=token)
    except stripe.error.InvalidRequestError:
        return HttpResponseRedirect(request.path_info)


def _set_stripe_id(customer_obj: Customer, customer: stripe.Customer):
    """ Sets stripe customer id to the obj of Customer model as stripe_id. """
    customer_obj.stripe_id = customer['id']
    customer_obj.save()
