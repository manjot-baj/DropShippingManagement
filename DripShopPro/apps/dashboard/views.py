import logging
import traceback
from django.shortcuts import render
from user_profile.models import UserProfile
from user_profile.middlewares import RoleRequiredMixin
from django.views import View
from django.contrib import messages
from store.models import StoreProduct, Store
from catalog.models import Category, ProductImage, Inventory
from order.models import Cart, OrderItem
from billing.models import PurchaseOrderInvoice
from common.functions import ORDER_STATUS_COLORS

logger = logging.getLogger("error_log")


class VendorDashboardView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(user=request.user)
            approval_pending = PurchaseOrderInvoice.objects.filter(
                reciever__user=request.user,
                is_invoiced=False,
                status="Approval_Pending",
            ).count()
            total_orders = OrderItem.objects.filter(
                vendor__user=request.user,
                is_deleted=False,
            ).count()
            orders_in_progress = OrderItem.objects.filter(
                vendor__user=request.user,
                is_deleted=False,
                status__in=["Confirmed", "Shipped"],
            ).count()
            orders_delivered = OrderItem.objects.filter(
                vendor__user=request.user, is_deleted=False, status="Delivered"
            ).count()

            payment_due_invoices = PurchaseOrderInvoice.objects.filter(
                reciever__user=request.user, is_invoiced=True, status="Payment_Pending"
            )
            payment_dues = 0
            for each in payment_due_invoices:
                order_item = each.order_item
                vendor_payment_amount = order_item.vendor_price * int(
                    order_item.quantity
                )
                payment_dues = float(payment_dues) + float(vendor_payment_amount)

            invoices = PurchaseOrderInvoice.objects.filter(
                reciever__user=request.user,
                is_invoiced=True,
                status="Payment_Completed",
            )
            revenue = 0
            for each in invoices:
                order_item = each.order_item
                vendor_payment_amount = order_item.vendor_price * int(
                    order_item.quantity
                )
                revenue = float(revenue) + float(vendor_payment_amount)
            catalog_products = (
                Inventory.objects.select_related("company", "product")
                .filter(
                    is_deleted=False,
                    catalog_display=True,
                )
                .count()
            )
            catalog_product_list = (
                Inventory.objects.select_related("company", "product").filter(
                    is_deleted=False,
                    catalog_display=True,
                )
            )[:5]

            customer_order_data = []
            customer_orders = OrderItem.objects.filter(
                vendor__user=request.user, is_deleted=False
            )[:5]

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
                    }
                )

            data = {
                "user": user,
                "total_orders": total_orders,
                "new_orders": approval_pending,
                "orders_in_progress": orders_in_progress,
                "orders_delivered": orders_delivered,
                "revenue": revenue,
                "payment_dues": payment_dues,
                "approval_pending": approval_pending,
                "catalog_products": catalog_products,
                "catalog_product_list": catalog_product_list,
                "customer_order_data": customer_order_data,
            }

            return render(request, f"vendor/dashboard.html", data)
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching companies.")
            return render(
                request,
                "vendor/error.html",
                {"message": "Error fetching companies."},
                status=500,
            )


