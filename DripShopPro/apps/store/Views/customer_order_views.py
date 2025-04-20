import logging
import traceback
from django.shortcuts import render
from user_profile.middlewares import RoleRequiredMixin
from store.Utils.middlewares import StoreRequiredMixin
from django.views import View
from django.contrib import messages
from order.models import OrderItem
from common.functions import ORDER_STATUS_COLORS
from billing.models import PurchaseOrderInvoice

logger = logging.getLogger("error_log")


class CustomerOrderListView(RoleRequiredMixin, StoreRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, *args, **kwargs):
        try:
            customer_order_data = []

            customer_orders = OrderItem.objects.filter(
                merchant__user=request.user, is_deleted=False
            )

            for order_item in customer_orders:
                total_amount = float(order_item.total_amount)
                customer_order_data.append(
                    {
                        "order_date": str(order_item.parent.created_at.date()),
                        "order_item_id": order_item.pk,
                        "tracking_id": order_item.tracking_id,
                        "product": order_item.product.inventory.product.name,
                        "quantity": int(order_item.quantity),
                        "total_amount": total_amount,
                        "store_price": order_item.store_price,
                        "status": order_item.status,
                        "status_color": ORDER_STATUS_COLORS[order_item.status],
                        "is_po_created": (
                            "Yes"
                            if PurchaseOrderInvoice.objects.filter(
                                order_item=order_item
                            ).exists()
                            else "No"
                        ),
                    }
                )
            return render(
                request,
                "merchant/customers/customer_order.html",
                {
                    "customer_order_data": customer_order_data,
                },
            )

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching orders.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error fetching orders."},
                status=500,
            )


class CustomerOrderDetailView(RoleRequiredMixin, StoreRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, order_item_id, *args, **kwargs):
        try:
            order_item = OrderItem.objects.get(pk=order_item_id, is_deleted=False)
            total_amount = float(order_item.total_amount)
            merchant_profit_amount = order_item.merchant_margin_price * int(
                order_item.quantity
            )
            vendor_payment_amount = order_item.vendor_price * int(order_item.quantity)

            customer_name = (
                order_item.parent.owner.first_name
                + " "
                + order_item.parent.owner.last_name
            )
            customer_address = order_item.parent.address
            customer_city = order_item.parent.city
            customer_state = order_item.parent.state
            customer_postal_code = order_item.parent.postal_code
            customer_country = order_item.parent.country
            customer_mobile_no = order_item.parent.owner.mobile_no
            customer_email = order_item.parent.owner.email_id

            merchant_name = (
                order_item.merchant.first_name + " " + order_item.merchant.last_name
            )
            merchant_store_name = order_item.product.store.name
            merchant_address = order_item.product.store.address
            merchant_city = order_item.product.store.city
            merchant_state = order_item.product.store.state
            merchant_postal_code = order_item.product.store.postal_code
            merchant_country = order_item.product.store.country
            merchant_mobile_no = order_item.product.store.owner.mobile_no
            merchant_email = order_item.product.store.owner.email_id

            vendor_name = (
                order_item.merchant.first_name + " " + order_item.merchant.last_name
            )
            vendor_company_name = order_item.product.inventory.company.name
            vendor_address = order_item.product.inventory.company.address
            vendor_city = order_item.product.inventory.company.city
            vendor_state = order_item.product.inventory.company.state
            vendor_postal_code = order_item.product.inventory.company.postal_code
            vendor_country = order_item.product.inventory.company.country
            vendor_mobile_no = order_item.product.inventory.company.owner.mobile_no
            vendor_email = order_item.product.inventory.company.owner.email_id

            order_detail_data = {
                "order_item_id": order_item.pk,
                "tracking_id": order_item.tracking_id,
                "order_date": str(order_item.parent.created_at.date()),
                "product": order_item.product.inventory.product.name,
                "product_description": order_item.product.inventory.product.description,
                "vendor_price": order_item.vendor_price,
                "margin": order_item.merchant_margin,
                "store_price": order_item.store_price,
                "quantity": int(order_item.quantity),
                "total_amount": total_amount,
                "merchant_profit_amount": float(merchant_profit_amount),
                "vendor_payment_amount": float(vendor_payment_amount),
                "status": order_item.status,
                "status_color": ORDER_STATUS_COLORS[order_item.status],
                "customer_name": customer_name,
                "customer_address": customer_address,
                "customer_city": customer_city,
                "customer_state": customer_state,
                "customer_postal_code": customer_postal_code,
                "customer_country": customer_country,
                "customer_mobile_no": customer_mobile_no,
                "customer_email": customer_email,
                "merchant_name": merchant_name,
                "merchant_store_name": merchant_store_name,
                "merchant_address": merchant_address,
                "merchant_city": merchant_city,
                "merchant_state": merchant_state,
                "merchant_postal_code": merchant_postal_code,
                "merchant_country": merchant_country,
                "merchant_mobile_no": merchant_mobile_no,
                "merchant_email": merchant_email,
                "vendor_name": vendor_name,
                "vendor_company_name": vendor_company_name,
                "vendor_address": vendor_address,
                "vendor_city": vendor_city,
                "vendor_state": vendor_state,
                "vendor_postal_code": vendor_postal_code,
                "vendor_country": vendor_country,
                "vendor_mobile_no": vendor_mobile_no,
                "vendor_email": vendor_email,
                "is_po_created": PurchaseOrderInvoice.objects.filter(
                    order_item=order_item
                ).exists(),
                # "confirmed_date": (
                #     str(order_item.confirmed_date.date())
                #     if order_item.confirmed_date
                #     else None
                # ),
                # "shipping_date": (
                #     str(order_item.shipping_date.date())
                #     if order_item.shipping_date
                #     else None
                # ),
                # "arrival_date": (
                #     str(order_item.arrival_date.date())
                #     if order_item.arrival_date
                #     else None
                # ),
                # "delivery_date": (
                #     str(order_item.delivery_date.date())
                #     if order_item.delivery_date
                #     else None
                # ),
            }
            return render(
                request,
                "merchant/customers/customer_order_detail.html",
                {
                    "data": order_detail_data,
                },
            )

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching order details.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error fetching order details."},
                status=500,
            )
