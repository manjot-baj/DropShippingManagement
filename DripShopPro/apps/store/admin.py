from django.contrib import admin
from common.admin import BaseAdmin
from .models import Store, StoreProduct


@admin.register(Store)
class StoreAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ("name", "email", "phone", "owner")
    search_fields = BaseAdmin.search_fields + (
        "name",
        "email",
        "phone",
    )
    list_filter = BaseAdmin.list_filter + ("city", "country")


@admin.register(StoreProduct)
class StoreProductAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + (
        "get_store_name",
        "get_product_name",
        "margin",
        "get_store_owner",
        "get_product_company_owner",
    )
    search_fields = BaseAdmin.search_fields + (
        "store__name",
        "inventory__product__name",
        "store__owner__username",
        "inventory__product__vendor__username",
    )
    list_filter = BaseAdmin.list_filter + (
        "store__name",
        "store__owner",
        "inventory__product__vendor",
    )

    # Optional: To avoid dot notation in list_display
    def get_store_name(self, obj):
        return obj.store.name

    get_store_name.short_description = "Store Name"

    def get_product_name(self, obj):
        return obj.inventory.product.name

    get_product_name.short_description = "Product Name"

    def get_store_owner(self, obj):
        return f"{obj.store.owner.first_name} {obj.store.owner.last_name}"

    get_store_owner.short_description = "Store Owner"

    def get_product_company_owner(self, obj):
        return f"{obj.inventory.product.vendor.first_name} {obj.inventory.product.vendor.last_name}"

    get_product_company_owner.short_description = "Product Vendor"
