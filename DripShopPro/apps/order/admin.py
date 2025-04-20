from django.contrib import admin
from .models import WishList, Cart, Order, OrderItem


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "owner", "created_at", "updated_at")
    search_fields = ("owner__user__email", "product__name")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "owner", "quantity", "created_at", "updated_at")
    search_fields = ("owner__user__email", "product__name")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_id",
        "owner",
        "grand_total",
        "city",
        "state",
        "postal_code",
        "is_closed",
        "created_at",
        "updated_at",
    )
    search_fields = ("order_id", "owner__user__email", "city", "state")
    list_filter = ("state", "is_closed", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "parent",
        "product",
        "merchant",
        "vendor",
        "status",
        "total_amount",
        "quantity",
        "confirmed_date",
        "shipping_date",
        "arrival_date",
        "delivery_date",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "parent__order_id",
        "product__name",
        "merchant__user__email",
        "vendor__user__email",
    )
    list_filter = ("status", "confirmed_date", "shipping_date", "delivery_date")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("parent", "product", "merchant", "vendor")
        )
