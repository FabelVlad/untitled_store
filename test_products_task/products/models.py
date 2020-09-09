from decimal import Decimal

from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Count, F, Sum, ExpressionWrapper
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from model_utils import Choices
from model_utils.models import TimeStampedModel

from config import settings
from test_products_task.common.utils import generate_unique_slug


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)

    PARAMS = Choices(
        ('following', 'following'),
        ('price_to', 'price_to'),
        ('price_from', 'price_from'),
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'category_slug': self.slug})


class Product(TimeStampedModel):
    GRADE_CHOICES = Choices(
        ('base', 'base', _('Base')),
        ('standard', 'standard', _('Standard')),
        ('premium', 'premium', _('Premium')),
    )

    name = models.CharField(_('Name'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=9,
                                validators=[MinValueValidator(Decimal('0.01'))])
    description = RichTextField(_('Description'), blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(_('Image'), upload_to='products/images/%Y/%m/%d', null=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(250, 270)],
                                     format='JPEG',
                                     options={'quality': 60})
    popular = models.BooleanField(_('Popular'))
    grade = models.CharField(max_length=15, choices=GRADE_CHOICES,
                             default='standard')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail',
                       kwargs={'category_slug': self.category.slug, 'product_slug': self.slug})

    def add_comment_url(self):
        """ Returns a link to add a comment. """
        return reverse('products:add_comment',
                       kwargs={'category_slug': self.category.slug, 'product_slug': self.slug})

    def add_like_url(self):
        """ Returns a link to add a like. """
        return reverse('products:like_toggle',
                       kwargs={'product_pk': self.pk})

    def add_to_cart_url(self):
        """ Returns a link to add to cart. """
        return reverse('products:add_to_cart',
                       kwargs={'product_pk': self.pk})

    def get_recent_comments(self):
        """ Get all recent comments (for the last 24hours) """
        return self.comments.filter(modified__gte=timezone.now() - timezone.timedelta(days=1))

    def count_likes(self):
        return self.likes.count()

    @classmethod
    def get_popular_products(cls, limit: int = 10):
        """ Returns a list of [limit] items. That contains all products tagged popular and products with the most likes """
        return cls.objects.annotate(likes_count=Count('likes')).order_by('-popular', '-likes_count') \
                   .select_related('category').prefetch_related('likes')[:limit]


class Like(TimeStampedModel):
    product = models.ForeignKey(Product, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='likes',
                             on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        unique_together = (('product', 'user'), ('product', 'ip'))

    def __str__(self):
        return '{} from {}'.format(self.product, self.user or self.ip)


class Comment(TimeStampedModel):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='comments',
                             on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(blank=True, null=True)
    text = models.CharField(_('Comment'), max_length=500, help_text='max comment length 500 characters')

    class Meta:
        ordering = ['-modified']

    def __str__(self):
        return 'Comment from {}'.format(self.user or self.ip)

    def get_absolute_url(self):
        return reverse('products:product_detail',
                       kwargs={'category_slug': self.product.category.slug, 'product_slug': self.product.slug})


class HitCountBase(models.Model):
    """ Model that stores the hit totals for Page by unique Day and (unique IP or unique User). """
    hits = models.PositiveIntegerField(default=0)
    page_url = models.URLField(verbose_name='Page url')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='hits',
                             on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(blank=True, null=True)
    pub_date = models.DateField(default=timezone.localdate)

    class Meta:
        unique_together = (('user', 'page_url', 'pub_date'), ('ip', 'page_url', 'pub_date'),)

    def __str__(self):
        return '{} hits from {} to page: {}'.format(self.hits, self.user or self.ip, self.page_url)

    def increase(self):
        self.hits = F('hits') + 1
        self.save()

    @classmethod
    def hits_in_last_week(cls):
        """ Returns hit count for each day in week. """
        period = timezone.now().date() - timezone.timedelta(days=6)
        return cls.objects.filter(pub_date__gte=period).values('pub_date').annotate(Sum('hits')).order_by('pub_date')


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='carts',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='carts', on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{} from {}'.format(self.product, self.user)

    @classmethod
    def get_total_price(cls, user):
        return cls.objects.filter(user=user).select_related('product') \
            .aggregate(price=ExpressionWrapper(Sum(F('product__price') * F('product_quantity')),
                                               output_field=models.FloatField()))