class MerchantDashboardView(RoleRequiredMixin, View):
    required_role = "Merchant"

    def get(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(user=request.user)
            new_orders = OrderItem.objects.filter(
                merchant__user=request.user, is_deleted=False, status="Placed"
            ).count()
            total_orders = OrderItem.objects.filter(
                merchant__user=request.user,
                is_deleted=False,
            ).count()
            orders_in_progress = OrderItem.objects.filter(
                merchant__user=request.user,
                is_deleted=False,
                status__in=["Confirmed", "Shipped"],
            ).count()
            orders_delivered = OrderItem.objects.filter(
                merchant__user=request.user, is_deleted=False, status="Delivered"
            ).count()
            approval_pending = PurchaseOrderInvoice.objects.filter(
                sender__user=request.user, is_invoiced=False, status="Approval_Pending"
            ).count()
            payment_due_invoices = PurchaseOrderInvoice.objects.filter(
                sender__user=request.user, is_invoiced=True, status="Payment_Pending"
            )
            payment_dues = 0
            for each in payment_due_invoices:
                order_item = each.order_item
                vendor_payment_amount = order_item.vendor_price * int(
                    order_item.quantity
                )
                payment_dues = float(payment_dues) + float(vendor_payment_amount)

            invoices = PurchaseOrderInvoice.objects.filter(
                sender__user=request.user, is_invoiced=True, status="Payment_Completed"
            )
            revenue = 0
            for each in invoices:
                order_item = each.order_item
                merchant_profit_amount = order_item.merchant_margin_price * int(
                    order_item.quantity
                )
                revenue = float(revenue) + float(merchant_profit_amount)
            store_products = StoreProduct.objects.filter(
                store__owner__user=request.user
            ).count()
            store_product_list = StoreProduct.objects.filter(
                store__owner__user=request.user
            )[:5]

            customer_order_data = []
            customer_orders = OrderItem.objects.filter(
                merchant__user=request.user, is_deleted=False
            )[:5]

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
                    }
                )

            data = {
                "user": user,
                "new_orders": new_orders,
                "total_orders": total_orders,
                "orders_in_progress": orders_in_progress,
                "orders_delivered": orders_delivered,
                "revenue": revenue,
                "payment_dues": payment_dues,
                "approval_pending": approval_pending,
                "store_products": store_products,
                "store_product_list": store_product_list,
                "customer_order_data": customer_order_data,
            }
            return render(request, f"merchant/dashboard.html", data)
        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching companies.")
            return render(
                request,
                "merchant/error.html",
                {"message": "Error fetching companies."},
                status=500,
            )


class CustomerDashboardView(RoleRequiredMixin, View):
    required_role = "Customer"

    def get(self, request, *args, **kwargs):
        try:
            user = UserProfile.objects.get(user=request.user)
            categorys = Category.objects.all()

            # Extract filter params
            category_filter = request.GET.get("category")
            name_filter = request.GET.get("name")
            price_min = request.GET.get("price_min")
            price_max = request.GET.get("price_max")

            # Base queryset
            store_products = StoreProduct.objects.filter(is_deleted=False)

            # Apply category filter
            if category_filter:
                store_products = store_products.filter(
                    inventory__product__category__name=category_filter
                )

            # Apply name filter
            if name_filter:
                store_products = store_products.filter(
                    inventory__product__name__icontains=name_filter
                )

            products = []
            for store_product in store_products:
                cost_price = float(store_product.inventory.price)
                margin_price = float(cost_price * (int(store_product.margin) / 100))
                selling_price = cost_price + margin_price

                # Apply price filter
                if price_min and selling_price < float(price_min):
                    continue
                if price_max and selling_price > float(price_max):
                    continue

                data = {
                    "name": store_product.inventory.product.name,
                    "category": store_product.inventory.product.category.name,
                    "description": store_product.inventory.product.description,
                    "price": selling_price,
                    "stock": store_product.inventory.stock,
                    "main_img": ProductImage.objects.filter(
                        product=store_product.inventory.product,
                        is_deleted=False,
                    ).latest("pk"),
                    "imgs": ProductImage.objects.filter(
                        product=store_product.inventory.product,
                        is_deleted=False,
                    ),
                    "product_id": store_product.pk,
                }
                products.append(data)

            cart_item_count = Cart.objects.filter(
                is_deleted=False, owner__user=request.user
            ).count()
            return render(
                request,
                "customer/dashboard.html",
                {
                    "user": user,
                    "categorys": categorys,
                    "products": products,
                    "selected_category": category_filter,
                    "searched_name": name_filter,
                    "price_min": price_min,
                    "price_max": price_max,
                    "cart_item_count": cart_item_count,
                },
            )

        except Exception:
            logger.error(traceback.format_exc())
            messages.error(request, "Error fetching products.")
            return render(
                request,
                "customer/error.html",
                {"message": "Error fetching products."},
                status=500,
            )
