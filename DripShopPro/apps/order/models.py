from django.db import models
from common.models import BaseModel
from store.models import StoreProduct
from user_profile.models import UserProfile


class WishList(BaseModel):
    product = models.ForeignKey(
        StoreProduct,
        on_delete=models.CASCADE,
        related_name="wishlist_product",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="wishlist_owner",
        null=True,
        blank=True,
    )


class Cart(BaseModel):
    product = models.ForeignKey(
        StoreProduct,
        on_delete=models.CASCADE,
        related_name="cart_product",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="cart_owner",
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(default=1)


class Order(BaseModel):
    INDIAN_STATES = [
        ("Andhra Pradesh", "Andhra Pradesh"),
        ("Arunachal Pradesh", "Arunachal Pradesh"),
        ("Assam", "Assam"),
        ("Bihar", "Bihar"),
        ("Chhattisgarh", "Chhattisgarh"),
        ("Goa", "Goa"),
        ("Gujarat", "Gujarat"),
        ("Haryana", "Haryana"),
        ("Himachal Pradesh", "Himachal Pradesh"),
        ("Jharkhand", "Jharkhand"),
        ("Karnataka", "Karnataka"),
        ("Kerala", "Kerala"),
        ("Madhya Pradesh", "Madhya Pradesh"),
        ("Maharashtra", "Maharashtra"),
        ("Manipur", "Manipur"),
        ("Meghalaya", "Meghalaya"),
        ("Mizoram", "Mizoram"),
        ("Nagaland", "Nagaland"),
        ("Odisha", "Odisha"),
        ("Punjab", "Punjab"),
        ("Rajasthan", "Rajasthan"),
        ("Sikkim", "Sikkim"),
        ("Tamil Nadu", "Tamil Nadu"),
        ("Telangana", "Telangana"),
        ("Tripura", "Tripura"),
        ("Uttar Pradesh", "Uttar Pradesh"),
        ("Uttarakhand", "Uttarakhand"),
        ("West Bengal", "West Bengal"),
        ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
        ("Chandigarh", "Chandigarh"),
        (
            "Dadra and Nagar Haveli and Daman and Diu",
            "Dadra and Nagar Haveli and Daman and Diu",
        ),
        ("Delhi", "Delhi"),
        ("Jammu and Kashmir", "Jammu and Kashmir"),
        ("Ladakh", "Ladakh"),
        ("Lakshadweep", "Lakshadweep"),
        ("Puducherry", "Puducherry"),
    ]

    order_id = models.CharField(max_length=255, unique=True)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=float(0)
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(
        max_length=100, choices=INDIAN_STATES, blank=True, null=True
    )
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, default="India")
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="order_owner",
        null=True,
        blank=True,
    )
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class OrderItem(BaseModel):
    
    ORDER_STATUS = [
        ("Placed", "Placed"),
        ("Confirmed", "Confirmed"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    ]
    parent = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_item_related",
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        StoreProduct,
        on_delete=models.CASCADE,
        related_name="order_item_product",
        null=True,
        blank=True,
    )
    tracking_id = models.CharField(max_length=255, blank=True, null=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=float(0)
    )
    store_price = models.DecimalField(max_digits=10, decimal_places=2, default=float(0))
    vendor_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=float(0)
    )
    merchant_margin_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=float(0)
    )
    merchant_margin = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=100, choices=ORDER_STATUS, blank=True, null=True, default="Placed"
    )
    quantity = models.PositiveIntegerField(default=1)

    confirmed_date = models.DateTimeField(null=True, blank=True)
    shipping_date = models.DateTimeField(null=True, blank=True)
    arrival_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    merchant = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="order_item_merchant",
        null=True,
        blank=True,
    )
    vendor = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="order_item_vendor",
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.pk)
