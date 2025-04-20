import logging
import traceback
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from user_profile.middlewares import RoleRequiredMixin
from catalog.models import Company, ProductImage
from store.models import StoreProduct, Store

logger = logging.getLogger("error_log")


class VendorInvoiceView(RoleRequiredMixin, View):
    required_role = "Vendor"

    def get(self, request, *args, **kwargs):
        try:
            # Base queryset
            store_products = StoreProduct.objects.filter(is_deleted=False)
            store = Store.objects.filter(is_deleted=False).latest("pk")
            company = Company.objects.filter(is_deleted=False).latest("pk")
            merchant = {
                "name": f"{store.owner.first_name} {store.owner.last_name }",
                "store": store.name,
                "email": store.email,
                "phone": store.phone,
                "state": store.state,
            }
            vendor = {
                "name": f"{company.owner.first_name} {company.owner.last_name }",
                "company": company.name,
                "email": company.email,
                "phone": company.phone,
                "state": company.state,
            }

            products = []
            total = 0
            count = 0
            for store_product in store_products:
                count = count + 1
                cost_price = float(store_product.inventory.price)
                margin_price = float(cost_price * (int(store_product.margin) / 100))
                selling_price = cost_price + margin_price
                total = total + selling_price
                data = {
                    "sr": count,
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

            return render(
                request,
                "vendor/billing/vendor_invoice.html",
                {
                    "products": products,
                    "total": total,
                    "count": store_products.count(),
                    "merchant": merchant,
                    "vendor": vendor,
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
