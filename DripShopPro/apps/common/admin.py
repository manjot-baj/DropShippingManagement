from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    list_display = ("id", "is_deleted", "created_at", "updated_at")
    list_filter = ("is_deleted", "created_at")
    search_fields = ("id",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
