import csv
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models.expressions import F

from test_products_task.products.models import Product

User = get_user_model()


class Command(BaseCommand):
    help = "Generate a CSV file with products with fields: 'id', 'name', 'comment_count', 'like_count'."
    fields = ['id', 'name', 'comment_count', 'like_count']

    comment_help = 'minimum number of comments, default value 0'
    like_help = 'minimum number of likes, default value 0'
    path_help = 'file destination'

    def add_arguments(self, parser):
        parser.add_argument('-comment', help=self.comment_help, type=int, nargs='?', default=0)
        parser.add_argument('-like', help=self.like_help, type=int, nargs='?', default=0)
        parser.add_argument('-path', help=self.path_help, type=str, nargs='?', default=None)

    def handle(self, *args, **options):
        comment_count = options['comment'] if options['comment'] else 0
        like_count = options['like'] if options['like'] else 0
        path = options['path']
        file_default_path = f'{os.path.dirname(__file__)}/products.csv'
        message = 'Generation has been finished.'

        queryset = Product.objects.annotate(
            like_count=Count(F('likes'), distinct=True),
            comment_count=Count(F('comments'), distinct=True)
        ).filter(
            like_count__gte=like_count,
            comment_count__gte=comment_count,
        ).values(*self.fields).iterator()

        if not path:
            path = file_default_path

        try:
            with open(path, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.fields)
                for element in queryset:
                    writer.writerow([element[field_name] for field_name in self.fields])
        except FileNotFoundError as e:
            message = f'{e.strerror}.'
        except PermissionError as e:
            message = f'{e.strerror}.'

        self.stdout.write(message)
