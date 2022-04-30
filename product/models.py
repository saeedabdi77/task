from django.db import models
from django.db.models.signals import pre_save
import random
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


# class Subcategory(models.Model):
#     category = models.ForeignKey(Category,
#                                  related_name='category',
#                                  on_delete=models.CASCADE)
#     title = models.CharField(max_length=50)
#
#     class Meta:
#         verbose_name_plural = 'subcategories'
#
#     def __str__(self):
#         return self.title


class CommonFeatures(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomManager(models.Manager):

    def check_availability(self, brand=None, category=None):
        if brand:
            return super().get_queryset().filter(brand=brand).filter(quantity__gt=10)
        elif category:
            return super().get_queryset().filter(categories=category).filter(quantity__gt=10)
        else:
            return super().get_queryset().filter(quantity__gt=10)


class ProductTypeOne(CommonFeatures):
    slug = models.SlugField(max_length=100, blank=True)
    objects = CustomManager()

    def __str__(self):
        return self.name


class ProductTypeTwo(CommonFeatures):
    slug = models.SlugField(max_length=100, blank=True)
    objects = CustomManager()

    def __str__(self):
        return self.name


class ProductTypeThree(CommonFeatures):
    slug = models.SlugField(max_length=100, blank=True)
    objects = CustomManager()

    def __str__(self):
        return self.name


def random_number_generator():
    return str(random.randint(100000, 999999))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)
    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{random}".format(
            slug=slug, random=random_number_generator())

        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=ProductTypeOne)
pre_save.connect(pre_save_receiver, sender=ProductTypeTwo)
pre_save.connect(pre_save_receiver, sender=ProductTypeThree)
