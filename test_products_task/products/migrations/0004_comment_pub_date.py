# Generated by Django 2.2 on 2020-07-26 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200725_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default='2020-07-26 17:45:11.636915', verbose_name='Comment publication date'),
            preserve_default=False,
        ),
    ]
