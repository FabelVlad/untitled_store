from __future__ import unicode_literals

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='customer', null=True, on_delete=models.SET_NULL)
    stripe_id = models.CharField(_('Stripe id'), max_length=50, blank=True)

    def __str__(self):
        return f'{self.user}'


class Order(TimeStampedModel):
    STATUSES = Choices(
        ('succeeded', _('Succeeded')),
        ('pending', _('Pending')),
        ('failed', _('Failed')),
    )

    customer = models.ForeignKey(Customer, related_name='orders', null=True, on_delete=models.SET_NULL)
    amount = models.PositiveIntegerField(_('Amount'))
    status = models.CharField(_('Status'), max_length=15, choices=STATUSES, default=STATUSES.pending)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'Order {self.id} by {self.customer}'

    def get_absolute_url(self):
        return reverse('payments:order_detail', kwargs={'pk': self.pk})
