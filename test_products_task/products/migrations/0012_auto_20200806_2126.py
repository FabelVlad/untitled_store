# Generated by Django 2.2 on 2020-08-06 18:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0011_auto_20200806_2117'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='hitcountbase',
            unique_together={('ip', 'page_url', 'pub_date'), ('user', 'page_url', 'pub_date')},
        ),
    ]
