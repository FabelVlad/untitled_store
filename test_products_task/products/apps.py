from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'test_products_task.products'

    def ready(self):
        import test_products_task.products.signals
