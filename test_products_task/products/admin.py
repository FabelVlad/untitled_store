from django.contrib import admin

from test_products_task.products.models import Category, Product, Like, Comment, HitCountBase, Cart


def make_popular(modeladmin, request, queryset):
    queryset.update(popular=True)


make_popular.short_description = "Mark selected product as popular"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    actions = (make_popular,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    view_on_site = False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(HitCountBase)
class HitCountBaseAdmin(admin.ModelAdmin):
    list_display = ('hits', 'user', 'ip', 'page_url', 'pub_date',)
    readonly_fields = ('hits', 'user', 'ip', 'page_url',)
    view_on_site = False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    view_on_site = False
