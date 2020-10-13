import django_filters
from django import forms
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django_filters import FilterSet, RangeFilter
from model_utils import Choices

from store_apps.products.models import Product


class ProductFilter(FilterSet):
    LIKE_CHOICES = Choices(
        ('liked_only', 'liked_only', _('Liked only')),
        ('without_likes_only', 'without_likes_only', _('Without likes only')),
    )
    COMMENT_CHOICES = Choices(
        ('commented_only', 'commented_only', _('Commented only')),
        ('without_comments_only', 'without_comments_only', _('Without comments only')),
    )

    price = RangeFilter(label='Price')
    grade = django_filters.ChoiceFilter(label='Class', choices=Product.GRADE_CHOICES, method='filter_by_grade')
    likes = django_filters.ChoiceFilter(label='Likes', choices=LIKE_CHOICES, method='filter_by_like')
    comments = django_filters.ChoiceFilter(label='Comments', choices=COMMENT_CHOICES, method='filter_by_comment')

    class Meta:
        model = Product
        fields = ('price',)

    def filter_by_grade(self, queryset, name, value):
        return queryset.filter(**{name: value})

    def filter_by_like(self, queryset, name, value):
        if value == 'liked_only':
            return queryset.annotate(Count('likes')).filter(likes__count__gt=0)
        elif value == 'without_likes_only':
            return queryset.annotate(Count('likes')).filter(likes__count=0)

    def filter_by_comment(self, queryset, name, value):
        """ Count all existed comments (displayed or not on product detail page) """
        if value == 'commented_only':
            return queryset.annotate(Count('comments')).filter(comments__count__gt=0)
        elif value == 'without_comments_only':
            return queryset.annotate(Count('comments')).filter(comments__count=0)
