from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from config import settings
from store_apps.products.models import Like, Product, Comment, Cart

User = get_user_model()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AddToCartForm(forms.Form):
    product_quantity = forms.DecimalField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
