from django.core.exceptions import ValidationError
from django.db import models
import random
import string
import os


# Create your models here.
def get_product_image_upload_path(instance, filename):
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    random_num = random.randint(100, 999)
    basename, extension = os.path.splitext(filename)
    filename = f"product-{random_str}{random_num}{extension}"
    return f"images/product/{filename}"


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Product Name", db_index=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
    name = models.CharField(max_length=50, verbose_name="Product Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="price")
    vat = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="vat")
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_date',)

    def __str__(self):
        return f"{self.name}"


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    def validate_max_images(self):
        max_images = 10
        if ProductImages.objects.filter(product=self.product).count() >= max_images:
            raise ValidationError(f"Max {max_images} images allowed per product.")

    image = models.ImageField(
        upload_to=get_product_image_upload_path,
        validators=[validate_image],
        verbose_name="product_image",
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        max_images = 5
        if ProductImages.objects.filter(product=self.product).count() >= max_images:
            raise ValidationError(f"Max {max_images} images allowed per product.")
        super(ProductImages, self).save(*args, **kwargs)

    def __str__(self):
        return f"Image of {self.product.name} {self.id}"
