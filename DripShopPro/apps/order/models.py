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
