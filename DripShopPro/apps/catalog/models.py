from django.db import models
from user_profile.models import UserProfile


class Category(models.Model):
    name = models.CharField(max_length=255)
    vendor = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    catalog_display = models.BooleanField(default=False)
    store_display = models.BooleanField(default=False)
    vendor = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"

