from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from store_apps.products.tests.factories import LikeFactory, CommentFactory
from store_apps.users.tests.factories import UserFactory

User = get_user_model()

