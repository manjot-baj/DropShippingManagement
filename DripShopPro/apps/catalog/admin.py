from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Catalog


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

    def image_preview(self, obj):
        return (
            format_html('<img src="{}" width="50" height="50"/>', obj.image.url)
            if obj.image
            else ""
        )

    image_preview.allow_tags = True
    image_preview.short_description = "Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "vendor")
    search_fields = ("name", "vendor")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "stock",
        "created_at",
        "updated_at",
        "catalog_display",
        "store_display",
        "vendor",
    )
    list_filter = (
        "category",
        "created_at",
        "updated_at",
        "catalog_display",
        "store_display",
    )
    search_fields = ("name", "vendor")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProductImageInline]


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at", "updated_at", "vendor")
    list_filter = (
        "is_active",
        "created_at",
    )
    search_fields = ("title", "vendor")
    filter_horizontal = ("products",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
