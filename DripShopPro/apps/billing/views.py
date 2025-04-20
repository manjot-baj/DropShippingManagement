import logging
import traceback
import datetime
from django.shortcuts import render, redirect
from user_profile.middlewares import RoleRequiredMixin
from store.Utils.middlewares import StoreRequiredMixin
from catalog.Utils.middlewares import CompanyRequiredMixin
from django.views import View
from django.contrib import messages
from order.models import OrderItem
from common.functions import PO_STATUS_COLORS, ORDER_STATUS_COLORS
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
                vendor_name = (
                    order_item.merchant.first_name + " " + order_item.merchant.last_name
                )
                vendor_company_name = order_item.product.inventory.company.name
                total_amount = float(order_item.total_amount)
                merchant_profit_amount = order_item.merchant_margin_price * int(
                    order_item.quantity
                )
                vendor_payment_amount = order_item.vendor_price * int(
                    order_item.quantity
                )
                po_list.append(
                    {
                        "po_id": each.pk,
                        "po_date": str(each.created_at.date()),
                        "po_no": order_item.tracking_id,
                        "vendor_name": vendor_name,
                        "vendor_company_name": vendor_company_name,
                        "vendor_payment_amount": float(vendor_payment_amount),
                        "merchant_profit_amount": float(merchant_profit_amount),
                        "total_amount": float(total_amount),
                        "status": each.status,
                        "status_color": PO_STATUS_COLORS[each.status],
                        "order_status": order_item.status,
                        "order_status_color": ORDER_STATUS_COLORS[order_item.status],
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


class MerchantPODetailView(RoleRequiredMixin, StoreRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, po_id, *args, **kwargs):
        try:
            po = PurchaseOrderInvoice.objects.get(pk=po_id)
            order_item = po.order_item
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
                "po_status": po.status,
                "po_status_color": PO_STATUS_COLORS[po.status],
            }
            return render(
                request,
                "merchant/billing/purchase_order_detail.html",
                {
                    "data": order_detail_data,
                },
            )

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching Po details.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error fetching Po details."},
                status=500,
            )


class VendorPurchaseOrderListView(RoleRequiredMixin, CompanyRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            purchase_order_list = PurchaseOrderInvoice.objects.filter(
                reciever__user=request.user
            )
            po_list = []
            for each in purchase_order_list:
                order_item = each.order_item
                merchant_name = (
                    order_item.merchant.first_name + " " + order_item.merchant.last_name
                )
                merchant_store_name = order_item.product.store.name
                vendor_payment_amount = order_item.vendor_price * int(
                    order_item.quantity
                )
                po_list.append(
                    {
                        "po_id": each.pk,
                        "po_date": str(each.created_at.date()),
                        "po_no": order_item.tracking_id,
                        "merchant_name": merchant_name,
                        "merchant_store_name": merchant_store_name,
                        "total_amount": float(vendor_payment_amount),
                        "status": each.status,
                        "status_color": PO_STATUS_COLORS[each.status],
                        "order_status": order_item.status,
                        "order_status_color": ORDER_STATUS_COLORS[order_item.status],
                        "is_invoiced": "Yes" if each.is_invoiced else "No",
                    }
                )

            return render(
                request,
                "vendor/billing/purchase_order_list.html",
                {
                    "po_list": po_list,
                },
            )

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while listing PO.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error while listing PO."},
                status=500,
            )


class VendorPODetailView(RoleRequiredMixin, CompanyRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, po_id, *args, **kwargs):
        try:
            po = PurchaseOrderInvoice.objects.get(pk=po_id)
            order_item = po.order_item
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
                "quantity": int(order_item.quantity),
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
                "po_status": po.status,
                "po_status_color": PO_STATUS_COLORS[po.status],
                "po_id": po.pk,
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
                "vendor/billing/purchase_order_detail.html",
                {
                    "data": order_detail_data,
                },
            )

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching Po details.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching Po details."},
                status=500,
            )


class ApprovePOView(RoleRequiredMixin, CompanyRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, po_id, *args, **kwargs):
        try:
            po = PurchaseOrderInvoice.objects.get(pk=po_id)
            po.status = "Approved"
            po.save()
            po.order_item.status = "Confirmed"
            po.order_item.save()
            po.order_item.confirmed_date = po.order_item.updated_at
            po.order_item.save()
            return redirect("vendor_purchase_order_list")

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while updating PO.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error while updating PO."},
                status=500,
            )


class ShipProductView(RoleRequiredMixin, CompanyRequiredMixin, View):
    required_role = "Vendor"

    def post(self, request, po_id, *args, **kwargs):
        try:
            po = PurchaseOrderInvoice.objects.get(pk=po_id)
            arrival_date_str = request.POST.get("arrival_date")
            arrival_date = datetime.datetime.strptime(
                arrival_date_str, "%Y-%m-%d"
            ).date()
            po.status = "In-Progress"
            po.save()
            po.order_item.status = "Shipped"
            po.order_item.save()
            po.order_item.shipping_date = po.order_item.updated_at
            po.order_item.arrival_date = arrival_date
            po.order_item.save()
            return redirect("vendor_purchase_order_list")

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while updating PO.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error while updating PO."},
                status=500,
            )


class MarkProductDeliveredView(RoleRequiredMixin, CompanyRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, po_id, *args, **kwargs):
        try:
            po = PurchaseOrderInvoice.objects.get(pk=po_id)
            po.status = "Fulfilled"
            po.save()
            po.order_item.status = "Delivered"
            po.order_item.save()
            po.order_item.delivery_date = po.order_item.updated_at
            po.order_item.save()
            return redirect("vendor_purchase_order_list")

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while updating PO.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error while updating PO."},
                status=500,
            )


class RaiseInvoiceView(RoleRequiredMixin, CompanyRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, po_id, *args, **kwargs):
        try:
            po = PurchaseOrderInvoice.objects.get(pk=po_id)
            po.status = "Payment_Pending"
            po.is_invoiced = True
            po.save()
            return redirect("vendor_purchase_order_list")

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error while updating PO.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error while updating PO."},
                status=500,
            )
