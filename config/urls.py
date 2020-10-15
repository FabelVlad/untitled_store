# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from store_apps.products.views import CategoryListView

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name="home"),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls[:2], namespace=admin.site.urls[2])),
    url(r'^products/', include(("store_apps.products.urls", 'products'), namespace="products")),
    url(r'^users/', include(("store_apps.users.urls", 'users'), namespace="users")),
    url(r'^payments/', include(("store_apps.payments.urls", 'payments'), namespace="payments")),
]

if settings.DEBUG is False:
    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


