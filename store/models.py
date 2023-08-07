from django.db import models

from product.models import Product


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=28)
    city = models.CharField(max_length=28)
    zipCode = models.CharField(max_length=5)
    address = models.CharField(max_length=150, verbose_name="Store Address")


class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_product_store")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="store_product")
