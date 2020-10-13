import json
from collections import OrderedDict

from braces.views import JSONResponseMixin, AjaxResponseMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.signals import request_finished
from django.db import IntegrityError, DataError
from django.db import models
from django.db.models import Sum, Case, When, IntegerField, Count, F, Q, Subquery, OuterRef, Max, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.dispatch import receiver
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse, resolve
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, FormView, TemplateView, View, CreateView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from django_filters.views import FilterView

from store_apps.common.mixins import NewArrivalsMixin, CategoryMixin, AdditionalMixin, HitCounterMixin
from store_apps.common.utils import get_ip_from_request
from store_apps.products.filters import ProductFilter
from store_apps.products.forms import CommentForm, AddToCartForm
from store_apps.products.models import Category, Product, Like, Comment, HitCountBase, Cart


class CategoryListView(NewArrivalsMixin, HitCounterMixin, ListView):
    model = Category

    @staticmethod
    def get_ordered_grade_info():
        ids = Product.objects.annotate(Count('likes', distinct=True)).filter(
            Q(grade='base', likes__count__gt=10) | Q(grade='standard', likes__count__gt=5) | Q(
                grade='premium')).values('id')
        return list(
            Product.objects.values('grade').annotate(value=Count('id', distinct=True)).filter(id__in=ids).order_by())

    def get_queryset(self):
        return Category.objects.annotate(Count('products')).prefetch_related('products__likes', 'products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grade_list'] = self.get_ordered_grade_info()
        context['popular_products_list'] = Product.get_popular_products()
        context['hit_list'] = HitCountBase.hits_in_last_week()
        return context


class CategoryDetailView(AdditionalMixin, DetailView, MultipleObjectMixin):
    model = Category
    slug_url_kwarg = 'category_slug'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        object_list = self.object.products.all().prefetch_related('likes')
        object_list = ProductFilter(self.request.GET, queryset=object_list)
        context = super().get_context_data(object_list=object_list.qs.distinct(), product_filter=object_list, **kwargs)
        return context


class ProductDetailView(AdditionalMixin, DetailView):
    count_hit = True
    model = Product
    slug_url_kwarg = 'product_slug'
    category = None

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = AddToCartForm()
        context['comment_form'] = CommentForm()
        return context


class AddCommentToProduct(CreateView):
    http_method_names = ('post',)
    form_class = CommentForm
    product = None
    user = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, slug=kwargs['product_slug'])
        if self.request.user.is_authenticated:
            self.user = self.request.user
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.product = self.product
        instance.user = self.user
        if not self.user:
            instance.ip = get_ip_from_request(self.request)
        instance.save()
        return redirect(self.product.get_absolute_url())

    def form_invalid(self, form):
        return redirect(self.product.get_absolute_url())


class LikeToggleView(AjaxResponseMixin, JSONResponseMixin, View):
    http_method_names = ('post',)

    product = None
    user = None
    ip = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_pk'])
        if self.request.user.is_authenticated:
            self.user = self.request.user
        else:
            self.ip = get_ip_from_request(self.request)
        return super().dispatch(request, *args, **kwargs)

    def post_ajax(self, request, *args, **kwargs):
        like_obj, created = Like.objects.get_or_create(product=self.product, user=self.user, ip=self.ip)
        if not created:
            like_obj.delete()
        response = {'likes': self.product.count_likes()}
        return self.render_json_response(response)

    # def delete_ajax(self, request, *args, **kwargs):
    #     like_obj = Like.objects.get(product=self.product, user=self.user, ip=self.ip)



class AddToCartView(AjaxResponseMixin, JSONResponseMixin, FormView):
    http_method_names = ('post',)
    form_class = AddToCartForm

    product = None
    user = None

    @method_decorator([login_required, csrf_exempt, ])
    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_pk'])
        self.user = self.request.user
        return super().dispatch(request, *args, **kwargs)

    def get_context_dict(self):
        """ This method create a dict for json_response (to dump). """
        storage = messages.get_messages(self.request)
        message_list = [{"message": message.message, "tags": message.tags} for message in storage]
        context_dict = {'items_in_cart': Cart.objects.filter(user=self.user).count(), 'messages': message_list}
        return context_dict

    def post_ajax(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST)
        if form.is_valid():  # todo add handle django.db.utils.DataError (too long)
            try:
                Cart.objects.create(product=self.product, user=self.user,
                                    product_quantity=form.cleaned_data['product_quantity'])
                messages.success(request, 'Added new item to cart.')
            except DataError:
                messages.error(request, 'Too many item quantity. Try to enter less.')
        return self.render_json_response(self.get_context_dict())

    # def delete_ajax(self, request, *args, **kwargs): or (class DeleteAllFromCartView and DeleteItemFromCartView)


class CartView(AdditionalMixin, TemplateView):
    template_name = 'products/cart.html'

    user = None

    @method_decorator([login_required, ])
    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_list = Cart.objects.filter(user=self.user).select_related('product')
        if cart_list:
            context['cart_list'] = cart_list
            context['total_price'] = Cart.get_total_price(user=self.user)
        return context
