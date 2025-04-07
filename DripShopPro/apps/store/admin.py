from django.contrib import admin
from django.utils.html import format_html
from common.admin import BaseAdmin
from .models import Store


@admin.register(Store)
class StoreAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ("name", "email", "phone", "owner")
    search_fields = BaseAdmin.search_fields + (
        "name",
        "email",
        "phone",
        "owner__user__email",
    )
    list_filter = BaseAdmin.list_filter + ("city", "country")
