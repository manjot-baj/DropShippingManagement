from django.contrib import admin
from common.admin import BaseAdmin
from .models import Store


@admin.register(Store)
class StoreAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ("name", "email", "phone", "owner")
    search_fields = BaseAdmin.search_fields + (
        "name",
        "email",
        "phone",
    )
    list_filter = BaseAdmin.list_filter + ("city", "country")
