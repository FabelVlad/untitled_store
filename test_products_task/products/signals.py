import os
import shutil

from django.db.models.signals import pre_delete
from django.utils import timezone

from test_products_task.common.utils import get_ip_from_request
from test_products_task.products.models import Product, HitCountBase
from django.dispatch import receiver, Signal


@receiver(pre_delete, sender=Product)
def delete_images(sender, instance, **kwargs):
    image_path = instance.image.path
    image_thumbnail_dir_path = '\\'.join(instance.image_thumbnail.path.split('\\')[:-1])

    if os.path.exists(image_path):
        os.remove(image_path)
    if os.path.exists(image_thumbnail_dir_path):
        shutil.rmtree(image_thumbnail_dir_path)


count_pages_hits_signal = Signal(providing_args=('request',))


@receiver(count_pages_hits_signal)
def count_pages_hits(sender, request, **kwargs):
    user = None
    ip = None
    url = request.get_full_path().split('?')[0]
    if request.user.is_authenticated:
        user = request.user
    else:
        ip = get_ip_from_request(request)
    obj, created = HitCountBase.objects.get_or_create(page_url=url, user=user, ip=ip, pub_date=timezone.localdate())
    obj.increase()
