from unittest.case import skipUnless

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from test_products_task.products.models import Product
from test_products_task.products.tests.factories import CategoryFactory, ProductFactory, LikeFactory, CommentFactory
from test_products_task.users.tests.factories import UserFactory

User = get_user_model()


class CategoryListViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory()
        cls.category_2 = CategoryFactory()
        cls.user = UserFactory()
        cls.product = ProductFactory()
        cls.url = reverse('products:category_list')

    def create_likes_by_0(self):
        # base products
        self.product_base_20_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.base)
        LikeFactory.create_batch(1, product=self.product_base_20_likes)
        self.product_base_5_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.base)
        LikeFactory.create_batch(1, product=self.product_base_5_likes)
        self.product_base_2_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.base)
        LikeFactory.create_batch(1, product=self.product_base_2_likes)

        # standard
        self.product_standard_20_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.standard)
        LikeFactory.create_batch(1, product=self.product_standard_20_likes)
        self.product_standard_5_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.standard)
        LikeFactory.create_batch(1, product=self.product_standard_5_likes)
        self.product_standard_2_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.standard)
        LikeFactory.create_batch(1, product=self.product_standard_2_likes)

        # premium
        self.product_premium_20_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.premium)
        self.product_premium_5_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.premium)
        self.product_premium_2_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.premium)

    def create_likes_by_1(self):
        # base products
        self.product_base_20_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.base)
        LikeFactory.create_batch(20, product=self.product_base_20_likes)
        self.product_base_5_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.base)
        LikeFactory.create_batch(5, product=self.product_base_5_likes)
        self.product_base_2_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.base)
        LikeFactory.create_batch(2, product=self.product_base_2_likes)

        # standard
        self.product_standard_20_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.standard)
        LikeFactory.create_batch(20, product=self.product_standard_20_likes)
        self.product_standard_5_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.standard)
        LikeFactory.create_batch(5, product=self.product_standard_5_likes)
        self.product_standard_2_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.standard)
        LikeFactory.create_batch(2, product=self.product_standard_2_likes)

        # premium
        self.product_premium_20_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.premium)
        LikeFactory.create_batch(20, product=self.product_premium_20_likes)
        self.product_premium_5_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.premium)
        LikeFactory.create_batch(5, product=self.product_premium_5_likes)
        self.product_premium_2_likes = ProductFactory(category=self.category, grade=Product.GRADE_CHOICES.premium)
        LikeFactory.create_batch(2, product=self.product_premium_2_likes)

    def create_likes_by_3(self):
        # base products
        self.product_base_20_likes = ProductFactory(grade=Product.GRADE_CHOICES.base)
        LikeFactory.create_batch(20, product=self.product_base_20_likes)
        self.product_base_5_likes = ProductFactory(grade=Product.GRADE_CHOICES.base)
        LikeFactory.create_batch(20, product=self.product_base_5_likes)
        self.product_base_2_likes = ProductFactory(grade=Product.GRADE_CHOICES.base)
        LikeFactory.create_batch(10, product=self.product_base_2_likes)

        # standard
        self.product_standard_20_likes = ProductFactory(grade=Product.GRADE_CHOICES.standard)
        LikeFactory.create_batch(20, product=self.product_standard_20_likes)
        self.product_standard_5_likes = ProductFactory(grade=Product.GRADE_CHOICES.standard)
        LikeFactory.create_batch(20, product=self.product_standard_5_likes)
        self.product_standard_2_likes = ProductFactory(grade=Product.GRADE_CHOICES.standard)
        LikeFactory.create_batch(5, product=self.product_standard_2_likes)

        # premium
        self.product_premium_20_likes = ProductFactory(grade=Product.GRADE_CHOICES.premium)
        LikeFactory.create_batch(2, product=self.product_premium_20_likes)
        self.product_premium_5_likes = ProductFactory(grade=Product.GRADE_CHOICES.premium)
        LikeFactory.create_batch(2, product=self.product_premium_5_likes)
        self.product_premium_2_likes = ProductFactory(grade=Product.GRADE_CHOICES.premium)
        LikeFactory.create_batch(2, product=self.product_premium_2_likes)

    @skipUnless(hasattr(Product, 'grade'), 'No need unless grade is added')
    def test_grade_condition_like_empty(self):
        response = self.client.get(self.url)
        grade_list = []
        self.assertEqual(response.context_data['grade_list'], grade_list)

    @skipUnless(hasattr(Product, 'grade'), 'No need unless grade is added')
    def test_grade_condition_like_0(self):
        self.create_likes_by_0()
        response = self.client.get(self.url)

        grades = Product.GRADE_CHOICES
        grade_list = [{'grade': grades.premium, 'value': 3}]
        self.assertEqual(response.context_data['grade_list'], grade_list)

    @skipUnless(hasattr(Product, 'grade'), 'No need unless grade is added')
    def test_grade_condition_like_1(self):
        self.create_likes_by_1()
        response = self.client.get(self.url)

        grades = Product.GRADE_CHOICES
        grade_list = [
            {'grade': grades.base, 'value': 1},
            {'grade': grades.premium, 'value': 3},
            {'grade': grades.standard, 'value': 1},
        ]
        self.assertEqual(response.context_data['grade_list'], grade_list)

    @skipUnless(hasattr(Product, 'grade'), 'No need unless grade is added')
    def test_grade_condition_like_3(self):
        self.create_likes_by_3()
        response = self.client.get(self.url)

        grades = Product.GRADE_CHOICES
        grade_list = [
            {'grade': grades.base, 'value': 2},
            {'grade': grades.premium, 'value': 3},
            {'grade': grades.standard, 'value': 2},
        ]
        self.assertEqual(response.context_data['grade_list'], grade_list)

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)


class CategoryDetailViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory()

        cls.product_1 = ProductFactory(category=cls.category, price=10, grade='base')
        cls.product_2 = ProductFactory(category=cls.category, price=20, grade='base')
        cls.product_3 = ProductFactory(category=cls.category, price=30, grade='base')
        cls.product_4 = ProductFactory(category=cls.category, price=40, grade='base')
        cls.product_5 = ProductFactory(category=cls.category, price=50, grade='standard')
        cls.product_6 = ProductFactory(category=cls.category, price=60, grade='standard')
        cls.product_7 = ProductFactory(category=cls.category, price=70, grade='standard')
        cls.product_8 = ProductFactory(category=cls.category, price=80, grade='standard')
        cls.product_9 = ProductFactory(category=cls.category, price=90, grade='standard')
        cls.product_10 = ProductFactory(category=cls.category, price=100, grade='premium')
        cls.product_11 = ProductFactory(category=cls.category, price=110, grade='premium')
        cls.product_12 = ProductFactory(category=cls.category, price=111, grade='premium')

        cls.user = UserFactory()

        LikeFactory(product=cls.product_1, user=cls.user)
        LikeFactory(product=cls.product_2, user=cls.user)
        LikeFactory(product=cls.product_3, user=cls.user)
        LikeFactory(product=cls.product_4, user=None, ip='127.1.1.1')

        CommentFactory(product=cls.product_3, user=cls.user)
        CommentFactory(product=cls.product_4, user=None, ip='127.1.1.1')
        CommentFactory(product=cls.product_5, user=cls.user)
        CommentFactory(product=cls.product_6, user=None, ip='127.1.1.1')

        cls.url = reverse('products:category_detail', args=(cls.category.slug,))

    def test_detail_page(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue('new_arrivals' in response.context)
        self.assertTrue(len(response.context['new_arrivals']) == 1)
        self.assertTrue('category_list' in response.context)
        self.assertTrue(len(response.context['category_list']) == 1)

    def test_invalid_detail_page(self):
        response = self.client.get(reverse('products:category_detail', args=('invalid.category.slug',)))
        self.assertEquals(response.context.get('exception'), 'No category found matching the query')
        self.assertEquals(response.status_code, 404)

    def test_filter_price_to(self):
        response = self.client.get(f'{self.url}?price_min=&price_max=45')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is False)
        self.assertTrue('object_list' in response.context)
        self.assertTrue(len(response.context['object_list']) == 4)

    def test_filter_price_from(self):
        response = self.client.get(f'{self.url}?price_min=90.01')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is False)
        self.assertTrue('object_list' in response.context)
        self.assertTrue(len(response.context['object_list']) == 3)

    def test_filter_price_from_and_to(self):
        response = self.client.get(f'{self.url}?price_min=20.01&price_max=50.01')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is False)
        self.assertTrue('object_list' in response.context)
        self.assertTrue(len(response.context['object_list']) == 3)

    def test_filter_empty(self):
        response = self.client.get(f'{self.url}?price_min=&price_max=&grade=&likes=&comments=')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue('object_list' in response.context)
        self.assertTrue(len(response.context['object_list']) == 4)

    def test_user_filter_by_like(self):
        response = self.client.get(f'{self.url}?likes=liked_only')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is False)
        self.assertTrue('object_list' in response.context)
        self.assertTrue(len(response.context['object_list']) == 4)

    def test_user_filter_by_comment(self):
        response = self.client.get(f'{self.url}?comments=commented_only')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is False)
        self.assertTrue('object_list' in response.context)
        self.assertTrue(len(response.context['object_list']) == 4)

    def test_user_filter_by_like_and_comment(self):
        response = self.client.get(f'{self.url}?likes=liked_only&comments=commented_only')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is False)
        self.assertTrue('object_list' in response.context)
        self.assertTrue(len(response.context['object_list']) == 2)

    def test_user_filter_by_grade_base(self):
        response = self.client.get(f'{self.url}?grade=base')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is False)
        self.assertTrue('object_list' in response.context)
        self.assertTrue(len(response.context['object_list']) == 4)

    def test_user_filter_by_grade_standard(self):
        response = self.client.get(f'{self.url}?grade=standard')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue('object_list' in response.context)
        self.assertTrue(len(response.context['object_list']) == 4)

    def test_user_filter_by_grade_premium(self):
        response = self.client.get(f'{self.url}?grade=premium')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is False)
        self.assertTrue('object_list' in response.context)
        self.assertTrue(len(response.context['object_list']) == 3)


class LikeToggleTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory()
        cls.product = ProductFactory(category=cls.category, price=30)

        cls.user = UserFactory(password='passuser1')
        cls.url_like = reverse('products:like_toggle', args=(cls.product.id,))

    def test_invalid_product(self):
        response = self.client.get(reverse('products:like_toggle', args=(900,)))
        self.assertEquals(response.context.get('exception'), 'No Product matches the given query.')
        self.assertEquals(response.status_code, 404)

    def test_anonymous_like_product(self):
        self.client.post(self.url_like, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(self.product.likes.count(), 1)
        self.assertEquals(self.product.likes.filter(user=self.user).count(), 0)

    def test_user_like_product(self):
        self.client.force_login(self.user)
        self.client.post(self.url_like, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(self.product.likes.count(), 1)
        self.assertEquals(self.product.likes.filter(user=self.user).count(), 1)


class DislikeToggleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory()
        cls.product = ProductFactory(category=cls.category, price=30)

        cls.user = UserFactory(password='passuser1')
        cls.url_like = reverse('products:like_toggle', args=(cls.product.id,))

    def setUp(self):
        """ one like for authenticated user and one like for anonymous user (represented by ip) """
        self.client.post(self.url_like, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        LikeFactory(product=self.product, user=self.user)

    def test_anonymous_dislike_product(self):
        self.client.post(self.url_like, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(self.product.likes.count(), 1)  # exist one like by user
        self.assertEquals(self.product.likes.filter(user=None).count(), 0)

    def test_user_dislike_product(self):
        self.client.force_login(self.user)
        self.client.post(self.url_like, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(self.product.likes.count(), 1)  # exist one like by ip
        self.assertEquals(self.product.likes.filter(user=self.user).count(), 0)
