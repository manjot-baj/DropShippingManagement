from django.contrib import admin
from common.admin import BaseAdmin
from .models import WishList, Cart, Order, OrderItem


@admin.register(WishList)
class WishListAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ("product", "owner")
    search_fields = BaseAdmin.search_fields + (
        "product__name",
        "owner__user__email",
    )
    list_filter = BaseAdmin.list_filter + ("product",)


@admin.register(Cart)
class CartAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ("product", "owner", "quantity")
    search_fields = BaseAdmin.search_fields + (
        "product__name",
        "owner__user__email",
    )
    list_filter = BaseAdmin.list_filter + ("product",)


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + (
        "order_id",
        "owner",
        "grand_total",
        "city",
        "state",
        "postal_code",
        "country",
    )
    search_fields = BaseAdmin.search_fields + (
        "order_id",
        "owner__user__email",
        "city",
        "state",
        "postal_code",
    )
    list_filter = BaseAdmin.list_filter + ("state", "country")
    readonly_fields = BaseAdmin.readonly_fields + ("order_id",)


@admin.register(OrderItem)
class OrderItemAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + (
        "parent",
        "product",
        "store_price",
        "vendor_price",
        "merchant_margin_price",
        "merchant_margin",
        "status",
        "quantity",
        "total_amount",
        "confirmed_date",
        "shipping_date",
        "arrival_date",
        "delivery_date",
    )
    search_fields = BaseAdmin.search_fields + (
        "parent__order_id",
        "product__name",
    )
    list_filter = BaseAdmin.list_filter + ("status",)
    readonly_fields = BaseAdmin.readonly_fields + (
        "store_price",
        "vendor_price",
        "merchant_margin_price",
    )
