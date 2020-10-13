from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'store_apps.products'

    def ready(self):
        import store_apps.products.signals
