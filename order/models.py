from django.db import models

from product.models import Product
from user.models import Profile


class Cargo(models.Model):
    name = models.CharField(max_length=50, db_index=True, unique=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="amount")
    vat = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="vat")


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="order_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_product")
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name="order_cargo")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_same_billing = models.BooleanField(default=True)
    order_status = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Order Status', choices=(
            (0, 'Prepare'),
            (1, 'Sended'),
            (2, 'Deliver'),
            (3, 'Recived'),
        )
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")


class OrderBilling(models.Model):
    order = models.ForeignKey(Order, related_name="order_billing_order")
    full_name = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=13, verbose_name="Billing Number", unique=True)
    country = models.CharField(max_length=28)
    city = models.CharField(max_length=28)
    zipCode = models.CharField(max_length=5)
    address = models.CharField(max_length=150, verbose_name="Billing Address")
