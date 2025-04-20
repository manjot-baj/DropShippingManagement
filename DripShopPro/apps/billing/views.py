import logging
import traceback
from django.shortcuts import render, redirect
from user_profile.middlewares import RoleRequiredMixin
from store.Utils.middlewares import StoreRequiredMixin
from django.views import View
from django.contrib import messages
from order.models import OrderItem
from common.functions import PO_STATUS_COLORS
from billing.models import PurchaseOrderInvoice

logger = logging.getLogger("error_log")


class CreatePurchaseOrderView(RoleRequiredMixin, StoreRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, order_item_id, *args, **kwargs):
        try:
            order_item = OrderItem.objects.get(pk=order_item_id, is_deleted=False)
            if not PurchaseOrderInvoice.objects.filter(
                order_item=order_item,
                sender=order_item.merchant,
                reciever=order_item.vendor,
            ).exists():
                po = PurchaseOrderInvoice(
                    order_item=order_item,
                    sender=order_item.merchant,
                    reciever=order_item.vendor,
                )
                po.save()
            return redirect("merchant_purchase_order_list")

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while creating PO.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error while creating PO."},
                status=500,
            )


class MerchantPurchaseOrderListView(RoleRequiredMixin, StoreRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, *args, **kwargs):
        try:
            purchase_order_list = PurchaseOrderInvoice.objects.filter(
                sender__user=request.user
            )
            po_list = []
            for each in purchase_order_list:
                order_item = each.order_item
                total_amount = float(order_item.total_amount)
                vendor_name = (
                    order_item.merchant.first_name + " " + order_item.merchant.last_name
                )
                vendor_company_name = order_item.product.inventory.company.name
                po_list.append(
                    {
                        "po_id": each.pk,
                        "po_date": str(each.created_at.date()),
                        "po_no": order_item.tracking_id,
                        "vendor_name": vendor_name,
                        "vendor_company_name": vendor_company_name,
                        "total_amount": total_amount,
                        "status": each.status,
                        "status_color": PO_STATUS_COLORS[each.status],
                    }
                )

            return render(
                request,
                "merchant/billing/purchase_order_list.html",
                {
                    "po_list": po_list,
                },
            )

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while listing PO.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error while listing PO."},
                status=500,
            )
