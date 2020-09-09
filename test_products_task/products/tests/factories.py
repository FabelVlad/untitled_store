import factory
from django.utils import timezone
from factory import fuzzy
from faker import Faker

from test_products_task.common.factories import BaseModelFactory
from test_products_task.products.models import Product, Category, Like, Comment, Cart, HitCountBase
from test_products_task.users.tests.factories import UserFactory

fake = Faker()


class CategoryFactory(BaseModelFactory):
    name = factory.Sequence(lambda n: 'category {}'.format(n))
    slug = factory.Sequence(lambda n: 'category-{}'.format(n))

    class Meta:
        model = Category


class ProductFactory(BaseModelFactory):
    name = factory.Sequence(lambda n: 'product {}'.format(n))
    slug = factory.Sequence(lambda n: 'product-{}'.format(n))
    price = factory.fuzzy.FuzzyDecimal(10, 100)
    description = fake.text()
    category = factory.SubFactory(CategoryFactory)
    image = factory.django.ImageField()
    popular = factory.Iterator((False, True,))
    grade = Product.GRADE_CHOICES.standard

    class Meta:
        model = Product


class LikeFactory(BaseModelFactory):
    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)
    ip = None

    class Meta:
        model = Like


class CommentFactory(BaseModelFactory):
    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)
    text = fake.text()
    ip = None

    class Meta:
        model = Comment


class HitCountBaseFactory(BaseModelFactory):
    hits = factory.fuzzy.FuzzyInteger(1, 402)
    page_url = factory.Sequence(lambda n: '127.0.0.{}'.format(n))
    user = factory.SubFactory(UserFactory)
    ip = None
    # ip = factory.Sequence(lambda n: '127.0.0.{}'.format(n))
    pub_date = factory.LazyFunction(timezone.localdate)

    class Meta:
        model = HitCountBase


class CartFactory(BaseModelFactory):
    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)
    product_quantity = factory.fuzzy.FuzzyInteger(1, 42)

    class Meta:
        model = Cart
