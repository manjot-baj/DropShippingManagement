from django.contrib import admin
from django.utils.html import format_html
from common.admin import BaseAdmin
from .models import Category, Product, ProductImage, Company, Catalog


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50"/>', obj.image.url)
        return ""

    image_preview.short_description = "Preview"


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ("name", "vendor")
    search_fields = BaseAdmin.search_fields + ("name", "vendor")


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + (
        "name",
        "category",
        "catalog_display",
        "vendor",
    )
    list_filter = BaseAdmin.list_filter + (
        "category",
        "catalog_display",
    )
    search_fields = BaseAdmin.search_fields + ("name", "vendor")
    ordering = BaseAdmin.ordering
    readonly_fields = BaseAdmin.readonly_fields
    inlines = [ProductImageInline]


@admin.register(Company)
class CompanyAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ("name", "email", "phone", "owner")
    search_fields = BaseAdmin.search_fields + (
        "name",
        "email",
        "phone",
        "owner__user__email",
    )
    list_filter = BaseAdmin.list_filter + ("city", "country")


@admin.register(Catalog)
class CatalogAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + (
        "company",
        "product",
        "price",
        "stock",
        "store_display",
    )
    search_fields = BaseAdmin.search_fields + (
        "company__name",
        "product__name",
    )
    list_filter = BaseAdmin.list_filter + (
        "store_display",
        "company",
    )
