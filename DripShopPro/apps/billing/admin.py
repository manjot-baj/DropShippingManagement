from django.contrib import admin
from billing.models import PurchaseOrderInvoice

from django.contrib import admin
from .models import PurchaseOrderInvoice


@admin.register(PurchaseOrderInvoice)
class PurchaseOrderInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_item",
        "sender",
        "reciever",
        "status",
        "is_payment_done",
        "is_invoiced",
        "invoice_date",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "is_payment_done", "is_invoiced")
    search_fields = (
        "id",
        "sender__user__email",
        "reciever__user__email",
        "order_item__id",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("sender", "reciever", "order_item")
        )
