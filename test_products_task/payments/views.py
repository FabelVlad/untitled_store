from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from test_products_task.common.mixins import AdditionalMixin
from test_products_task.payments.forms import OrderPayForm
from test_products_task.payments.models import Order
from test_products_task.payments.stripe_service import make_payment
from test_products_task.products.models import Cart


class OrderPayView(FormView):
    template_name = 'payments/order_pay.html'
    form_class = OrderPayForm
    success_url = reverse_lazy('payments:order_list')
    extra_context = {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY}

    user = None
    amount = None

    @method_decorator([login_required, csrf_exempt, ])
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.amount = Cart.get_total_price(user=self.user)['price']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = self.amount
        return context

    def form_valid(self, form):
        make_payment(self.request, self.user, form, self.amount)
        return HttpResponseRedirect(self.get_success_url())


class OrderListView(AdditionalMixin, ListView):
    model = Order
    template_name = 'payments/order_list.html'

    @method_decorator([login_required, ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.user)


class OrderDetailView(AdditionalMixin, DetailView):
    model = Order
    template_name = 'payments/order_detail.html'

    @method_decorator([login_required, ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.select_related('customer__user')
