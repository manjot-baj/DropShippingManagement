from django.db import models
from common.models import BaseModel
from user_profile.models import UserProfile


class Category(BaseModel):
    name = models.CharField(max_length=255)
    vendor = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    catalog_display = models.BooleanField(default=False)
    vendor = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.name


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.product.name}"


class Company(BaseModel):
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="company_owner",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, unique=True)
    # contact
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    # address
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    # other
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Catalog(BaseModel):
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="company_catalog",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CatalogProduct(BaseModel):
    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        related_name="catalog",
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="catalog_product",
        null=True,
        blank=True,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    store_display = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)
