from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.db.models import Max, Count
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, CreateView
from django.views.generic.base import View

from test_products_task.common.utils import get_ip_from_request
from test_products_task.products.models import Product, Category, HitCountBase
# from test_products_task.products.signals import count_pages_hits_signal
from test_products_task.products.signals import count_pages_hits_signal


class AjaxFormViewMixin(AjaxResponseMixin, JSONResponseMixin):

    def form_invalid(self, form):
        return self.render_json_response(form.errors, status=400)
        # if self.request.is_ajax():
        #     return self.render_json_response(form.errors, status=400)
        # return super(AjaxResponseMixin, self).form_invalid(form)


class NewArrivalsMixin(object):
    """ Adds (to template) a list of products (latest) one from each category. """

    @staticmethod
    def get_new_arrivals():
        ids = Category.objects.annotate(Max('products__id')).values('products__id__max').order_by('name')
        return Product.objects.filter(id__in=ids)

    def get_context_data(self, **kwargs):
        context = super(NewArrivalsMixin, self).get_context_data(**kwargs)
        context['new_arrivals'] = self.get_new_arrivals()
        return context


class CategoryMixin(object):
    """ Adds (to template) a category and quantity of products for each. """

    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.annotate(Count('products'))
        return context


class HitCounterMixin(object):
    """ Counts the number of hits. """
    def dispatch(self, request, *args, **kwargs):
        count_pages_hits_signal.send(sender=self.__class__, request=request)
        return super(HitCounterMixin, self).dispatch(request, *args, **kwargs)


class AdditionalMixin(CategoryMixin, NewArrivalsMixin, HitCounterMixin):
    pass
