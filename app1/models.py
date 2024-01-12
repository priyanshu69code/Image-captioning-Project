# models.py

from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    product_id = models.IntegerField(primary_key=True, unique=True)
    credit_grant = models.PositiveIntegerField()
    price = models.PositiveIntegerField(null=True)
    ben1 = models.CharField(max_length=255, null=True, blank=True)
    ben2 = models.CharField(max_length=255, null=True, blank=True)
    ben3 = models.CharField(max_length=255, null=True, blank=True)
    ben4 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class SubscriptionLevel(models.Model):
    purchase_date = models.DateTimeField(auto_now_add=True)
    subscribed_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    credit_left = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscribed_product.name}"


class History(models.Model):
    image_name = models.CharField(max_length=255)
    generation_datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.image_name} - {self.user.username}"
